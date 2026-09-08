# PRE-TRIP COACH — UNREAL ENGINE 5 BUILD PROMPT

Self-contained. Paste into any AI. Attach the `content/` folder and
`assets/reference/curated/` alongside it.

---

You are a senior Unreal Engine 5 developer. Build a production, store-shippable 3D
training game for iOS, Android and Windows. Build it to ship — no placeholder screens,
no unimplemented systems presented as working.

## THE PRODUCT

**Pre-Trip Coach** — a 3D CDL pre-trip inspection trainer for a US truck-driving school.

The commercial driving test is a spoken, physical performance. A student walks a truck,
touches ~64 safety-critical parts, and says out loud what they are checking each one
for. The official scoring sheet states:

> "You MUST name, point to and/or touch and fully explain what you are inspecting each
> safety critical item for. If you do not do so, you will not get credit."

The air brake portion is marked **automatic failure if not performed correctly**.

The player sits in the driver's seat, performs the in-cab air brake test, then walks the
truck, taps parts, and **speaks the callout out loud**. The game grades what they said.

## PLAYERS

Adults 25–55, changing careers. English, Spanish and Portuguese are all first languages
among them; many speak English as a second or third language. Mid-range phones, 2022 or
newer. Unreliable signal, metered data. Motivated, not gamers. Design for that person:
huge touch targets, very high contrast, readable in direct sunlight, no twitch input.

## PLATFORM TARGETS

| Platform | Notes |
|---|---|
| iOS | App Store. Metal. iOS 15+ |
| Android | Google Play. Vulkan with GLES3.2 fallback. Android 11+ |
| Windows | Microsoft Store, packaged as MSIX |

UE5 has no web export. Accept that; do not attempt one.

---

## PART 1 — CONTENT (provided; never author or edit it)

Content ships as JSON in `content/`. **Import it, never rewrite it.** It is authored
from source material and validated. If you think it is wrong, say so — do not change it.

| File | Contains |
|---|---|
| `pretrip.en.json` | 13 sections, 64 graded items, 263 scoreable concepts, 7 auto-fail items |
| `airbrakes.en.json` | 9 gated phases, 60 ordered steps, 3 timers, 10 live readings |
| `i18n/{en,es,pt}.json` | UI strings + full ES/PT labels and callouts |
| `i18n/concepts.{es,pt}.json` | ES/PT accept-lists for all 136 item-specific concepts |
| `schema.json` | JSON Schema for both content files |

### The item shape

```jsonc
{
  "id": "lug_nuts",
  "label": "Lug Nuts",
  "image": "assets/reference/curated/07_steering_axle/rim_lugnuts.png",
  "script": "My lug nuts are tight and secure, all present, no cracks, and no rust streaks...",
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
  "coach_tip": "Explaining WHY rust matters is what earns the credit."
}
```

- `script` is the **model answer**. Never require it word-for-word.
- `concepts` are the **scoreable ideas**. Correct paraphrase scores full marks.
- `accept` is a **hint list**, not a whitelist. "It's not going anywhere" satisfies `secure`.
- Only `required: true` concepts count toward the score.

All numeric thresholds live in `pretrip.en.json → standards`, split by vehicle class and
jurisdiction (`us_fl`, `us_ma`). **Never hardcode a graded number in Blueprint or C++.**

### Implementation

Write a C++ JSON importer producing `UPrimaryDataAsset` classes — `UInspectionItem`,
`UInspectionSection`, `UAirBrakePhase`, `UStandards`. Validate against `schema.json` at
cook time; fail the cook on malformed content. Do **not** hand-convert JSON to DataTables
— content is regenerated upstream and must re-import cleanly.

---

## PART 2 — SCORING (build this first; everything depends on it)

```
item_score  = required concepts hit / required concepts total
item_passed = item_score >= 0.8 AND no dangerous error
run_passed  = overall >= 80% AND zero auto-fail misses
```

The second condition of `run_passed` is **not configurable**.

Two graders behind one C++ interface `IGrader`:

- **`UOfflineGrader`** — normalise the transcript (lowercase, strip punctuation and
  filler), then fuzzy-match concept `accept` phrases plus the per-language
  `defect_vocabulary` and `concepts.{es,pt}.json`. Use token-set matching with stemming,
  not substring equality. Must work offline, in all three languages.
- **`UAIGrader`** — HTTPS call to a server proxy you also write, sending the concept list
  and transcript, receiving hit/missed JSON. **Never embed an API key in the client.**

Online uses the AI grader; offline falls back with a visible banner and re-grades on
reconnect. Assert the offline grader never scores higher than the AI grader.

**Grade meaning, not words.** Ignore grammar, accent, filler and transcription noise.
A **dangerous error** — a wrong threshold or wrong procedure — is flagged and corrected
even when every concept was hit.

