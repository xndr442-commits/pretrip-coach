# IMAGE GENERATION PROMPTS

## Read this first

**You already own 59 real photographs** of the exact trucks your students train on
(`assets/reference/curated/`). Those are better than anything a model will generate,
for one reason: a student who studies a generated photo of a *plausible* air chamber
and then stands in front of a *real* one has to re-learn it. Use the real photos as
the primary reference on every item screen.

Generate images only for the three jobs below, where no photo exists.

---

## 1. UI illustration and empty states

Style spec, apply to all:

> Flat vector illustration, bold geometric shapes, thick uniform outlines. Palette
> strictly limited to: red `#E11B22`, near-black `#111318`, off-white `#F7F7F5`,
> accent orange `#F26B21`. No gradients, no photorealism, no text in the image.
> Transparent background. Centred composition with generous margin.

- `empty_review_queue` — a clipboard with a checkmark, resting against a tyre
- `streak_flame` — a stylised phoenix flame (the Fenix mark), 7-day streak badge
- `level_up` — a gear-shift knob with an upward chevron
- `offline_badge` — a truck silhouette inside a downloaded-cloud outline
- `exam_passed` — a CDL card silhouette with a laurel
- `exam_failed` — a red octagon with a wrench (retry, not shame — no sad faces)

## 2. Diagram overlays for parts a photo can't show clearly

The booklet already uses a line diagram for the steering linkage (page 18) — match
that language:

> Technical line diagram, single-weight red `#E11B22` strokes on transparent
> background, no shading, no perspective. Numbered call-out leaders in filled red
> circles with white numerals. Engineering-drawing clarity.

- `steering_linkage` — pitman arm (1), drag link (2), upper control arm (3),
  lower control arm (4), tie rod (5). *This exists on page 18 — extract that page
  instead of generating if you can.*
- `air_brake_schematic` — compressor → governor → wet tank → primary/secondary tanks
  → chambers, with the cut-in/cut-out points labelled
- `light_walk_path` — overhead view of tractor-trailer with the 8-zone lights
  sequence numbered as a walking route
- `triangle_placement` — road plan view, triangles at 10 ft, 100 ft behind, 100 ft ahead

## 3. Store assets

- **App icon**: the Fenix phoenix mark in red on near-black, no text, no truck.
  Must read at 29pt. `assets/reference/curated/00_brand/` has the mark to trace.
- **Screenshots**: real screens from the built app, not mockups. Both stores reject
  or down-rank fabricated screenshots.
- **Feature graphic** (Play, 1024×500): a real photo from `00_brand/` with the app
  name; do not generate a fake truck.

---

## What NOT to generate, ever

- Fake photographs of truck parts presented as real reference material. A student
  memorising a hallucinated air chamber is a safety problem, not a design problem.
- Any image showing a defect ("cracked frame", "worn brake lining") unless it is
  clearly labelled as an illustration. If you want real defect photos, shoot them at
  the yard — that is a half-day with a phone and it is worth far more than any
  generated set.
- Anything containing a real DOT number, plate, VIN, or a student's face without a
  signed release.

## Suggested shoot list (half a day at the yard, phone camera is fine)

The single highest-value addition to this app. Shoot each **twice: good and defective.**
Defect photos are what turn a memorisation app into a real inspection trainer.

Tyre with visible cut · tyre worn below 4/32 with a gauge in frame · lug nut with
rust streak · cracked frame rail · leaking shock · frayed air line · glad hand with
a worn seal · fifth wheel with a visible gap at the apron · loose battery connector ·
cracked lens · DOT tape peeling · landing gear crank not stowed.
