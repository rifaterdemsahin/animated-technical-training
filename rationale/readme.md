# Why we decided on this pipeline

Core principle: **Cognitive Offload — Show, Don't Tell.** Narration and visuals must
never carry the same information twice (Sweller/Mayer redundancy effect). Concept
transfer lives in the animation; voiceover stays light and confirmatory. Every
decision below is in service of that, plus Canva's real constraints (300-page
import limit, no reliable animation/voice API).

<a name="canva"></a>
## 1. Canva — Source of Truth

Script, sprite images, storyboard and per-frame notes all live inside one Canva
design instead of being split across a doc, an image folder and a spreadsheet.
Keeping them co-located means the written script and the drawn frame can't drift
apart before any tooling touches them, and non-engineers can edit the source
directly.

<a name="carousel"></a>
## 2. Carousel Review App

Reviewing scene-by-scene *before* export lets us apply the "mute test" cheaply —
catch a scene where the voiceover is doing the explaining instead of the
animation — while it's still just an edit, not a rendered video. Inline edit,
clone and reorder happen here because fixing a scene after Canva Bulk Create has
already turned it into a video page is much more expensive.

<a name="export"></a>
## 3. Export Step

Canva enforces a hard 300-page limit per import. Flattening only scenes marked
✅ "ready" keeps drafts out of the export, and batching by video when a domain
exceeds 300 scenes is what makes bulk creation possible at all instead of
hitting the ceiling mid-import.

<a name="bulk-create"></a>
## 4. Canva Bulk Create

Assembling sprite + incoming + outgoing + voiceover per page by hand doesn't
scale past a handful of scenes. Bulk create mechanically turns every reviewed
scene into a draft video page in one pass, so the only work left for a human is
the part that actually needs judgement: animation and voice.

<a name="manual-finishing"></a>
## 5. Canva Manual Finishing

Animation and voice generation stay manual on purpose (see MASTER_SPEC §11 Out
of Scope) — Canva doesn't expose reliable per-element animation or voice
generation via API, and this is a comic: aesthetics matter more than shipping a
generic-entrance-FX version that reads as cringe to the people watching it.

<a name="export-mp4"></a>
## 6. Export MP4

Exporting per-domain rather than one merged file means a re-render only touches
the domain that changed, and distribution/review naturally happens per training
topic anyway. Cross-domain stitching is explicitly out of scope for v1
(MASTER_SPEC §11) — it can be automated later without changing this pipeline.
