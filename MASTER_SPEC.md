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

---

## 3. Repo Structure

```
index.html > show the pipeline and how it works
Canva Course Folder > Linked in here 
   /sprites
   /script
   /storyboards/
  /presentation
README.md                 → project overview, this spec linked
MASTER_SPEC.md             → this file
```
>>>>>> left over here move on from here!
---

## 4. Prompt Schema

### 4.1 Scene generation



### 4.2 Sprite generation 

---

## 5. Naming of Files 

---

## 6. Presentation Export Spec 

---

## 7. Canva-Video Import Setup (

Import the presentation
4. Add Audio → Generate AI voice, feeding `incoming` + `outgoing` text per page.
5. Share → Download → MP4 Video, per domain file.
6. Record output location in `/output/mp4_manifest.json`.

---

## 8. Validation / Quality Gates

- watch and outline the todos

---

## 9. Build Phases (for an AI coding agent to execute in order)

1. Outline
2. Script
3. Production for the visuals for animation
4. Import
5. VoiceOvers
6. Polish

---

## 10. Known Constraints (from Canva, current as of this doc)

- 

---

## 11. Out of Scope (v1)

- Automated animation generation (still manual per page in Canva).
- Automated voiceover triggering via API (manual Generate AI voice per page).
- Automatic MP4 stitching across domain files (manual or a later script).




## 12. References

- Manual Animation : https://www.canva.com/design/DAHP1RV4ILg/nTilowGAWQrxcqefQoFSUQ/edit

- Manual Animation Output : https://www.canva.com/design/DAHP1c7gOR8/BNhFha3kTMtMAdpgteVUPw/edit?ui=e30#

- Solve Bulk Generation : https://animated-technical-training.fly.dev/

- Canva AI Costs
https://www.canva.com/settings/billing-and-teams
- Canva Tool Design
https://www.canva.com/design/DAHP2V5vSG8/4qcv0DB6I-WgbCEVLrhJkw/edit

Manual build also makes sense due to the fact that this is a comic and aesthethics rocks over thecringe output that would be shown to many people.
