# Implementation & Study Facts (grounded reference for rebuttal + figure)

Compact, source-verified reference so the rebuttal figure and prose use the
**real** class/method names and the **real** pipeline — not paraphrase.

- **Codebase (local):** `C:\Users\admin\unity\OXRAvatarForge\UnifiedXRMotion`
  - Unity package `com.kisti.unifiedxrmotion`, version **1.8.4**, Unity 6000.2,
    author KISTI OpenXR Research Center.
  - Public mirror: `github.com/oxr-sdk/UnifiedXRMotion` (private/404 without auth).
- **Study repo:** `github.com/hyeonjang/unifiedxrmotion-uxstudy-2025` (public).
- Paper draft: `euro-xr/main-rebuttal.tex`. Rebuttal docs: `euro-xr/rebuttal/`.

> ⚠️ Naming note: the paper uses some labels that differ slightly from the code.
> Paper says `KinematicBuffer<T>` / `BodyType` views → code is `FullBodyBuffer<T>`
> with `KinematicBufferViewSlice<T>` accessors and a `BodyType` enum. Paper says
> consumers gate via `PoseFlag` → code method is `RetargetSystem.AssignToBody/
> AssignToRoot` checking `poseFlag.HasFlag(...)`. Keep paper labels, but the
> figure should use names that actually exist in the code where it shows specifics.

---

## THE FRAMEWORK MODEL (read this first — the lens for everything below)

This is the agreed conceptual model of what UnifiedXRMotion *is* and what we must
deliver to reviewers. Sections 0–7 below are the source-verified evidence for it.

### One sentence

> UnifiedXRMotion is a **validity-aware runtime contract**: a live, in-memory,
> per-frame, schema-defined representation (`PhysicBone` + `PoseFlag` stored in a
> `KinematicBuffer`, sliced by `View`) that heterogeneous sources **enter at the
> adapter boundary** and that any consumer **reuses through region views** — all by
> upholding *set / gate / preserve* obligations rather than depending on each
> other's SDK.

### The "room" metaphor (how the parts relate)

- **The contract = the room.** The shared representation where availability is
  first-class: `(schema S,P,R,K) + PhysicBone value + PoseFlag availability + View`.
  This is the contribution. It is a *data representation + a discipline*, not a node.
- **The adapter boundary = the IN door.** The point where native source data becomes
  the contract: map native joints → schema slots, convert coordinates, **mark
  availability** (`PoseFlag`). Availability is *born here*. Below the door = vendor
  code (inside `ITrackingDeviceHandler.Track()`); above it = generic over the contract.
- **Region views = the OUT doors.** `KinematicBufferView` / `KinematicBufferViewSlice`
  expose any body subset of the *same* buffer (full-body, two-hands, …). Any consumer
  reads the region it needs, sees per-slot availability, no source dependency.
- **Nodes (tracker, retargeter, recorder, `RetargetSystem`, `MotionAvatar`) = parties**
  who walk in/out of the room. They are *roles*, replaceable, secondary. They are NOT
  where availability "lives."

### What makes it a CONTRACT

Mutual agreement that lets mutually-ignorant parties interoperate. Producers and
consumers never reference each other or each other's SDK; they only agree on:
slot identity (schema), the per-slot payload (`PhysicBone`), the availability flag
(`PoseFlag`), and how to view any region (`View`). The C# interfaces
(`IMotionContainer`, `IKinematicBufferViewNode<T>`, `IRootMotionNode<T>`) are the
typed surface of that agreement.

**Obligations are honored by convention, not enforced by a checker** (design-by-
convention). Nothing throws on violation; every node upholds them, so the system
composes:
- **Producer (set):** set `PoseFlag` for components you publish.
- **Consumer (gate):** read a component only if its flag is set
  (`if (poseFlag.HasFlag(...))` — in `RetargetSystem` *and* in `MotionAvatar.OnAnimatorIK`).
