# Naming Conventions

## Topics

- One file per topic: `scripts/<topic>.json`, topic name in kebab-case
  (`forward-proxy`, `reverse-proxy`).
- `topic` field inside the file must match the filename stem.

## Scene `page_id`

- Format: `<topic-abbreviation>-<NNN>`, zero-padded to 3 digits
  (`fp-001`, `fp-002`, ...). The abbreviation is short and unique per topic so
  IDs stay legible in the Canva Bulk Create CSV and in `exam_ref` cross-links.
- IDs are stable once a scene is exported — clone a scene rather than
  renumbering existing ones, so history/exam references don't drift.

## Sprites

- File: `sprites/<character>/<character>_<pose>_<expression>.png`
  (`sprites/client/client_idle_neutral.png`).
- `character`, `pose`, `expression` are lowercase, single words (use `_` if a
  concept genuinely needs two, e.g. `client_action_neutral`).
- Canvas: fixed **512x512**, transparent background, subject vertically
  centered with roughly 40px margin — this keeps every sprite drop-in
  compatible with the same Canva template placeholder regardless of pose.
- `sprites/manifest.json` is the single source of truth mapping a
  `sprite_id` (used in `sprite_sequence`) to its file path, character, pose,
  and expression. Never reference a sprite file path directly from
  `scripts/*.json` — always go through the manifest ID.

## CSV export columns

- Fixed sprite slot columns are `sprite_1`, `sprite_2`, ... `sprite_N`, where
  `N` is the longest `sprite_sequence` among the ready scenes being exported.
  These names must match the placeholder element names in the Canva master
  template exactly (see `CANVA_UPLOAD_CHECKLIST.md`).
- Text columns: `page_id`, `incoming`, `outgoing` — same casing as the JSON
  schema fields, since they map 1:1 to template placeholders.
