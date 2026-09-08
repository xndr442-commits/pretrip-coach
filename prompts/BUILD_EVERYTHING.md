# BUILD EVERYTHING — 3D truck + complete game

Paste as one message. Attach `content/` and `assets/reference/curated/`.

---

You are a senior technical artist and game developer. Build a complete 3D CDL pre-trip
inspection training game, **including generating the 3D truck and trailer yourself.**

You cannot sculpt meshes, so **generate the vehicle procedurally with a script** — a
Blender Python script (`bpy`) that builds the tractor and trailer from primitives at
correct real-world dimensions, with every inspectable part as a separate, correctly
named object, exported to glTF.

Stylized low-poly is the correct look. Do not attempt photorealism. The game shows a
**real photograph** of each part when tapped, and the photo does the teaching — the 3D
exists to teach *where things are*, not what they look like.

---

## PART A — GENERATE THE VEHICLE

Write `scripts/generate_truck.py`, a Blender script producing `truck.glb` and
`trailer.glb`.

### Real-world dimensions (US Class 8, metres)

**Tractor — sleeper cab**
| | |
|---|---|
| Overall length | 7.2 |
| Width | 2.60 |
| Height (roof fairing) | 4.00 |
| Wheelbase (steer → drive centre) | 4.50 |
| Bumper → steer axle | 1.35 |
| Frame rail top height | 1.10 |
| Steer tire diameter / width | 1.07 / 0.295 |
| Drive tire diameter / width | 1.05 / 0.295 (dual, 0.33 spacing) |
| Fifth wheel plate height / diameter | 1.25 / 1.00 |
| Fifth wheel position | 0.30 forward of drive-axle centre |
| Hood length | 2.10 |
| Cab floor height | 1.45 |

**Trailer — 53 ft dry van**
| | |
|---|---|
| Length | 16.15 |
| Width | 2.60 |
| Box height | 2.90 |
| Floor height | 1.25 |
| Kingpin from nose | 0.90 |
| Landing gear from nose | 2.40 |
| Tandem axles from rear | 1.50 and 2.80 |
| Trailer tire diameter | 1.05 |

Combination overall ≈ 21.5 m. Place the origin at the tractor's front bumper centre,
ground level, +X rearward, +Z up.

### Naming contract — non-negotiable

Every inspectable part is a **separate object** named exactly `part_<item_id>`.
A validation script must confirm every id below exists exactly once.

### Parts requiring geometry

**Exterior — front of truck**
`part_truck_leveled` (whole-vehicle proxy at front) · `part_front_lenses` ·
`part_headlights` · `part_coolant` · `part_oil` · `part_power_steering` ·
`part_fluid_air_leaks` · `part_steering_gear_box` · `part_pitman_arm` ·
`part_drag_link` · `part_control_arms` · `part_tie_rod`

