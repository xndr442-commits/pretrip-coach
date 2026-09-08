#!/usr/bin/env python3
"""Stage 1 of the asset pipeline: PDF -> page renders + deduped unique photos.

Requires poppler (`brew install poppler`) for pdftoppm/pdfimages.
Run order: extract_assets -> curate_assets -> detect_hotspots
"""
import hashlib, json, os, shutil, subprocess, sys
from PIL import Image, ImageStat

ROOT = os.path.expanduser("~/Desktop/PreTripCoach")
PDF  = f"{ROOT}/source/NEW_MATERIAL_PRE_TRIP.pdf"
PAGES = f"{ROOT}/assets/reference/pages"
RAW   = f"{ROOT}/assets/reference/extracted/raw"
UNIQ  = f"{ROOT}/assets/reference/extracted/unique"

def sh(*a):
    r = subprocess.run(a, capture_output=True, text=True)
    if r.returncode: sys.exit(f"failed: {' '.join(a)}\n{r.stderr}")

def main():
    if not os.path.exists(PDF): sys.exit(f"missing source PDF: {PDF}")
    for d in (PAGES, RAW, UNIQ): os.makedirs(d, exist_ok=True)

    print("rendering pages at 150dpi…")
    sh("pdftoppm", "-r", "150", "-png", PDF, f"{PAGES}/page")
    print(f"  {len(os.listdir(PAGES))} pages")

    print("extracting embedded images…")
    sh("pdfimages", "-png", "-p", PDF, f"{RAW}/img")
    print(f"  {len(os.listdir(RAW))} raw images")

    print("deduping and filtering…")
    seen = {}
    for f in sorted(os.listdir(RAW)):
        if not f.endswith(".png"): continue
        im = Image.open(os.path.join(RAW, f))
        w, h = im.size
        if w < 150 or h < 150:                      # icons, bullets, rules
            continue
        if im.mode in ("L", "1"):                   # flat soft-masks
            if ImageStat.Stat(im.convert("L")).stddev[0] < 12:
                continue
        d = hashlib.md5(im.tobytes()).hexdigest()
        page = int(f.split("-")[1])
        if d in seen:
            seen[d]["pages"].append(page); continue
        shutil.copy(os.path.join(RAW, f), os.path.join(UNIQ, f))
        seen[d] = {"file": f, "w": w, "h": h, "pages": [page]}

    rows = sorted(seen.values(), key=lambda r: (r["pages"][0], r["file"]))
    json.dump(rows, open(f"{UNIQ}/_index.json", "w"), indent=1)
    print(f"  {len(rows)} unique photos -> {UNIQ}")
    print("\nnext: python3 scripts/curate_assets.py")

if __name__ == "__main__":
    main()
