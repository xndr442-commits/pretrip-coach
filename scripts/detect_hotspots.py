#!/usr/bin/env python3
"""Add hotspot coordinates to every curated photo.

BUILD_SPEC #3: the item screen is a photograph with a press-and-hold hotspot on the
part. The original booklet drew orange pointer arrows at the exact contact point on
~20 photos, so we detect those and use the arrow as the hotspot.

Arrows point INWARD at their subject, so the hotspot is the arrow's centroid nudged
toward the image centre. Photos with no arrow get a centred default, flagged
`"hotspot_source": "default_center"` for a human to refine.
"""
import json, os
import numpy as np
from PIL import Image

ROOT = os.path.expanduser("~/Projects/PreTripCoach")
MAN = f"{ROOT}/assets/reference/curated/manifest.json"

def orange_mask(a):
    """Booklet pointer orange ~#F26B21: strong R, mid G, low B."""
    r, g, b = a[..., 0].astype(int), a[..., 1].astype(int), a[..., 2].astype(int)
    return (r > 180) & (g > 70) & (g < 165) & (b < 90) & ((r - b) > 110) & ((r - g) > 55)

def main():
    man = json.load(open(MAN))
    detected = 0
    for m in man["images"]:
        p = os.path.join(ROOT, m["file"])
        im = Image.open(p).convert("RGB")
        W, H = im.size
        a = np.asarray(im)
        mask = orange_mask(a)
        # require a real blob, not a few stray pixels or a whole orange background
        frac = mask.mean()
        # >8% orange means the orange thing IS the subject (e.g. a warning
        # triangle), not a pointer arrow drawn over it.
        if mask.sum() >= 250 and frac < 0.08:
            ys, xs = np.nonzero(mask)
            cx, cy = xs.mean() / W, ys.mean() / H
            # blob radius in normalised units
            br = float(np.sqrt(frac / np.pi))
            # step PAST the arrow tip, along the vector toward the image centre
            vx, vy = 0.5 - cx, 0.5 - cy
            n = (vx * vx + vy * vy) ** 0.5 or 1.0
            step = br * 2.2
            cx, cy = cx + vx / n * step, cy + vy / n * step
            cx, cy = min(max(cx, 0.12), 0.88), min(max(cy, 0.12), 0.88)
            m["hotspot"] = {"x": round(float(cx), 3), "y": round(float(cy), 3), "r": 0.13}
            m["hotspot_source"] = "arrow_detected"
            detected += 1
        else:
            m["hotspot"] = {"x": 0.5, "y": 0.5, "r": 0.20}
            m["hotspot_source"] = "default_center"

    man["hotspot_note"] = (
        "x/y/r are normalised 0-1 of image width/height; r is a fraction of the "
        "smaller dimension. 'arrow_detected' came from the booklet's own pointer "
        "arrow and is reliable. 'default_center' is a placeholder — refine those by "
        "hand before release."
    )
    json.dump(man, open(MAN, "w"), indent=2)
    print(f"arrow-detected hotspots : {detected}")
    print(f"default-centre fallbacks: {len(man['images']) - detected}")
    print("\nDetected from booklet arrows:")
    for m in man["images"]:
        if m["hotspot_source"] == "arrow_detected":
            h = m["hotspot"]
            print(f"  {m['id']:<45s} x={h['x']:.2f} y={h['y']:.2f}")

if __name__ == "__main__":
    main()
