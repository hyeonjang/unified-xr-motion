# /// script
# requires-python = ">=3.10"
# dependencies = ["pandas", "scipy", "statsmodels", "pingouin", "openpyxl"]
# ///
"""Reproduce the statistics reported in the EuroXR camera-ready results section.

Reads rawdata_sdk_a.csv (UnifiedXRMotion) and rawdata_sdk_b.csv (vendor SDK),
computes descriptives, paired t-tests, Wilcoxon, Shapiro-Wilk, Levene,
the 2x2 mixed ANOVA (condition within x order between), Welch simple effects,
and the linear mixed-effects regression.

Run: uv run analyze.py
"""
import numpy as np
import pandas as pd
from pathlib import Path
from scipy import stats
import pingouin as pg
import statsmodels.formula.api as smf

HERE = Path(__file__).parent


def load(path, condition):
    df = pd.read_csv(path)
    d = pd.DataFrame({
        "pid": df["participant_id"],
        "order": df["order"].str.strip(),
        "time": df["time_sec"].astype(float),
    })
    # Raw TLX: mean of six subscales, performance reversed (higher = more workload)
    tlx_cols = ["tlx_mental", "tlx_physical", "tlx_temporal",
                "tlx_performance", "tlx_effort", "tlx_frustration"]
    tlx = df[tlx_cols].astype(float).copy()
    tlx["tlx_performance"] = 100 - tlx["tlx_performance"]
    d["tlx"] = tlx.mean(axis=1)
    # SUS: odd items score-1, even items 5-score, sum * 2.5
    sus = 0.0
    for i in range(1, 11):
        q = df[f"sus_q{i}"].astype(float)
        sus = sus + (q - 1 if i % 2 == 1 else 5 - q)
    d["sus"] = sus * 2.5
    d["condition"] = condition
    return d


def hedges_g_av(x, y):
    """Hedges' g_av for paired designs (Lakens 2013, eq. 10)."""
    diff = x - y
    n = len(diff)
    s_av = np.sqrt((x.std(ddof=1) ** 2 + y.std(ddof=1) ** 2) / 2)
    corr = 1 - 3 / (4 * (n - 1) - 1)
    return (diff.mean() / s_av) * corr


uxm = load(HERE / "rawdata_sdk_a.csv", "uxm")
sdk = load(HERE / "rawdata_sdk_b.csv", "sdk")
wide = uxm.merge(sdk, on=["pid", "order"], suffixes=("_uxm", "_sdk"))
assert len(wide) == 19, f"expected 19 paired participants, got {len(wide)}"
print(f"N={len(wide)}  AB n={(wide['order']=='AB').sum()}  BA n={(wide['order']=='BA').sum()}\n")

long = pd.concat([uxm, sdk], ignore_index=True)

for m, label in [("time", "Completion time (s)"), ("tlx", "NASA-TLX"), ("sus", "SUS")]:
    a, b = wide[f"{m}_uxm"], wide[f"{m}_sdk"]
    diff = a - b
    print(f"=== {label} ===")
    print(f"  UXM {a.mean():.2f} ± {a.std(ddof=1):.2f}   SDK {b.mean():.2f} ± {b.std(ddof=1):.2f}")
    for o in ("AB", "BA"):
        s = wide["order"] == o
        print(f"  [{o}] UXM {a[s].mean():.2f} ± {a[s].std(ddof=1):.2f}   "
              f"SDK {b[s].mean():.2f} ± {b[s].std(ddof=1):.2f}")
    t, pv = stats.ttest_rel(a, b)
    ci = stats.t.interval(0.95, len(diff) - 1, loc=diff.mean(), scale=stats.sem(diff))
    print(f"  paired t({len(diff)-1})={t:.2f}, p={pv:.2e}, Mdiff={diff.mean():.1f}, "
          f"95% CI [{ci[0]:.2f}, {ci[1]:.2f}], g_av={hedges_g_av(a, b):.2f}")
    w, wp = stats.wilcoxon(a, b)
    print(f"  Wilcoxon W={w:.1f}, p={wp:.2e}")
    sw = stats.shapiro(diff)
    print(f"  Shapiro-Wilk diffs: W={sw.statistic:.3f}, p={sw.pvalue:.3f}", end="  ")
    for o in ("AB", "BA"):
        s = stats.shapiro(diff[wide["order"] == o])
        print(f"[{o}] p={s.pvalue:.3f}", end="  ")
    lev = stats.levene(diff[wide["order"] == "AB"], diff[wide["order"] == "BA"])
    print(f"\n  Levene diffs across order: p={lev.pvalue:.3f}")

    an = pg.mixed_anova(data=long, dv=m, within="condition", between="order",
                        subject="pid")
    print(an.round(4).to_string(index=False))

    # Welch simple effects: each condition compared across order groups
    for col, name in [(f"{m}_sdk", "SDK by position"), (f"{m}_uxm", "UXM by position")]:
        g1, g2 = wide.loc[wide["order"] == "AB", col], wide.loc[wide["order"] == "BA", col]
        res = stats.ttest_ind(g1, g2, equal_var=False)
        print(f"  Welch {name}: t({res.df:.2f})={res.statistic:.2f}, p={res.pvalue:.3f}")
    # Original submission's Welch on difference scores across orders
    res = stats.ttest_ind(diff[wide["order"] == "AB"], diff[wide["order"] == "BA"],
                          equal_var=False)
    print(f"  Welch on diffs across orders (orig submission): "
          f"t({res.df:.2f})={res.statistic:.2f}, p={res.pvalue:.4f}")
    # Paired simple effects of condition within each order
    for o in ("AB", "BA"):
        s = wide["order"] == o
        ts, ps = stats.ttest_rel(a[s], b[s])
        print(f"  Paired within {o}: Mdiff={(a[s]-b[s]).mean():.1f}, "
              f"t({s.sum()-1})={ts:.2f}, p={ps:.4f}")
    print()

# Linear mixed-effects regression for completion time (ref: vendor SDK, order AB)
long_t = long.copy()
long_t["condition"] = pd.Categorical(long_t["condition"], categories=["sdk", "uxm"])
long_t["order"] = pd.Categorical(long_t["order"], categories=["AB", "BA"])
for reml in (True, False):
    mlm = smf.mixedlm("time ~ condition * order", long_t,
                      groups=long_t["pid"]).fit(reml=reml)
    print(f"=== Mixed-effects regression, completion time "
          f"(ref: SDK, AB; {'REML' if reml else 'ML'}) ===")
    print(mlm.summary().tables[1])
