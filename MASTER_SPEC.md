# Master Spec: Script-to-Animated-Video Pipeline 

## 1. Purpose

Build a video pipeline  presentation that represents the video production workflow (script + storyboard +
sprites, frames ) into animated technical training videos, using Canva and AI to Create videos use this project as the bluprint for the production.

**Core design principle — Cognitive Offload / Show, Don't Tell**
Narration and visuals must not carry the same information twice. Redundant
audio+text forces the audience to process the same content through two channels,
increasing cognitive load (Sweller/Mayer redundancy effect). This pipeline instead
puts concept transfer into animated visuals (`visual_action`), and keeps voiceover
(`incoming`/`outgoing`) light and confirmatory rather than explanatory.

**Acceptance test for every scene ("mute test"):** if the animation, watched with
no audio, does not convey the concept, the scene is not done.

---

## 2. High-Level Architecture

```
[Canva: source of truth]
   script  master flow for the content
   images/*.png  (AI-generated assets)
   storyboard  ( gemini created inspitional images )
   notes   (per-frame the script and the animations)
        │
        ▼
[Carousel Review App] (Canva Presentations)
   - Frame view per scene: sprite preview + incoming/outgoing + visual_action in notes
   - inline edit, clone scene, reorder, mark "ready" check mark
   - Script gets updates if needed         │
        ▼
[Export Step]
   - flattens ready scenes into Canva to be imported by the video format
   - Embeds sprite images 
   - respects Canva limits: max 300 pages
   - batches by video if >300 scenes
        │
        ▼
[Canva: Bulk Create]
   - Export all as video (sprite, incoming, outgoing)
   - Voiceovers inside the videos 
        │
        ▼
[Canva: Manual finishing]
   - Animate per element/page (motion path preferred over generic entrance fx)
   - Generate AI voice per page, from incoming/outgoing text
        │
        ▼
[Canva: Export MP4]  →  per-domain video files
```
>>>>>> left over here move on from here!
---

## 3. Repo Structure

```
/scripts/                → per-topic JSON scene files
    forward-proxy.json
    reverse-proxy.json
    ...
/sprites/
    manifest.json         → sprite_id → file path, character, pose, expression
    <character>/*.png
/storyboards/             → optional: derived shot-list view (generated, not hand-authored)
/tools/
    carousel/              → the review/edit web app
    export_csv.py          → scripts/*.json + sprites/manifest.json → Canva Bulk Create CSV
    validate_scenes.py     → schema + "mute test" checklist validator
/pipeline/
    NAMING_CONVENTIONS.md
    CANVA_UPLOAD_CHECKLIST.md
/output/
    csv/                   → generated Bulk Create CSVs, batched by domain
    mp4_manifest.json      → tracks exported video links (MP4s not stored in repo)
README.md                 → project overview, this spec linked
MASTER_SPEC.md             → this file
```

---

## 4. Data Schema

### 4.1 Scene object (`scripts/<topic>.json`)

```json
{
  "topic": "forward-proxy",
  "scenes": [
    {
      "page_id": "fp-001",
      "status": "draft | ready | exported",
      "visual_action": "Client sends request; proxy intercepts and relabels sender before forwarding to server",
      "sprite_sequence": ["client_idle", "client_action", "proxy_relabel", "server_receive"],
      "incoming": "Every request from this office goes through one desk first.",
      "outgoing": "The server never sees who really asked.",
      "domain": "networking",
      "exam_ref": "CCA-F-net-03",
      "notes": ""
    }
  ]
}
```

Field rules:
- `visual_action` is mandatory and must describe a physical/causal change, not a
  restatement of the narration. If it can't be filled concretely, the scene fails
  review and stays `draft`.
- `sprite_sequence` references IDs in `sprites/manifest.json`, in playback order.
- `incoming`/`outgoing` are short — captions, not explanations.
- `status` gates export: only `ready` scenes are included in CSV export.

### 4.2 Sprite manifest (`sprites/manifest.json`)

```json
{
  "client_idle": { "file": "sprites/client/idle.png", "character": "client", "pose": "idle" },
  "client_action": { "file": "sprites/client/action.png", "character": "client", "pose": "action" }
}
```

Naming convention: `character_pose_expression.png`, transparent background, fixed
canvas size across all sprites (define once in `pipeline/NAMING_CONVENTIONS.md`).

---

## 5. Carousel Review App — Functional Spec

