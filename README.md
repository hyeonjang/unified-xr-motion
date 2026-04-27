# UnifiedXRMotion EuroXR 2026 Medium Paper

This package contains the revised Springer LNCS source for the EuroXR 2026 Scientific Track medium-paper version of UnifiedXRMotion.

Main files:
- `main.tex`: LNCS manuscript source
- `bib/references.bib`: bibliography
- `main.pdf`: compiled manuscript
- `author_report.md`: change report, claim audit, and remaining limitations
- `llncs.cls`, `splncs04.bst`: Springer LNCS class/style files

Compile command:

```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

If `bibtex` is unavailable due to a broken symlink, use `bibtex.original main` or `bibtex8 main`.
