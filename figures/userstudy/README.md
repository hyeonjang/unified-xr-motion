# Participant Manual — SDK A vs SDK B

**Goal:** Follow clear steps to set up the same scene in Unity using **two different SDKs** and verify the results with the simulator.

link: https://docs.google.com/forms/d/e/1FAIpQLSfKta_5VTDDhBr73GycSTtEXZZVMVA3GtLfT6Oyh-QB05UxIw/viewform?usp=header

> Please **follow each step exactly as written**. Do **not** skip or optimize. If a step is unclear, flag the issue to the administrator.

> **Important — Hand–Axis Alignment is pre‑completed** &#x20;
> For this study, all **hand retargeting / axis alignment** for the custom hand meshes was **performed by the research team prior to your session**. You do **not** need to tune axes or run any hand retargeting tools. &#x20;
> *Rationale:* SDK A performs automatic anatomical‑frame alignment via the **XR Hand Retargeter**, removing per‑avatar manual tuning. SDK B does not include built‑in hand‑axis alignment; therefore, we completed the required retargeting and mesh‑specific adjustments **before** sessions to avoid confounding task time and questionnaire ratings.

---
## Quick Checklist (Before You Start)

* Unity installed: **6000.0.33f1**
* Project opens without errors
* Meta Core SDK available for SDK B condition (**78.0.0**)
* Movement SDK available for SDK B condition (**78.0.0**)
* Meta XR Simulator available and enabled when needed (**78.0.0**)
* **Hand–Axis Alignment:** Pre‑session retargeting for custom hand meshes is **already done**. Do **not** perform additional axis tuning.
* You can see these assets in the **Project** window:

  * **Assets/Scenes/Task-A.unity** and **Assets/Scenes/Task-B.unity**
  * **SceneObjects**, **Y Bot**, **Hands**
  * **Hands** contains **OpenXRCustomHandPrefab\_L** and **OpenXRCustomHandPrefab\_R**

---

## Plain‑Language Glossary (1‑minute read)

* **SDK** (Software Development Kit): A set of tools that adds features to Unity.
* **Prefab**: A ready‑made object you can place into the scene (like a template).
* **Hierarchy**: The list of objects in the current scene (left side of Unity by default).
* **Inspector**: The panel to change settings of the selected object (right side of Unity by default).
* **Project window**: The file browser for assets in your project (bottom of Unity by default).
* **Simulator**: A tool that fakes body and hand movements so you can test without a headset.

You will interact with: **Hierarchy**, **Inspector**, **Project window**, and the **Simulator**.

---

## Start Here — Open Your Assigned Scene

