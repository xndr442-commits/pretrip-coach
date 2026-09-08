# Paste this into Codex as your first message

Unzip `PreTripCoach_handoff.zip` into the repo root first, so `content/`,
`assets/`, `docs/` and `prompts/` are present. Then paste everything below.

---

You are a senior full-stack engineer building a production, store-shippable training app. Build it to ship: real offline support, real accessibility, real error states. No placeholder screens, no TODOs in shipped paths.

## THE REPO

This repo already contains authored, validated content. Read it, never rewrite it:

- `BUILD_SPEC.md` — the complete brief. Read this first, in full.
- `content/pretrip.en.json` — 13 sections, 64 graded items, 263 scoreable concepts, 7 auto-fail items
- `content/airbrakes.en.json` — 9 gated phases, 60 ordered steps, 3 timers, 10 live readings
- `content/i18n/{en,es,pt}.json` — UI strings + full ES/PT labels and callouts (64/64 each)
- `content/i18n/concepts.{es,pt}.json` — ES/PT accept-lists for all 136 item-specific concepts
- `content/schema.json` — JSON Schema for both content files
- `assets/reference/curated/**` — 59 real photographs + `manifest.json` with touch hotspots
- `prompts/01_AI_INSTRUCTOR_SYSTEM_PROMPT.md`, `prompts/02_GRADER_PROMPT.md` — use verbatim, later
- `docs/` — background, decisions, 3D constraints

## THE PRODUCT

**Pre-Trip Coach** — a voice-first trainer for the CDL pre-trip inspection and air brake test, for a US truck-driving school.

The commercial driving test is a spoken, physical performance. A student walks a truck, touches ~64 safety-critical parts, and says out loud what they are checking each one for. The official scoring sheet states: "You MUST name, point to and/or touch and fully explain what you are inspecting each safety critical item for. If you do not do so, you will not get credit." The air brake portion is marked automatic failure if not performed correctly.

Users are adults, 25–55, changing careers. English, Spanish and Portuguese are all first languages among them; many are recent immigrants and speak English as a second or third language. Mid-range phones, 2022 or newer. Unreliable signal, metered data. Motivated, but not gamers.

## STACK

React Native + Expo + TypeScript. Expo Router, Zustand, expo-sqlite. One codebase targeting iOS, Android and web. (3D via react-three-fiber comes much later — not in this task.)

## THE CONTENT MODEL — the thing to get right

Each item looks like this:

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
  "auto_fail": false
}
```

Critical distinctions:

- `script` is the model answer. **Never require it word-for-word.**
- `concepts` are the scoreable ideas. A student who paraphrases correctly gets full marks.
- `accept` is a hint list for the keyword matcher, **not a whitelist**. "It's not going anywhere" satisfies `secure`.
- Only `required: true` concepts count toward the score.

All numeric thresholds live in `content/pretrip.en.json → standards`, split by vehicle class and jurisdiction (`us_fl`, `us_ma`). **Never hardcode a threshold in a component.** Read from `standards`.

## SCORING RULES

```
item_score  = required concepts hit / required concepts total
item_passed = item_score >= 0.8 AND no dangerous error
```

Grade meaning, not words. Ignore grammar, accent, filler words, false starts and transcription noise. If the transcript is unintelligible, say so rather than scoring zero.

## YOUR TASK — steps 1–3 only

Do **not** build the 3D scene, Learn Mode, Test Mode, the air brake module, or the game layer yet. Build exactly this and stop:

**1. Content loader.**
Typed TypeScript models for `pretrip.en.json` and `airbrakes.en.json`. Validate both against `content/schema.json` on boot. Fail loudly and visibly on malformed content — never start with bad content.

**2. A single item screen.**
- The part photograph, full-bleed, from the item's `image`
- Its touch hotspot from `assets/reference/curated/manifest.json` (`hotspot: {x, y, r}`, normalised 0–1). Note `hotspot_source`: `arrow_detected` is reliable, `default_center` is a placeholder.
- **Concept pips**: one empty pip per required concept, filling live as each is covered. `LUG NUTS ● ● ○ ○` means two of four said.
- **Press and hold the hotspot to record.** Mic opens on press, closes on release. On-device speech recognition only — no cloud STT.
- Live transcript shown while speaking, with the ability to re-record before submitting.
- **A typed fallback that scores identically.** This is mandatory, not optional — accented English is recognised less accurately and this app's users are overwhelmingly ESL speakers. A student who can't get the mic to understand them will quit.

**3. The offline keyword grader and a score card.**
- Match transcripts against `concepts[].accept`, plus `defect_vocabulary` in the i18n files and `concepts.{es,pt}.json` for item-specific concepts.
- Must work in **English, Spanish and Portuguese**.
- Score card shows: what was said, which concepts were hit, which were missed, and the model callout with the missed concepts highlighted.
- Feedback names what was missing in the words they should have said. Never "not quite" — always "you didn't say anything about cracks."

## ACCEPTANCE TEST — I will run this

Open `lug_nuts` and say only: *"they're tight and all there."*

Exactly **two** pips must fill — `secure` and `all_present` — and the score card must report that `no_cracks` and `rust` were missed. If four pips fill, or a vague answer is accepted, the grader is wrong and everything built on top of it is untrustworthy.

Run the same test in Spanish (*"están apretadas y todas presentes"*) and Portuguese (*"estão apertadas e todas presentes"*). Same result.

## NON-NEGOTIABLES

1. Never alter the inspection content to make grading easier.
2. Every graded number traces back to `standards`.
3. A typed answer always scores identically to a spoken one.
4. Audio is transcribed on device and deleted after each run. No upload. No AI provider key in the client.
5. No account required. The app is free.
6. Content is generated from scripts in `scripts/` — do not hand-edit the JSON, it will be overwritten.

Start by reading `BUILD_SPEC.md` in full, then confirm your plan before writing code.
