# Store Submission

## Targets

| Store | Build | Notes |
|---|---|---|
| Apple App Store | Expo → EAS Build → TestFlight → review | Needs a paid Apple Developer account ($99/yr) |
| Google Play | Expo → EAS Build → internal testing → review | $25 one-time |
| Microsoft Store | Expo web → PWA → PWABuilder → MSIX | Free for individuals; no fourth codebase |

## Before you submit anything

**Microphone permission is the review risk.** Both Apple and Google reject vague
purpose strings. Be specific:

> "Pre-Trip Coach uses your microphone so you can practice speaking the CDL
> inspection out loud and receive a score. Audio is processed on your device and is
> not uploaded unless you choose to save a practice run."

And make that statement *true* in the build.

**Apple specifics**
- Privacy manifest (`PrivacyInfo.xcprivacy`) declaring microphone and any analytics.
- Data-collection disclosures in App Store Connect must match the manifest exactly.
- Age rating 4+. There is nothing objectionable here.
- Sign-in with Apple is required only if you offer other third-party sign-in. Ship
  v1 with no account at all and avoid the whole question.

**Google specifics**
- Data safety form; declare microphone, mark audio as not-collected if you keep it
  on device.
- Target the current API level or the upload is rejected.

**Both**
- Real screenshots from the real app. Fabricated store screenshots get rejected and,
  worse, get accounts flagged.
- An account-deletion path is required by both stores if you ever add accounts. One
  more reason to ship v1 without them.

## Educational-claims caution

Do not claim in store copy that the app is state-approved, DMV-endorsed, or that it
guarantees a passing result. Describe it as practice material from Fenix Truck
School. Anything stronger invites both a store rejection and a complaint from a
state agency.

Suggested subtitle: *"Practice the CDL pre-trip inspection out loud, in English,
Spanish or Portuguese."*

## Release sequence

1. Internal build → the school's own instructors. Fix what they say is wrong about
   the content before a single student sees it.
2. TestFlight / Play internal → one cohort of current students, one section only.
3. Watch: where do they abandon a run? Which items does the grader get wrong?
4. Public release once the grader's golden tests hold on real student audio.

Do not release publicly before instructors have signed off on the content — the
whole value of this app is that its callouts are the ones your school teaches.
