# PRE-TRIP COACH — COMPLETE BUILD SPECIFICATION

**Version 2.0 · 2026-09-08 · Fenix Truck School**

> **v2.0 supersedes v1.0.** All 20 open questions are now answered and folded in — most importantly the move to a **full 3D truck** (§3, §11) and **all content in three languages** (§10). See `docs/00_DECISIONS.md` for the decision log.

> **How to use this document.** This is the full brief. Give it to your AI builder
> together with the folders `content/`, `assets/`, and `prompts/`. It is written to
> be model-agnostic — it does not depend on any particular builder or model.
>
> Build in the order given in §12. Do not start at the UI.

---

## TABLE OF CONTENTS

1. [What we are building and why](#1-what-we-are-building-and-why)
2. [The user](#2-the-user)
3. [The core interaction — read this twice](#3-the-core-interaction--read-this-twice)
4. [Content — already authored, do not rewrite](#4-content--already-authored-do-not-rewrite)
5. [Modes](#5-modes)
6. [Scoring engine](#6-scoring-engine)
7. [The air brake module](#7-the-air-brake-module)
8. [Screen-by-screen specification](#8-screen-by-screen-specification)
9. [Game layer](#9-game-layer)
10. [Languages](#10-languages)
11. [Technical architecture](#11-technical-architecture)
12. [Build order and acceptance criteria](#12-build-order-and-acceptance-criteria)
13. [Non-negotiables](#13-non-negotiables)

---

## 1. WHAT WE ARE BUILDING AND WHY

### The situation

Fenix Truck School trains commercial drivers. Every student must pass a **CDL
pre-trip inspection** — a spoken, physical examination given by a state examiner
beside an actual truck. The student walks the vehicle, touches roughly 64 safety-
critical components, and says out loud what they are checking each one for.

The official scoring sheet states the rule plainly:

> "You MUST name, point to and/or touch and fully explain what you are inspecting
> each safety critical item for. If you do not do so, you will not get credit for
> the item(s)."

The air brake portion carries a further marking:

> `* Automatic failure if not performed correctly`

### The problem

Truck time is the school's scarcest and most expensive resource. A student gets
limited hours beside a real vehicle. But almost none of what makes a student pass
requires a truck — it requires **repetition of a spoken procedure with correction**.

Today that repetition happens by reading a paper booklet. Paper cannot listen. It
cannot tell a student they forgot to mention cracks. It cannot tell them they just
failed the air brake test.

### The product

A phone-first app where the student performs the inspection out loud and is scored
against the same concepts an examiner scores — with an AI instructor that teaches
before it tests, in English, Spanish or Portuguese, with or without a signal.

### What success looks like

1. A student rehearses the whole inspection with no truck present and knows their score.
2. Instructors can see who is ready before booking a state test slot.
3. Fewer failed first attempts.
4. The school hands the app to every new student on day one.

---

## 2. THE USER

Build for this specific person, not a generic user:

- An adult, 25–55, changing careers. A CDL is a direct and immediate income change.
- English, Spanish **or** Portuguese as a first language. Many are recent immigrants.
  English is often their second or third language.
- On a **mid-range phone, roughly 2022 or newer** (confirmed device floor). Often Android, often with a cracked screen.
- Standing in a yard in Florida sun, or in a cab at night, or on a bus.
- Signal is unreliable. Data is metered.
- Highly motivated. Will grind if the grind visibly moves them toward passing.
- Not a gamer. Will not tolerate cute. Will tolerate demanding.

**Design consequences, all mandatory:**

| Because | Therefore |
|---|---|
| Bright sun, cracked screen | Very high contrast, very large type, no thin fonts |
| Mid-range GPU | Hard 3D budget: 150k tris, 80 draw calls, 30fps locked (§11) |
| Gloves, big hands | 44pt minimum touch targets, no small controls |
| ESL speakers | Speech recognition **must** have a typed fallback that scores identically |
| Unreliable signal | Everything except AI grading works offline, bundled |
| Metered data | No video streaming, no unnecessary network calls |
| Not a gamer | No lives, no hearts, no energy timers, no dark patterns |
| Adults paying for a license | Respect. Specific feedback, not confetti |

---

## 3. THE CORE INTERACTION — READ THIS TWICE

The student inspects a **3D truck**, sitting in the driver's seat for the in-cab work
and walking the vehicle for the exterior. But the 3D is only half of it.

### The hybrid — this is the key architectural idea

| Layer | What it is | Its job |
|---|---|---|
| **3D scene** | Low-poly truck, fixed camera stations | *Where* is this part, what is it next to |
| **Photo detail** | The 59 real photographs of Fenix's own trucks | *What* does this part actually look like |

The student looks around a station, **taps a part on the truck**, and the app opens
the **real photograph** of that part. The callout is spoken and graded there.

**The 3D teaches spatial memory. The photograph teaches recognition.** A rendered
brake chamber is a guess; a photo of your brake chamber is the thing they'll see on
test day. Never replace the photo layer with a render.

### Station-based, not free-roam

Not an open-world sim. The student stands at a **fixed camera station**, looks around
freely (drag or gyro), taps parts, and moves between stations by tapping a waypoint.

Free-roam locomotion on a phone is awkward and nauseating, fixed stations let you
cull aggressively, and the real inspection *is* a fixed route. The student is never
lost. Stations map to the content's `location` field:

`driver_seat` · `front_of_truck` · `steer_axle` · `driver_side` ·
`behind_cab` (coupling) · `trailer_side` · `trailer_rear`

### The gesture

Analysis of real pre-trip footage produced one finding that shapes everything
(`docs/07_VIDEO_MECHANICS.md`):

> **The unit of this test is not a sentence. It is a hand on a part.**

A real inspection repeats the same grammar ~64 times: stand at the zone → put your
hand on the part → name it → say what you're checking it for, while still touching it.

So in the photo detail view the student **presses and holds the part while speaking**.
The mic opens on press and closes on release. That trains the physical habit the
examiner scores ("name, point to and/or touch"), and gives reliable push-to-talk,
which beats voice-activity detection in a windy yard.

```
┌──────────────────────────────────┐
│   [ 3D truck, steer axle station ]│
│                                   │
│      ◉ tap a part                 │
└──────────────────────────────────┘
              ↓ opens
┌──────────────────────────────────┐
│   [ real photo of the part ]      │
│        ◉ ← press and hold         │
├──────────────────────────────────┤
│  LUG NUTS                         │
│  ● ● ○ ○      ← concept pips      │
│   ┌────────────────────────┐      │
│   │  HOLD TO SPEAK         │      │
│   └────────────────────────┘      │
│         or type instead           │
└──────────────────────────────────┘
```

### Hotspots already exist

Every photo in `assets/reference/curated/` carries a `hotspot {x, y, r}` in
`manifest.json`. **23 were derived from the booklet's own orange pointer arrows** and
are reliable; **36 are default-centred placeholders** flagged `default_center` and
need refining by hand before release. Check `hotspot_source` before trusting one.

### Concept pips — implement this early

Show one empty pip per required concept, filling live as each is covered.
`LUG NUTS ● ● ○ ○` means: you've said two of the four things.

This converts a vague "have I said enough?" into a visible target. It's the highest-
value UI element in the app and costs almost nothing — the content knows the counts.

## 4. CONTENT — ALREADY AUTHORED, DO NOT REWRITE

All inspection content is extracted, structured and validated. **Load it. Never
retype it. Never edit it to make grading easier.**

| File | Contains |
|---|---|
| `content/pretrip.en.json` | 13 sections · 64 graded items · 263 scoreable concepts · 7 auto-fail items |
| `content/airbrakes.en.json` | Air brake test · 9 phases · 60 ordered spoken steps |
| `content/i18n/es.json` · `pt.json` | Complete Spanish + Portuguese labels and callouts (64/64 each) |
| `content/i18n/concepts.es.json` · `concepts.pt.json` | ES/PT accept-lists for all 136 item-specific concepts — offline grading in three languages |
| `content/i18n/en.json` | English UI strings |
| `content/schema.json` | JSON Schema for both content files |
| `assets/reference/curated/**` | 59 named photographs + `manifest.json` |
| `assets/reference/pages/` | All 36 booklet pages at 150 dpi |

### The item shape

```jsonc
{
  "id": "lug_nuts",
  "label": "Lug Nuts",
  "action": "name_point_explain",
  "image": "assets/reference/curated/07_steering_axle/rim_lugnuts.png",

  // the model answer — what a perfect student says
  "script": "My lug nuts are tight and secure, all present, no cracks, and no rust
             streaks — if I see rust they might be loose and they need to be tightened.",

  // ← THE SCOREABLE UNITS. This is what you grade against.
  "concepts": [
    { "id": "secure",      "label": "Tight and securely mounted",
      "accept": ["tight","secure","securely mounted","not loose"], "required": true },
    { "id": "all_present", "label": "All present",
      "accept": ["all present","none missing","all there"],        "required": true },
    { "id": "no_cracks",   "label": "No cracks",
      "accept": ["no cracks","not cracked"],                       "required": true },
    { "id": "rust",        "label": "No rust streaks (sign of looseness)",
      "accept": ["no rust","rust streaks","shiny threads"],        "required": true }
  ],

  "auto_fail": false,
  "coach_tip": "Explaining WHY rust matters is what earns the credit.",
  "common_errors": [ … ]
}
```

**Critical distinction:**
- `script` is the *model answer*. Never require it word-for-word.
- `concepts` are the *ideas* that must be present. A student who paraphrases
  correctly scores full marks.
- `accept` is a **hint list for the offline matcher**, not a whitelist. "It's not
  going anywhere" satisfies `secure`.

### Thresholds live in configuration

`content/pretrip.en.json → standards` holds every number, split by vehicle class:
psi ranges, tread depths, timer durations, pass threshold.

**Never hardcode a number in a component.** Read from `standards`.

The previously disputed static air-leak limit is **resolved**: 3 psi/min released,
4 psi/min applied, for both Florida and Massachusetts, per the Fenix air-brake
handout. It is recorded in `standards._leak_limit_resolved` with
`confirmed: true`, and `scripts/validate_content.py` asserts that
`pretrip.en.json` and `airbrakes.en.json` never drift apart on it.

`standards.jurisdictions` holds `us_fl` and `us_ma`. Each student is assigned one.
**Florida's checklist reference is still a placeholder** (`checklist_confirmed:
false`) pending the FL examiner sheet — thresholds are settled, only the checklist
wording is outstanding.

---

## 5. MODES

### Learn — the AI instructor teaches
One item at a time. Photo → instructor says the callout → explains *why it matters*
in one plain sentence → student repeats → instructor names exactly which concepts
were missed. No score, no timer. Where a student starts a new section.

Use `prompts/01_AI_INSTRUCTOR_SYSTEM_PROMPT.md` verbatim.

### Practice — the workhorse
One full section, no commentary between items. Hints available. Score at the end.
Auto-fails are flagged loudly but do **not** end the run. Timers may be skipped, and
the score card says so.

### Quick Drill — 90 seconds
Random items weighted toward the student's weak list. Built for a spare moment in a
queue. Ends on one number plus one line: *"You're weakest on steering axle."*

### Exam Simulator — the real thing
The complete run, timed, examiner silence, no hints. **Real 60-second timers, not
skippable.** Auto-fail ends the run immediately. Produces the score card that tells
a student whether to book their test.

### Audio Drill — needs a yard recording session first
Play a sound (governor cut-out, low-air buzzer, valves popping), student names it.
Students are graded on *hearing* these on test day, and paper fundamentally cannot
teach it. Blocked only on capturing clean audio — the shot list is in
`docs/07_VIDEO_MECHANICS.md` §6, and it can piggyback on the truck walkaround shoot.

### Find the Defect — v1.5, and the reason 3D is worth it
Spawn the truck with one to three randomised defects and let the student walk it and
call them out. Defects are **material and mesh variants** on parts — a swapped tyre
mesh, a rust decal, an apron translated a few centimetres to open a fifth-wheel gap.

This is real inspection training rather than recitation, and it replaces the defect
photo shoot that was declined. It is **v1.5, not v1** — but the model must be authored
for variant swapping from the start (parts as separate named nodes), because
retrofitting it means rebuilding the model. See `docs/08_3D_TRUCK.md` §4.

---

## 6. SCORING ENGINE

**Build this before any UI beyond a single item screen. If scoring is wrong, nothing
else matters.**

### Formula

```
item_score  = required concepts hit / required concepts total
item_passed = item_score >= 0.8  AND  no dangerous error
run_passed  = overall >= 80%     AND  zero auto-fail misses
```

The second condition of `run_passed` is **not configurable**.

### Two graders, one contract

| | Online (default) | Offline |
|---|---|---|
| Engine | AI grader, `prompts/02_GRADER_PROMPT.md` | Deterministic keyword matcher |
| Handles | Paraphrase, accent, code-switching, any language | Literal and near-literal matches |
| Vocabulary | Concept `label`, semantically | `concepts[].accept` + `defect_vocabulary` per language |

Offline runs are **flagged in history** and re-graded by AI on reconnect. Never
silently mix the two within one score.

The offline matcher will under-score paraphrase. That is acceptable. What is **not**
acceptable is failing a student in offline mode without telling them grading was
degraded. Show a banner.

**Assertion for the test suite:** the offline grader must never score *higher* than
the AI grader on the same transcript.

### Show the transcript before grading

Nothing destroys trust faster than being marked wrong for something you said
correctly and the microphone misheard. Display the live transcript, let the student
re-record before submitting.

### Dangerous errors

If a student states a **wrong threshold** or **wrong procedure** — "I can't lose more
than 10 psi", "no recaps needed on the steer axle" — that is a `dangerous_error`,
flagged and corrected even if every required concept was hit. Getting the words right
while holding a wrong fact is worse than saying nothing.

---

## 7. THE AIR BRAKE MODULE

This is the part that fails students. Treat it as its own sub-product.

### Preconditions are a mechanic, not a footnote

Reference footage shows each stage gated by a short state checklist *before* the
stage runs — engine on / valves in, then engine off / electric on, and so on.

**Students fail this test far more often by having the truck in the wrong state than
by forgetting a word.**

So: add a `preconditions[]` array to each phase in `airbrakes.en.json`, and **gate
the phase in the UI**. The student sets engine state, key state and valve state
correctly before the phase will start. Get it wrong and the phase refuses to begin,
with an explanation.

That is a small state-machine puzzle, and it drills exactly the thing that fails
people.

### Live gauge and spoken readings

Every step with a `reading` block requires a **spoken number, not a range.**
"I'm at full pressure" scores less than "I am at full pressure, 132 psi."

At each reading: the number appears large on screen and is validated against
`standards` immediately — green in range, red with the correct range if not.
Out of range is a **dangerous error**, not a miss.

### Timers are real

`kind: "timer"` steps must actually elapse. A student who claims a minute passed in
twelve seconds gets no credit — the examiner has a watch too. A complete run is about
15 minutes and roughly 2 of those are silent waiting. **A student who has never sat
through a real 60-second static leak test will rush it in front of the examiner.**

Exam Simulator: timers run in full.
Practice: skippable, marked on the score card as skipped.

### Order is graded here

`airbrakes.en.json` sets `"ordered": true`. A step performed out of sequence scores
zero even with perfect wording — performing the leak test before shutting the engine
off is simply not the test. The walk-around, by contrast, does **not** require a fixed
order within a section.

---

## 8. SCREEN-BY-SCREEN SPECIFICATION

### Screen language

Four layers, always legible in direct sunlight:

| Layer | Position | Purpose |
|---|---|---|
| Module chip | top-left, persistent | which test you are in |
| Stage chip | bottom-left, numbered, high-contrast | which stage of that test |
| Precondition list | centre, numbered, temporary | what must be true before starting |
| Item name + pips | lower-centre, on contact | what you are touching right now |

### Brand

Red `#E11B22` · near-black `#111318` · off-white `#F7F7F5` · accent orange `#F26B21`
(taken from the booklet's pointer arrows). Dark mode required — students practice in
cabs at night.

### Screens

**Home** — the review queue is the hero. "12 items due today." One primary button:
*Start*. Streak and level secondary. Not a menu of features.

**Section list** — 13 rows, each with medal state (bronze/silver/gold) and
items-due count. Auto-fail sections marked in red.

**Item screen** — as specified in §3. Full-bleed photo, hotspot, part name, concept
pips, hold-to-speak, typed fallback link. One primary action.

**Feedback** — what you said (transcript), which pips filled, which did not, and the
model callout with missed concepts highlighted. Never restate the whole callout as
prose.

**Air brake phase** — precondition checklist gate, then live gauge, stage chip,
spoken-reading capture, running timer when active.

**Score card** — per item: hit/missed concepts, your audio next to the model callout.
Auto-fail failures shown **separately and above** the percentage, never averaged into it.

**Auto-fail result** — full screen, red, unambiguous. The item that ended the run,
what was missed, and one button: *Relearn this item*. This is exactly what happens on
test day; do not soften it.

---

## 9. GAME LAYER

The game layer exists for exactly one reason: **spaced, corrected repetition is what
moves a callout into long-term memory, and people do not do it voluntarily unless it
feels good.**

### Spaced repetition — the core mechanic

Back it with a real table, not a shuffle.

Intervals: **1 day → 3 days → 7 days → 21 days → mastered.**
Any miss resets that item to 1 day. The review queue is what the app opens to.

If you build only one thing past basic scoring, build this.

### Progression

- **Item mastery** — *learned* on first clean run; *mastered* after 3 clean runs on 3
  separate days. Decays to *learned* after 30 days untouched.
- **Section medals** — bronze (completed), silver (80%+ clean), gold (3 clean runs,
  no hints, no misses).
- **XP** — 10/item clean, 25/section, 100/clean exam run. XP buys nothing. It is a
  visible record of work done, which is the point.
- **Streaks** — one free freeze per week. These students drive shifts; a streak broken
  by a 14-hour day is a reason to delete the app, not to try harder.

### Social

Opt-in leaderboard **scoped to the student's own school**. First name + last initial,
weekly XP only. No global board — a stranger's score is not motivating and invites
gaming.

### Feedback discipline

- Correction is immediate and specific. Never "not quite" — always "you didn't say
  anything about cracks."
- Praise is specific and rationed. "That was clean, all four" beats "Great job!"
  Constant praise after sloppy work teaches that sloppy is fine.
- Auto-fails are never softened into a percentage.

---

## 10. LANGUAGES

**Everything in English, Spanish and Portuguese.** Not just the interface — the
teaching text, the model callouts, and grading.

- All 64 items have complete ES and PT labels and callouts.
- All 136 item-specific concepts have ES and PT accept-lists, plus a 10-term shared
  defect vocabulary per language. **The offline keyword grader therefore works in all
  three languages**, not only the AI grader. `validate_content.py` enforces 100%
  coverage — it fails the build if a concept is missing a translation.
- A student may practice and be graded speaking any of the three.
- Language switches instantly, no restart, persisted.
- Speech-recognition locale follows the language being spoken.
- Content falls back to `en` on a missing key, and logs the gap.
- Numbers and units are never translated. "132 psi" stays "132 psi".

**Worth surfacing in the UI:** the state examiner speaks English. A student who
practices only in Portuguese should be nudged toward English runs as their test date
approaches — not forced, but prompted.

## 11. TECHNICAL ARCHITECTURE

**React Native + Expo, TypeScript, with react-three-fiber (Three.js) on expo-gl for
the 3D.** One codebase → iOS, Android, web.

Chosen for the distribution requirement: App Store, Google Play and Microsoft Store
from one repository. The Expo web build, shipped as an installable PWA, satisfies the
Microsoft Store without a fourth native target — and Three.js keeps that intact,
which Unity would not.

The 3D here is a *scene*, not an action-game workload. Three.js is sufficient.

### 3D budget — hard limits, enforced in CI

| Budget | Limit |
|---|---|
| Triangles on screen | ≤ 150k |
| Draw calls | ≤ 80 |
| Texture memory | ≤ 120 MB |
| Frame rate | 30 fps locked |
| Initial download | ≤ 60 MB · 3D assets ≤ 40 MB |
| Time to first interaction | ≤ 4 s on the floor device |

Required: glTF/GLB with Draco + KTX2/Basis (never `.blend` or raw PNG), three LODs per
assembly, per-station culling, baked lighting only, texture atlases by zone,
on-demand station streaming.

**Device tiering:** High (full geometry) · Mid, the floor (LOD1, 1K atlases) · Low or
GL failure → **automatic fallback to photo-only mode**. The fallback ships in v1 and
is not optional: every mode must remain fully usable with the 3D disabled, because
photos and grading are independent of the renderer.

**Part naming contract:** every inspectable part is a separate node named exactly
`part_<item_id>` (`part_lug_nuts`, `part_king_pin`), with a simplified collider — never
raycast against render geometry. The validator asserts all 64 items resolve to a real
node. Full detail in `docs/08_3D_TRUCK.md`; the supplied models are assessed in
`docs/09_MODEL_ASSESSMENT.md`.

| Concern | Choice | Why |
|---|---|---|
| Navigation | Expo Router | File-based, works on web |
| State | Zustand | Small, easy to persist |
| Local DB | expo-sqlite | Review queue and history need real queries |
| STT | on-device first | Free, private, works with no signal |
| TTS | expo-speech | Instant, offline |
| AI | server-side proxy | Cost control; **never ship a key in the client** |
| 3D | react-three-fiber + expo-gl | Single codebase, keeps the PWA route |
| Payments | none | Free, bundled with tuition |

### Voice pipeline

```
hold hotspot → on-device STT → live transcript on screen
             → student confirms or re-records
             → grader (AI online / keyword offline)
             → score + filled pips + feedback
             → review queue update
```

Three rules, all mandatory:

1. **On-device STT first.** Cloud STT per minute × 64 callouts × a class is a real
   bill, and it fails exactly when a student is practicing in a yard with no signal.
   Cloud STT is an opt-in upgrade for noisy environments.
2. **Always offer typing.** Accented English is recognised less accurately, and this
   app's users are overwhelmingly ESL speakers. A student who cannot get the mic to
   understand them will quit. Typed answers score identically, and the app says so.
3. **Show the transcript before grading.**

### Data model

```
items          id, section_id, payload
attempts       id, item_id, ts, transcript, score, hit[], missed[],
               grader ('ai'|'offline'), lang, audio_path?
review_queue   item_id, due_at, interval_days, ease, streak
runs           id, mode, started_at, finished_at, score, passed, auto_fail_item_id?
progress       item_id, state ('new'|'learned'|'mastered'), clean_runs, last_clean_at
```

Content is read-only, versioned by `content_version`. On content update, migrate
progress **by item `id`**, never by index.

### Offline

All content JSON and all 59 images ship **in the bundle**. Everything works in
airplane mode except AI grading and the AI instructor, which degrade to the offline
grader with a visible banner. Runs queue locally and sync on reconnect.

### Privacy

Audio is the sensitive asset.

- Transcribe on device by default. Audio never leaves the phone unless the student
  explicitly saves a run.
- Explicit, revocable consent before the first recording, in the student's own language.
- Auto-delete audio after each run unless saved.
- No account required to practice. Sign-in only to sync devices.

---

## 12. BUILD ORDER AND ACCEPTANCE CRITERIA

**Do not start with the 3D.** The 3D is a navigation shell around a product that must
already work without it. Ship steps 1–4 as a working vertical slice first.

| # | Step | Done when |
|---|---|---|
| 1 | Content loader + typed models | Boots, validates both content files against `schema.json`, fails loudly on malformed content |
| 2 | Photo item screen: hotspot, pips, hold-to-speak, typed fallback | A student can hold a part, speak, and see a live transcript |
| 3 | **Offline keyword grader + score card** | Concepts light correctly on 20 hand-checked transcripts, in all three languages |
| 4 | AI grader behind a server proxy | Golden tests pass; offline never scores higher than AI |
| 5 | Learn Mode with the AI instructor | Instructor never invents content outside the item |
| 6 | Test Mode + auto-fail handling | A missed auto-fail ends the run with a full-screen result |
| 7 | Air brake module: precondition gates, gauge, real timers | A 60-second timer cannot be skipped in Exam Simulator |
| 8 | Spaced repetition + XP + streaks | Missed items reappear tomorrow; verified across a date change |
| 9 | i18n wiring, three languages, voice locales | A full run can be completed and graded in each language |
| 10 | **3D: blocky placeholder truck** — correct dimensions, all stations, all named nodes | Tap → item → callout → grade works end to end in 3D |
| 11 | **3D: performance harness on the floor device** | Budget locked *before* real art exists |
| 12 | 3D: real model, decimated, LODs, baked lighting, streaming | 30 fps held on the floor device |
| 13 | Device tiering + photo-only fallback | App fully usable with 3D force-disabled |
| 14 | Store packaging | Icons, splash, real screenshots, privacy manifest |
| — | *v1.5* | Find-the-Defect mode, Audio Drill |

Steps 10 and 11 are deliberately before the real model arrives. **A blocky
placeholder that holds 30 fps and correctly wires all 64 parts is worth far more than
a beautiful model that stutters** — and it de-risks the 3D decision while changing
course is still cheap.

### Test suite requirements

- Content validation in CI — malformed content must never reach a build.
- Grader golden tests over real transcripts, **including messy, accented and
  code-switched ones**, in all three languages.
- Assert: the offline grader never scores higher than the AI grader.
- Assert: every `part_<item_id>` node in the model resolves to a content item, and
  every content item resolves to a node.

## 13. NON-NEGOTIABLES

1. **Never alter the inspection content to make grading easier.**
2. **Never let a student pass a run in which they missed an auto-fail item.**
3. **Never record or upload audio without explicit, revocable consent.**
4. **Never ship an AI provider key in the client.**
5. **Every number a student is graded on traces back to `standards`.**
6. **A typed answer always scores identically to a spoken one.**
7. **Do not copy any content from third-party reference video.** The reference footage
   in `docs/07_VIDEO_MECHANICS.md` was analysed for *mechanics only* — it belongs to
   another school. All spoken content comes from Fenix's own booklet and handout.
8. **Do not claim in store copy that the app is state-approved or DMV-endorsed**, or
   that it guarantees a pass. It is practice material from Fenix Truck School.

9. **No payments, no accounts to practice.** The app is free and bundled with tuition.
   No paywall, no subscription, no sign-in gate.
10. **Audio is deleted after each run** unless the student explicitly saves it. No
    upload, no instructor submission in v1.
11. **The photo-only fallback ships in v1.** The app must be fully usable with the 3D
    scene disabled.

### Still blocking release

| Blocker | Owner |
|---|---|
| Florida examiner checklist — `us_fl.checklist_confirmed` is `false` | Alexandre |
| 3D model **commercial licence** — required if this is ever sold | Alexandre |
| Replacement trailer model — the current one is a single un-inspectable mesh | Alexandre |
| Content sign-off — `review/content_signoff.html`, 64 items + 9 phases | Alexandre |

The air-leak threshold is **resolved** (3 released / 4 applied, both states).

---

## APPENDIX — DOCUMENT MAP

| Document | Read it for |
|---|---|
| `README.md` | Repo orientation, how to rebuild content |
| `BUILD_SPEC.md` | **This file — the full brief** |
| `docs/00_DECISIONS.md` | **All 20 decisions and what each changed** |
| `docs/01_PRODUCT_SPEC.md` | Problem, users, scope |
| `docs/02_GAME_DESIGN.md` | Modes, progression, feedback discipline |
| `docs/03_SCORING_RULES.md` | Exact scoring rules, auto-fail list, source corrections |
| `docs/04_TECH_ARCHITECTURE.md` | Stack, voice pipeline, data model, privacy |
| `docs/05_STORE_SUBMISSION.md` | Apple / Google / Microsoft submission |
| `docs/06_OPEN_QUESTIONS.md` | **Decisions needed from Alexandre** |
| `docs/07_VIDEO_MECHANICS.md` | Reference-footage analysis; the hand-on-part finding |
| `docs/08_3D_TRUCK.md` | 3D constraint set, budgets, defect rendering, part contract |
| `docs/09_MODEL_ASSESSMENT.md` | The two supplied models, measured |
| `review/content_signoff.html` | Printable 64-item sign-off sheet |
| `prompts/00_MASTER_BUILD_PROMPT.md` | Condensed paste-in version of this spec |
| `prompts/01_AI_INSTRUCTOR_SYSTEM_PROMPT.md` | The AI teacher |
| `prompts/02_GRADER_PROMPT.md` | The speech grader |
| `prompts/03_IMAGE_GENERATION_PROMPTS.md` | Art direction, and what not to generate |
