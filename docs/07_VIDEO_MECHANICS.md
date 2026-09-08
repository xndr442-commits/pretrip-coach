# Video Mechanics Analysis

**Source:** a third-party YouTube pre-trip walkthrough (15:23, 1080p30) supplied as a
reference. 92 sampled frames + 134 detected shot changes + audio event analysis.

> **Use restriction.** This is someone else's copyrighted video from another school.
> It is analysed here for *mechanics only* — how the procedure is physically
> performed, how information is layered on screen, how a run is paced. Its narration,
> its on-screen text, its branding and its footage are **not** to be copied into the
> app. All spoken content in the app comes from Fenix's own booklet and handout.

---

## 1. The single most important finding

**The unit of the test is not a sentence. It is a hand on a part.**

The video's grammar repeats identically for ~50 items:

```
wide shot — person standing at the zone
   ↓
CUT to close-up — hand physically touching the part
   ↓
part name appears on screen at the exact moment of contact
   ↓
callout is spoken while the hand stays on the part
```

That is the whole interaction model for the game. An item is not "read this text and
say it back." An item is **contact + name + explanation, simultaneously.**

### What this means for the build

The item screen should be a **photograph with a touch hotspot**, not a card with a
label. The student presses and holds the part in the photo, and the mic opens while
they hold. Releasing ends the callout.

