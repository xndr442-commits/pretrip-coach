# Game Design

## The design constraint

This is a safety exam, not a casual game. Every mechanic must serve retention of a
spoken procedure. No lives, no energy timers, no paywalled hearts, no punishment
loops. Students are paying for a license, and treating them like a mobile-game whale
would be both wrong and obvious.

The game layer exists for one reason: **spaced, corrected repetition is what moves a
callout into long-term memory, and people don't do it voluntarily unless it feels
good.**

## Modes

### Learn
One item at a time with the AI instructor. Photo → model callout → why it matters →
student repeats → specific correction. No score, no timer. This is where a student
starts a section.

### Practice
A full section, no instructor commentary between items. Score shown at the end,
hints available, no auto-fail termination. The workhorse mode.

### Quick Drill
90 seconds, random items weighted toward the student's weak list. Built for a spare
moment in a queue. Ends with a single number and a one-line "you're weakest on
steering axle."

### Exam Simulator
The whole thing, timed, examiner-style silence. No hints. Auto-fails end the run
immediately. Produces the real score card. This is the mode that tells a student
whether to book a test.

## Progression

**Per-item mastery** — an item is *learned* on first clean run, *mastered* after 3
clean runs across 3 separate days. Mastery decays: an item untouched for 30 days
drops back to *learned* and re-enters the queue.

**Section medals** — bronze (section completed), silver (80%+ clean), gold (3 clean
runs, no hints, no misses).

**XP** — 10 per item hit clean, 25 per section completed, 100 per clean exam run.
XP buys nothing. It is a visible record of work done, which is the point.

**Streaks** — consecutive days with at least one drill. One free "freeze" per week,
because these students drive and work shifts and a broken streak over a 14-hour day
is a reason to quit the app, not to try harder.

## Spaced repetition — the core mechanic

Build this properly, backed by a real table, not a shuffle.

A missed concept schedules its item for review. Intervals: **1 day → 3 days → 7 days
→ 21 days → mastered.** Any miss resets the item to 1 day. The review queue is what
the app opens to.

This is the single highest-value feature in the product. If you build only one thing
past basic scoring, build this.

## Feedback rules

- Correction is **immediate and specific**. Never "not quite" — always "you didn't
  say anything about cracks."
- Praise is **specific and rationed**. "That was clean, all five" beats "Great job!"
  every time, and constant praise after sloppy work teaches a student that sloppy is
  fine.
- Automatic failures are **never** softened into a percentage. A student who misses
  the brake check sees a full-screen result that says the run is over and why, because
  that is exactly what happens on test day.
- Every wrong answer shows the model callout with the missed concepts highlighted.

## Social

Opt-in school leaderboard: first name + last initial, weekly XP only. Scoped to the
student's own school so the comparison set is people they actually know. No global
board — a stranger's score is not motivating, and it invites gaming.

## Anti-goals

Nothing that rewards speed over accuracy. Nothing that lets a student pass a run
with an auto-fail miss. No streak mechanic aggressive enough to make someone open
the app while driving.
