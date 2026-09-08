# Pre-Trip Coach

A voice-first, gamified CDL pre-trip inspection and air brake trainer, built from
Fenix Truck School's own 36-page inspection booklet.

The commercial driving test is a **spoken, physical performance**. The student walks
the truck, touches roughly 64 safety-critical parts, and says out loud what they are
checking each one for. The official scoring sheet is blunt about it:

> "You MUST name, point to and/or touch and fully explain what you are inspecting
> each safety critical item for. If you do not do so, you will not get credit."

This app rehearses that performance — on a phone, in English, Spanish or Portuguese,
with no truck present and no signal required.

---

## Start here

| If you want to… | Read |
|---|---|
| **Build the app** | **[BUILD_SPEC.md](BUILD_SPEC.md)** — the complete brief |
| Paste a prompt into a builder | [prompts/00_MASTER_BUILD_PROMPT.md](prompts/00_MASTER_BUILD_PROMPT.md) |
| Know what Alexandre still has to decide | [docs/06_OPEN_QUESTIONS.md](docs/06_OPEN_QUESTIONS.md) |
| Understand the core interaction | [docs/07_VIDEO_MECHANICS.md](docs/07_VIDEO_MECHANICS.md) |

## What's here

```
BUILD_SPEC.md         The full specification — start here to build

content/              The game's source of truth, extracted from the booklet
  pretrip.en.json       13 sections · 64 items · 263 concepts · 7 auto-fails
  airbrakes.en.json     9 phases · 60 ordered steps · 3 timers · 10 live readings
  i18n/en|es|pt.json    UI strings + full ES/PT labels and callouts (64/64 each)
  schema.json           JSON Schema for both content files

assets/reference/
  curated/              59 named photographs + manifest.json with touch hotspots
  pages/                All 36 booklet pages at 150 dpi
  extracted/            Raw + deduped extraction (working files)

prompts/
  00_MASTER_BUILD_PROMPT.md          Condensed paste-in brief
  01_AI_INSTRUCTOR_SYSTEM_PROMPT.md  The AI teacher (Learn Mode)
  02_GRADER_PROMPT.md                The speech grader (Test Mode)
  03_IMAGE_GENERATION_PROMPTS.md     Art direction + what NOT to generate

docs/                 Product spec, game design, scoring rules, architecture,
                      store submission, open questions, video analysis
scripts/              Reproducible extraction and content builders
source/               The original PDFs
```

## Verify the content

```bash
python3 scripts/validate_content.py
```

Checks structure, cross-references, image existence, translation coverage, duplicate
ids, and that every graded number resolves against `standards`. **Run this in CI** —
malformed content must never reach a build.

## Rebuild the content

Content is generated, not hand-edited. Edit the builder scripts, never the JSON.

```bash
python3 scripts/extract_assets.py     # PDF → page renders + deduped photos
python3 scripts/curate_assets.py      # → named library + manifest
python3 scripts/detect_hotspots.py    # → touch hotspots from the booklet's arrows
python3 scripts/build_content.py      # → content/pretrip.en.json
python3 scripts/build_airbrakes.py    # → content/airbrakes.en.json
python3 scripts/build_i18n.py         # → content/i18n/*.json
python3 scripts/validate_content.py   # verify
```

Requires `poppler` (`brew install poppler`) and Pillow.

## Current state

| | |
|---|---|
| Sections | 13 |
| Graded items | 64 |
| Scoreable concepts | 263 |
| Auto-fail items | 7 (the entire in-cab brake check) |
| Air brake steps | 60 across 9 gated phases |
| Reference photos | 59, all named and captioned |
| Touch hotspots | 23 derived from the booklet's own pointer arrows; 36 default-centred and **needing manual refinement** |
| Translations | Spanish 64/64 · Portuguese 64/64 |
| Validation | 0 errors, 0 warnings |

## Sources

| Document | Used for |
|---|---|
| `NEW MATERIAL PRE TRIP.pdf` (36 pp) | Every walk-around item, all 59 photos |
| `AIR BRAKES TEST` handout | The full spoken air brake procedure |
| Class A Vehicle Inspection checklist §11M (2022-09-09) | Official scoring categories, auto-fail marking |
| Third-party reference video | **Mechanics only** — see the restriction in [docs/07_VIDEO_MECHANICS.md](docs/07_VIDEO_MECHANICS.md). None of its content is used in the app. |

## Before students use this

Two things must happen first, both in [docs/06_OPEN_QUESTIONS.md](docs/06_OPEN_QUESTIONS.md):

1. **Resolve the air-leak threshold conflict.** The booklet and the air-brake handout
   disagree on the static leak limit. Teaching a wrong threshold is the one failure
   mode of this app that is worse than not having it.
2. **Get an instructor to sign off on all 64 callouts.** The whole value here is that
   the wording is what your school actually teaches.
