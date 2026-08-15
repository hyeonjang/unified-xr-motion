# Rebuttal Response Plan

## Tasks

1. Reframe novelty and contributions around the runtime contract and reusable authoring pattern.
2. Separate runtime availability validation from the setup-burden user study.
3. Add concrete capability examples, study details, and implementation/reproducibility details.
4. Fix terminology, calibration framing, limitations, and local writing issues.

## Coverage Status (audit of main-rebuttal.tex, 2026-06-28)

Track: Medium paper, 8–12 pp excluding refs (paper ≈11 content pp). Markup `\radd`/`\rdel`; flip `\rebuttaltrue`→`\rebuttalfalse` for camera-ready.

**Done:**
- **#G2** — eval intro split into two purposes + traceability para; study fully described (N=19, Likert experience, consent/compensation, two conditions, simulator verification, pre-completed hand-axis, Unity/SDK versions); completion-time order-effect caveat clarified to "for completion time".
- **#G3** — `availability_boundary.png` figure + boundary walkthrough; concrete task table.
- **#G4** — related work adds sparse reconstruction (jiang2022avatarposer, dai2024hmd), AvatarGo, EuroXR AR patterns.
- **#G6** — binary availability ≠ confidence stated; Discussion limitations cover provenance, confidence, timestamps, schema version.
- **Task analysis** — Table 4 added (no-first-column, full-width bold Hands/Body/Pattern headers + `cellsteps` numbered lists). Numeric micro-action counts DROPPED on purpose (undefined unit, attackable). Detailed counted version kept in `task-analysis-table.tex` as backing reference only (not `\input`).

**Remaining:**
- **#G1 (R3-M1, score-7) — IN PROGRESS:** contribution list已部분 수정됨. `main-rebuttal.tex:74`의 옛 결합 항목("reuse + setup evidence")은 `\rdel` 처리되었고, `:75`에 새 "reusable authoring pattern + scoped setup-burden benefit" 항목이 `\radd`로 추가됨. 그러나 list 전체는 아직 옛 item-1/item-2 framing(`:72-73`)을 유지함. `letter.txt`는 이미 최신 framing으로 작성됨: contract + adapter boundary가 핵심이고, R3 요청대로 user study를 **standalone contribution으로 promote**, 옛 결합 항목은 삭제. 남은 작업: `:72-73` 항목을 letter.txt의 3-contribution 구조와 일치시킬지 최종 확정.
- **#G7 local fixes NOT done:** "Textbook IK" → "FABRIK/FABRIK-style" (~L87, L198 — 코드상 실제 `FABRIKSolver.cs`); "FishNet-based transport" still has NO citation (~L198 — 코드상 `Network/NetworkNodeWrapper.cs`); repetition of "selected/representative/scoped" not cleaned.
- **#G5 unconfirmed (R2-M3, R3-m2, R4-M4):** move Sec. 3–6 technical detail to supplementary / add schema-adapter reproducibility detail — no evidence done.
- **Draft typos:** "the two purpose" + "precedural" (eval intro); caption "comparision between of the workflows".
- **Video supplementary** (in letter.txt) — confirm it exists / is referenced.
- **#R1-M2 broader evaluation** — correctly DECLINED via scoping (intentional, not a gap); ensure letter frames as scoping.

