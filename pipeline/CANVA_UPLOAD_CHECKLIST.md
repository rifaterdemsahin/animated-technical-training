# Canva Upload Checklist

Manual, one-time-per-domain-style setup, plus the per-batch steps for turning
an exported CSV into a finished MP4 (see `MASTER_SPEC.md` sections 6-7).

## Reference example (manual baseline we're automating around)

These two Canva designs are the hand-built reference for what this pipeline
should produce faster and more consistently:

- Template / editing view: https://www.canva.com/design/DAHP1RV4ILg/nTilowGAWQrxcqefQoFSUQ/edit
- Exported video output: https://www.canva.com/design/DAHP1c7gOR8/BNhFha3kTMtMAdpgteVUPw/edit

Use these as the target bar for animation quality and pacing when building or
refining the master template below — the goal of the repo-driven pipeline is
to reach this same output quality without hand-placing every sprite per page.

## One-time per domain style

1. Build a master template design with placeholders whose names match the
   CSV columns exactly: `sprite_1..sprite_N`, `incoming`, `outgoing`
   (`page_id` is for traceability only — it doesn't need a visible
   placeholder unless you want it as a debug watermark).
2. Confirm the template's sprite placeholders sit at the canvas position/size
   that matches the 512x512 sprite canvas (see `NAMING_CONVENTIONS.md`) so
   Bulk Create doesn't stretch or crop them.

## Per export batch

1. Run `tools/export_csv.py` to produce `output/csv/<topic>[_partN].csv`.
2. In Canva: **Apps → Bulk create → Upload CSV**, select the matching master
   template, generate pages.
3. Upload the sprite PNGs referenced by the CSV's `sprite_N` columns to the
   Bulk Create media step so filenames resolve to images (Bulk Create does
   not accept image URLs — see `MASTER_SPEC.md` section 6).
4. Per page: apply **Animate**, preferring **Motion Path** / sequenced
   entrance-exit over generic effects, to sequence `sprite_1 → sprite_2 →
   sprite_3 → ...` in `sprite_sequence` order.
5. Add **Audio → Generate AI voice**, feeding the page's `incoming` text then
   `outgoing` text.
6. Run the "mute test" (`MASTER_SPEC.md` section 1) on each page before
   export: watch with sound off — if the concept isn't conveyed, fix the
   animation, don't add narration.
7. **Share → Download → MP4 Video** per domain file.
8. Record the output location in `/output/mp4_manifest.json`.

## Known Canva limits to respect

- Bulk Create: max 300 rows, 150 columns, one data field per element, images
  embedded (not URLs), desktop only.
- Presentation/video designs: max 500 pages per file — batch by domain well
  before this limit.
