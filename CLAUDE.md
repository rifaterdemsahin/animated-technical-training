# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A single static page (`index.html`) documenting and pitching the pipeline for turning
Canva-based comic/whiteboard content into animated technical training videos. It is
published via GitHub Pages (no build step, no framework, no package manager) at
https://rifaterdemsahin.github.io/animated-technical-training/

The rest of the repo (`pipeline/`, `scripts/`, `tools/`) is a **dormant/partial**
sub-project sketching an automated Canva Bulk Create export pipeline (scenes →
CSV → Canva). Most of its supporting code (`tools/export_csv.py`,
`tools/validate_scenes.py`, a Go/MongoDB carousel server, Fly.io deploy) was built
and then **deleted** in later commits — only the design docs and one sample
topic (`scripts/forward-proxy.json`) remain. `tools/tests/test_export_csv.py`
currently imports a module that no longer exists in the repo, and
`.github/workflows/validate-scenes.yml` only triggers on paths
(`scripts/*.json`, `sprites/manifest.json`, `tools/validate_scenes.py`) that
mostly don't exist either — don't assume either is currently exercised. Check
`git log -- tools/` before resurrecting any of this.

## Commands

There is no build/lint/test tooling for the live site — it's hand-edited HTML/CSS/JS
in one file. To preview it locally in Chrome (per user's global preference):

```bash
open -a "Google Chrome" index.html
```

The only runnable code in the repo is the dormant pipeline sub-project:

```bash
python3 -m unittest discover -s tools/tests   # will currently fail: export_csv.py is gone
```

Deployment is automatic: `.github/workflows/static.yml` deploys the entire repo
to GitHub Pages on every push to `main`.

## Architecture of `index.html` (the file that matters)

Everything — styles, markup, and JS — lives in this one file. Key structural pieces:

- **Header**: title + `.version` badge (`#versionBadge`, e.g. `v8.2.0 · Updated
  2026-07-27 17:03 UTC`) + a "time ago" span updated client-side every second.
- **Top nav**: sticky bar with anchor links to each `<section id="...">`, a
  "Stages" dropdown (hover-triggered, `openStagesDropdown()`/
  `scheduleCloseStagesDropdown()`) listing Preprod/Prod/Post stage groups, and
  a client-side search box that filters sections.
- **Sections** (`<section id="problem">`, `#solution`, `#problem-solution-fit`,
  `#core-principle`, `#hands-on`, `#pipeline`, `#build-phases`, `#references`,
  `#toolbox`): every section/stage heading follows the same pattern —
  `<h2>`/`<h3>` with a deep-link (`?section=<id>`), a `.confidence-bar` +
  `.confidence-marker`, and a collapse `<button>` wired to `toggleSection(id)`.
- **Pipeline stages** (`#pipeline` section, `.stage.s0`..`.s14`, `id="stage0"`..
  `id="stage14"`): 15 numbered stages (Research → Canva Slides → Review →
  Add Animation Frames → Export → Mindmap Architecture → Build GitHub Repo →
  Bulk Create → Asset Generation → Manual Finishing → Export MP4 →
  Distribution → Sanity Check → Architecture → Archielogy). Stage 14
  (Archielogy) is an ongoing, parallel "continuous exploration" stage — it
  must never block a scheduled release; that's its whole reason for being
  separate from the locked 0-13 pipeline. Each stage has the same
  confidence-bar/collapse/notes-textarea structure as top-level sections.
- **Left stage-jump rail** (`<nav class="stage-rail">`, right after `<body>`):
  fixed vertical strip of emoji links, one per pipeline stage 0-14, each with
  a `data-tip` attribute rendered as a CSS hover tooltip (see `.stage-rail
  a:hover::after`). Uses the same `?section=<id>` + on-load
  `scrollIntoView` pattern as the top nav — no separate JS wiring needed when
  adding a stage, just add the `<a>`. Hidden below `max-width: 1150px` so it
  never overlaps the centered `.wrap` content.
- **Collapse All**: `#collapseAllBtn` in `.cookie-tools` calls
  `toggleAllSections()`, which flips every section/stage between collapsed
  and expanded via `setAllCollapsed()`/`areAllCollapsed()` and persists
  through the same `sectionCollapseState` cookie as individual toggles.
- **Overall Feedback**: a page-wide `<textarea id="notes-overall-feedback">`
  near the bottom (above the copy button), included in `stageNames` like any
  other id so save/load/copy pick it up automatically. Same cookie-only rule
  applies — ships empty in source.
- **Copy Stage Data button** (`copyStageData()`): copies confidence + notes
  for every id in `stageNames`, framed explicitly as a task list for a
  Claude-like coding/LLM agent to act on (each note becomes a "Task for
  agent:" line, with a preamble explaining the intended use) — not just a
  plain data dump.
- **Confidence % next to each bar**: every `.confidence-bar` header is
  followed by a `<span class="confidence-pct" id="pct-<id>">`, kept in sync
  by `updateConfidenceBar(id)` (same function that positions the marker) —
  so the number is visible without expanding the section. New
  sections/stages get this automatically as long as they follow the standard
  `bar-<id>`/`marker-<id>` markup and are added to `stageNames`.
- **Maturity List** (`<div class="overall-feedback">` containing
  `#maturityTable`, near the bottom): a live, JS-generated table of every id
  in `stageNames` that has a confidence value, each row tagged with a tier by
  `maturityTier(val)` (🔴 ≤25 / 🟠 ≤50 / 🟡 ≤75 / 🟢 else) and a "what to do"
  recommendation, plus a `.maturity-note-input` text field and a leading "#"
  order-index column from `getOrderIndex(id)` (top-level sections: 1-based
  position in `sectionOrder`; stages: their own fixed number parsed from the
  id, e.g. `stage3` → `3`). Sortable by clicking the "#", "Section / Stage",
  or "Confidence" `<th class="sortable">` (`setMaturitySort(key)` flips
  `maturitySort {key, dir}` and re-renders; default is confidence ascending).
  The note input is NOT separate storage —
  `onMaturityNoteInput()` writes straight into that row's real
  `notes-<id>` element and calls `saveStageData()`, so it's just an
  alternate editor for the same cookie-backed note (two-way: editing the
  section's own textarea also re-renders the row via `renderMaturityList()`,
  wired into every notes textarea's `oninput`). Because of this, **every**
  id in `stageNames` needs a real `notes-<id>` element somewhere in the DOM
  — including `pipeline`, `build-phases`, and `references`, which now carry
  one too (previously they had confidence only). `renderMaturityList()`
  rebuilds `#maturityTableBody` on load, on every `adjustConfidence()` call,
  and on every notes textarea's `oninput` — it's fully derived, never
  hand-edited, and values are HTML-escaped via `escapeHtml()` before being
  injected through `innerHTML`.
- **Section reorder**: each top-level section's `<h2>` has a numbered
  `<span class="order-badge" id="order-<id>">` (e.g. Problem shows `1`,
  matching its position) right before the title link, plus "⬆"/"⬇"
  `.reorder-btn` buttons calling `moveSection(id, ±1)`, which swaps entries
  in the mutable `sectionOrder` array (seeded from `defaultSectionOrder` —
  keep both in sync if the section list ever changes) and physically moves
  the `<section>` DOM node via `applySectionOrder()` (inserts before the
  Maturity List's `.overall-feedback` div, the anchor for "first non-section
  sibling after Toolbox" — and also calls `updateOrderBadges()` +
  `renderMaturityList()` so the badges and the Maturity List's "#" column
  stay live). Persists to the `sectionOrderState` cookie via
  `saveSectionOrder()`/`loadSectionOrder()`. When `sectionOrder` differs from
  `defaultSectionOrder`, `copyStageData()` prepends a task line spelling out
  the custom order, so pasting the copy output to an agent carries the
  reorder request through to an actual `index.html` edit.
- **Per-section state**: every section/stage has a `<textarea id="notes-<id>">`
  and a confidence `%` with `−`/`+` buttons (`adjustConfidence(id, delta)`).
  Both notes and confidence are persisted client-side in a single cookie
  (`pipelineStageData`, `setCookie`/`getCookie`, 365-day expiry) via
  `saveStageData()`/`loadStageData()` — **not** a backend. The `notes-*`
  textareas always ship empty in source (placeholder text only); actual note
  content only ever exists in a given browser's cookie, loaded at runtime by
  `loadStageData()` — see editing conventions below. Collapse/expand
  state for every section is stored the same way in a separate cookie
  (`sectionCollapseState`).
- **Images**: referenced with absolute raw GitHub URLs
  (`https://raw.githubusercontent.com/rifaterdemsahin/animated-technical-training/main/...`),
  not relative paths, so they render correctly wherever the page is embedded/viewed.
- **Footer**: `#lastCommit` link is populated at page load by fetching
  `https://api.github.com/repos/rifaterdemsahin/animated-technical-training/commits/main`
  and rewriting the href/text to the actual latest commit SHA + message.

## Editing conventions (standing rules for this repo)

- **Bump the version badge on every `index.html` edit.** Update both the
  version number in `.version` (`#versionBadge`) and the `Updated YYYY-MM-DD
  HH:MM UTC` text next to it, in the same commit as the content change. Don't
  touch the badge for edits that don't touch `index.html` (README, MASTER_SPEC, etc).
  Bump patch (`v1.0.0`→`v1.0.1`) for copy fixes, minor (`v1.0.0`→`v1.1.0`) for
  additive content, major for structural/stage renumbering.
- **Keep `CONTENT.md` a 1:1 markdown mirror of `index.html`'s visible text**
  (headers, body copy, list items, why/task lines, link labels, image
  captions, footer) — update both in the same turn whenever either changes.
- **Never hardcode the footer's last-commit link/SHA.** It must stay the
  self-updating `fetch()` against the GitHub API described above; if that
  mechanism is ever removed, replace it with something equally self-updating
  (e.g. a link to `/commits/main`), never a static SHA.
- **Always `git push` after committing** in this repo — don't leave commits
  sitting local-only.
- New pipeline stages/sections should follow the exact existing markup
  pattern (confidence-bar + marker + collapse button + notes textarea +
  section-nav prev/next buttons) so the shared JS (`toggleSection`,
  `adjustConfidence`, `scrollSection`, save/load cookie functions) keeps working
  without per-section special-casing.
- **Never write note text into a `notes-<id>` textarea's HTML content.** Every
  `<textarea id="notes-*">` must ship as `<textarea ...></textarea>` — empty,
  placeholder only. Notes are per-user, per-browser scratch state that
  `loadStageData()` fills in from the `pipelineStageData` cookie at load time;
  they are never part of the committed page. This applies even when a user
  pastes their current notes/confidence snapshot (e.g. via "📋 Copy All Stage
  Data") and asks for it to be "applied to `index.html`" — confidence `%`
  defaults are fine to hardcode (they're the public roadmap estimate), but
  note text is not. If asked to record notes content, put it in this file, a
  memory, or a separate doc — not in a `notes-*` textarea.