---

## PART 3 — SPEECH (the hardest part in Unreal; do not underestimate it)

Unreal has no built-in speech recognition. You must write a plugin exposing one
Blueprint-callable interface backed by three native implementations:

| Platform | API |
|---|---|
| iOS | `SFSpeechRecognizer` + `AVAudioEngine` (Objective-C++, `.mm`) |
| Android | `android.speech.SpeechRecognizer` via JNI |
| Windows | `Windows.Media.SpeechRecognition` (WinRT) |

Requirements:
- **On-device recognition only.** No cloud STT — it costs per minute, fails with no
  signal, and these students practice in yards.
- Locale follows the spoken language (`en-US`, `es-US`, `pt-BR`).
- **Push-to-talk**: recognition starts on press, ends on release. Do not use
  voice-activity detection — it fails in a windy yard.
- Surface a **live partial transcript** while speaking.
- Let the player re-record before submitting.

**A typed fallback is mandatory and must score identically.** Accented English is
recognised less accurately and this game's players are overwhelmingly ESL speakers. A
player who cannot make the mic understand them will quit. Ship an on-screen keyboard
path to every graded interaction.

Request microphone permission with a specific, truthful purpose string.

---

## PART 4 — THE 3D WORLD

### Station-based, not free-roam

The player occupies **fixed camera stations**, looks around freely (touch drag or gyro),
taps parts, and moves between stations by tapping a waypoint. Free locomotion on a phone
is awkward and nauseating, and the real inspection is a fixed route.

Stations: `driver_seat` · `front_of_truck` · `steer_axle` · `driver_side` ·
`behind_cab` (coupling) · `trailer_side` · `trailer_rear`

### The hybrid — do not skip this

| Layer | Job |
|---|---|
| 3D scene | *Where* is this part, what is it next to |
| **Real photograph** | *What* does this part actually look like |

Tapping a part opens a **UMG panel showing the real photograph** from
`assets/reference/curated/`, and the spoken callout is graded there.

A rendered brake chamber is a guess. A photo of the real one is what they will see on
test day. **Never replace the photo layer with a render.**

### Part naming contract

Every inspectable part is a separate `UStaticMeshComponent` named exactly
`part_<item_id>` — `part_lug_nuts`, `part_king_pin`, `part_air_chamber` — each with a
simple box or sphere collider for tracing. **Never line-trace against render geometry.**

Write an editor commandlet asserting every one of the 64 content item ids resolves to a
component, and every `part_` component resolves to an item. Fail the cook on mismatch.

### Missing geometry — use proxies

A typical truck model lacks the underside inspection parts (brake chambers, slack
adjusters, leaf springs, U-bolts, shocks, king pin, locking jaws, glad hands, landing
gear, battery box, DEF tank — roughly 25 of the 64).

**Generate proxy volumes**: a simple box or cylinder at the anatomically correct
location, correctly named, tappable. The photograph does the teaching. Write this as a
data-driven placement script so real meshes can be swapped in later without touching
game code.

### Mobile performance budget — hard limits, enforced in CI

| Budget | Limit |
|---|---|
| Triangles on screen | ≤ 300k |
| Draw calls | ≤ 150 |
| Frame rate | 30 fps locked |
| Package size | ≤ 250 MB |
| Time to first interaction | ≤ 8 s |

**Nanite and Lumen off on mobile.** Use baked lightmaps, 3 LODs per assembly, aggressive
per-station culling, texture streaming, ASTC on mobile. Run `stat unit`, `stat rhi` and
the GPU profiler on a real mid-range Android and report measured numbers — not estimates.

Provide a **quality tier** (High/Mid/Low) detected at first launch, and a **photo-only
mode** that bypasses the 3D scene entirely and remains fully playable.

---

## PART 5 — THE AIR BRAKE MODULE

This is the part that fails students. Treat it as its own sub-product.

- **Preconditions are a mechanic.** Each phase has `preconditions[]` describing required
  truck state (engine on/off, key position, valve positions). Model this as a state
  machine. Wrong state → the phase refuses to start and explains why. Students fail this
  test by having the truck in the wrong state far more often than by forgetting words.
- **Interactive cab**: ignition key, both valves, brake pedal, gear shift — each a
  tappable component with real state driving a **live animated air-pressure gauge**.
- **Spoken readings**: `reading` steps require a spoken number validated against
  `standards` live. Green in range, red with the correct range if not. Out of range is a
  **dangerous error**, not a miss.
- **Real timers**: `timer` steps run in full in Exam Simulator and are not skippable. A
  player who has never sat through a real 60-second leak test will rush it on test day.
- **Order is graded** (`"ordered": true`). A step out of sequence scores zero.
- Honour `variants` / `variant_must` for manual vs automatic transmission.