- **Preserve:** copies / republishes / views keep the flag with the value
  (`TwoHandsRetargeter`, `TrackingSpaceCorrection`, `MetaBodyRetargeter` masks `&`).

### What makes it RUNTIME (vs. an interchange format)

It is an **in-memory, per-frame, live** agreement — NOT a file/wire format (FBX,
glTF, BVH) and NOT a compile-time API or a startup-negotiated schema. Concretely:
`Span<T>` / `ref struct` representation, advanced every `FixedUpdate` (30 Hz),
propagated by runtime events (`OnUpdate` / `RegisterMotionUpdate`), with availability
**recomputed each frame** (`TrackingManager` clears `&= None`, then re-sets `|=` per
producer). Availability is a *runtime* fact ("is this component present **this
frame**"), not a static property. The paper's own limitation states this: "an
implemented in-memory runtime contract, not a standardized interchange format."

### What "validity-aware" means (and does NOT mean) — R4's point

The defining trait of this contract is that **availability is part of what's agreed**
— first-class in the representation, recomputed live. A `PoseFlag` bit says ONLY
"this component is published under the producer's semantics." It is **not** confidence,
**not** provenance (you cannot tell from the data whether a present component was
observed, inferred, replayed, or retargeted — provenance is implicit in whichever node
wrote it), **not** freshness/timestamp, **not** schema-version negotiation.

### The two contributions are ONE structure, two sides

Both contributions are facets of the single runtime contract — that is why splitting
them into two figure-halves felt improper:
- **Contribution 1 (the IN side):** the contract is *validity-aware* — availability is
  first-class, separate from value and schema slot identity — so heterogeneous
  producers publish partial poses into it **across the adapter boundary**.
- **Contribution 2 (the OUT side):** the contract is *reusable through region views* —
  one buffer, many views — so any consumer reuses the data by reading a view and
  upholding the gate obligation, without depending on the producing source.
- The setup-burden **study** is a *third, separate* contribution: it tests one
  downstream consequence (authoring on this contract reuses one producer–retargeter–
  avatar pattern for hands and body), NOT a validation of availability itself.

### Symmetry to keep honest (R2's calibration point)

The boundary **localizes, does not eliminate**, source-specific work: joint mapping,
coordinate/axis conversion, calibration assumptions, and confidence→bit thresholding
all stay *below* the IN door (adapter-authoring effort). There is a mirror cost on the
OUT side: a **retargeter** maps the contract onto a *specific rig* (T-pose / axis /
scale alignment) — rig-specific code at the consuming end, the mirror of the adapter at
the producing end. So neither door is free; the contract is what's reusable *between*
the doors.

### THE CAPABILITY THAT IS *OF THE CONTRACT* (answers "is this just engineering?")

The risk with an end-to-end demo (hand+body -> Y Bot in simulator) is that it
reads as "a graph-configuration engineering product" -> feeds R1's "just
engineering." The escape: show a capability that **only exists because availability
is first-class runtime data**, i.e. the contract doing intellectual work, not
wiring. Two verified code sites give exactly this:

- **`UpperBodyFusioner.TrackState()`** (MotionNodes/CodebookMatching/UpperbodyFusioner.cs,
  lines 131-164): a consumer **reads the wrist slots' `PoseFlag`** and switches
  inference strategy on availability — `OK -> Lost -> LostLong`; when LostLong it
  runs `InferenceUntracked(...)` (a *different* model), otherwise `InferenceTracked(...)`.
  So the avatar **keeps moving when wrist tracking drops**, and recovers when it
  returns — driven purely by the availability bit, with **no knowledge of which
  source produced the wrist** (Meta / MediaPipe / replay / glove all identical).
- **`LowerBodyRegressor`** (…/LowerBodyRegressor.cs, line 74): **synthesizes**
  lower-body motion no tracker provides and publishes it back into the contract
  with `poseFlag = PoseFlag.Pose`. Downstream consumers treat the inferred legs
  **identically to observed slots** — provenance is implicit, availability is all
  they see.

**The capability, stated for reviewers:** *because availability is first-class
runtime data, consumers adapt their strategy to what is available (graceful
fallback to inference when tracking drops) and producers inject synthesized motion
that downstream code consumes identically to observed motion — so heterogeneous,
partial, time-varying inputs combine into one complete avatar with no consumer
depending on any source.* That is not graph wiring; it is the **representation
making graceful degradation + source-agnostic fusion fall out for free**. This is
the scientific point (R1), the concrete capability (R2), and the end-to-end example
(R4) at once.

**The "aha":** the avatar stays alive and complete as availability changes
underneath it, and nothing downstream had to know.

### What the figure must therefore deliver

The contract as the **center** (room), the adapter boundary as the **IN door**
(heterogeneous → contract, availability born here), region views as the **OUT doors**
(contract → any consumer), on the real hand+body → Y Bot example — with availability
shown as **first-class in the representation**, not as a node behavior.

### FIGURE LINEUP & GAP ANALYSIS (supersedes the single-figure brief above)

We do NOT need to re-draw the contract, the boundary, or configurability — the
paper already has figures that carry those. The new figure's job is ONLY the gap
those figures leave. Mapping the rebuttal requirements against existing assets:

**Requirements (what a reader must concretely understand):**
1. what the system is — the validity-aware runtime contract (representation + obligations)
2. the adapter boundary — where heterogeneous sources enter the contract
3. that it is configurable — many source/node configs, one reusable downstream
4. what problem it solves / what it can do — R2 "capabilities", concretely (a worked example)
5. what "availability" means and does NOT mean — R4 availability ≠ confidence ≠ provenance

**Existing assets (already own these — do NOT redraw):**
- **Fig 1** (`availability_boundary.png`): the ABSTRACT contrast (source-specific
  tangle vs. availability-aware contract). Covers req 1 abstractly + the motivation.
- **`figX-specificexample.png`** — caption "(a) Adapter Boundary & Runtime
  Contract": the MECHANISM — node as sender/receiver, `Write` into `KinematicBuffer`,
  `KinematicBuffer.View` exposed, `Invoke`/`Refer to` edges. Covers req 2 + req 1
  at implementation altitude. (Plumbing-styled — R2 said too technical for the body,
  but it genuinely shows the boundary+contract concept well.)
- **`fig5-configure.pdf`**: THREE real device configs side-by-side — (a) Meta Body
  Tracking, (b) XREAL + regressors/fusioner, (c) VIVE trackers + Upper-Body
  Regressor + Leg IK — each → Retarget Manager / avatar, with real screenshots.
  Covers req 3 (configurable pipeline) concretely. My HTML "config A/B/C → one
  downstream" draft is a paler, redundant version of THIS — abandon it.

**What is therefore STILL MISSING (the only job of a new figure):**
- **req 4 — a single concrete WORKED end-to-end example.** `fig5` shows configs
  *exist* as static node trees; no figure shows one narratable path *real partial
  inputs → contract → complete avatar out*. This is literally what R2/R4 asked for
  and no current figure delivers.
- **req 5 — the meaning of an availability bit.** Fig 1 shows `[P R V ω]` glyphs
  but never DEFINES a bit or denies the other readings. `figX`/`fig5` don't touch
  it. R4's availability≠confidence≠provenance ask has NO home in any figure.
- **availability shown DOING WORK.** All three existing figures show availability as
  a STATIC LABEL on slots. None shows a value present here / absent there with the
  downstream behaving correctly *because* of it. This is the line between "we have
  flags" (engineering) and "the flags are the mechanism" (the contribution).

**Conclusion — what the new figure must include (and ONLY this):**
1. ONE concrete worked path: named real partial inputs (hand+body tracking) →
   the contract → the actual Y Bot avatar result.
2. Availability *doing something*: ≥1 slot where presence/absence changes the
   downstream outcome (so "validity-aware" is not decorative).
3. The meaning of a bit: published-only, NOT confidence / provenance / freshness (R4).

**Do NOT re-include** (already owned, and re-drawing them is what made prior drafts
redundant and "explain nothing"): the abstract why (Fig 1), the node/sender-receiver/
buffer mechanism (`figX`), the device-config space (`fig5`).

> Note: this is a content conclusion, not a layout decision. How many figures, and
> whether to bring `figX`/`fig5` earlier vs. add one new worked-example figure, is
> still open and deferred.

---

## 1. The contract data structures (REAL)

**File:** `Runtime/Scripts/MotionAvatar/PhysicBone.cs`

`PhysicBone` struct fields: `poseFlag`, `localPosition/localRotation`,
`position`, `rotation`, `velocity`, `angularVelocity` (note: **scalar** float),
`LocalMatrix`/`WorldMatrix`, `parentIndex`, `children`.

The availability bitmask is **`PoseFlag`** (a `[Flags] enum : uint`):

```
None=0, Position=1, Rotation=2, Velocity=4, AngularVelocity=8,
Pose = Position|Rotation, PoseWithVelocity = Pose|Velocity,
All = Position|Rotation|Velocity|AngularVelocity
```

So the four guarded components are **Position, Rotation, Velocity,
AngularVelocity** — i.e. the figure's `[P R V ω]` glyph is correct, and it maps
1:1 to `PoseFlag`. Each runtime sample = a `PhysicBone` with its `poseFlag` set.

## 2. Region views (REAL)

**Files:** `MotionAvatar/KinematicFormat.cs`, `KinematicBuffer.cs`

`BodyType` enum (`[Flags] : short`) with bone counts:
- `FullBody` (77), `UpperLowerBody` (27), `UpperBody` (19), `LowerBody` (9),
  `TwoArms` (6), `Spine`, `Arm`, `Leg`, `TwoHands` (52), `Hand` (26/hand).

Views exposed on `FullBodyBuffer<T>` as `KinematicBufferViewSlice<T>`:
`UpperLowerBodyView`, `UpperBodyView`, `LowerBodyView`, `TwoArmsView`,
`TwoHandsView`, `LeftHandView`, `RightHandView` (each backed by static index
arrays `…Ids`). **The study uses the full-body view and the two-hands view.**

## 3. Producer / adapter interface (REAL)

**File:** `Runtime/Scripts/Tracking/ITrackingDeviceHandler.cs`

```csharp
interface ITrackingDeviceHandler {
    void Initialize();
    FullBody.BoneId[] TrackingPointIds { get; }   // device output → schema slot
    TrackingInfo TrackingInfo { get; }            // per-frame pose buffer
    void Track();                                 // populate TrackingInfo each frame
}
```

`TrackingInfo` holds parallel arrays incl. `PoseFlag[] isTracked`, `positions[]`,
`rotations[]`, `velocities[]`, `angularVelocities[]`.

**How a producer sets availability** (e.g. `Tracking/Unity/UnityXRInputDevices.cs`,
`SampleDevice`): start `isTracked = PoseFlag.None`, then `|= PoseFlag.Position`
only if `devicePosition` was actually read, `|= PoseFlag.Rotation` only if
rotation was read, etc. **Availability = "this producer actually obtained this
component this frame," nothing stronger.** This is exactly the paper's claim.

## 4. Consumer gating (REAL)

**File:** `Runtime/Scripts/Retargeting/RetargetSystem.cs`

- Subscribes in `OnEnable`: `motionInput.OnUpdate += RegisterMotionUpdate;`
- `RegisterMotionUpdate(IMotionContainer)` dispatches:
  - `IKinematicBufferViewNode<PhysicBone>` → `AssignToBody(...)`
  - `IRootMotionNode<PhysicBone>` → `AssignToRoot(...)`
- The gate (the decisive lines):
  ```csharp
  if (view[i].poseFlag.HasFlag(PoseFlag.Position)) transform.position = ...;
  if (view[i].poseFlag.HasFlag(PoseFlag.Rotation)) transform.rotation = ...;
  ```
  If a component is unavailable, the assignment is **skipped** (no default/stale
  write). `AssignToBody` switches on `view.BodyType` to pick the matching avatar
  view (full body, upper/lower, two-arms, two-hands).

## 5. End-to-end wiring for the STUDY scenario (REAL)

Pipeline: **producers → TrackingManager (aggregate) → OnUpdate event →
RetargetSystem (gated assign) → MotionAvatar.**

- Producers implement `ITrackingDeviceHandler` (hand source + body source).
- `TrackingManager` (`IMotionTrigger` + `IKinematicBufferViewNode<PhysicBone>`)
  merges device outputs into a `FullBodyBuffer<PhysicBone>`, **accumulating
  flags**: `_tracked.View[trackId] |= deviceTracked;`, then `OnUpdate?.Invoke(this)`.
- `RetargetSystem` (subscribed) gates and writes to `MotionAvatar`.
- `MotionSystem` drives it on **FixedUpdate (30 Hz default, `_frameRate`)**:
  `TriggerUpdate()` → `TriggerFixedUpdate()` (TrackingInfo→PhysicBone) →
  `Invoke()` (fire OnUpdate).

**Minimal user setup (README "Setting Up the Scene"):**
1. Drop in a MotionSystem entry prefab (e.g. `ThreePointsFullBody.prefab`,
   `TrackerFullBody.prefab`, `VideoBasedTracking.prefab`, or the `Network/…`
   variants).
2. `WaypointManager` auto-detects the XR rig (`XROrigin`/`OVRCameraRig`, else
   `Camera.main`).
3. Point `RetargetSystem` at the avatar's `MotionAvatar`.
4. Press Play (FixedUpdate @30 Hz).

→ The **"same producer–view–retargeter–avatar pattern" claim is literally true**:
both hand and body tracking are just another `ITrackingDeviceHandler` feeding the
same `TrackingManager` → `RetargetSystem` → `MotionAvatar` chain.

## 6. Calibration / coordinate conversion (REAL) — matters for R2

- Adapter-side: each producer reads in its **device-native space**
  (`UnityXRInputDevices` reads `CommonUsages.devicePosition/Rotation` directly;
  MediaPipe in its own world frame).
- Contract/consumer-side correction node:
  `MotionNodes/TrackingSpaceCorrection.cs` applies
  `transformation = _trackingRoot.WorldMatrix * node.View[i].WorldMatrix;`.
- Avatar calibration anchor: `MotionAvatar.Spawn` matrix (set in `Respawn()`),
  applied as `MotionAvatar.Spawn * view[i].WorldMatrix` before assignment.
- `Retargeting/Calibration.cs` exists but is **currently stubbed/commented**.

→ Honest rebuttal line for R2: UXM **localizes** calibration/coordinate
conversion at the adapter and at `TrackingSpaceCorrection` / `Spawn`; it does
**not** eliminate calibration as a problem. (Matches `self-validation-summary.md`.)

## 0. THE ACTUAL ARCHITECTURE — two levels, not three ownership bands (REVISED)

Earlier I modeled this as "vendor adapters | shared contract | reusable consumers"
(3 ownership bands). **That is wrong.** The code shows a different, stronger story:

**Level A — a uniform node-graph protocol (`MotionNodes/IMotionNode.cs`).**
*Everything* is an `IMotionNode`. Trackers, filters, IK, retargeters, recorder,
network wrapper, space-correction — all implement the same two interface families:
- **Containers (carry data):** `IMotionContainer` →
  `IRootMotionNode<T>` (`ref T Root`), `IKinematicBufferViewNode<T>`
  (`KinematicBufferView<T> View`), `IKinematicsNode<T>` (both), `ITextureNode`.
- **Communication (move data):** `IMotionSender` (`event Update OnUpdate`),
  `IMotionReceiver` (`RegisterMotionUpdate(IMotionContainer)`),
  `IMotionMonoReceiver`/`IMotionMultiReceiver`, and `IMotionTrigger` (a source:
  `TriggerUpdate`/`TriggerFixedUpdate`/`Invoke`/`Initialize`).

So a "tracker/adapter" is **not a special layer** — it is simply a node that is a
*source* (`IMotionTrigger`, produces). A retargeter/recorder is a node that
*consumes and may republish*. They are **peers on one dataflow graph**, all
MonoBehaviours wired in the Unity scene. `MotionSystem` (`MotionSystem.cs`,
`[DefaultExecutionOrder(100)]`) just holds the trigger list and pumps them on
`FixedUpdate`: `TriggerUpdate()` (poll devices) → `TriggerFixedUpdate()`
(convert) → `Invoke()` (fire `OnUpdate`). No global scheduler.

**Level B — the typed data contract that flows on every edge**
(`MotionAvatar/PhysicBone.cs` + `KinematicBuffer.cs` + `KinematicFormat.cs`).
This is a PURE DATA layer (no MonoBehaviour; `ref struct` views over `Span<T>`):
- `PhysicBone` (value + `PoseFlag`) = per-slot payload.
- `KinematicBuffer<T>`/`FullBodyBuffer<T>` = storage; `KinematicBufferView<T>`
  (ref struct over `Span<T>`) and `KinematicBufferViewSlice<T>` (a **remapped**
  view via a static `…Ids` index array — zero-copy slice) = region views.
- `BodyType` enum + static schema classes `FullBody`(77)/`UpperLowerBody`(27)/
  `UpperBody`(19)/`LowerBody`(9)/`TwoArms`(6)/`TwoHands`(52)/`Hand`(26): each
  defines `Length`, `…Ids` slice maps, `ParentMap`, and cross-schema
  `ToFullBodyId`/`FromFullBodyId` maps. **This is the paper's schema S=(S,P,R,K)
  made concrete:** slot identity, parent relation, region views, component kinds.

**So the two "levels" you flagged are real and orthogonal:**
- the **node graph** (scene MonoBehaviours, runtime wiring) — vertical dataflow;
- the **kinematic-buffer contract** (typed value+flag+view structs) — what every
  edge carries.
- The **"adapter boundary" is an EDGE PROPERTY, not a band**: it is the moment a
  source node first emits an `IMotionContainer`. Below that emit, code is
  source-specific (inside the device handler); from that emit onward, every node
  is generic over `KinematicBufferView<PhysicBone>` + `PoseFlag`.

**Implication for novelty (R1):** the contribution is not "availability flags."
It is that **one typed dataflow contract makes every node — source, filter, IK,
retarget, record, network — interchangeable on the same graph**, with
per-component availability riding on each slot. The figure should show the
**graph of homogeneous nodes + the contract on the wire**, with the boundary as
the *first publish edge* — NOT three ownership bands.

**Verified detail — `TrackingManager` aggregation (`Tracking/TrackingManager.cs`):**
it is itself an `IMotionTrigger` + `IKinematicBufferViewNode<PhysicBone>`. It
keeps three buffers: `_trackingBody`, `_accumulation`, and `_tracked`
(`FullBodyBuffer<PoseFlag>`). Per frame it clears flags (`&= None`), then for each
device merges `_tracked.View[id] |= deviceTracked` and falls back to the
accumulated value when a component is absent, then writes `_trackingBody` with
flag-gated Lerp/Slerp. So multi-producer fusion is real and flag-driven. (It also
seeds an A-pose reference and has a `Compensate()` head-fallback heuristic.)

## 7. Event propagation (REAL)

**File:** `MotionNodes/IMotionNode.cs`

```csharp
interface IMotionSender   { event Update OnUpdate; }   // Update(IMotionContainer)
interface IMotionReceiver { void RegisterMotionUpdate(IMotionContainer input); }
```

Producer fires `OnUpdate?.Invoke(this)`; receivers (RetargetSystem, Recorder,
NetworkNodeWrapper, filters) implement `RegisterMotionUpdate`. No global graph
scheduler — explicit per-event propagation (matches paper §Implementation).

---

## Producer / consumer inventory actually present in code

**Producers (`ITrackingDeviceHandler` + sources):** UnityXR/OpenXR input
(`UnityXRInputDevices`, `UnityXROriginTracking`), Vive hands (`ViveHandTracking`),
MediaPipe vision (`MediapipeHandTracking`, `MediapipeUpperBodyTracking`, +
`MobRecon`, `YoloRegionCropper`), Android tablet AR (`AndroidTabletAR`),
transform/given-points/mouse dummies (`TransformTracking`, `TPDTracking`,
`GivenPointsTracking`, `MouseController`), replay (`Replayer`, `ReplayNode`),
codebook inference (`LowerBodyRegressor`, `UpperBodyRegressor`,
`UpperBodyPredictor`, `UpperbodyFusioner`).

**Consumers / republishers:** `RetargetSystem` + retargeters (`TwoHandsRetargeter`,
`HandRetargeter`, `MetaFullBodyRetarget`, `CodebookLowerBodyRetarget`,
`UpperBodyIKRetarget`, FABRIK family in `Retargeting/IK/`), `Recorder`/`RecordNode`/
`ReplayNode`, `NetworkNodeWrapper` (FishNet transport), filters
(`KalmanFilterNode`, `MotionBlend`), `TrackingSpaceCorrection`.

**Retarget/IK algorithms present:** FABRIK (`FABRIKSolver`, `FullBodyFABRIK`,
`Upper/LowerBodyFABRIK`), two-bone / trig / CCD / closed-loop solvers, codebook
matching (AI4Animation SIGGRAPH 2024 weights, obtained separately, CC BY-NC 4.0).

> Paper writing fixes this confirms (for #G7): the IK is literally **FABRIK**
> (`FABRIKSolver.cs`), so "Textbook IK" → "FABRIK"; transport is **FishNet**
> (`Network/NetworkNodeWrapper.cs`), so add a FishNet citation/definition.

---

## Study (user study) facts — `unifiedxrmotion-uxstudy-2025`

- **Design:** within-subjects, two conditions, same scene-level goal.
  - **Task-A = UnifiedXRMotion** (with automatic hand-axis alignment).
  - **Task-B = Vendor SDK** = Meta XR Core SDK + Movement SDK body tracking,
    OVRCameraRig, OVRInteractionComprehensive, synthetic hands, Movement SDK
    retargeting workflow; custom hand meshes **pre-aligned**.
- **Goal in both:** make custom **OpenXR hand prefabs** follow simulated hand
  motion + make the same **Y Bot** avatar follow simulated full-body motion.
- **Verification:** Meta **XR Simulator**, compared against **reference video clips**.
- **Versions:** Unity **6000.0.33f1**; Meta Core / Movement SDK / XR Simulator **78.0.0**.
- **Confound control:** hand retargeting / hand-axis alignment **pre-completed**
  in both conditions (so axis tuning is not in the measured task).
- **Metrics:** completion (time-to-verified-state), **NASA-TLX**, **SUS**
  (not raw speed; participants told to prioritize correctness).
- **N = 19** (per `main-rebuttal.tex` Table). Results: UXM faster + lower TLX +
  higher SUS, all p<.0001; completion-time had a significant **order effect**
  (AB vs BA), so timing magnitude is not a general-productivity estimate.
- **Repo layout:** `Assets/Scenes/{Task-A.unity,Task-B.unity}`,
  `Assets/Y Bot/`, `Assets/Hands/OpenXRCustomHandPrefab_{L,R}`,
  `Packages/{Unified XR Motion, Meta XR Core SDK}`, `Data/Videos/` (reference
  clips), README with glossary + step-by-step per-condition instructions.

### Task guide — actual setup steps per condition (for the glue-point table)

Verbatim from the study README. THIS is the source for the task-analysis table.
The key fact is not just "fewer steps" but **A reuses one pattern; B uses two
different mechanisms** (hands ≠ body). Stay neutral: report wiring *categories*,
not "vendor is worse."

**Task-A = UnifiedXRMotion**
- Hands (6 steps): add `MotionAvatar` to Hands; set `BodyType = Two Hands`; add
  MotionSystem prefab; under TrackingSystem add `Meta Hand Tracking`; under
  RetargetSystem add `Two Hands Retargeter` + set its `MotionAvatar = Hands`;
  connect data flow (add retargeter to `Input Motions`, set retargeter
  `Input Motion = TrackingSystem`).
- Full body (4 steps): add `MotionAvatar` to Y Bot; add 2nd MotionSystem; under
  TrackingSystem add `Meta Body Tracking` + under RetargetSystem add
  `Meta Full Body Retarget` + set `MotionAvatar = Y Bot`; connect data flow.
- **Pattern is identical for hands and body:** MotionAvatar → MotionSystem →
  (TrackingSystem producer) → (RetargetSystem retargeter) → connect Input Motion.

**Task-B = Vendor SDK (Meta)**
- Hands (11 steps): add `OVRCameraRig`; add `OVRInteractionComprehensive` child;
  retain only OVRHands; set `OVR Camera Rig Ref`; add `OVR{Left,Right}HandSynthetic`;
  delete default visuals (`OpenXR*Hand`, `OculusHand_*`); reparent custom hands
  under the synthetic hand visuals; configure each `OVR*HandVisual` (enable
  Update Root Pose/Scale, assign skinned mesh renderer, set OVR Custom Skeleton);
  link data sources (`Source = OVRHands`, read `OVRHands.Left/Right`).
- Full body (3 steps, 2 wizards): on `OVRManager` set Tracking Origin = Floor,
  Body Tracking = Required, Joint Set = Full Body; run Movement SDK "Retargeting
  Configuration Editor" wizard (Next→Validate&Save→Done); run "Add Character
  Retargeter" wizard (Next→Validate&Save→Done).
- **Hands and body use different mechanisms:** hands = manual hierarchy surgery +
  visual/renderer config + data-source linking; body = OVRManager flags +
  Movement SDK wizards. No shared pattern between the two.

**Verification (both):** Meta XR Simulator toggle → Play; hands via WASD/pinch;
body via "Play random movement"; compare to reference clips.

→ Glue-point categories that distinguish the conditions (neutral wording):
scene-hierarchy construction, prefab reparenting, visual/renderer setup,
data-source binding, retargeting configuration, and **pattern reuse across body
regions** (A: one pattern reused; B: two distinct mechanisms).

---

## Figure implication (what the end-to-end figure should depict)

The study scenario IS the end-to-end example R2/R4 asked for. Real labels to use:

- **Producers (left):** a hand source + a body source, each an
  `ITrackingDeviceHandler` (Task-A uses UXM hand + body tracking → Y Bot;
  custom `OpenXRCustomHandPrefab`).
- **Contract (mid):** publish into `FullBodyBuffer<PhysicBone>`; per-component
  availability = `PoseFlag` `[Position Rotation Velocity AngularVelocity]`;
  read via region views (`FullBody` view + `TwoHands` view).
- **Reusable pattern (right):** producer → `TrackingManager` (flags accumulate
  `|=`) → `OnUpdate` → `RetargetSystem` (gates `poseFlag.HasFlag` → `AssignToBody`/
  `AssignToRoot`) → `MotionAvatar`. **Same chain for hands and full body.**
- **Vendor (bottom contrast):** Meta condition wires OVRCameraRig +
  OVRInteractionComprehensive hierarchy, per-source reference/renderer/data-source,
  and the Movement SDK retargeting workflow — source-specific per source.

Compliant with the minor-revision rule: this depicts existing code + the
already-run study; no new implementation or data.
