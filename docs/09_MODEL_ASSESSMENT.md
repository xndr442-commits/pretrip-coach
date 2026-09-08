# 3D Model Assessment

Two candidate models supplied 2026-09-08. Measured directly from the files, not
eyeballed.

---

## What was measured

### Volvo VNL 2025 — `volvo-vnl-2025/source/vnl mtd.blend`

| | |
|---|---|
| Format | Blender 3.06 `.blend`, 80 MB (104 MB with textures) |
| Mesh datablocks | 106 |
| Vertices | 502,108 |
| Polygons | 480,555 → **~961,000 triangles** |
| Named objects | ~138 |
| Materials | 156 |
| Textures | 17 files, 1K–2K, ~31 MB raw PNG |

### Semi-trailer — `semi-trailer-freestanding/`

| | |
|---|---|
| Format | FBX 7200 binary (+ `.3ds`, `.max`), 136 KB |
| Objects | **One**, named "trailer freestanding" |
| Polygons | ~3,000–4,000 |
| Textures | 2 × TGA, 2.6 MB |

---

## Verdict

**The Volvo is a good start. The trailer is not usable. Neither is sufficient
as-is — but the gap is smaller than it looks, for a reason worth understanding.**

### ✅ What the Volvo gives you

- **Parts are separate objects, not one welded mesh.** This is the single most
  important property and it's the one thing that can't be fixed cheaply. 106 meshes
  across ~138 named objects.
- **It has a cab interior** — seat, sleeper, console, buttons, windshield
  (`asiento msa`, `cama vnl`, `camarote`, `consola 01`, `botones`, `PARA BRISAS`).
  That's the driver's-seat station, which is where the auto-fail air brake test happens.
- **Some inspection parts already exist**: `5ta rueda` (fifth wheel),
  `deposito de gasolina` (fuel tank), `axle diferential`, `rines`/`base rim`,
  `lllantas` (tyres), `acople aire` (air coupling), `escalera` (steps),
  `freno de parqueo`, a reflector material.
- **Texture sizes are sane.** 1K–2K compresses to roughly 8–12 MB in KTX2/Basis,
  comfortably inside the 40 MB asset budget.

### ⚠️ Problems, in order of cost to fix

**1. It's ~6.4× over the triangle budget.**
961k triangles against a 150k on-screen budget. Not fatal — station-based culling
means you never render the whole truck at once, and LODs handle the rest. But it
needs a decimation and LOD pass to roughly 250–300k total. Half a day to a day of
work for someone who knows Blender.

**2. The inspection-critical parts are mostly missing.**
This is the real finding. I searched the object names for every suspension, brake and
steering term in both English and Spanish. **Not present:** brake chamber, brake drum,
shoes/linings, slack adjuster, leaf springs, spring mounts, U-bolts, shock absorber,
steering gear box, pitman arm, drag link, tie rod, control arms, king pin, locking
jaws, glad hands, air lines, battery box, DEF tank, landing gear.

That is expected — this is a *visualisation* model, built to look right in a render.
Nobody renders a brake chamber. But those parts are roughly **25 of the 64 things a
pre-trip inspects.**

**3. Naming is ad-hoc Spanish.**
`5ta rueda`, `deposito de gasolina001`, `drr bs001`, `apol puetas`. The app needs
`part_<item_id>` nodes (BUILD_SPEC §5 of the 3D doc). This is a mapping table, not a
rebuild — roughly half a day.

**4. The trailer is a prop, not an inspectable object.**
One single mesh, ~3.5k polys, no separate wheels, lights, landing gear, DOT tape,
king pin or apron. Seven of the 64 items live on the trailer and none of them can be
tapped on this model. **Replace it.**

---

## The reframe that saves most of the cost

The missing parts matter **much less than they appear**, because of the hybrid design
already specced in `08_3D_TRUCK.md`:

> **The 3D scene teaches *where*. The real photograph teaches *what*.**

A student taps a location on the truck; the app opens the actual photo of that part
and grades the spoken callout there. So a missing brake chamber does **not** require a
photoreal brake chamber to be modelled. It requires a **simple low-poly proxy at the
correct location**, named `part_air_chamber`, that is tappable.

A box or a rough cylinder in the right place, correctly named, is enough for v1.
The 59 real photographs — of your actual trucks — do the teaching, and they are more
accurate than any model would be.

That turns "model 25 missing components in detail" (expensive, weeks) into "place 25
named proxy volumes" (a day or two). Detail can be added later, part by part, without
touching the app.

**One exception:** if you want the *"find the defect"* mode from `08_3D_TRUCK.md` §4,
those specific parts do need real geometry, because the student has to *see* the
defect in 3D. That's v1.5 and it can be done a few parts at a time.

---

## Recommendation

1. **Keep the Volvo VNL** as the tractor. Decimate to ~250–300k triangles, build LODs.
2. **Replace the trailer** with one that has separate objects — at minimum: landing
   gear, wheels, mud flaps, each light cluster, DOT tape strips, king pin, apron.
3. **Rename objects** to the `part_<item_id>` contract; add proxy volumes for the ~25
   missing inspection parts at correct locations.
4. **Keep the photo detail layer.** It is what makes the missing geometry survivable,
   and it means students study the truck they'll actually test on.
5. Convert to **glTF/GLB with Draco + KTX2**. Never ship `.blend` or raw PNG.

### ⚠️ Before any of this — check the licence

Where did these come from? A `.blend` with Spanish object names and a `Copilot_…png`
texture suggests a marketplace or free-model site. You answered earlier that you may
**sell this to other schools later**, which means you need **commercial redistribution
rights**, not just personal use. A model licensed CC-BY-NC or "personal use only"
cannot ship in a product you sell — and it's far cheaper to find that out now than
after the app is built.

Send me the source page or licence file and I'll tell you whether it's clear.
