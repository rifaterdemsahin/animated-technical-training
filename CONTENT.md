# 🎬 Animated Technical Training

Show, don't tell. A repo-driven pipeline that turns scripts, storyboards & sprites into animated technical training videos using Canva + AI.

[📐 Master Spec](MASTER_SPEC.md) · [📄 README](README.md)

## 🧩 Problem

**Problem:** Rapid AI progress keeps raising the skill expectations placed on people, faster than most can keep up.

**How:** We need to create technical animation for the Claude AI Architect course — and cast a wide net so we can include a much wider audience.

**👥 People:** people who are part of the new AI revolution that started with GPT, and are now updating their workflows to a much more powerful tool.

**🛠️ Domain:** tools getting enabled with AI are shifting and effecting many industries not just coding.

![Problem illustration](https://raw.githubusercontent.com/rifaterdemsahin/animated-technical-training/main/3_Simulations/problem.png)

## ✅ Solution

Comics-based animated technical training, so the concepts are easier to consume.

![Comic animation sample](https://raw.githubusercontent.com/rifaterdemsahin/animated-technical-training/main/3_Simulations/comic_animation_sample.jpeg)

## 🧠 Core Principle

**Cognitive Offload — Show, Don't Tell 👁️**
Narration and visuals must never carry the same information twice. Concept transfer lives in the animation (`visual_action`); voiceover (`incoming`/`outgoing`) stays light and confirmatory.

✅ **The Mute Test:** if a scene, watched with no audio, doesn't convey the concept — it isn't done.

## ⚖️ Half Hands-On, Half Automated

Bulk export and asset generation are automated to move fast; animation timing and voice are finished manually to reach top quality — **audience retention and reach are on the line, so we can't risk low quality.**

🎯 That means every scene needs to be **frame by frame mapped** — script, storyboard and animation direction locked before automation touches it, not patched after.

![Animation example](https://raw.githubusercontent.com/rifaterdemsahin/animated-technical-training/main/3_Simulations/animation.jpg)
![Automated vs manual example](https://raw.githubusercontent.com/rifaterdemsahin/animated-technical-training/main/3_Simulations/automated_manual.jpg)

## 🔗 Pipeline

### 🧪 Preprod

#### 🔍 0. Research — Canva Whiteboard

- Save reference images & text as they're found
- Left to right flow — chronological research trail

![Whiteboard notes](https://raw.githubusercontent.com/rifaterdemsahin/animated-technical-training/main/3_Simulations/whiteboard_notes.jpeg)

🗂️ [Open whiteboard →](https://www.canva.com/design/DAHN5D7MhYE/ZPkd6ouYrf20A1MhZu0WZQ/edit)

☐ **Task:** [Create the Canva course folder structure →](https://www.canva.com/folder/FAHMZK9u-JE)

#### 🎨 1. Canva Slides — Source of Cohort Session

- Script — master flow for the content
- Images (AI-generated sprite assets)
- Storyboard — Gemini-generated inspirational frames
- Notes — per-frame script & animation direction

☐ **Task:** Build the script, images, storyboard & notes in one Canva design.

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

1. Outline 📝
2. Script 📜
3. Visual Production 🖼️
4. Import 📥
5. Voiceovers 🎙️
6. Polish 💎

## 📁 Repo Layout

```
index.html            → this page: pipeline overview
MASTER_SPEC.md        → full design, schema & build phases
Canva Course Folder   → script / storyboards / presentation (linked)
README.md             → project overview
rationale/            → why the pipeline was designed this way
output/               → sample MP4 outputs (cringe vs. quality)
models/               → image-model comparison for sprite generation
```

## 🌐 References

### 🖌️ Manual Animation

[Source design](https://www.canva.com/design/DAHP1RV4ILg/nTilowGAWQrxcqefQoFSUQ/edit)

### 🎥 Manual Animation Output

[Rendered output](https://www.canva.com/design/DAHP1c7gOR8/BNhFha3kTMtMAdpgteVUPw/edit?ui=e30#)

### 💳 Canva AI Costs

[Billing & teams](https://www.canva.com/settings/billing-and-teams)

---

Manual build wins on aesthetics — a comic deserves craft over cringe. 🎨✨

[🌐 View on GitHub Pages](https://rifaterdemsahin.github.io/animated-technical-training/)