**Steer axle** (build on the driver's side)
`part_front_tire` · `part_rims` · `part_lug_nuts` · `part_spring_mounts` ·
`part_leaf_springs` · `part_u_bolts` · `part_shock_absorber` · `part_brake_hose` ·
`part_air_chamber` · `part_brake_contaminants` (brake drum)

**Driver side**
`part_turn_signal_side` · `part_mirrors_side` · `part_fuel_tank` · `part_def_tank` ·
`part_battery` · `part_frame`

**Behind cab / coupling**
`part_electrical_line` · `part_air_lines` · `part_fifth_wheel_skid` · `part_king_pin` ·
`part_locking_jaws` · `part_locking_pins`

**Trailer**
`part_landing_gear` · `part_trailer_clearance_lights` · `part_dot_tape` ·
`part_rear_lenses` · `part_rear_clearance` · `part_rear_lights`

**Cab interior** (build a driver's-seat view: dash, wheel, seat, controls)
`part_seat_belt` · `part_valves_up` (yellow octagon + red octagon knobs) ·
`part_gearshift_neutral` · `part_windshield` · `part_mirrors` · `part_wipers` ·
`part_washer_fluid` · `part_heater_defroster` · `part_horns` ·
`part_light_indicators` (dash cluster) · `part_fire_extinguisher` · `part_triangles` ·
`part_spare_fuses`

Plus these **shared cab controls**, referenced by the air-brake tests:
`ctrl_air_gauge_primary` · `ctrl_air_gauge_secondary` · `ctrl_ignition_key` ·
`ctrl_brake_pedal` · `ctrl_yellow_valve` · `ctrl_red_valve` · `ctrl_low_air_light`

### Items that need NO geometry

These are **procedures and tests, not parts** — they are driven by UI and the cab
controls above. Do not create meshes for them:

`part_safe_start` · `part_air_compressor_governor` · `part_air_leak_test` ·
`part_low_air_warning` · `part_spring_brakes_popout` · `part_rate_of_buildup` ·
`part_parking_brake_check` · `part_trailer_brake_check` · `part_service_brake_check` ·
`part_rr_procedure` · `part_emergency_procedure`

### Build rules

- Primitives only: cubes, cylinders, spheres, simple extrusions and bevels.
- **Under 80,000 triangles total** for tractor + trailer.
- Flat/vertex colours or a single small atlas. No PBR texture painting.
- Every part gets a simple box or cylinder **collider** child named `col_<item_id>`.
- Correct colours where they carry meaning: yellow parking-brake knob, red trailer-air
  knob, blue service line, red emergency line, green electrical cable, amber front
  markers, red rear markers, red/white DOT tape.
- Export glTF 2.0, +Y up, metres, with object names preserved.
- Also emit `truck_manifest.json` listing every part id, its world position, bounding
  box, and which camera station it belongs to.

---

## PART B — THE GAME

Build the full game around it.

### Content — provided, never edit

`content/pretrip.en.json` (13 sections, 64 items, 263 concepts, 7 auto-fails),
`content/airbrakes.en.json` (9 gated phases, 60 ordered steps), `content/i18n/*`
(English, Spanish, Portuguese — labels, callouts, and concept accept-lists),
`content/schema.json`.

Import and validate at build time. **Never hand-edit it** — it is generated upstream and
your changes would be overwritten. If you think it is wrong, say so.

Item shape:

```jsonc
{
  "id": "lug_nuts",
  "script": "My lug nuts are tight and secure, all present, no cracks, no rust streaks...",
  "concepts": [
    { "id": "secure", "label": "Tight and securely mounted",
      "accept": ["tight","secure","not loose"], "required": true },
    ...
  ],
  "auto_fail": false
}
```

`script` is the model answer — never require it verbatim. `concepts` are the scoreable
ideas; correct paraphrase scores full marks. `accept` is a hint list, not a whitelist.
All thresholds come from `standards` — **never hardcode a graded number**.

### The core loop

Player stands at a **fixed camera station**, looks around, **taps a part** → the **real
photograph** opens → they **press and hold while speaking** the callout → it is graded
against the concepts → **concept pips** fill (`LUG NUTS ● ● ○ ○`).

Stations: `driver_seat` · `front_of_truck` · `steer_axle` · `driver_side` ·
`behind_cab` · `trailer_side` · `trailer_rear`. Tap a waypoint to move. No free roam.

### Scoring

```
item_score  = required concepts hit / required total
run_passed  = overall >= 80% AND zero auto-fail misses   ← not configurable
```

Offline keyword grader (token-set matching with stemming, all three languages) plus an
online AI grader behind a server proxy. **Never ship an API key in the client.** Offline
must never score higher than online.

### Speech

On-device recognition, push-to-talk (starts on press, ends on release — not
voice-activity detection, which fails outdoors). Live partial transcript, re-record
before submitting. Locale follows the spoken language.

**A typed fallback is mandatory and scores identically.** These players are
overwhelmingly ESL speakers and accented English is recognised less accurately; one who
cannot make the mic understand them will quit.

### Air brakes — the part that fails students

Gate each phase on its `preconditions[]` (engine state, key, valve positions) as a state
machine. Wrong state → the phase refuses to start and explains why. Interactive cab
controls drive a **live animated air gauge**. `reading` steps need a spoken number
validated live against `standards` — out of range is a *dangerous error*, not a miss.
`timer` steps run for real and are not skippable in Exam Simulator. Order is graded.

### Modes

Learn (AI instructor) · Practice · Quick Drill (90s) · Exam Simulator (real timers,
auto-fail ends the run with a full-screen result) · Find the Defect *(v1.5 — swap mesh
and material variants: cut tyre, rust decal, apron shifted to open a fifth-wheel gap)*.

### Progression

Spaced repetition, **1 → 3 → 7 → 21 days → mastered**, any miss resets to 1 day, backed
by a real SQLite table. XP that buys nothing. Section medals. Streaks with one free
freeze a week. **No lives, no hearts, no paywalls** — these are adults paying for a
license.

### Players and platforms

Adults 25–55 changing careers, English/Spanish/Portuguese, mid-range phones from 2022,
bad signal, metered data, bright sun. Huge touch targets, very high contrast, large type.

Ship iOS, Android and desktop. Budget: **≤300k tris on screen, 30fps locked, ≤250MB
package, ≤8s to first interaction.** Provide a **photo-only mode** that bypasses 3D
entirely and stays fully playable.

---

## BUILD ORDER — stop and report at each checkpoint

**Phase 1 — Content + grading.** Importer, validation, offline grader, a bare test
screen with a typed input box.

> **CHECKPOINT 1 — run these and paste the real output:**
> 1. `lug_nuts` + `they're tight and all there` → exactly **2** pips
> 2. `lug_nuts` + `they are not loose, none are missing, no cracks, and no rust streaks` → **4** pips *(pure paraphrase — nothing matches `accept` literally)*
> 3. `front_tire` + `the tire looks fine` → **0** pips
> 4. `están apretadas y todas presentes` → **2** pips
> 5. `estão apertadas e todas presentes` → **2** pips
>
> Fail (2) and the grader is too literal — it will fail students who answered correctly.
> Score anything on (3) and it is rubber-stamping and the game is worthless.
> **Fix before continuing.**

**Phase 2 — Generate the vehicle.** `generate_truck.py`, both glTF exports, the
manifest, and the validator confirming all named parts exist.
*Checkpoint: screenshots from all 7 stations + the triangle count.*

**Phase 3 — 3D world.** Stations, tap-to-select, photo panel, callout, grading in 3D.
*Checkpoint: measured tris, draw calls, fps on a real mid-range device.*

**Phase 4 — Speech.** On-device recognition per platform, push-to-talk, typed fallback.
*Checkpoint: the five tests again, spoken, on a real device.*

**Phase 5 — Air brakes.** Precondition state machine, live gauge, real timers.
*Checkpoint: an auto-fail ending a run; a 60s timer that cannot be skipped.*

**Phase 6 — Modes, progression, three languages.**
*Checkpoint: a full graded run in each language.*

**Phase 7 — Polish and packaging.** Icons, splash, real screenshots, privacy manifests,
specific microphone purpose strings.

---

## NON-NEGOTIABLES

1. Never alter inspection content to make grading easier.
2. Never let a player pass a run with an auto-fail miss.
3. Every graded number traces to `standards`.
4. A typed answer always scores identically to a spoken one.
5. Never ship an API key in the client.
6. Audio transcribed on device, deleted after each run, no upload without explicit consent.
7. Photo-only mode ships in v1.
8. Never claim the game is state-approved, DMV-endorsed, or guarantees a pass.
9. **If you stub or fake anything, say so plainly.** Never present a stub as working.

## FINAL REPORT

How to build and run · every checkpoint result with real measured numbers · everything
stubbed or incomplete, bluntly · what you would fix first · anything here you disagree
with and why.

Start with Phase 1. Stop at Checkpoint 1 and wait for me.
