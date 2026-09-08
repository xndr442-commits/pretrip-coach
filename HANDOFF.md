# HANDOFF — What to send the builder, and in what order

Everything below is ready now. Work top to bottom.

---

## STEP 1 · Send this, in this order

**1. Paste as your first message:** `prompts/00_MASTER_BUILD_PROMPT.md`
   — everything between the `====` markers.

**2. Attach these folders:**

```
BUILD_SPEC.md                  the complete brief (the prompt is the summary)
content/                       all 8 JSON files — the source of truth
assets/reference/curated/      59 photos + manifest.json with hotspots
prompts/                       instructor + grader system prompts
docs/                          background, decisions, 3D constraints
```

**3. Do NOT send:**
- `source/` — the original PDFs. Content is already extracted; sending them invites
  the builder to re-derive it and get it wrong.
- `assets/reference/extracted/` — working files, 21 MB of duplicates.
- `assets/reference/pages/` — the 36 page renders. Useful to you, noise to a builder.
- The third-party reference video. It's another school's copyright and none of it is
  in the app.

---

## STEP 2 · The first task to give it

Do not ask for the whole app. Ask for the vertical slice, and make it prove the
scoring works before any UI polish or 3D exists:

> Build steps 1–3 of the build order in BUILD_SPEC.md §12 only.
>
> 1. Content loader with typed TypeScript models for `pretrip.en.json` and
>    `airbrakes.en.json`. Validate against `content/schema.json` on boot and fail
>    loudly.
> 2. A single item screen: the part photo from `manifest.json` with its hotspot,
>    concept pips, press-and-hold to record, live transcript, and a typed fallback
>    that scores identically.
> 3. The offline keyword grader and a score card, working in English, Spanish and
>    Portuguese using `concepts.es.json` / `concepts.pt.json`.
>
> Do not build the 3D scene, Learn Mode, the air brake module, or the game layer yet.
> Stop when I can hold a part, speak a callout, and see the right concept pips fill.

**Then verify it yourself before letting it continue.** Try `lug_nuts` and say only
*"they're tight and all there."* Exactly two pips should fill — `secure` and
`all_present` — and it should tell you that you missed cracks and rust. If it fills
four, or accepts a vague answer, the grader is wrong and nothing built on top of it
will be trustworthy.

---

## STEP 3 · Four things only you can unblock

| # | Blocker | Why it matters |
|---|---|---|
| 1 | **Florida examiner checklist** | `us_fl.checklist_confirmed` is `false`. MA §11M is mapped; FL is a placeholder. Thresholds are settled — only the checklist wording is missing. |
| 2 | **3D model commercial licence** | You said you may sell this later. That needs commercial redistribution rights, not personal-use. Send the source page or licence file. Cheaper to know now than after the app is built. |
| 3 | **A replacement trailer model** | The current one is a single mesh with no separate parts. Seven of the 64 items live on the trailer and none can be tapped. |
| 4 | **Content sign-off** | `review/content_signoff.html` — open in a browser, print to PDF, read all 64 callouts, sign. Nothing should reach a student before this. |

None of these block starting Step 2. All four block release.

---

## STEP 4 · Things you're doing that feed in later

- **Truck walkaround video** (Q16) — for the 3D model. Shoot in even light, slow and
  steady, full circle plus the cab interior, overlapping frames.
  **Record the audio too** — the governor cut-out, the low-air buzzer, both valves
  popping. That unlocks the Audio Drill mode, which no competitor has, and it's free
  while you're already at the truck.
- **Store accounts** (Q17) — Apple Developer $99/yr, Google Play $25 one-time. Register
  both under the school's business entity, never a personal account. Do this early;
  Apple's verification can take days.
- **app.fenix.school** (Q19) — a DNS record pointing at the web build. Also the
  Microsoft Store route.

---

## What's already done, so nobody rebuilds it

| | |
|---|---|
| Sections / items / concepts | 13 / 64 / 263 |
| Auto-fail items | 7 (the whole in-cab brake check) |
| Air brake steps | 60 across 9 gated phases, 3 real timers, 10 live readings |
| Reference photos | 59, named, captioned, with touch hotspots |
| Translations | ES 64/64 · PT 64/64 |
| Concept accept-lists | ES 136/136 · PT 136/136, plus 10 shared per language |
| Jurisdictions | `us_fl`, `us_ma` |
| Air-leak threshold | **Resolved** — 3 released / 4 applied, both states |
| Transmission variants | Manual + automatic on both brake-hold steps |
| Validation | 0 errors, 0 warnings |

Run `python3 scripts/validate_content.py` any time. Put it in CI — malformed content
must never reach a build.

**Content is generated, not hand-edited.** If something needs changing, edit the
script in `scripts/` and rebuild. A builder that edits the JSON directly will have its
work overwritten.
