# 🎨 Stage Image Prompts (Mage.space)

Generation prompts for one explanatory image per pipeline stage, meant for [mage.space/models](https://www.mage.space/models). All eight share a **style anchor** so the set reads as one consistent course, not eight random images — paste the style anchor at the start of every prompt, then swap in the stage-specific scene.

**Style anchor** (prepend to every prompt):
> flat vector comic illustration, bold clean linework, warm limited color palette (navy, teal, amber, coral), soft cel shading, tech-startup whiteboard aesthetic, no text or logos in image, 16:9

**Model:** Flux.1 Dev — best default on Mage.space for clean flat-illustration/comic style with consistent characters and legible composition. Dreamshaper XL is a good fallback if you want a slightly softer, more painterly look; avoid photoreal models (Realistic Vision, Juggernaut XL) for this set since the site's whole premise is comic-style, not photoreal. Model names on Mage.space change over time — check [mage.space/models](https://www.mage.space/models) for the current list before generating.

**Settings:** 16:9, steps 30–40, guidance/CFG ~4–6 (Flux likes lower CFG than SD), seed locked per stage once you find a result you like so re-rolls stay in the same visual family.

---

## 🧪 Preprod

### 🔍 0. Research — Canva Whiteboard

> flat vector comic illustration, bold clean linework, warm limited color palette (navy, teal, amber, coral), soft cel shading, tech-startup whiteboard aesthetic, no text or logos in image, 16:9 — a person pinning printed screenshots and sticky notes onto a large whiteboard in a left-to-right timeline, research trail of images and scribbled arrows, coffee cup on a nearby desk, early-morning light through a window

### 🎨 1. Canva Slides — Source of Cohort Session

> [style anchor] — a person at a laptop building a slide deck, floating panels around them showing a script document, AI-generated sprite characters, a storyboard strip, and sticky notes with frame-by-frame directions, all panels converging into one central Canva-branded slide canvas

### 🎞️ 2. Review Canva Presentations

> [style anchor] — a person reviewing a horizontal carousel of slide thumbnails floating in front of them, one thumbnail glowing with a green checkmark for "ready," their hand mid-gesture reordering two cards, small callout bubbles showing incoming/outgoing text notes

### 📦 3. Export Step

> [style anchor] — a wide funnel machine on a desk, slides flowing in from the top and compressing into stacked video batches coming out the bottom, a small progress meter showing "300-page limit," sprite thumbnails visible inside the funnel

## 🏭 Prod

### ⚡ 4. Canva Bulk Create

> [style anchor] — a grid of video frames all rendering simultaneously on a wall of monitors, small progress bars under each, sprite characters mid-animation on several screens, a sound-wave icon indicating embedded voiceover, energetic parallel-processing feel

### 🧬 5. Asset Generation

> [style anchor] — a robotic arm or AI sparkle-wand painting in missing pieces of a half-finished scene — a background, a sprite silhouette, an extra prop — onto a canvas that's otherwise complete, gap-filling motif

## 🎬 Post

### ✨ 6. Canva Manual Finishing

> [style anchor] — an animator at a desk dragging a glowing motion-path curve across a character sprite on screen, a microphone icon nearby recording AI voice, meticulous hands-on craft feeling, magnifying glass on the desk suggesting frame-by-frame precision

### 🚀 7. Export MP4

> [style anchor] — a stack of labeled film reels or video file icons (one per domain) rolling off a conveyor belt into neat labeled bins, a checkered "finished" flag, warm completed-project glow

---

[⬅ Back to Content](CONTENT.md) · [🌐 Live Page](https://rifaterdemsahin.github.io/animated-technical-training/)
