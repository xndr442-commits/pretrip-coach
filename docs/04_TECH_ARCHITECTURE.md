# Technical Architecture

## Stack

**React Native + Expo, TypeScript.** One codebase → iOS, Android, and web.

This is the recommendation because of the distribution requirement: App Store,
Play Store, and Microsoft Store from one repo. Expo's web build, shipped as an
installable PWA, satisfies the Microsoft Store without a fourth native target.

| Concern | Choice | Why |
|---|---|---|
| Navigation | Expo Router | File-based, works on web |
| State | Zustand | Small, no boilerplate, easy to persist |
| Local DB | expo-sqlite | Review queue and run history need real queries |
| STT | expo-speech-recognition (on-device) | Free, private, works with no signal |
| TTS | expo-speech, optional cloud voice | On-device is instant and offline |
| AI | Server-side proxy, never a key in the client | Cost control + key safety |
| Analytics | PostHog or similar, opt-in | Need to see where students drop off |

## The voice pipeline — the part that decides whether this works

```
mic → on-device STT → live transcript on screen
                    → student confirms or re-records
                    → grader (AI online / keyword offline)
                    → score + feedback
                    → review queue update
```

Three rules:

1. **On-device STT first.** Cloud STT per minute of speech, times a hundred callouts,
   times a class, is a real bill — and it fails exactly when a student is practicing
   in a yard with no signal. Cloud STT is an opt-in upgrade for noisy environments.

2. **Always offer typing.** Accented English is recognised less accurately, and this
   app's users are overwhelmingly ESL speakers. A student who can't get the mic to
   understand them will quit. A typed answer scores identically and says so.

3. **Show the transcript before grading.** Nothing destroys trust faster than being
   marked wrong for something you said correctly and the mic misheard. Let them see
   it and re-record.

## Offline

All content JSON and all 59 images ship **in the bundle**. Everything works in
airplane mode except AI grading and the AI instructor, both of which degrade to the
offline keyword grader with a visible banner.

Run results queue locally and sync when connectivity returns. Offline-graded runs are
flagged and re-graded server-side on sync.

## Data model

```
items          id, section_id, payload (from content JSON)
attempts       id, item_id, ts, transcript, score, hit[], missed[],
               grader ('ai'|'offline'), lang, audio_path?
review_queue   item_id, due_at, interval_days, ease, streak
runs           id, mode, started_at, finished_at, score, passed,
               auto_fail_item_id?
progress       item_id, state ('new'|'learned'|'mastered'), clean_runs, last_clean_at
```

Content is read-only and versioned by `content_version`. On a content update, migrate
progress by item `id` — never by index.

## Internationalisation

- `study_language` and `test_language` are **separate settings**. A student studies in
  Portuguese and tests in English, because the examiner speaks English. This is the
  single most-requested behaviour from this school's students and it must be
  first-class, not an afterthought.
- STT locale follows whichever language the student is currently speaking in.
- Content falls back: `pt` → `en` if a key is missing, and logs the gap.
- Numbers, units and psi values are never translated — "132 psi" stays "132 psi".

## Privacy

Audio is the sensitive asset here.

- Transcribe on device by default. Audio never leaves the phone unless the student
  explicitly saves a run for review.
- Explicit, revocable consent screen before the first recording. Plain language, in
  the student's own language.
- Auto-delete audio after a run unless saved. Hard cap on retention.
- No account needed to practice. Sign-in only to sync across devices.
- Under no circumstances ship an AI provider key in the client.

## Testing

- Content validation runs in CI (`scripts/validate_content.py`) — a malformed content
  file must never reach a build.
- Grader golden tests: a fixture set of real transcripts (including messy, accented,
  code-switched ones) with expected hit/miss sets. Run against both graders.
- The offline grader must never score *higher* than the AI grader on the same
  transcript; assert this.
