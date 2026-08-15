# Self-Validation Summary for Rebuttal and Revision

## Core Validated Position

The rebuttal should not defend the paper as if it invented missing-data handling or validity flags. Those primitives are old.

The defensible contribution is narrower and stronger:

> UnifiedXRMotion is a scoped systems contribution: a runtime avatar-motion contract boundary where selected heterogeneous producers publish schema-defined records with binary component availability, and downstream consumers reuse region views with availability-gated access.

## Evidence Separation

The most important validated distinction is:

```text
implementation traceability
= availability is published, preserved, and gated in the runtime

user study
= setup-burden evidence for a prepared authoring workflow

NOT:
user study validates availability bits
```

Recommended claim:

> The runtime mechanism is supported by implementation traceability; the within-subjects study evaluates setup burden for the reusable authoring workflow built on that mechanism.

## Reviewer-Claim Validation

| Reviewer concern | Validated response |
|---|---|
| Missing data, validity flags, coordinate mappings, retargeting, and incomplete skeletons are not new. | Agree. Novelty is not the availability bit alone; it is the runtime XR avatar-motion producer-consumer boundary. |
| The work looks like a useful engineering framework, not a mature scientific contribution. | Reframe as a scoped systems contribution: contract, boundary, operational obligations, implementation traceability, and workflow evidence. |
| The evaluation is narrow. | Agree. It supports the tested setup-burden task, not broad developer productivity, maintainability, runtime performance, motion quality, or general interoperability. |
| The study does not validate component availability. | Agree. Availability is supported by implementation traceability; the study evaluates workflow-level setup burden. |
| The Meta/vendor SDK workflow may simply be worse. | Do not claim Meta SDK is generally worse. Claim only that the tested vendor workflow required more source-specific wiring categories in the prepared task. |
| Real glue code includes coordinate relationships and calibration. | Agree. UXM localizes calibration/coordinate conversion at the adapter or tracking-space boundary; it does not eliminate calibration. |
| "Validity-aware" is misleading. | Agree. Define it as binary component availability under producer semantics, not confidence, provenance, freshness, correctness, or source type. |
| Practical examples and study details are underrepresented. | Agree. Add early concrete example and expand study procedure details. |

## Highest-Risk Paper Problems

1. The contribution list still contains a bad duplicate line:

   ```tex
   \radd{\item Availability validation through : a within-subjects Unity setup-burden study ...}
   ```

   This contradicts the validated logic. The study should not be described as availability validation.

2. The evaluation opening still says:

   ```tex
   The evaluation follows the evidence chain implied by the contract...
   ```

   R2 explicitly objected to this wording, and it blurs implementation traceability with user-study evidence.

3. The abstract compresses evidence types too much.

4. Related work needs stronger contrast with adjacent areas, not just more citations.

5. A concrete end-to-end example should appear earlier in the paper.

## Recommended Paper Revision Spine

### Contribution List

Use three contributions:

```tex
\item \textbf{A runtime avatar-motion contract and adapter boundary}: a schema-parameterized representation that separates slot identity, component values, and binary component availability, together with adapter and producer responsibilities for publishing selected XR, vision, replay, synthetic, inferred, and retargeted sources into that shared representation.

\item \textbf{Availability-gated downstream reuse through region views}: retargeting, recording/replay, and optional transport consumers read schema-defined views rather than source-specific motion records.

\item \textbf{A scoped setup-burden study of the authoring workflow}: a within-subjects Unity task comparing the UnifiedXRMotion workflow with a vendor-SDK workflow for a prepared hand/body avatar setup.
```

If using revision markup, keep `\item` outside `\radd{}`:

```tex
\item \radd{\textbf{A runtime avatar-motion contract and adapter boundary}: ...}
```

Do not use:

```tex
\radd{\item ...}
```

### Evaluation Opening

Replace the abstract "evidence chain" phrasing with:

```tex
The evaluation has two purposes. First, it traces whether the runtime contract is implemented: producers publish component availability, buffers and region views preserve it with slot identity, and representative consumers gate reads or assignments on it. Second, it evaluates whether the authoring workflow built on this contract reduces procedural setup burden in one prepared Unity task. The evaluation does not measure tracking accuracy, motion quality, latency, broad SDK coverage, long-term maintainability, adapter-authoring cost, or general developer productivity.
```

### Abstract Evidence Sentence

Recommended sentence:

```tex
Evaluation combines implementation traceability showing that availability is published, preserved through buffers and views, and gated by consumers; representative producer-to-consumer paths; and a within-subjects Unity study of setup burden for a prepared hand/body avatar authoring task.
```

### Related-Work Contrast Paragraph

Recommended merged paragraph:

```tex
UnifiedXRMotion operates between existing layers. Tracking middleware and OpenXR abstract devices, tracking states, and transforms; skeletal interchange and mocap formats support asset or motion exchange; retargeting systems map motion to target rigs; and sparse-pose methods reconstruct missing body motion. UnifiedXRMotion instead targets the runtime avatar-motion record shared after heterogeneous producers map their source-specific outputs and before downstream consumers retarget, record, replay, or transport the motion. The boundary addressed here appears when a single XR pipeline combines sparse device tracking, articulated hands, vision landmarks, replay streams, inferred motion, and retargeted outputs. At that boundary, producers need a shared representation with schema-defined slot identity, region views, and per-component availability, while downstream consumers need to read available components without depending on the producing SDK. The contribution is therefore not a new estimator, retargeter, or interchange format, but a contract for carrying partial component availability through this runtime producer-consumer boundary.
```

### Early Concrete Example

Recommended paragraph:

```tex
As a concrete example, consider a Unity scene that combines articulated hand tracking, full-body tracking, and avatar retargeting for a custom hand rig and a humanoid avatar. In a source-specific workflow, hand joints, body joints, renderer references, data sources, and retargeting configuration are wired through SDK-specific scene objects. In UnifiedXRMotion, the source-specific work is localized before publication: a hand or body producer publishes available components into a schema-defined region view, and downstream retargeters connect that view to a \texttt{MotionAvatar}. The same producer-view-retargeter-avatar pattern is then used for both hand and body motion, while calibration, coordinate conversion, and mesh-specific alignment remain adapter- or setup-side responsibilities.
```

## Final Rebuttal Thesis

Use this as the backbone of the rebuttal:

> The original manuscript compressed several distinct claims: the systems contribution, the implementation traceability, and the setup-burden evidence. The revision separates these claims and states the scope more explicitly.

Short version:

> Novelty is not "availability flags." Novelty is the runtime avatar-motion contract boundary. Implementation traceability supports the availability mechanism. The study supports reduced setup burden for the prepared authoring workflow. Calibration, confidence, provenance, broad productivity, and broad interoperability remain out of scope.

## Consistency Checklist Before Final Rebuttal

| Rebuttal claim | Paper must contain |
|---|---|
| "Contribution is runtime boundary." | Contribution list and intro must not frame availability bits alone as novelty. |
| "Implementation traceability supports availability." | Evaluation/implementation section must show publish -> preserve -> gate. |
| "Study evaluates setup burden." | Study section must avoid saying it validates availability bits. |
| "Reusable authoring pattern." | Example/study text must show hand/body producer-view-retargeter-avatar repetition. |
| "Calibration is not solved." | Limitations or adapter section must explicitly say calibration/coordinate conversion remains adapter-side. |
| "Validity means availability." | Terminology must define binary availability and exclude confidence/provenance/correctness/freshness. |

After the paper edits are actually made, convert rebuttal wording from "we will revise" to "we revised."