**Priority before submission:** (1) `:72-73` 항목을 letter.txt 3-contribution 구조로 확정 (#G1); (2) #G7 local fixes; (3) draft typos (incl. `:226` "the two purpose" → "two purposes"); (4) confirm/decide #G5.

## Tag → Group Mapping

| Tag | Group(s) |
|-----|----------|
| #R1-M1 | #G1 #G4 |
| #R1-M2 | #G2 #G3 #G6 |
| #R1-m1 | #G6 |
| #R2-M1 | #G3 |
| #R2-M2 | #G2 |
| #R2-M3 | #G5 |
| #R2-m1 | #G6 |
| #R2-m2 | #G7 |
| #R2-m3 | #G7 |
| #R2-m4 | #G7 |
| #R2-m5 | #G7 |
| #R2-m6 | #G2 #G7 |
| #R3-M1 | #G1 #G2 |
| #R3-M2 | #G4 |
| #R3-m1 | #G4 |
| #R3-m2 | #G5 |
| #R4-M1 | #G2 #G6 |
| #R4-M2 | #G3 |
| #R4-M3 | #G6 |
| #R4-M4 | #G5 |
| #R4-m1 | #G7 |
| #R4-m2 | #G4 |

## A. Grouped Themes (cross-reviewer)

### #G1 Scientific contribution and novelty framing #R1-M1 #R3-M1

> letter.txt §1 기준으로 정리. headline framing = "runtime contract + adapter boundary가 per-vendor glue-code rewriting을 없애는 reusable 구조"이며, 새로운 estimator/retargeter/interchange format이 아님.

#### #G1 Response

- (1) contribution correction: motion capture, animation, biomechanics, robotics에서 오래 다뤄온 문제임을 **인정**한다. 다만 우리가 방어하는 contribution은 그 문제들을 각각의 system integration으로 종합 해결했다는 것이 아니다.
- 핵심은 **runtime contract + adapter boundary**다: 일정한 구조 안에서, producer는 availability-gated로 shared schema-defined representation에 publish하고, consumer는 이를 downstream에서 반복 재사용한다.
- 실용적 동기: heterogeneity 때문에 end-user는 vendor/application마다 glue code를 rewriting해야 하는 "sticky" 상황에 놓인다. middleware는 device/transform 추상화를 제공하지만, end-user 저작 단계에서는 여전히 source-specific 코드 재작성이 남는다. 우리의 contract는 그 boundary를 재사용 가능하게 만든다.
- 따라서 우리의 기여는 새로운 estimator, retargeter, interchange format이 아니라, runtime producer-consumer boundary를 통해 **partial component availability를 전달하는 contract**이며, 이것이 구현 가능하고 그 위의 authoring이 **하나의 pattern으로 재사용**된다는 근거다.
- (2) standalone contribution promotion (R3-M1): R3 제안에 따라 contribution list (Sec. 1)를 재구성했다. 옛 "reuse + setup evidence" 결합 항목은 삭제하고(`main-rebuttal.tex:74` `\rdel`), authoring-pattern 검증인 **user study를 standalone contribution으로 promote**했다(`:75` `\radd`). 남은 작업은 `:72-73`의 item-1/item-2를 letter.txt의 3-contribution 구조로 최종 일치시키는 것.

### #G2 Evaluation scope, user-study description, and reusable authoring pattern #R1-M2 #R2-M2 #R3-M1 #R4-M1

> letter.txt §2 기준으로 정리. 옛 "implementation traceability vs. user study" 분리 프레이밍은 폐기. user study는 standalone contribution(#G1과 일치)이며, 그 목적은 "contract 위에 구현된 reusable schema prototype이 setup-burden task를 줄여주는가"이다. study description을 정확히 보강하고, 미측정 항목은 limitation으로 명시한다.

#### #G2 Response Core

- 앞선 논의(§1)를 reviewer가 충분히 이해하기에 user study 기재가 부족했다는 의견을 반영한다. user study의 condition을 정확히 기재하고, UnifiedXRMotion과 Vendor SDK의 task 절차를 비교한 테이블(Tab. 4)을 추가하여 어떤 실험이 행해졌는지 이해하기 쉽게 다시 설명했다.
- 해당 내용은 기존 study guide에 이미 포함된 것이며, scope을 새로 재정의하거나 추가 contribution을 derive하는 것이 아니다 (minor-revision 정책 준수: 새 데이터 수집·구현 없음).
- 이 within-subjects 실험의 질문은: UnifiedXRMotion의 **availability + adapter boundary로 구현된 reusable schema prototype**이 setup-burden task를 줄여줄 수 있는가이다. 두 condition은 동일한 scene-level 목표를 가지며, **Custom-Hands**와 **Full-body**를 순차적으로 authoring하는 두 subtask로 구성된다.
- 공정성 통제: condition order counterbalanced, simulator verification(reference clip 대비), 그리고 hand-axis tuning은 측정 task에서 제외(양 condition 모두 pre-completed)임을 기재한다.

#### #G2 Paper Revision

- 해당 evaluation은 두 목적을 가진다. 첫째, availability가 runtime contract로 실제 어떻게 구현되었는지; 둘째, 그 contract 기반 authoring workflow가 준비된 Unity 환경에서 procedural setup burden을 실제로 줄여주는지.
  - ⚠ 논문 측 typo: `main-rebuttal.tex:226` `\radd`가 "The evaluation has **the two purpose**"로 되어 있음 → "has two purposes"로 수정 필요. (Coverage Status 참조)
- availability와 boundary decoupling으로 만들어진 source-agnostic authoring pattern이 user setup-burden을 감소시킬 것으로 가정하고 within-subjects 실험을 준비했다. 실험은 Unity setup task에서 사용자 아바타 표현을 위한 setup을 UXM과 vendor SDK workflow로 비교했다. 두 task는 연속된 두 subtask(Custom-Hands → Full-body)로 구성되며, 결과물은 시뮬레이터에서 재생된 reference 모션과 대조해 검증한다.
- 총 N=19명이 참여했다.
  - (1. counterbalancing) condition 순서를 counterbalance했다(AB/BA).
  - (2. instruction to prioritize correctness) 참여자에게는 속도가 아니라 결과의 정확성을 우선하도록 지시했고, 결과는 reference behaviour 대비 simulator verification으로 확인한다.
  - (3. balance condition) Custom Hand prefab 사용을 위한 Meta SDK 기능 부재를 보정하기 위해, 해당 hand-axis alignment를 양 condition 모두 미리 셋팅했다.
  - (4. task analysis) task instruction은 Tab. 4에 기재된 바와 같으며, 공식 문서를 따른다. 단순 비교 시, source-agnostic 구조가 availability를 활용해 hand와 full body 모두 동일 pattern으로 authoring 가능함을 보인다.
- (R1-M2, R4-M1) 미측정 항목 — motion quality, tracking accuracy, latency, broad SDK coverage, long-term maintainability, adapter-authoring cost, general developer productivity — 은 XR system 평가를 위해 필요하나 본 연구 범위 밖이며 limitation으로 밝힌다. 또한 record가 담지 않는 항목(provenance, continuous confidence, timestamps, schema-version negotiation)도 함께 한계로 명시한다.

### #G3 Practical examples, demonstrations, and early end-to-end example #R1-M2 #R2-M1 #R4-M2

> letter.txt §3 기준. prototype 형태 이해를 돕는 figure를 추가하고, adapter boundary가 무엇으로 정의되는지 명시한다.

#### #G3 Response

- prototype의 형태 이해를 돕기 위해 figure를 추가했다(스터디 시나리오 = hand + body → Y Bot 의 end-to-end 경로). 이 경로는 R2/R4가 요청한 concrete end-to-end example에 해당한다.
- adapter boundary가 무엇으로 정의되는지(= source node가 contract를 처음 emit하는 edge; 그 아래는 source-specific, 그 위는 contract에 대해 generic) 명시한다.
- overclaim 금지: demo/figure는 capability illustration이지 broad device coverage나 motion quality evidence가 아니다.

### #G4 Related work expansion and novelty contrast #R1-M1 #R3-M2 #R3-m1 #R4-m2

> letter.txt §1-(3) 기준. reviewer 지적은 "이 시스템이 왜 필요한지"를 명시적으로 충분히 서술하지 못했다는 것으로 이해한다.

#### #G4 Response

- 리뷰어 지적은 본 논문에서 해당 시스템이 왜 필요한지에 대한 논의를 명시적으로 표현하지 못한 것으로 이해했다.
- 최신 sparse tracking problem 관련 related work를 추가해 그 논의를 분명히 하고, VR social co-presence 관련 work도 추가하여 VR avatar motion에 관한 내용을 재요약했다.
- Reviewer-suggested refs는 positioning을 뒷받침할 때만 인용한다(checklist식 인용 지양): R3의 IMUPoser / intent-driven input arbitration, R4의 sparse-pose·avatar-motion refs는 optional.

### #G5 Technical specificity, reproducibility, and detail rebalancing #R2-M3 #R3-m2 #R4-M4

> 상충하는 두 요청의 절충: R2는 technical narrative 축소 요청, R3/R4는 reproducibility detail 추가 요청 → **less walkthrough, more specification**. (letter.txt에는 아직 본 항목이 명시적으로 기재되지 않음 — letter 작성 단계에서 결정 필요.)

#### #G5 Response (draft — letter 미반영)

- narrative implementation walkthrough는 줄이고, contract boundary 재현에 필요한 schema/adapter/availability-gating detail은 보강한다.
- 유지/강화: contract math·schema fields, `ITrackingDeviceHandler` 책임, `PhysicBone` + `PoseFlag`, `TrackingManager` flag propagation, `RetargetSystem` gated assignment, one end-to-end example.
- 축소/이동: 반복적 scoping 문장, per-adapter walkthrough, 필요 이상 FishNet transport detail, 재현성에 불필요한 trigger/event propagation detail.

### #G6 Terminology, calibration, and scoped limitations #R1-m1 #R2-m1 #R4-M1 #R4-M3

> letter.txt §2 말미(provenance/confidence/timestamps/schema-version를 limitation으로 명시)와 일치. calibration 관련 R2-m1 응답은 letter.txt §3 "(R2) calibration"에 자리만 잡혀 있고 미작성 — letter 단계에서 채울 것.

#### #G6 Response

- 용어: "validity-aware"는 **binary component availability**(producer semantics 하에서 "이 component가 publish되었는가")로 정의하며, confidence·provenance·source type·freshness·correctness가 아님을 명확히 한다. record가 담지 않는 것: timestamps, schema-version negotiation, continuous confidence, provenance.
- Calibration (R2-m1): real glue code가 tracking-space calibration / room transform을 포함한다는 지적을 인정한다. UXM은 coordinate conversion·calibration을 adapter 및 `TrackingSpaceCorrection` / `MotionAvatar.Spawn` boundary에서 **localize**할 뿐, calibration 문제 자체를 제거하지 않는다. contract는 source-space 값이 합의된 schema/space로 매핑된 이후에 시작한다.
- Limitations: motion quality, tracking accuracy, latency, broad device coverage, maintainability, adapter-authoring cost 미측정; general developer productivity에 대한 주장 없음; setup study는 prepared-task 근거에 한정.

### #G7 Local writing fixes and repetition cleanup #R2-m2 #R2-m3 #R2-m4 #R2-m5 #R2-m6 #R4-m1

> 순수 local writing 수정 목록 (letter에는 개별 기재 불필요 — 논문에서 직접 수정; rebuttal에는 "addressed the noted local issues" 정도로 묶어 언급 가능). 코드 근거는 implementation-and-study-facts.md.

#### #G7 Response (checklist — 논문 직접 수정)

- "tied to one SDK"에 example SDK 명시 (Meta XR Core / Interaction / Movement SDK).
- "Textbook IK" → "FABRIK" 또는 "FABRIK-style IK" + 능동태 (코드: `FABRIKSolver.cs`; `main-rebuttal.tex:87`, ~L198).
- 어색한 EuroXR 문장 재작성/삭제.
- FishNet 언급 시 citation/정의 추가, 아니면 FishNet detail 제거 (코드: `Network/NetworkNodeWrapper.cs`).
- "The evaluation follows the evidence chain implied by the contract"를 평이한 영어로 재작성 (`main-rebuttal.tex:229`에서 이미 `\rdel` 처리됨 — 대체 문장 `:226` 확인).
- "selected/representative/scoped" 반복 축소; claim을 보호하는 scope 문장은 유지.

## B. Per-Reviewer Details

### R1 (score 4)

#### Major

- #R1-M1 "Not yet as a sufficiently mature scientific contribution"
  - Related work too narrow: mocap, animation, biomechanics, robotics, skeletal data interchange
- #R1-M2 Evaluation is narrow: should be broader
  - developer productivity, maintainability, runtime performance, motion quality, general interoperability

#### Minor

- #R1-m1 Clarify terminology "validity-aware" (binary availability ≠ confidence/provenance)

### R2 (score 5)

#### Major

- #R2-M1 Practical examples / demonstrations to highlight capabilities (in the paper body and evaluation section)
  - Video
- #R2-M2 Study poorly described + evaluation needs higher-level introduction: participant numbers, ethics permissions, full study materials; frame the purpose before software terminology
- #R2-M3 Move technical details (Sec. 3–6) to Supplementary

#### Minor

- #R2-m1 Real pain is tracking coordinate relationships / calibration step, not slot availability
- #R2-m2 Example SDK for "tied to one SDK"
- #R2-m3 Textbook IK (→ FABRIK), grammar + active voice "Textbook IK and prior codebook-style control ..."
- #R2-m4 EuroXR sentence
- #R2-m5 FishNet citation
- #R2-m6 "The evaluation follows the evidence chain implied by the contract" — rewrite in plainer English

### R3 (score 7)

#### Major

- #R3-M1 Restructure contributions: within-subjects validation as standalone, fold first item into others
- #R3-M2 Related Work is thin: avatars in VR, social presence

#### Minor

- #R3-m1 Suggested refs: IMUPoser (Mollyn et al.), intent-driven input arbitration (Gonzales et al.)
- #R3-m2 More implementation details (reproducibility)

### R4 (score 7)

#### Major

- #R4-M1 Weaknesses mostly scope & presentation: evaluation doesn't measure motion quality, tracking accuracy, latency, broad device coverage, long-term maintainability, cost of writing new adapters
- #R4-M2 Concrete end-to-end example early in the paper
- #R4-M3 Distinction availability / confidence / provenance more explicit
  - annotate limitations, discuss future extension of the system
  - record also omits: timestamps, schema-version negotiation
- #R4-M4 More adapter/schema details (reproducibility)

#### Minor

- #R4-m1 Reducing repetition ("selected/representative/scoped")
- #R4-m2 (Optional) 6 suggested refs — no need to cite
