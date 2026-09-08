Build me a complete 3D CDL pre-trip inspection training game — including generating the 3D truck and trailer yourself.

I've attached PRETRIP_CONTENT_BUNDLE.json. It contains everything: 13 sections, 64 graded inspection items, 263 scoreable concepts, 7 auto-fail items, a 9-phase air brake test, full English/Spanish/Portuguese translations, and a manifest of 59 reference photographs.

**Two expensive things are already done for you. Do not redo them:**

- **`truck_layout`** — all 53 inspectable parts already positioned on a real Class 8 tractor-trailer (7.2 m tractor, 4.5 m wheelbase, 53 ft trailer, 20.8 m combined), each with its primitive type, dimensions, colour and camera station, plus 7 station camera positions. Write the Blender script as a **loop over this data**. Do not hand-place geometry or invent dimensions.
- **`grader_tests`** — 21 golden fixtures defining correct grading in all three languages, including negation cases. Your Phase 1 job is to **make these pass**, not to invent a matching algorithm. A working reference implementation exists and passes all 21; if you want the approach: normalise (strip accents, punctuation, filler) → expand accept phrases from the item's list plus the shared defect vocabulary plus the per-language list → match contiguous token runs or all content tokens within a short window → check polarity so "there are cracks" never satisfies "no cracks".

**Read that file first. Never rewrite, invent, or "improve" any inspection content in it.** It comes from a truck-driving school's own material and the official state vehicle-inspection checklist. Inventing CDL content is a safety problem, not a design choice. If you think something in it is wrong, tell me — don't change it.

## WHAT THIS IS

The CDL driving test is a spoken, physical exam. A student walks a truck, touches ~64 safety-critical parts, and says out loud what they're checking each one for. The official scoring sheet says: "You MUST name, point to and/or touch and fully explain what you are inspecting each safety critical item for. If you do not do so, you will not get credit." The air brake portion is marked **automatic failure if not performed correctly**.

The game: the player sits in the driver's seat, does the in-cab air brake test, then walks the truck, taps parts, and **speaks the callout out loud**. The game grades what they actually said.

## PLAYERS

Adults 25–55 changing careers. English, Spanish and Portuguese are all first languages among them; many speak English as a second or third language. Mid-range phones from 2022 or newer. Bad signal, metered data, bright sunlight. Motivated, not gamers. So: huge touch targets, very high contrast, large type, no twitch input.

## PART A — GENERATE THE TRUCK

You can't sculpt meshes, so **generate the vehicle procedurally**: write a Blender Python script (`bpy`) that builds the tractor and trailer from primitives at correct real-world dimensions, with every inspectable part as a separate named object, exported to glTF.

Stylized low-poly is correct. Don't attempt photorealism — the game shows a **real photograph** of each part when tapped, and the photo does the teaching. The 3D exists to teach *where things are*.

**Tractor (sleeper cab), metres:** overall length 7.2 · width 2.60 · height 4.00 · wheelbase 4.50 · bumper→steer axle 1.35 · frame rail top 1.10 · steer tire 1.07 dia × 0.295 · drive tires 1.05 dia, dual at 0.33 spacing · fifth wheel plate 1.25 high, 1.00 dia, 0.30 forward of drive-axle centre · hood 2.10 · cab floor 1.45

**Trailer (53 ft dry van), metres:** length 16.15 · width 2.60 · box height 2.90 · floor height 1.25 · kingpin 0.90 from nose · landing gear 2.40 from nose · tandems 1.50 and 2.80 from rear · tires 1.05 dia

Combination ≈ 21.5 m. Origin at the tractor's front bumper centre at ground level, +X rearward, +Z up.

**Naming contract — non-negotiable.** Every inspectable part is a separate object named exactly `part_<item_id>`, using the ids from the bundle. Each gets a simple box or cylinder collider child named `col_<item_id>`. Write a validator confirming every id exists exactly once.

**11 of the 64 items are procedures, not parts — do NOT model these:** `safe_start`, `air_compressor_governor`, `air_leak_test`, `low_air_warning`, `spring_brakes_popout`, `rate_of_buildup`, `parking_brake_check`, `trailer_brake_check`, `service_brake_check`, `rr_procedure`, `emergency_procedure`. They're driven by UI and by shared cab controls. Build those controls instead: `ctrl_air_gauge_primary`, `ctrl_air_gauge_secondary`, `ctrl_ignition_key`, `ctrl_brake_pedal`, `ctrl_yellow_valve`, `ctrl_red_valve`, `ctrl_low_air_light`.

**Rules:** primitives only (cubes, cylinders, spheres, simple extrusions, bevels) · under 80,000 triangles total · flat/vertex colours or one small atlas, no PBR painting · export glTF 2.0, metres, names preserved · emit `truck_manifest.json` with each part's id, world position, bounding box and camera station.

**Colours carry meaning — get these right:** yellow parking-brake knob, red trailer-air-supply knob, blue service line, red emergency line, green electrical cable, amber front markers, red rear markers, red/white DOT tape.

## PART B — THE GAME

**Core loop:** the player stands at a fixed camera station, looks around (drag or gyro), **taps a part** → the **real photograph** opens → they **press and hold while speaking** the callout → it's graded against the concepts → **concept pips fill** (`LUG NUTS ● ● ○ ○` = two of four things said).

Stations: `driver_seat` · `front_of_truck` · `steer_axle` · `driver_side` · `behind_cab` · `trailer_side` · `trailer_rear`. Tap a waypoint to move between them. **No free roam** — it's nauseating on a phone and the real inspection is a fixed route.

