# UnifiedXRMotion EuroXR 2026 Medium Paper - Revision Report

## Summary
This revision keeps the submission as a focused EuroXR medium paper. It does not expand the work into a long paper, because the current evidence does not include payload benchmarks, determinism checks, vendor-native runtime baselines, or motion-to-photon instrumentation.

## Major changes made
- Reframed the evaluation as case-study evidence rather than complete performance evaluation.
- Added an authoring/setup-burden case study using the SDK A vs SDK B task manual and raw user-study data.
- Added a task-equivalence table comparing UnifiedXRMotion and the vendor SDK workflow.
- Added a user-study results table for completion time, SUS, and NASA-TLX.
- Reframed latency as a local/remote node-placement case study, not latency superiority.
- Added a node-placement latency table with sample counts and percentile summaries.
- Removed LaTeX TODO comments from the manuscript body and moved unresolved validation needs to Limitations/Future Work.
- Removed the in-paper claim-audit table to keep the manuscript within medium-paper scope; the audit is included below instead.

## User-study evidence added
Within-subjects setup-burden results (N=19):

| Metric | UnifiedXRMotion | Vendor SDK | Difference | Interpretation |
|---|---:|---:|---:|---|
| Completion time (s) | 564.03 | 972.89 | -408.86 | Lower procedural setup burden, with order-effect risk |
| SUS (0-100) | 73.42 | 34.47 | +38.95 | Higher perceived usability in this task |
| NASA-TLX raw avg. (0-100) | 41.05 | 58.60 | -17.54 | Lower perceived workload in this task |

Important caveats now stated in the manuscript:
- Participants were instructed to prioritize correctness and completion rather than speed.
- Completion time is treated as a coarse proxy for setup burden, not pure speed.
- Hand-axis alignment and mesh-specific retargeting were pre-completed before sessions.
- The study does not measure full unseen-avatar integration cost, adapter-authoring effort, or long-term maintainability.
- Completion time showed order-effect risk.

## Latency evidence added
Latency is now presented as a local/remote node-placement case study.

| Device | Placement | n | Mean | p50 | p95 | p99 |
|---|---|---:|---:|---:|---:|---:|
| Meta Quest 3 | Local path | 7859 | 15.27 | 14.86 | 18.98 | 26.96 |
| Meta Quest 3 | Remote path | 8627 | 13.91 | 13.88 | 14.52 | 14.91 |
| XREAL X4000 | Local path | 4190 | 28.64 | 30.46 | 40.21 | 50.90 |
| XREAL X4000 | Remote path | 5913 | 20.30 | 18.53 | 33.34 | 36.29 |

Safe interpretation now used:
- The traces characterize application-level motion-pipeline latency.
- They illustrate that node-placement choices can be inspected in the prototype.
- They do not establish vendor superiority or general latency improvement.
- They are not input-to-photon or motion-to-photon measurements.

## Claim audit
| Claim | Evidence | Safe? | Reviewer risk / required fix |
|---|---|---:|---|
| UnifiedXRMotion defines a schema-based validity-aware motion contract. | Schema, slot records, validity flags, buffer views, serialization design. | Yes | Later strengthen with round-trip serialization tests. |
| The 77-slot full-body schema is a prototype instantiation. | Current Unity implementation. | Yes | Never present as a universal skeleton or contribution by itself. |
| The adapter boundary localizes SDK-specific tracking logic. | Implemented adapters mapped into shared records. | Mostly | Add adapter LOC and new-adapter effort for a stronger long paper. |
| The authoring study indicates lower setup burden for one prepared task. | Within-subjects setup task, matched scene goal, SUS, NASA-TLX. | Mostly | Order effect and pre-completed hand-axis alignment limit generalization. |
| The runtime is a DAG execution engine. | Not supported by code audit. | No | Use event-driven motion-node pipeline wording. |
| Remote placement improves latency generally. | Existing traces are descriptive, not vendor baselines. | No | Report only placement characterization. |
| The system measures input-to-photon latency. | Capture/render/compositor timestamps are absent. | No | Requires new instrumentation and clock synchronization. |
| UnifiedXRMotion improves avatar quality. | No quantitative pose or perception evidence. | No | Requires pose-error, jitter, foot-skating, or user-perception study. |

## Remaining limitations / future validation
These are not required for the current medium-paper framing, but they would be required for a stronger long paper:
- Serialization round-trip test.
- Bytes-per-frame payload-size benchmark.
- Local/remote determinism check on identical replay input.
- Vendor-native runtime latency baseline.
- Component-level timing breakdown.
- Capture/render timestamping and clock synchronization for motion-to-photon or input-to-photon claims.
- Adapter-authoring effort case study.
- Stronger statistical modeling of the order effect in the user study.

## Compile status
- Compiled with Springer LNCS class.
- Final PDF: 13 pages total including references.
- Main text before references is within medium-paper scope.
- No unresolved citations or references in the final compile log.
- Minor overfull/underfull warnings remain and are not fatal.