---

## PART 6 — MODES

- **Learn** — one item at a time, an AI instructor demonstrates, player repeats, gets
  specific correction. No score, no timer.
- **Practice** — a full section, hints available, score at the end, auto-fails flagged
  but not terminal.
- **Quick Drill** — 90 seconds, random items weighted to weak areas.
- **Exam Simulator** — the whole run, timed, examiner silence, no hints, **real timers**,
  auto-fail ends the run immediately with a full-screen result naming the item.
- **Find the Defect** *(v1.5)* — spawn 1–3 randomised defects as material and mesh
  variants (swapped tyre mesh, rust decal, apron translated to open a fifth-wheel gap);
  the player walks the truck and calls them out.

---

## PART 7 — UI, LANGUAGES, PROGRESSION

**UMG**, driven by UE's localisation system with all three languages. Switch instantly,
no restart. Numbers and units never translated — "132 psi" stays "132 psi".

Screens: Home (review queue is the hero) · Section list with medals · 3D station view ·
Part detail with photo, **concept pips**, push-to-talk and typed fallback · Feedback ·
Air brake phase with gauge and timer · Score card · Auto-fail result.

**Concept pips**: one empty pip per required concept, filling live as each is covered.
`LUG NUTS ● ● ○ ○` means two of four said. Highest-value UI element in the game.

**Spaced repetition** is the core loop: intervals **1 → 3 → 7 → 21 days → mastered**,
any miss resets to 1 day. Back it with a real SQLite table, not a shuffle. The review
queue is what the game opens to.

XP (buys nothing — a record of work), section medals bronze/silver/gold, streaks with
one free freeze per week. **No lives, no hearts, no energy timers, no paywalls.** These
are adults paying for a license, not mobile-game whales.

Persist progress in SQLite: `attempts`, `review_queue`, `runs`, `progress`. Migrate by
item `id`, never by index.

---

## PART 8 — BUILD ORDER

Stop and report at each checkpoint. Do not proceed past a failed checkpoint.

**Phase 1 — Content + grading.** JSON importer, data assets, cook-time validation,
`UOfflineGrader`, a bare test map with one part and a typed input box.

> **CHECKPOINT 1 — run these and paste actual output:**
> 1. `lug_nuts` + `they're tight and all there` → exactly **2** pips (`secure`, `all_present`)
> 2. `lug_nuts` + `they are not loose, none are missing, no cracks, and no rust streaks` → **4** pips *(pure paraphrase; nothing matches `accept` literally)*
> 3. `front_tire` + `the tire looks fine` → **0** pips
> 4. Spanish: `están apretadas y todas presentes` → **2** pips
> 5. Portuguese: `estão apertadas e todas presentes` → **2** pips
>
> If (2) fails, the grader is too literal and will fail students who answered correctly.
> If (3) scores anything, it is rubber-stamping and the game is worthless.

**Phase 2 — Speech plugin.** iOS, Android and Windows implementations, push-to-talk,
partial transcripts, typed fallback. *Checkpoint: same five tests, spoken, on a real
device of each platform.*

**Phase 3 — 3D world.** Blocky placeholder truck at correct real-world dimensions, all
7 stations, all 64 named parts with colliders, tap → photo → callout → grade.
*Checkpoint: measured tris, draw calls and fps on a real mid-range Android.*

**Phase 4 — Air brakes.** Precondition state machine, interactive cab, live gauge, real
timers. *Checkpoint: show an auto-fail ending a run, and a 60s timer that cannot be
skipped.*

**Phase 5 — Modes, progression, languages.** *Checkpoint: a full graded run in each of
the three languages.*

**Phase 6 — Real art, LODs, baked lighting, quality tiers, photo-only mode.**

**Phase 7 — Packaging.** iOS, Android, Windows MSIX. Icons, splash, store screenshots
from the real game, privacy manifests, specific microphone purpose strings.

---

## NON-NEGOTIABLES

1. Never alter inspection content to make grading easier.
2. Never let a player pass a run with an auto-fail miss.
3. Every graded number traces to `standards`.
4. A typed answer always scores identically to a spoken one.
5. Never ship an API key in the client.
6. Audio is transcribed on device and deleted after each run. No upload without explicit,
   revocable consent.
7. Photo-only mode ships in v1 and must be fully playable.
8. Do not claim the game is state-approved, DMV-endorsed, or that it guarantees a pass.
9. If you stub or fake anything, say so plainly. Never present a stub as working.

## FINAL REPORT

1. How to build and run on each platform
2. Every checkpoint result, with real measured numbers
3. Everything stubbed or incomplete — be blunt
4. What you would fix first with more time
5. Anything here you disagree with, and why

Start with Phase 1. Stop at Checkpoint 1 and wait.
