# Open Questions

> **Questions 2, 3, 4 and 6 are answered** — see [00_DECISIONS.md](00_DECISIONS.md).
> They are struck through below and kept for the record.

Grouped by whether they block the build. Answer the ⛔ ones before students see the
app; the rest can be decided as we go.

---

## ⛔ BLOCKING — content correctness

**1. The static air-leak limit conflict.**
Your two documents disagree and I will not guess on a number a student gets graded on.

| Source | Brakes released | Brakes applied (90 psi) |
|---|---|---|
| `NEW MATERIAL PRE TRIP` p.8 | — | 4 psi/min (Class A), 3 (Class B) |
| `AIR BRAKES TEST` handout | 3 psi/min | 4 psi/min |

Which is what your examiners actually score in **Florida**? And is it different in
**Massachusetts** for the Moov students? Now that the app targets both states, I need
both answers — they're allowed to differ, `threshold_overrides` exists per jurisdiction.

**Also needed: the Florida CDL vehicle inspection checklist.** I built against the MA
§11M sheet. The FL jurisdiction is currently a placeholder marked
`checklist_confirmed: false`.

**2. ~~Which state(s) is this app for?~~ ANSWERED — both FL and MA.**
Your checklist is Massachusetts §11M. Your booklet is branded Jacksonville, Florida.
If both, the app needs a state setting, because the checklists differ. If FL only,
I'll swap the checklist reference.

**3. ~~Class A only, or Class B too?~~ ANSWERED — Class A only.**
The content is written for Class A combination. Class B (straight truck) skips the
combination and trailer sections and uses different air-brake numbers. Adding it is
straightforward — but only if you want it.

**4. ~~Manual, automatic, or both?~~ ANSWERED — both, student picks.**
The air-brake hold tests in your handout say "let up on the clutch until it starts to
grab." That is manual-transmission language. Several of your test applications on file
are for automatics. Does the app need both procedures?

**5. Who signs off on the content?**
Before a student studies from this, an instructor needs to read all 64 items and
confirm each callout is what your school teaches. Who is that, and can I generate a
printable review sheet for them?

---

## ⛔ BLOCKING — scope and money

**6. ~~Is this for your school only, or for sale?~~ ANSWERED — schools first, tenant-ready for later sale.**
Completely different products. School-only: no accounts, no payments, ship it and
hand out install links. For sale: accounts, subscriptions, multi-school tenancy,
support burden, refunds. Decide before the first line of code.

**7. Free to your students, or paid?**
If paid, both stores take 15–30%.

**8. What's the budget for AI calls?**
The AI instructor and AI grader cost per use. On-device speech recognition is free
and works offline. My recommendation: on-device speech + AI grading only, with the
conversational instructor as a premium or instructor-supervised feature. But it
depends what you want to spend per student per month.

---

## Product decisions

**9. Study language vs test language.** I've specced these as separate settings — a
student studies in Portuguese but tests in English, since the examiner speaks
English. Confirm that's what you want.

**10. Does the app need to grade the *physical* actions** — pointing and touching —
or is speech enough for v1? Camera-based verification is possible but is a much
larger build. My recommendation: speech only in v1, teach the pointing.

**11. Instructor dashboard.** Do you want to see which students are ready before you
book their test slot? This is probably your highest-value feature after the core app,
but it's v2.

**12. Do you want the road-test items** (backing, straight line, offset, alley dock)
eventually, or is this pre-trip and air brakes only?

**13. Should students be able to submit a run to you for review?** Their audio plus
score card, sent to an instructor.

---

## Content additions worth doing

**14. Defect photos.** The single biggest upgrade available. Half a day at the yard
photographing each part *good and bad* — a cut tyre, a rusted lug nut, a gapped fifth
wheel — turns this from a memorisation app into an actual inspection trainer. Can we
schedule that shoot?

**15. Your own instructor audio.** Recording you or your lead instructor saying each
callout would beat any synthesised voice, and it's your brand. About 64 short takes.

**16. Video.** You've sent one reference video. Do you have footage of *your own*
trucks and instructors we can use? Anything from another school's channel is their
copyright — I'm using it to understand the mechanics, not as content.

---

## Technical

**17. Apple Developer and Google Play accounts** — do you have them, or do I set them
up? ($99/yr and $25 one-time, under the school's business entity.)

**18. What's the oldest phone a student is likely to use?** It sets the minimum
Android version and whether on-device speech recognition is even available.

**19. Do you have a domain for it?** `fenix.school` exists — a subdomain like
`app.fenix.school` would host the web version.

**20. Data retention.** How long do we keep a student's practice audio? My
recommendation: delete after each run unless they explicitly save it.
