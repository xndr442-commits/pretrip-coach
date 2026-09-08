# Product Spec

## The problem

A CDL student gets limited hours next to an actual truck. The pre-trip inspection
is roughly 100 spoken callouts they must deliver from memory, on their feet, to a
state examiner, under pressure — and in a second language for most of this school's
students. Truck time is the scarcest, most expensive resource in the school.

The inspection is memorisable **away from the truck**. Nothing about rehearsing
"my lug nuts are tight and secure, all present, no cracks, no rust streaks" requires
standing next to a wheel. It requires repetition and correction.

Today that repetition happens by reading a paper booklet. Paper cannot listen, cannot
tell you what you left out, and cannot tell you that you just failed the air brake
check.

## The product

A phone-first app where a student runs the inspection out loud and gets scored, with
an AI instructor that teaches before it tests.

**Learn Mode** — the instructor shows the part, says the callout, explains why it
matters, listens to the student repeat it, and names exactly which required ideas
they left out.

**Test Mode** — the student performs unaided. The app grades against the same
concepts an examiner scores, calls automatic failures loudly, and produces a score
card with their own audio next to the model callout.

## Users

CDL-A students at Fenix Truck School (Jacksonville FL) and Moov (Boston MA).

- Adults, often 25–55, frequently changing careers.
- English, Spanish, Portuguese all present as first languages.
- Mixed device quality; assume a mid-range Android and intermittent signal.
- Mixed comfort with apps. Assume the interface must be obvious without a tutorial.
- Highly motivated — a CDL is a direct, immediate income change. They will grind if
  the grind clearly moves them toward passing.

## Success looks like

1. A student can rehearse the full inspection without a truck and know their score.
2. Instructors see who is ready and who is not before booking a test slot.
3. Fewer failed first attempts on the state test.
4. The school can hand the app to a new student on day one as part of the course.

## Scope

**In scope, v1**
Full walk-around (13 sections, 64 items) · Air brake test · Learn/Test/Drill/Exam
modes · Voice + typed input · EN/ES/PT · Offline practice · Spaced repetition ·
Score cards and run history · iOS, Android, web/PWA.

**Out of scope, v1**
Backing manoeuvres · Road test · The written knowledge exam · Instructor dashboard
(v2) · Multi-school tenancy (v2) · Payments.

## What makes this defensible

The content. Any competent developer can build a quiz app. The value here is 64
items and 263 graded concepts derived from *this school's own material*, matched to
the official checklist categories, with correct auto-fail marking and real
photographs of the trucks the students will actually test on. That is the asset.
