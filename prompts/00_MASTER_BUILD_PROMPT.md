# MASTER BUILD PROMPT — "Pre-Trip Coach" (v2.0)

> **How to use this file.** Paste everything between the `====` markers as your first
> message to the builder, and attach `content/`, `assets/reference/curated/`,
> `prompts/`, and `BUILD_SPEC.md`. This is the condensed brief; `BUILD_SPEC.md` is the
> complete one. Where they differ, `BUILD_SPEC.md` wins.

====================================================================

## ROLE

You are a senior full-stack engineer building a production, store-shippable training
app. Build it to ship: real offline support, real accessibility, real error states.
No placeholder screens, no `TODO` in shipped paths.

## PRODUCT

**Pre-Trip Coach** — a voice-first 3D trainer for the CDL pre-trip inspection and air
brake test, for Fenix Truck School (Jacksonville FL) and Moov (Boston MA).

The commercial driving test is a **spoken, physical performance**. A student walks a
truck, touches ~64 safety-critical parts, and says out loud what they're checking each
one for. The official scoring sheet is blunt:

> "You MUST name, point to and/or touch and fully explain what you are inspecting each
> safety critical item for. If you do not do so, you will not get credit."

The air brake portion is marked **automatic failure if not performed correctly.**

This app rehearses that performance without a truck present.

**Users:** adults, 25–55, career-changing. English, Spanish and Portuguese are all
first languages here; many are recent immigrants. Mid-range phones, 2022 or newer.
Unreliable signal, metered data. Motivated, not gamers. Design for that person.

## THE CORE INTERACTION

A **3D truck** the student inspects — driver's seat for in-cab work, walking the
vehicle outside. But the 3D is only half:

- **3D scene** → *where* is this part, what's next to it
- **Real photograph** → *what* does this part actually look like

Tap a part in 3D → the real photo of it opens → **press and hold the part while
speaking** the callout. Mic opens on press, closes on release.

That gesture trains the physical habit the examiner scores, and beats voice-activity
detection in a windy yard. Never replace the photo layer with a render — a rendered
brake chamber is a guess; a photo of their brake chamber is what they'll see on test day.

**Station-based, not free-roam.** Fixed camera stations, look around freely, tap a
waypoint to move. The real inspection is a fixed route; the student is never lost.

**Concept pips.** Show one empty pip per required concept, filling live as each is
covered: `LUG NUTS ● ● ○ ○`. Highest-value UI element in the app, nearly free.

## CONTENT — ALREADY AUTHORED, DO NOT REWRITE

| File | Contains |
|---|---|
| `content/pretrip.en.json` | 13 sections · 64 items · 263 concepts · 7 auto-fails |
| `content/airbrakes.en.json` | 9 gated phases · 60 ordered steps · 3 timers · 10 readings |
| `content/i18n/es.json` · `pt.json` | Full ES/PT labels and callouts, 64/64 |
| `content/i18n/concepts.{es,pt}.json` | ES/PT accept-lists, all 136 item-specific concepts |
| `assets/reference/curated/**` | 59 real photographs + `manifest.json` with hotspots |

`script` is the model answer — never require it word-for-word. `concepts` are the
scoreable ideas; `accept` is a hint list for the offline matcher, not a whitelist.
"It's not going anywhere" satisfies `secure`.

All numbers live in `standards`, split by vehicle class and jurisdiction
(`us_fl`, `us_ma`). **Never hardcode a threshold in a component.**

## GRADING

```
item_score  = required concepts hit / required concepts total
item_passed = score >= 0.8 AND no dangerous error
run_passed  = overall >= 80% AND zero auto-fail misses   ← second condition not configurable
```

Two graders, one contract: **AI grader** online (`prompts/02_GRADER_PROMPT.md`),
**offline keyword matcher** as fallback. Offline runs are flagged and re-graded on
reconnect. The offline grader must never score higher than the AI grader — assert it.

Show the transcript before grading and let them re-record. Being marked wrong for
something the mic misheard destroys trust faster than anything else.

**Auto-fail is loud.** In Exam Simulator a missed auto-fail ends the run immediately:
full screen, what was missed, one button to relearn it. That's what test day does.

