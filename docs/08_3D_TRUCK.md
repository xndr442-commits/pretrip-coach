# The 3D Truck

**Decision (Q10):** a full 3D truck the student moves around, with the student in the
driver's seat performing the in-cab work. **Device floor (Q18):** mid-range phones,
roughly 2022 or newer.

That combination is buildable, but only with a deliberate performance budget. This
document is the constraint set.

---

## 1. What "3D" means here, precisely

Not an open-world driving sim. A **station-based inspection environment**:

- The student stands at a **fixed camera station** — driver's seat, front of truck,
  steer axle, driver side, coupling area, trailer side, rear.
- At each station they **look around freely** (drag / gyro) and **tap parts**.
- They **move between stations** by tapping a waypoint, not by walking with a stick.

This is the right shape for three reasons: free-roam locomotion on a phone is
awkward and nauseating, fixed stations let us aggressively cull geometry, and the
real inspection *is* a fixed route around the vehicle. The student is never lost.

### The hybrid that makes it work

| Layer | What it is | Job |
|---|---|---|
| 3D scene | Low-poly truck, station cameras | Where am I, what am I looking at, what's near what |
| **Photo detail view** | The 59 real photographs already curated | What does this part *actually* look like |

Tapping a part in 3D opens the real photograph of it, then the press-and-hold callout
happens there. **The 3D teaches spatial memory; the photo teaches recognition.** This
also means nothing built so far is wasted — the photos, hotspots, concepts and
grading all carry over unchanged.

---

## 2. Engine choice

**react-three-fiber (Three.js) on expo-gl.**

| Option | Verdict |
|---|---|
| **react-three-fiber / Three.js** | **Chosen.** Keeps the single Expo codebase, ships to iOS, Android and web — and the web build is what becomes the Microsoft Store PWA. Comfortably handles a station-based scene at this fidelity. |
| Unity | Better 3D tooling and performance ceiling, but it becomes a second codebase, complicates the web/PWA route, and adds a heavy runtime for what is not an action game. |
| Godot | Free and capable, weakest React/Expo integration story of the three. |

The 3D is a *scene*, not a game engine workload. Three.js is sufficient and keeps the
distribution plan from §11 of BUILD_SPEC intact.

---

## 3. Performance budget — mid-range Android, 2022+

Treat these as hard limits, enforced in CI:

| Budget | Limit |
|---|---|
| Triangles on screen | ≤ 150k |
| Draw calls | ≤ 80 |
| Texture memory | ≤ 120 MB |
| Target frame rate | 30 fps locked (not 60) |
| Initial download | ≤ 60 MB |
| 3D assets total | ≤ 40 MB |
| Time to first interaction | ≤ 4 s on the floor device |

Techniques, all required:

- **glTF/GLB with Draco** mesh compression and **KTX2/Basis** textures. Never ship PNG
  or raw OBJ into the app.
- **Three LODs** per major assembly, switched by station distance.
- **Aggressive per-station culling** — the trailer's far side is never in the frustum
  from the steer axle; do not keep it resident.
- **Baked lighting.** One baked lightmap per station. No realtime shadows, no dynamic
  lights beyond a single directional for orientation.
- **Atlas textures** by zone to keep draw calls down.
- **Stream stations on demand**, don't load the whole vehicle at boot.

### Device tiering

Detect at first launch and pick a tier:

| Tier | Behaviour |
|---|---|
| High | Full geometry, 2K atlases, ambient occlusion |
| Mid *(the floor)* | LOD1 geometry, 1K atlases, no AO |
| Low / failure | **Automatic fallback to photo-only mode** |

The fallback is not optional, even though the floor is 2022+. Some student will show
up with a phone below spec, or a device where GL init fails. **The app must remain
fully usable with the 3D scene disabled** — every mode still works, because the
photos and the grading are independent of the renderer. Ship the fallback in v1.

---

## 4. Defect rendering — this replaces the photo shoot

Q14 was answered "use what we have" — no defect photo shoot. **3D gives us defects
for free, and better.**

A defect becomes a **material or mesh variant** on a part:

| Defect | Implementation |
|---|---|
| Cut / bulged tyre | Swap tyre mesh variant |
| Worn tread | Swap normal + roughness map |
| Rust streak on a lug nut | Decal on the hub atlas |
| Gapped fifth wheel | Translate the apron mesh a few centimetres |
| Frayed air line | Alternate line mesh |
| Cracked lens | Emissive off + crack decal |
| Leaking shock | Decal + a drip particle |

That unlocks the mode this app was missing: **"find the defect."** Spawn a truck with
one to three randomised defects, let the student walk it and call them out. That is
real inspection training rather than recitation, and it is the single strongest
argument for having gone 3D at all.

**Scope note:** defect variants are v1.5, not v1. Build the clean truck and the
inspection flow first. But **author the model with variant swapping in mind from the
start** — parts as separate named nodes, materials not baked into one atlas per
vehicle — because retrofitting that later means rebuilding the model.

---

## 5. Part naming contract

The 3D model is worthless to the app unless its nodes map to content item ids.

**Every inspectable part must be a separate node named exactly `part_<item_id>`** —
`part_lug_nuts`, `part_king_pin`, `part_air_chamber`. Each gets a simplified
collider for tapping; do not raycast against render geometry.

Add to `manifest.json` per item: `node` (the 3D node name) and `station` (which
camera station it is inspected from). Then the validator can assert that all 64 items
resolve to a real node — catching a mismatch at build time instead of when a student
taps a part that does nothing.

Stations, matching the content's `location` field:
`driver_seat` · `front_of_truck` · `steer_axle` · `driver_side` · `behind_cab`
(coupling) · `trailer_side` · `trailer_rear`

---

## 6. Build order for the 3D layer

Do **not** start here. The scoring engine and the photo-based item flow (BUILD_SPEC
steps 1–6) must work first. The 3D is a navigation shell around a product that
already functions without it.

1. Placeholder blocky truck, correct dimensions, all stations, all named nodes.
   Prove the tap → item → callout → grade loop end to end.
2. Performance harness on the floor device. Lock the budget before art exists.
3. Swap in the scanned model, retopologised to budget.
4. Baked lighting, LODs, station streaming.
5. Device tiering and the photo-only fallback.
6. *(v1.5)* Defect variants and "find the defect" mode.

A blocky placeholder that hits 30 fps and correctly wires all 64 parts is worth far
more than a beautiful model that stutters — and it de-risks the whole decision early,
while it is still cheap to change.
