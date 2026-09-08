# Scoring Rules

## The rule the whole app is built on

From the official Class A Vehicle Inspection checklist (§11M):

> "You MUST name, point to and/or touch and fully explain what you are inspecting
> each safety critical item for. If you do not do so, you will not get credit for
> the item(s)."

Three obligations per item — **name it, indicate it, explain what you're checking
it for.** The app can verify the first and third from speech. The second is a
physical act; the app teaches it and reminds, but cannot grade it. Be honest about
that in the UI rather than implying full-fidelity grading.

## Concept scoring

Each item declares `concepts` — the individual ideas that must appear.

```
item_score = required concepts hit / required concepts total
item_passed = item_score >= 0.8 AND no dangerous error
```

A concept is hit if the student expressed the idea **in any wording, in any
supported language.** `accept` lists are matcher hints, not whitelists.

Optional concepts (`required: false`) report as bonus and never lower a score.

## Two graders, one contract

| | Online (default) | Offline |
|---|---|---|
| Engine | AI grader, `prompts/02_GRADER_PROMPT.md` | Deterministic keyword matcher |
| Handles | Paraphrase, accent, code-switching, any language | Literal and near-literal matches |
| Vocabulary | The concept `label` semantically | `concepts[].accept` + `defect_vocabulary` per language |
| When | Connectivity available | Airplane mode, no signal, AI unavailable |

Offline runs are **flagged as offline-graded** in history and re-graded by AI when
connectivity returns. Never silently mix the two in one score.

The offline matcher will under-score paraphrase. That's acceptable and expected —
what is not acceptable is failing a student in offline mode without telling them the
grading was degraded.

## Automatic failure

The checklist marks the air/hydraulic brake check with:

> `* Automatic failure if not performed correctly`

In this content that is `section.auto_fail_section: true` on `in_cab_brake_check`,
plus `item.auto_fail: true` on 7 individual items:

| Item | Section |
|---|---|
| `air_compressor_governor` | In-Cab Air Brake Check |
| `air_leak_test` | In-Cab Air Brake Check |
| `low_air_warning` | In-Cab Air Brake Check |
| `spring_brakes_popout` | In-Cab Air Brake Check |
| `parking_brake_check` | In-Cab Air Brake Check |
| `trailer_brake_check` | In-Cab Air Brake Check |
| `service_brake_check` | In-Cab Air Brake Check |

Behaviour in **Exam Simulator**: the run ends the moment one is failed. Full-screen
result, the item that ended it, what was missed, and a direct link to relearn it.

Behaviour in **Practice**: flagged loudly, run continues.

Also auto-fail on test day, and taught as such even though the app can't detect them:
pulling the spring brake valves by hand instead of letting them pop, shifting gears
on railroad tracks, stopping on the tracks.

## Ordered vs unordered

`pretrip.en.json` — order within a section is not graded. A student may cover an axle
in whatever order they like as long as every item is covered.

`airbrakes.en.json` — `"ordered": true`. Sequence *is* the procedure. A step
performed out of order scores zero even with perfect wording, because performing the
leak test before shutting the engine off is not the test.

## Numeric readings

Steps with a `reading` block require the student to speak an actual number, not a
range. "I'm at full pressure" scores less than "I am at full pressure, 132 psi."

Validate the spoken number against the range in `standards`. A number outside the
range is a **dangerous error**, not just a miss — the student has misread a gauge or
misremembered a threshold, and both are worth stopping for.

Timed steps (`kind: "timer"`) must actually elapse. A student who claims a minute
passed in twelve seconds gets no credit — the real examiner has a watch too.

## Pass threshold

80% overall (`grading.pass_threshold_pct`), **and** zero auto-fail misses. The second
condition is not negotiable by configuration.

## ⚠️ Unresolved: the static leak limit

The two source documents disagree, and this must be settled before launch.

| Source | Brakes released | Brakes applied (90 psi) |
|---|---|---|
| `NEW MATERIAL PRE TRIP` p.8 | — | **4 psi/min** (Class A), 3 psi/min (Class B) |
| `AIR BRAKES TEST` handout | **3 psi/min** | **4 psi/min** |

The handout matches the common AAMVA figures for a single vehicle; the booklet
states 4 psi for Class A. Both are captured in `content/pretrip.en.json → standards`
and `content/airbrakes.en.json → variables` so the app can be configured, and the
grader reads from there rather than hardcoding.

**This needs Alexandre to confirm against the current FL and MA examiner sheets
before students study from it.** Teaching a student the wrong threshold is the one
failure mode of this app that is worse than not having it. See
[06_OPEN_QUESTIONS.md](06_OPEN_QUESTIONS.md).

## Corrections already applied to the source

- Booklet p.20 reads "tread depth no less than 4,32 inches." Corrected to
  **4/32 of an inch** (steer axle; 2/32 elsewhere). The original is a typo that
  would confuse a student reading it literally.
- Booklet p.8 gives spring-brake pop-out as 20–45 psi; the Portuguese edition says
  40–20. Standardised on **20–45 psi**.
