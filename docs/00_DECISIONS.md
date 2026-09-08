# Decisions Log

Answered by Alexandre, 2026-09-08. These are implemented in the content — see the
"where it lives" column.

| # | Decision | Chosen | Where it lives |
|---|---|---|---|
| 1 | Jurisdiction | **Both Florida and Massachusetts** | `pretrip.en.json → jurisdictions.us_fl / us_ma` |
| 2 | Commercial scope | **Fenix/Moov first, sell later** — build school-only, keep the data model tenant-ready | `pretrip.en.json → tenancy` |
| 3 | License class | **Class A only** | `pretrip.en.json → vehicle_classes_supported` |
| 4 | Transmission | **Both, student picks** | `airbrakes.en.json → transmissions`, `steps[].variants` |

## What each decision changed

**1 · Both states.** Added a `jurisdictions` block. Each student is assigned one, and
all checklist wording plus any threshold overrides resolve from it. MA is mapped to
§11M (2022-09-09) and marked confirmed. **Florida's checklist reference is a
placeholder and `checklist_confirmed: false`** — I don't have the FL sheet. Send it
and I'll map it properly.

**2 · Tenant-ready but single-org.** `tenancy.mode = "single_org"`. Every run,
progress row and leaderboard entry must carry an `org_id` from day one. That costs
almost nothing now and avoids a data migration when you sell to a third school.
The UI stays single-school — no org switcher, no billing.

**3 · Class A only.** `vehicle_classes_supported` is a list with one entry. The Class B
threshold set is still present in `standards.class_b_straight` and unused, so adding
Class B later is a config change plus hiding the combination and trailer sections —
not a rewrite.

**4 · Both transmissions.** The two brake-hold steps that reference the clutch now
carry `variants.manual` / `variants.automatic` with separate `variant_must` concept
lists. The student picks their test vehicle once; the app renders and grades the
matching variant. Every other step is identical for both.

## Round two — all 16 remaining questions answered 2026-09-08

| # | Question | Answer | Impact |
|---|---|---|---|
| 1 | Static air-leak limit | **Handout: 3 released / 4 applied**, both states | ✅ Resolved. Marked `confirmed: true`. Was the one blocking item. |
| 5 | Content sign-off | **Alexandre** | `review/content_signoff.html` generated — 64 items + 9 phases, print and sign |
| 7 | Pricing | **Free, bundled with tuition** | No payment code, no store commission, no refunds. Big scope saving. |
| 8 | AI budget | **AI grading + live AI instructor** | Needs a server proxy and per-student cost monitoring |
| 9 | Languages | **All three, everywhere** | ES/PT accept-lists authored for all 136 item-specific concepts — offline grading now works in 3 languages |
| 10 | Physical verification | **Full 3D truck, student in the driver's seat** | Major change — see `08_3D_TRUCK.md` |
| 11 | Instructor dashboard | **v2** | Out of v1 scope |
| 12 | Road test items | **Pre-trip + air brakes only** | Scope held |
| 13 | Submit run to instructor | **Not in v1** | No audio upload, no storage, smaller privacy surface |
| 14 | Defect photo shoot | **No — use what we have** | Replaced by 3D defect *rendering*, see `08_3D_TRUCK.md` §4 |
| 15 | Instructor voice-over | **Synthetic for now** | On-device TTS; real recordings later |
| 16 | Truck capture | **Alexandre will shoot a walkaround** | For photogrammetry / model reference |
| 17 | Store accounts | **Doesn't have them** | Apple $99/yr, Google $25 once, under the business entity |
| 18 | Device floor | **Mid-range, 2022+** | Makes low-poly 3D viable at 30fps; photo fallback still required |
| 19 | Web hosting | **app.fenix.school** | Also the Microsoft Store PWA route |
| 20 | Audio retention | **Delete after each run unless saved** | Smallest privacy surface |

### The two that changed the build most

**Q9 — all three languages.** I'd only built the shared defect vocabulary in ES/PT,
covering 48% of concepts. Now all 136 item-specific concepts have Spanish and
Portuguese accept-lists, so the *offline* grader works in all three languages, not
just the AI grader. Validation enforces 100% coverage.

**Q10 — full 3D.** This is a genuine architecture change. I flagged that full 3D is
heavy for old phones; Q18 came back as mid-range 2022+, which makes it viable with a
strict budget. See `08_3D_TRUCK.md` for the constraint set and `09_MODEL_ASSESSMENT.md`
for the two candidate models.

## Still open

1. **The Florida examiner checklist.** MA §11M is mapped and confirmed; the FL
   jurisdiction is a placeholder with `checklist_confirmed: false`. Thresholds are
   settled for both states — only the checklist wording is outstanding.
2. **3D model licensing.** If you may sell this later you need commercial
   redistribution rights on the Volvo model. See `09_MODEL_ASSESSMENT.md`.
3. **A replacement trailer model.** The current one is a single mesh and cannot be
   inspected part by part.
4. **Content sign-off.** `review/content_signoff.html` — print, review, sign.