This does three things at once:
- Trains the physical habit the examiner is actually scoring ("name, point to and/or
  touch")
- Gives a natural push-to-talk gesture, which is more reliable than
  voice-activity detection in a noisy yard
- Makes "which part is this?" a scoreable question on its own

Every photo in `assets/reference/curated/` should get hotspot coordinates. The
booklet's own orange arrows (visible in ~20 of the extracted photos) already mark the
exact contact point — use those as the hotspot centres.

---

## 2. Air brake test — staged decomposition

The video breaks the air brake test into **four named, numbered stages, each with a
preliminary gate that must be satisfied before the stage begins.** The gate is shown
as a short numbered checklist, then the stage runs.

| Stage | Gate before it | What is measured |
|---|---|---|
| 1 · Governor cut-off | engine on, valves in | pressure at which the governor cuts out |
| 2 · Applied pressure | engine off / electric on, HSA off | psi lost in one minute under applied pressure |
| 3 · Warning light & buzzer | (continues from 2) | psi at which light + buzzer activate |
| 4 · Valve deployment | (continues from 3) | psi at which both valves pop |

**Why this matters for the game:** our `airbrakes.en.json` currently models 9 phases
as a flat ordered list. The video's structure is better for teaching because it
separates *preconditions* from *measurements*. A student fails this test far more
often by having the engine in the wrong state than by forgetting a word.

**Recommended change:** add an explicit `preconditions[]` array to each air-brake
phase, and gate the phase in the UI. The student must set the truck state correctly
before the phase will start — a small state-machine puzzle. Getting the state wrong
is exactly the mistake that fails people, so make it a mechanic rather than a
footnote.

### Live reading capture

At each measurement moment the video puts the number on screen as it happens
("…at 125 PSI", "…deployed at 25 PSI"). The game must do the same: at each
`reading` step the student speaks a number, it appears large on screen, and it is
validated against the range in `standards` immediately — green if in range, red with
the correct range if not.

Our content already has these `reading` blocks. Wire them to a visible gauge.

---

## 3. Screen-language patterns worth adopting

Observed layering, all four present simultaneously without clutter:

| Layer | Position | Purpose |
|---|---|---|
| Module chip | top-left, persistent | which test you're in |
| Stage chip | bottom-left, numbered, high-contrast | which stage of that test |
| Precondition list | centre, numbered, temporary | what must be true before starting |
| Item name | lower-centre, appears on contact | what you're touching right now |

Adopt this hierarchy. It is legible in bright outdoor sun at a glance, which is the
real design constraint.

### Count annotations — adopt this immediately

The video labels some items with **how many things you must name**:
- "Indicators (6)"
- "Five Functions / Five Locations" (for lights)

This is a memory scaffold and it is free to implement: our content already knows how
many required concepts each item has.

**Show the required-concept count on every item as a progress pip row.** Six empty
dots that fill as the student covers each concept. The student can see, live, that
they've said four of six things. This converts a vague "did I say enough?" into a
visible target, and it is the highest-value single UI addition available.

---

## 4. Pacing — what a real run costs

| Segment | Elapsed | Note |
|---|---|---|
| In-cab air brake test | ~00:45 – 04:00 | ~3¼ min, includes two real 60s timers |
| In-cab equipment & visibility | ~04:00 – 06:30 | rapid, ~10s per item |
| Tugs & service brake | ~05:50 – 06:35 | |
| Driver side & coupling | ~06:35 – 10:00 | the densest section |
| Engine compartment | ~10:10 – 12:00 | |
| Steering & steer axle | ~11:20 – 13:00 | |
| Lights section | ~13:05 – 15:20 | |

**A complete run is about 15 minutes, and roughly 2 of those are silent timer waits.**

Design consequences:
- **Exam Simulator must be ~15 minutes and must not skip the timers.** A student who
  has never sat through a real 60-second static leak test will rush it in front of
  the examiner.
- **Practice mode should let timers be skipped** with an explicit "timer skipped"
  mark on the score card, so a 15-minute run isn't required to drill wording.
- **Quick Drill at 90 seconds** is well-calibrated — that's ~9 items at the observed
  10s/item walk-around pace.

---

## 5. Zone ordering

The route observed, which matches our section order closely enough to keep ours:

in-cab brake check → indicators & emergency equipment → visibility & controls →
tugs & service brake → mirrors → battery → fuel/DEF tanks → frame & cross members →
air lines & glad hands → apron & gap → fifth wheel, mounting bolts, safety latch →
landing gear → locking jaws → engine hoses (passenger side) → engine (driver side) →
fluids → steering gearbox → steering linkage → brake lines → brake contaminants →
spring mounts → shock → steer tire → lugs → lights (tractor then trailer)

Two differences from our content, both worth adopting:

1. **The engine compartment is walked twice — passenger side, then driver side.**
   Our `front_operations` treats it as one zone. Splitting it matches how a student
   actually walks and reduces "I already said that" confusion.
2. **Lights are done last**, as a dedicated section with a helper mnemonic, rather
   than second. Our content has lights at position 5. Consider making section order
   configurable — schools sequence this differently, and the examiner does not
   require a fixed order between sections.

---

## 6. Audio

Audio analysis found **no cleanly isolatable air-release or buzzer samples** — the
narration is mixed over every mechanical sound, and the tonal detections at
~1000 Hz were voiced speech, not the buzzer.

**Conclusion: we cannot and should not extract game audio from this video.** It is
copyrighted and it is technically unusable.

**Instead, record our own at the yard.** A phone voice recorder is fine. Shot list —
about 30 minutes of work, and these become real trainable cues:

| Clip | Why it matters |
|---|---|
| Governor cut-out (the air release) | the student is graded on *hearing* this |
| Governor cut-in | " |
| Low-air buzzer, isolated | " |
| Both valves popping out | " |
| One valve popping (the failure case) | teaches "keep fanning until the second pops" |
| Brake pedal fanning | ambience for the timed stages |
| Engine start, idle, 1500 rpm | state cue for the preconditions puzzle |
| Air horn, city horn | |
| Glad hand connect / disconnect | |

Then add an **audio identification drill**: play a sound, student names it. That
mode does not exist in any competitor and it trains something the paper booklet
fundamentally cannot.

---

## 7. Summary — what to change in the build

1. Item interaction = **press-and-hold the part in the photo while speaking.**
2. Add **hotspot coordinates** to every curated photo (booklet arrows mark them).
3. Add **`preconditions[]`** to air-brake phases and gate them in the UI.
4. Show a **concept-count pip row** on every item, filling live as concepts are hit.
5. **Exam Simulator runs the real 60-second timers**; Practice may skip with a mark.
6. Split the engine compartment into **passenger side / driver side**.
7. Make **section order configurable**.
8. Record **our own audio** at the yard and add an audio-identification drill.