**Goal:** Let the user review/edit scenes quickly, screen at a time, with minimal
friction — the "ease of editing and cloning" requirement.

Minimum feature set:
- Load a topic's `scripts/<topic>.json`.
- Render one scene per card: sprite thumbnails in sequence, `incoming`/`outgoing`
  text fields (editable), `visual_action` field (editable), status toggle.
- **Clone**: duplicate current scene as a new `page_id`, insert after current.
- **Reorder**: drag or move up/down.
- **Mark ready**: sets `status: ready`; only ready scenes are eligible for export.
- **Save**: writes back to the JSON file (or opens a PR-ready diff if run against
  a git-backed environment).
- Validation warnings inline: missing `visual_action`, empty sprite_sequence,
  incoming/outgoing over a length threshold (redundancy risk).

Non-goals for v1: does not talk to the Canva API directly; does not render actual
animation — sprite sequence is shown as a static filmstrip preview only.

---

## 6. CSV Export Spec (`tools/export_csv.py`)

Input: one or more `scripts/<topic>.json` with `status: ready` scenes, plus
`sprites/manifest.json`.

Output: CSV(s) matching Canva Bulk Create constraints:
- Max 300 rows per file → batch by topic/domain; if a topic exceeds 300 scenes,
  split into part files (`forward-proxy_part1.csv`, `part2.csv`, ...).
- Max 150 columns.
- One data field per template element — so multi-sprite sequences must map to
  fixed named columns (e.g. `sprite_1`, `sprite_2`, `sprite_3`, `sprite_4`) matching
  placeholder slots in the Canva master template, not a single repeated field.
- Images embedded, not linked by URL (Canva Bulk Create does not support image URLs).
- Text columns: `incoming`, `outgoing`, `page_id` (for traceability).

Output written to `/output/csv/<topic>_<part>.csv`.

---

## 7. Canva-Side Setup (manual, one-time per domain style)

1. Build one master template design with placeholders matching the CSV column
   names exactly (sprite slots + incoming/outgoing text boxes).
2. Apps → Bulk create → upload CSV → generate pages.
3. Per page: apply Animate (prefer Motion Path / sequenced entrance-exit over
   generic effects) to sequence sprite_1 → sprite_2 → sprite_3 → sprite_4.
4. Add Audio → Generate AI voice, feeding `incoming` + `outgoing` text per page.
5. Share → Download → MP4 Video, per domain file.
6. Record output location in `/output/mp4_manifest.json`.

---

## 8. Validation / Quality Gates

`tools/validate_scenes.py` should check, before a scene can be marked `ready`:
- `visual_action` is non-empty and distinct in wording from `incoming`/`outgoing`
  (basic redundancy check).
- `sprite_sequence` has at least 2 entries (idle → action minimum) and all IDs
  exist in the manifest.
- `incoming`/`outgoing` are each under a configurable word cap (default 20 words)
  to keep voiceover light.

CI (GitHub Actions) should run this validator on every PR touching `scripts/*.json`.

---

## 9. Build Phases (for an AI coding agent to execute in order)

1. **Repo scaffold** — directory structure, schema files, sample topic with 3-5
   scenes, sample sprite manifest (placeholder PNGs OK).
2. **Validator** — `validate_scenes.py` + GitHub Action running it on PRs.
3. **CSV exporter** — `export_csv.py` implementing Section 6, with unit tests
   against the sample topic.
4. **Carousel app** — web app (React or plain HTML/JS) implementing Section 5
   against the sample topic; local file read/write, no backend required for v1.
5. **Docs** — `pipeline/NAMING_CONVENTIONS.md`, `pipeline/CANVA_UPLOAD_CHECKLIST.md`,
   top-level `README.md` summarizing the flow and linking this spec.
6. **Dry run** — export sample topic to CSV, manually verify against a real Canva
   Bulk Create template, document any schema adjustments back into this spec.

---

## 10. Known Constraints (from Canva, current as of this doc)

- Bulk Create: max 300 rows, 150 columns, one data field per element, images must
  be embedded (no URLs), desktop only.
- Presentation/video designs: max 500 pages per Canva file — batch by domain well
  before this limit for editing sanity.
- No confirmed public API trigger for Bulk Create — this step stays manual/UI-driven
  for now; revisit if Canva ships an API for it.

---

## 11. Out of Scope (v1)

- Automated animation generation (still manual per page in Canva).
- Automated voiceover triggering via API (manual Generate AI voice per page).
- Automatic MP4 stitching across domain files (manual or a later script).