## AIR BRAKES

- **Preconditions are a mechanic.** Each phase is gated on truck state (engine on/off,
  key, valves). Students fail this test by having the truck in the wrong state far more
  than by forgetting words. Wrong state → the phase refuses to start, with an explanation.
- **Spoken numbers, not ranges.** "132 psi" scores; "full pressure" doesn't. Validate
  against `standards` live — out of range is a *dangerous error*, not a miss.
- **Timers are real.** 60 seconds means 60 seconds in Exam Simulator. A student who's
  never sat through it will rush it in front of the examiner.
- **Order is graded here** (`"ordered": true`), unlike the walk-around.
- Two brake-hold steps carry manual/automatic `variants` — the student picks their
  test vehicle once.

## STACK

**React Native + Expo + TypeScript, react-three-fiber (Three.js) on expo-gl.**
One codebase → iOS, Android, web. The web build becomes the Microsoft Store PWA —
Unity would break that.

**3D budget, enforced in CI:** ≤150k tris on screen · ≤80 draw calls · ≤120MB texture
memory · 30fps locked · ≤40MB 3D assets · ≤4s to first interaction.
glTF/GLB + Draco + KTX2. Three LODs. Per-station culling. Baked lighting only.

**Part naming contract:** every inspectable part is a node named exactly
`part_<item_id>`, with a simplified collider. Assert all 64 items resolve to a node.

**Photo-only fallback ships in v1.** Every mode must work with 3D disabled.

**Voice:** on-device STT first (free, private, offline). Cloud STT opt-in for noisy
yards. **Always offer typing — a typed answer scores identically.** Accented English is
recognised less accurately and this app's users are overwhelmingly ESL speakers; a
student who can't get the mic to understand them will quit.

**Offline:** all content and images bundled. Everything except AI works in airplane mode.

**Privacy:** transcribe on device, delete audio after each run unless saved, no upload,
no account to practice, never ship an AI key in the client.

## LANGUAGES

All three — English, Spanish, Portuguese — for interface, teaching, callouts *and*
grading. Offline grading works in all three; `validate_content.py` fails the build if a
concept lacks a translation. Switch instantly, no restart. Numbers never translated.

Nudge students toward English runs as their test date nears — the examiner speaks English.

## GAME LAYER

Spaced repetition is the point: **1 → 3 → 7 → 21 days → mastered**, any miss resets to
1 day. Back it with a real table, not a shuffle. The review queue is what the app opens to.

XP (buys nothing, it's a record of work), section medals, streaks with one free freeze
per week. School-scoped opt-in leaderboard, first name + last initial.

No lives, no hearts, no energy timers, no paywalls. These are adults paying for a
license. Praise is specific and rationed — "that was clean, all four" beats "Great job!"

## BUILD ORDER

**Do not start with the 3D.** Ship 1–4 as a working vertical slice first.

1. Content loader + validation on boot
2. Photo item screen: hotspot, pips, hold-to-speak, typed fallback
3. **Offline grader + score card** — get scoring right before anything else
4. AI grader behind a server proxy
5. Learn Mode · 6. Test Mode + auto-fail · 7. Air brakes · 8. Spaced repetition
9. Three-language wiring
10. **3D: blocky placeholder truck**, all stations, all named nodes, loop working
11. **3D: performance harness on the floor device** — lock the budget before art
12. Real model, decimated, LODs, streaming · 13. Device tiering + fallback
14. Store packaging

Steps 10–11 come before the real model on purpose. A blocky placeholder holding 30fps
with all 64 parts wired is worth more than a beautiful model that stutters.

## NON-NEGOTIABLES

1. Never alter inspection content to make grading easier.
2. Never let a student pass a run with an auto-fail miss.
3. Never record or upload audio without explicit, revocable consent.
4. Never ship an AI provider key in the client.
5. Every graded number traces to `standards`.
6. A typed answer always scores identically to a spoken one.
7. The photo-only fallback ships in v1.
8. Do not copy anything from third-party reference video — it belongs to another
   school and was analysed for mechanics only. All content comes from Fenix's own
   booklet and handout.
9. Do not claim the app is state-approved, DMV-endorsed, or guarantees a pass.

====================================================================
