# animated-technical-training
animated technical training focus on show not tell

Live: https://rifaterdemsahin.github.io/animated-technical-training/

## What this is

DeliveryPilot: a repo-driven pipeline that turns structured scene data
(script + storyboard + sprites) into animated technical training videos,
using Canva Bulk Create for slide generation and Canva's native Animate + AI
voiceover for production.

Full design, schema, and build phases: **[MASTER_SPEC.md](MASTER_SPEC.md)**.

Core principle: narration and visuals never carry the same information twice
— concept transfer lives in the animation (`visual_action`), voiceover
(`incoming`/`outgoing`) stays light and confirmatory. Every scene must pass
the **mute test**: if it doesn't convey the concept with the sound off, it
isn't done.

## Repo layout

```
scripts/<topic>.json        per-topic scene arrays (source of truth)
sprites/manifest.json       sprite_id -> file, character, pose, expression
sprites/<character>/*.png   sprite art (512x512, transparent)
tools/validate_scenes.py    schema + "mute test" checklist validator
tools/export_csv.py         scripts/*.json -> Canva Bulk Create CSV
tools/carousel/server/      carousel review app (Go backend + MongoDB, Section 5)
pipeline/                   naming conventions, Canva upload checklist
output/csv/                 generated Bulk Create CSVs (git-ignored per batch)
```

## Quickstart

Validate all scenes (used in CI on every PR touching `scripts/*.json`):

```
python3 tools/validate_scenes.py
```

Export `status: ready` scenes to a Canva Bulk Create CSV:

```
python3 tools/export_csv.py
```

Run the exporter's unit tests:

```
python3 -m unittest discover -s tools/tests
```

Run the carousel review app locally:

```
cd tools/carousel/server
MONGODB_URI="mongodb://..." go run . serve
```

The app serves scene cards for review/edit/clone/reorder against MongoDB —
see `MASTER_SPEC.md` section 5 and `tools/carousel/server/README.md` for the
Mongo/Fly.io setup.

## Canva reference

`pipeline/CANVA_UPLOAD_CHECKLIST.md` links the hand-built Canva template and
its exported video that this pipeline is automating around.