1. In Unity, open the **Project** window.
2. Go to **Assets/Scenes/**.
3. Open both scenes once: **Task-A.unity** and **Task-B.unity**.
4. Double‑click **your assigned scene** (Task‑A or Task‑B) to make it active.

> The scene includes a basic layout: `SceneObjects`, **Y Bot**, and **Hands** with **OpenXRCustomHandPrefab\_L** and **OpenXRCustomHandPrefab\_R**.

> **Note:** Hand retargeting for the provided custom hand prefabs (L/R) was completed before your session. No action is required for axis alignment.
---

## How You Will Check Your Work (both SDKs)

You will compare what you see to short reference clips.

### Run the Simulator

1. In the Unity toolbar, turn on the **Meta Simulator** toggle (next to **Play**).
2. Click **Play**.
3. In the running scene, open **Inputs → Movement Tracking Controls** in the **Meta XR Simulator** window.
4. To test **full body**: click **Play random movement**.
5. To test **hands**: use **WASD** to move hands, or **click** inside the Simulator window to make a **pinch** gesture.

### What “Correct” Looks Like

**SDK A — expected behavior**

<table>
  <tr>
    <td align="center" width="50%">
      <img src="Data/Videos/ours-fullbody-result.gif" width="100%" alt="FullBody Tracking (SDK A)">
      <div><em>Full‑Body Tracking (SDK A)</em></div>
    </td>
    <td align="center" width="50%">
      <img src="Data/Videos/ours-hands-result.gif" width="100%" alt="Hands Tracking and Retargeting (SDK A)">
      <div><em>Hands Tracking & Retargeting (SDK A)</em></div>
    </td>
  </tr>
</table>

**SDK B — expected behavior**

<table>
  <tr>
    <td align="center" width="50%">
      <img src="Data/Videos/meta-fullbody-result.gif" width="100%" alt="FullBody Tracking (SDK B)">
      <div><em>Full‑Body Tracking (SDK B)</em></div>
    </td>
    <td align="center" width="50%">
      <img src="Data/Videos/meta-hands-result.gif" width="100%" alt="Hands Tracking and Retargeting (SDK B)">
      <div><em>Hands Tracking & Retargeting (SDK B)</em></div>
    </td>
  </tr>
</table>

If your scene behaves like the clips, your setup is **correct**.

---

# Task‑A — SDK A

* **Assets/Scenes/Task-A.unity**
* **SceneObjects**, **Y Bot**, **Hands**
* **Hands** contains **OpenXRCustomHandPrefab\_L** and **OpenXRCustomHandPrefab\_R**

**Goal:**

* Make the custom hand models (**`OpenXRCustomHandPrefab_L/R`**) follow simulated hand motion.
* Make **Y Bot** move with simulated full‑body motion.

---

## Steps — Hands (Hands‑only simulation)

> **SDK A Hand Alignment**
> SDK A uses the **XR Hand Retargeter** for automatic anatomical‑frame alignment. No manual axis tuning is required.

1. **Confirm hand prefabs exist**

   * In the **Hierarchy**, expand **`Hands`** → confirm **`OpenXRCustomHandPrefab_L`** and **`OpenXRCustomHandPrefab_R`** are present.

2. **Add Motion Avatar to Hands**

   * Select **`Hands`** (Hierarchy) → in **Inspector** → **Add Component** → add **`Motion Avatar`**.

3. **Configure Motion Avatar (Hands)**

   * On **`Hands`** → **`Motion Avatar`**, set **`Body Type = Two Hands`**.

4. **Add MotionSystem prefab (for Hands)**

   * From `Packages/Unified XR Motion/Assets/Prefabs/MotionSystem.asset`, drag **`MotionSystem`** into the scene.

5. **Assemble MotionSystem (for Hands)**

   * Under **`TrackingSystem`**, add **`Meta Hand Tracking`**.
   * Under **`RetargetSystem`**, add **`Two Hands Retargeter`**.
   * On **`RetargetSystem / Retarget System`**, set **`Motion Avatar = Hands`**.

6. **Connect the parts**

   * In **`Retarget System`**, add **`Two Hands Retargeter`** to **`Input Motions`**.
   * On **`Two Hands Retargeter`**, set **`Input Motion = TrackingSystem`**.

---

## Steps — Full Body

1. **Add Motion Avatar to Y‑Bot**

   * Select **`Y Bot`** → **Inspector** → **Add Component** → add **`Motion Avatar`**.

2. **Add a separate MotionSystem prefab (for Full Body)**

   * From `Packages/Unified XR Motion/Assets/Prefabs/MotionSystem.asset`, add another **`MotionSystem`** into the scene.

3. **Assemble MotionSystem (for Full Body)**

   * Under **`TrackingSystem`**, add **`Meta Body Tracking`**.
   * Under **`RetargetSystem`**, add **`Meta Full Body Retarget`**.
   * On **`RetargetSystem / Retarget System`**, set **`Motion Avatar = Y Bot`**.

4. **Connect the parts**

   * In **`Retarget System`**, add **Meta Full Body Retarget** to **Input Motions**.
   * On **`Meta Full Body Retarget`**, set **`Input Motion = TrackingSystem`**.

---

## Verify — SDK A

1. Turn on the **Meta Simulator** toggle → click **Play**.
2. **Hands:** move with **WASD** or click for **pinch**.
3. **Full body:** **Inputs → Movement Tracking Controls → Play random movement**.
4. Compare with the **SDK A** reference clips.

---

# Task‑B — SDK B

* **Assets/Scenes/Task-B.unity**
* **SceneObjects**, **Y Bot**, **Hands**
* **Hands** contains **OpenXRCustomHandPrefab\_L** and **OpenXRCustomHandPrefab\_R**

**Goal:**

* Make **Y Bot** move with simulated full‑body motion.
* Use the provided custom hand models (**`OpenXRCustomHandPrefab_L/R`**) for hands‑only motion.

---

## Steps — Hands (Hands‑only simulation)
-  ref1: https://developers.meta.com/horizon/documentation/unity/unity-handtracking-hands-setup
-  ref2: https://developers.meta.com/horizon/documentation/unity/unity-isdk-customize-hand-model
-  ref3: https://developers.meta.com/horizon/documentation/unity/unity-isdk-input-processing/

> **SDK B Hand Alignment**
> SDK B lacks built‑in hand‑axis alignment. The research team **pre‑retargeted** the custom hand meshes. **Do not** run retargeting tools or change axes.

1. **Confirm hand prefabs exist**

   * In the **Hierarchy**, expand **`Hands`** → confirm **`OpenXRCustomHandPrefab_L`** and **`OpenXRCustomHandPrefab_R`** are present.

2. **Add the camera rig**

   * From `Packages/Meta XR Core SDK/Prefabs`, drag **`OVRCameraRig`** into the root of the scene.

3. **Add hand interaction prefabs**

   * From `Packages/Meta XR Interaction SDK/Runtime/Prefabs`, drag **`OVRInteractionComprehensive`** as a child of **`OVRCameraRig`**.
   * Keep only **`OVRHands`** under **`OVRInteractionComprehensive`** (remove extras).
   * On **`OVRInteractionComprehensive`**, set **`OVR Camera Rig Ref → OVR Camera Rig = OVRCameraRig`**.

4. **Add synthetic hands for simulation**

   * From `Packages/Meta XR Interaction SDK Essentials/Runtime/Prefabs/Hands/`, add **`OVRLeftHandSynthetic`** and **`OVRRightHandSynthetic`** as children of `OVRCameraRig/OVRInteractionComprehensive`.

5. **Remove default hand visuals**

   * Under **`OVRLeftHandSynthetic/OVRLeftHandVisual`**, delete **`OpenXRLeftHand`** and **`OculusHand_L`**.
   * Under **`OVRRightHandSynthetic/OVRRightHandVisual`**, delete **`OpenXRRightHand`** and **`OculusHand_R`**.

6. **Add the custom hand prefabs**

   * Drag **`OpenXRCustomHandPrefab_L`** under `OVRLeftHandSynthetic/OVRLeftHandVisual`.
   * Drag **`OpenXRCustomHandPrefab_R`** under `OVRRightHandSynthetic/OVRRightHandVisual`.

7. **Adjust Hand Visual settings**

   * **Left:**

     * On **`OVRLeftHandVisual`**, enable **`Update Root Pose`** and **`Update Root Scale`**.
     * Assign **Open XR Skinned Mesh Renderer** to **`LeftHand`** (child of `OpenXRCustomHandPrefab_L/OpenXRLeftHand`).
     * On **`OpenXRCustomHandPrefab_L`**, enable **`Update Root Pose`** and **`Update Root Scale`** in **OVR Custom Skeleton**.
   * **Right:**

     * On **`OVRRightHandVisual`**, enable **`Update Root Pose`** and **`Update Root Scale`**.
     * Assign **Open XR Skinned Mesh Renderer** to **`RightHand`** (child of `OpenXRCustomHandPrefab_R/OpenXRRightHand`).
     * On **`OpenXRCustomHandPrefab_R`**, enable **`Update Root Pose`** and **`Update Root Scale`** in **OVR Custom Skeleton**.

8. **Link DataModifier components**

   * **Left:**

     * On **`OVRLeftHandSynthetic`**, set **Source = OVRHands** in **Modify Data From Source**.
     * Ensure **Left** reads from **`OVRHands.Left`**.
   * **Right:**

     * On **`OVRRightHandSynthetic`**, set **Source = OVRHands**.
     * Ensure **Right** reads from **`OVRHands.Right`**.

---

## Steps — Full Body
- ref: https://developers.meta.com/horizon/documentation/unity/move-body-tracking/

1. **Enable body tracking on the rig**

   * On **`OVRCameraRig`** → **`OVRManager`**:

     * **Tracking Origin Type = Floor Level**
     * **Body Tracking Support = Required**
     * **Body Tracking Joint Set = Full Body**
     * *(Optional)* Hand Tracking Support = Controllers And Hands

2. **Create a Movement SDK retargeting config for Y‑Bot**

   * In **Hierarchy**, right‑click **Y‑Bot** → **Movement SDK → Body Tracking → Open Retargeting Configuration Editor**.
   * In the wizard: click **Next**, review mappings → **Validate and Save Config** → **Done**.
> When the Retargeting Configuration Editor wizard appears, you do not need to adjust any mappings or transforms for this task. Simply click Next on each screen and proceed until you reach the final Validate and Save Config step. Save the configuration as prompted.

3. **Add a Character Retargeter to Y‑Bot**

   * Right‑click **Y‑Bot** → **Movement SDK → Body Tracking → Add Character Retargeter**.
   * In the wizard: click **Next**, review mappings → **Validate and Save Config** → **Done**.
> When the Retargeting Configuration Editor wizard appears, you do not need to adjust any mappings or transforms for this task. Simply click Next on each screen and proceed until you reach the final Validate and Save Config step. Save the configuration as prompted.
---

### Verify — SDK B

1. Turn on the **Meta Simulator** toggle → click **Play**.
2. Full body: **Inputs → Movement Tracking Controls → Play random movement**.
3. Hands: use **WASD** or click for **pinch**.
4. Compare with the **SDK B** reference clips.


<table>
  <tr>
    <td align="center" width="50%">
      <img src="Data/Videos/meta-fullbody-result.gif" width="100%" alt="FullBody Tracking (Meta)">
      <div><em>Full‑Body Tracking (SDK B)</em></div>
    </td>
    <td align="center" width="50%">
      <img src="Data/Videos/meta-hands-result.gif" width="100%" alt="Hands Tracking and Retargeting (Meta)">
      <div><em>Hands Tracking & Retargeting (SDK B)</em></div>
    </td>
  </tr>
</table>

---

## Troubleshooting (Quick Fixes)

* **I don’t see the Simulator panel.** Stop Play mode. Toggle the **Meta Simulator** off and on, then press **Play** again.
* **Hands don’t move.** Recheck that **OVRHands** is assigned to both **DataModifier** components (Meta task) or that **Two Hands Retargeter** input is the **TrackingSystem** (Task A).
* **Y Bot doesn’t move.** Confirm **Body Tracking** is enabled (Meta task) or that **Meta Body Tracking** feeds into **Meta Body Retargeter** with **Motion Avatar = Y Bot** (Task A).
* **Pink/missing models.** Ensure the **OpenXRCustomHandPrefab\_L/R** and **Y Bot** objects are present in the **Hierarchy** and their materials are assigned in the **Inspector**.

---

## After You Finish

1. Compare your scene behavior to the reference clips.
2. If your result matches, tell the administrator you are done.
3. Complete the questionnaires: **NASA‑TLX** and **SUS**.
4. Submit the survey here: **[Study Survey Link](https://docs.google.com/forms/d/e/1FAIpQLSfKta_5VTDDhBr73GycSTtEXZZVMVA3GtLfT6Oyh-QB05UxIw/viewform?usp=header)**.

> Focus on **accuracy** and **task completion**, not speed.

---

## Version & Date

* **Unity**: 6000.0.33f1
* **Meta Core SDK**: 78.0.0 (SDK B condition)
* **Movement SDK**: 78.0.0 (SDK B condition)
* **Meta XR Simulator**: 78.0.0
* Manual last updated: **September 8, 2025**
