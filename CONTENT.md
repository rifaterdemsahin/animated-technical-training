# 🎬 Animated Technical Training

Show, don't tell. A repo-driven video production pipeline that turns scripts, storyboards & sprites into animated technical training videos using Canva + AI.

[📐 Master Spec](MASTER_SPEC.md) · [📄 README](README.md) · [📝 Content](CONTENT.md) · [✏️ Edit Content](https://github.com/rifaterdemsahin/animated-technical-training/edit/main/CONTENT.md)

**On this page:** [🧩 Problem](#-problem) · [✅ Solution](#-solution) · [🧠 Core Principle](#-core-principle) · [⚖️ Half Hands-On, Half Automated](#%EF%B8%8F-half-hands-on-half-automated) · [🔗 Video Production Pipeline](#-video-production-pipeline) · [🏗️ Stages](#%EF%B8%8F-stages) · [🌐 References](#-references)

## 🧩 Problem

**Problem:** Rapid AI progress keeps raising the skill expectations placed on people, faster than most can keep up.

**👥 Audience:** people who are part of the new AI revolution that started with chatGPT, and are now updating their workflows to a much more powerful AI tools such as claude code.

**🛠️ Domain:** tools getting enabled with AI are shifting and effecting many industries not just coding.

![Problem illustration](https://raw.githubusercontent.com/rifaterdemsahin/animated-technical-training/main/3_Simulations/problem.png)

## ✅ Solution

Comics-based animated technical training, so the concepts are easier to consume. 

** Rationale :** We have seen shorter animated videos have a much higher retention.

![Comic animation sample](https://raw.githubusercontent.com/rifaterdemsahin/animated-technical-training/main/3_Simulations/comic_animation_sample.jpeg)

**How:** We need to create technical animation for the Claude AI Architect course — Collect feedback in our cohorts and take daily notes in a whiteboard, and cast a wide net so we can include a much wider audience and listen audience problems.

## 🧠 Core Principle

**Cognitive Offload — Show, Don't Tell 👁️**
Narration and visuals must never carry the same information twice. Concept transfer lives in the animation (`visual_action`); voiceover (`incoming`/`outgoing`) stays light and confirmatory.

✅ **The Mute Test:** if a scene, watched with no audio, doesn't convey the concept — it isn't done.

🧪 **The Subtitle Test:** watch the scene with just the subtitle showing — if the animation still makes sense on its own, that's the main animation test.

## ⚖️ Half Hands-On, Half Automated

Bulk export and asset generation are automated to move fast; animation timing and voice are finished manually to reach top quality — **audience retention and reach are on the line, so we can't risk low quality by auto generating content that does not line up with what audience needs.**

🎯 That means every scene needs to be **frame by frame mapped** — whiteboard,script,slides, storyboard and animation direction locked before automation and generation touches it, not patched after.

![Animation example](https://raw.githubusercontent.com/rifaterdemsahin/animated-technical-training/main/3_Simulations/animation.jpg)
![Automated vs manual example](https://raw.githubusercontent.com/rifaterdemsahin/animated-technical-training/main/3_Simulations/automated_manual.jpg)

## 🔗 Video Production Pipeline

### 🧪 Preprod

#### 🔍 0. Research — Canva Whiteboard

- Save reference images & text as they're found
- Left to right flow — chronological research trail

![Whiteboard notes](https://raw.githubusercontent.com/rifaterdemsahin/animated-technical-training/main/3_Simulations/whiteboard_notes.jpeg)

🗂️ [Open whiteboard →](https://www.canva.com/design/DAHN5D7MhYE/ZPkd6ouYrf20A1MhZu0WZQ/edit)

📅 **Cadence:** Daily

☐ **Task:** [Create the Canva course folder structure →](https://www.canva.com/folder/FAHMZK9u-JE)

#### 🎨 1. Canva Slides — Source of Cohort Session

- Script — master flow for the content
- Images (AI-generated sprite assets)
- Storyboard — Gemini-generated inspirational frames
- Notes — per-frame script & animation direction

☐ **Task:** Build the script, images, storyboard & notes in one Canva design.

🎨 [Open Slides →](https://www.canva.com/design/DAHQCqMC7Ck/2MvbdPMlSTcF9wtS6Y75zQ/edit?ui=eyJBIjp7fX0)

🖼️ [Open Storyboard →](https://www.canva.com/design/DAHOxcN-Gx4/6kGlPNG10LlEP6bzv4PXSQ/edit)

📅 **Cadence:** Sundays

💡 [Why one Canva design →](rationale/readme.md#canva)

#### 🎞️ 2. Review Canva Presentations

Done in Canva Presentations — no separate tool.

- Frame view per scene: sprite preview + incoming/outgoing + `visual_action` notes
- Inline edit, clone scene, reorder
- Mark scenes ✅ "ready"

☐ **Task:** Review each scene in Canva Presentations and mark it "ready".

💡 [Why review before export →](rationale/readme.md#carousel)

#### 📦 3. Export Step

Exports from the Canva Slides presentation, to import into Canva Video.

- Flattens "ready" scenes for Canva import
- Embeds sprite images
- Respects Canva's 300-page limit — batches by video if exceeded

☐ **Task:** Run the export script to flatten "ready" scenes for Canva import.

💡 [Why flatten & batch →](rationale/readme.md#export)

### 🏭 Prod

#### ⚡ 4. Canva Bulk Create

- Exports all pages as video (sprite + incoming + outgoing)
- Voiceovers embedded inside the videos

☐ **Task:** Run Canva Bulk Create to export all pages as video.

💡 [Why bulk create →](rationale/readme.md#bulk-create)

#### 🧬 5. Asset Generation

- Generate any AI assets still missing after bulk create — sprites, backgrounds, extra imagery
- Fill gaps before manual finishing starts

☐ **Task:** Generate and collect any missing AI assets for scenes.

### 🎬 Post

#### ✨ 6. Canva Manual Finishing

- Animate per element/page — motion path preferred over generic entrance FX
- Generate AI voice per page from incoming/outgoing text

☐ **Task:** Manually animate elements per page and generate AI voice for each.

💡 [Why manual, not automated →](rationale/readme.md#manual-finishing)

#### 🚀 7. Export MP4

Final per-domain training video files.

☐ **Task:** Export the final per-domain MP4 training video files.

💡 [Why per-domain files →](rationale/readme.md#export-mp4)

## 🏗️ Stages

### 🧪 Preprod

- 0. Research 🔍 — 2 subtasks
- 1. Canva Slides 🎨 — 1 subtask
- 2. Review 🎞️ — 1 subtask
- 3. Export Step 📦 — 1 subtask

### 🏭 Prod

- 4. Bulk Create ⚡ — 1 subtask
- 5. Asset Gen 🧬 — 1 subtask

### 🎬 Post

- 6. Manual Finish ✨ — 1 subtask
- 7. Export MP4 🚀 — 1 subtask

## 🌐 References

### 🖌️ Manual Animation

[Source design](https://www.canva.com/design/DAHP1RV4ILg/nTilowGAWQrxcqefQoFSUQ/edit)

### 🎥 Manual Animation Output

[Rendered output](https://www.canva.com/design/DAHP1c7gOR8/BNhFha3kTMtMAdpgteVUPw/edit?ui=e30#)

### 💳 Canva AI Costs

[Billing & teams](https://www.canva.com/settings/billing-and-teams)

### 🤖 Claude

[claude.ai](https://claude.ai/)

### 🪄 Mage.space

[Creations](https://www.mage.space/creations)

### ♊ Gemini

[gemini.google.com](https://gemini.google.com/)

### 🎞️ Higgsfield

[higgsfield.ai](https://higgsfield.ai/)

---

Manual build wins on aesthetics — a comic deserves craft over cringe. 🎨✨

[🌐 View on GitHub Pages](https://rifaterdemsahin.github.io/animated-technical-training/)