**Occlusion — this is already a known problem, handle it from the start.** A real truck hides its own parts: the battery box covers the fifth wheel, the steer tyre covers the brake chamber, the trailer covers the whole coupling area. I generated the model and confirmed it. No camera placement fixes this for all 53 parts. So: **when a part is selected, fade every mesh between the camera and it to ~15% and disable its collider**, restoring on deselect. Give each station a short orbit arc rather than one fixed eye point, so the player can look around an obstruction the way they'd crouch beside a real truck. See `truck_layout.occlusion_rule`.

**Scoring:**
```
item_score  = required concepts hit / required concepts total
run_passed  = overall >= 80% AND zero auto-fail misses   ← second condition NOT configurable
```

In each item, `script` is the model answer — **never require it word-for-word**. `concepts` are the scoreable ideas; correct paraphrase gets full marks. `accept` is a hint list, **not a whitelist** — "it's not going anywhere" satisfies `secure`. Only `required: true` concepts count.

**All graded numbers come from `standards` in the bundle. Never hardcode a threshold.**

Build two graders behind one interface: an **offline** keyword matcher (token-set matching with stemming, working in all three languages using the `concepts_es`/`concepts_pt` accept-lists) and an **online AI grader** behind a server proxy. Never ship an API key in the client. Offline must never score higher than online.

**Speech:** on-device recognition, **push-to-talk** (starts on press, ends on release — not voice-activity detection, which fails outdoors). Live partial transcript, re-record before submitting, locale follows the spoken language. **A typed fallback is mandatory and must score identically** — these players are overwhelmingly ESL speakers, accented English is recognised less accurately, and one who can't make the mic understand them will quit.

**Air brakes — the part that fails students.** Gate each phase on its `preconditions[]` (engine state, key position, valve positions) as a state machine. Wrong state → the phase refuses to start and explains why. Students fail this far more often by having the truck in the wrong state than by forgetting words. Interactive cab controls drive a **live animated air gauge**. `reading` steps need a spoken number validated live against `standards` — out of range is a *dangerous error*, not just a miss. `timer` steps run for real and are **not skippable** in Exam Simulator. Order is graded.

**Modes:** Learn (AI instructor demonstrates, player repeats, gets specific correction) · Practice · Quick Drill (90 seconds, weighted to weak items) · Exam Simulator (timed, no hints, real timers, auto-fail ends the run immediately with a full-screen result naming the item) · Find the Defect (v1.5 — swap mesh and material variants: cut tyre, rust decal, apron shifted to open a fifth-wheel gap).

**Progression:** spaced repetition is the core loop — **1 → 3 → 7 → 21 days → mastered**, any miss resets to 1 day, backed by a real database table, not a shuffle. XP that buys nothing. Section medals. Streaks with one free freeze per week. **No lives, no hearts, no energy timers, no paywalls** — these are adults paying for a license.

**Feedback discipline:** correction is immediate and specific. Never "not quite" — always "you didn't say anything about cracks." Praise is rationed and specific: "that was clean, all four" beats "Great job!"

**Platforms:** iOS, Android, desktop. Budget ≤300k triangles on screen, 30fps locked, ≤250MB package, ≤8s to first interaction. Ship a **photo-only mode** that bypasses the 3D entirely and stays fully playable.

Pick whatever engine you think is best and tell me why.

## BUILD ORDER — stop and report at each checkpoint

**Phase 1 — Content + grading.** Import the bundle, validate it, build the offline grader, and make a bare test screen with a typed input box.

> **CHECKPOINT 1 — run ALL 21 fixtures in `grader_tests` and paste the ACTUAL output, not a description. These five are the gate:**
> 1. `lug_nuts` + "they're tight and all there" → exactly **2** pips
> 2. `lug_nuts` + "they are not loose, none are missing, no cracks, and no rust streaks" → **4** pips *(pure paraphrase — none of it matches `accept` literally)*
> 3. `front_tire` + "the tire looks fine" → **0** pips
> 4. `lug_nuts` + "están apretadas y todas presentes" → **2** pips
> 5. `lug_nuts` + "estão apertadas e todas presentes" → **2** pips
>
> If (2) fails, your grader is too literal and will fail students who answered correctly. If (3) scores anything, it's rubber-stamping and the game is worthless. **Fix before continuing.**

**Phase 2 — Generate the vehicle.** The Blender script, both glTF exports, the manifest, the name validator. *Report: screenshots from all 7 stations and the triangle count.*

**Phase 3 — 3D world.** Stations, tap-to-select, photo panel, callout, grading in 3D. *Report: measured triangles, draw calls, fps.*

**Phase 4 — Speech.** On-device recognition, push-to-talk, typed fallback. *Report: the five tests again, spoken.*

**Phase 5 — Air brakes.** Precondition state machine, live gauge, real timers. *Report: an auto-fail ending a run; a 60-second timer that can't be skipped.*

**Phase 6 — Modes, progression, three languages.** *Report: a full graded run in each language.*

**Phase 7 — Polish and packaging.**

## NON-NEGOTIABLES

1. Never alter the inspection content to make grading easier.
2. Never let a player pass a run with an auto-fail miss.
3. Every graded number traces back to `standards`.
4. A typed answer always scores identically to a spoken one.
5. Never ship an API key in the client.
6. Audio is transcribed on device and deleted after each run.
7. Photo-only mode ships in v1.
8. Never claim the game is state-approved, DMV-endorsed, or that it guarantees a pass.
9. **If you stub or fake anything, say so plainly. Never present a stub as working.**

Start with Phase 1. Stop at Checkpoint 1 and wait for me.
