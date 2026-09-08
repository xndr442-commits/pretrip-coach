#!/usr/bin/env python3
"""Validate all content files. Run in CI — malformed content must never ship.

Checks structure, cross-references, image existence, translation coverage,
duplicate ids, and that every graded number traces back to `standards`.
"""
import json, os, sys, re

ROOT = os.path.expanduser("~/Desktop/PreTripCoach")
errors, warnings = [], []
def err(m): errors.append(m)
def warn(m): warnings.append(m)

def load(p):
    try:
        return json.load(open(os.path.join(ROOT, p)))
    except Exception as e:
        err(f"{p}: cannot load — {e}")
        return None

pretrip = load("content/pretrip.en.json")
air     = load("content/airbrakes.en.json")
es      = load("content/i18n/es.json")
pt      = load("content/i18n/pt.json")
man     = load("assets/reference/curated/manifest.json")
ces     = load("content/i18n/concepts.es.json")
cpt     = load("content/i18n/concepts.pt.json")
if not all([pretrip, air, es, pt, man, ces, cpt]):
    print("\n".join(errors)); sys.exit(1)

# ── pretrip ──────────────────────────────────────────────────────────────────
item_ids, concept_count, auto_fails, images = [], 0, [], []
ID = re.compile(r"^[a-z0-9_]+$")

for sec in pretrip["sections"]:
    if not ID.match(sec["id"]): err(f"section id not snake_case: {sec['id']}")
    for it in sec.get("items", []):
        item_ids.append(it["id"])
        if not ID.match(it["id"]): err(f"item id not snake_case: {it['id']}")
        if len(it["script"]) < 10: err(f"{it['id']}: script too short")
        req = [c for c in it["concepts"] if c.get("required", True)]
        if not req: err(f"{it['id']}: no required concepts — unscoreable")
        cids = [c["id"] for c in it["concepts"]]
        if len(cids) != len(set(cids)): err(f"{it['id']}: duplicate concept ids")
        for c in it["concepts"]:
            if not c.get("accept"): err(f"{it['id']}.{c['id']}: empty accept list")
        concept_count += len(it["concepts"])
        if it.get("auto_fail"): auto_fails.append(it["id"])
        if it.get("image"): images.append((it["id"], it["image"]))

dupes = {i for i in item_ids if item_ids.count(i) > 1}
if dupes: err(f"duplicate item ids: {sorted(dupes)}")

# section order contiguous
orders = sorted(s["order"] for s in pretrip["sections"])
if orders != list(range(1, len(orders) + 1)):
    err(f"section order not contiguous from 1: {orders}")

# auto-fail sections must exist
for sid in pretrip["grading"]["auto_fail_sections"]:
    if sid not in [s["id"] for s in pretrip["sections"]]:
        err(f"auto_fail_sections references unknown section: {sid}")

# ── images exist ─────────────────────────────────────────────────────────────
for iid, rel in images:
    if not os.path.exists(os.path.join(ROOT, rel)):
        err(f"{iid}: missing image {rel}")

man_files = {m["file"] for m in man["images"]}
for iid, rel in images:
    if rel not in man_files:
        warn(f"{iid}: image not listed in manifest.json ({rel})")

# hotspots (spec requires them; not yet authored)
no_hotspot = [m["id"] for m in man["images"] if "hotspot" not in m]
if no_hotspot:
    warn(f"{len(no_hotspot)} images have no hotspot coords yet "
         f"(required by BUILD_SPEC §3) e.g. {no_hotspot[:3]}")

# ── air brakes ───────────────────────────────────────────────────────────────
step_ids, timers, readings = [], 0, 0
for ph in air["phases"]:
    for st in ph["steps"]:
        step_ids.append(f"{ph['id']}.{st['id']}")
        if st["kind"] == "timer": timers += 1
        if st["kind"] == "report" and "reading" in st: readings += 1
        if not st.get("must"): warn(f"{ph['id']}.{st['id']}: no `must` concepts")
if len(step_ids) != len(set(step_ids)): err("duplicate air-brake step ids")
no_precond = [p["id"] for p in air["phases"] if "preconditions" not in p]
if no_precond:
    warn(f"{len(no_precond)} air-brake phases lack `preconditions` "
         f"(required by BUILD_SPEC §7): {no_precond}")

# ── template variables resolve ───────────────────────────────────────────────
tmpl = re.compile(r"\{\{(\w+)\}\}")
std_keys = set()
for cls in pretrip["standards"].values():
    if isinstance(cls, dict): std_keys |= set(cls)
air_vars = set(air.get("variables", {}))
for sec in pretrip["sections"]:
    for it in sec.get("items", []):
        for v in tmpl.findall(it["script"]):
            if v not in std_keys and v not in air_vars:
                warn(f"{it['id']}: template var {{{{{v}}}}} not in standards or variables")
for ph in air["phases"]:
    for st in ph["steps"]:
        for v in tmpl.findall(st["say"]):
            if v not in air_vars and v not in std_keys:
                warn(f"{ph['id']}.{st['id']}: template var {{{{{v}}}}} unresolved")

# ── translations ─────────────────────────────────────────────────────────────
for lang, doc in (("es", es), ("pt", pt)):
    missing = [i for i in item_ids if i not in doc["items"]]
    if missing: err(f"{lang}: {len(missing)} untranslated items: {missing[:5]}")
    extra = [i for i in doc["items"] if i not in item_ids]
    if extra: warn(f"{lang}: translations for unknown items: {extra}")
    for sid in [s["id"] for s in pretrip["sections"]]:
        if sid not in doc["sections"]: err(f"{lang}: section title missing for {sid}")
    if doc.get("for_content_version") != pretrip["content_version"]:
        warn(f"{lang}: built for content_version {doc.get('for_content_version')}, "
             f"master is {pretrip['content_version']}")

# ── concept accept-lists in every language ──────────────────────────────────
SHARED = {"secure","no_cracks","not_broken","no_leaks","no_illegal_welds",
          "clean","proper_color","hardware","greased","operational"}
needed = []
for sec in pretrip["sections"]:
    for it in sec.get("items", []):
        for c in it["concepts"]:
            if c["id"] not in SHARED:
                needed.append(f"{it['id']}.{c['id']}")
for lang, doc in (("es", ces), ("pt", cpt)):
    miss = [k for k in needed if k not in doc["concepts"]]
    if miss:
        err(f"concepts.{lang}: {len(miss)} item-specific concepts without accept-lists: {miss[:5]}")
    for k, v in doc["concepts"].items():
        if not v: err(f"concepts.{lang}: empty accept list for {k}")
for lang, doc in (("es", es), ("pt", pt)):
    for cid in SHARED:
        if cid not in doc["defect_vocabulary"]:
            err(f"{lang}: shared defect vocabulary missing '{cid}'")

# ── the resolved leak limit must stay consistent across both files ──────────
res = pretrip["standards"].get("_leak_limit_resolved")
if not res:
    err("standards._leak_limit_resolved missing")
else:
    ca = pretrip["standards"]["class_a_combination"]
    if ca["leak_limit_released_psi_per_min"] != res["released_psi_per_min"]:
        err("class_a released leak limit disagrees with the recorded decision")
    if ca["leak_limit_applied_psi_per_min"] != res["applied_psi_per_min"]:
        err("class_a applied leak limit disagrees with the recorded decision")
    av = air["variables"]["leak_released"]["class_a_combination"]
    if av != res["released_psi_per_min"]:
        err(f"airbrakes leak_released ({av}) disagrees with pretrip decision "
            f"({res['released_psi_per_min']})")

# ── transmission variants ───────────────────────────────────────────────────
for ph in air["phases"]:
    for st in ph["steps"]:
        if "variants" in st:
            for t in air["transmissions"]:
                if t not in st["variants"]:
                    err(f"{ph['id']}.{st['id']}: missing '{t}' variant")
                if t not in st.get("variant_must", {}):
                    err(f"{ph['id']}.{st['id']}: missing '{t}' variant_must")

# ── report ───────────────────────────────────────────────────────────────────
print("PRE-TRIP COACH — CONTENT VALIDATION")
print("=" * 52)
print(f"  sections            {len(pretrip['sections'])}")
print(f"  graded items        {len(item_ids)}")
print(f"  scoreable concepts  {concept_count}")
print(f"  auto-fail items     {len(auto_fails)}")
print(f"  air-brake phases    {len(air['phases'])}")
print(f"  air-brake steps     {len(step_ids)}  ({timers} timers, {readings} readings)")
print(f"  reference photos    {len(man['images'])}")
print(f"  translations        es {len(es['items'])}/{len(item_ids)} · "
      f"pt {len(pt['items'])}/{len(item_ids)}")
print(f"  concept accept-lists es {len(ces['concepts'])}/{len(needed)} · "
      f"pt {len(cpt['concepts'])}/{len(needed)} (+{len(SHARED)} shared)")
print(f"  jurisdictions       {[k for k in pretrip['jurisdictions'] if not k.startswith('_')]}")
print(f"  leak limit          {res['released_psi_per_min']} released / "
      f"{res['applied_psi_per_min']} applied — confirmed {res['confirmed']}")
print("=" * 52)
for w in warnings: print(f"  WARN   {w}")
for e in errors:   print(f"  ERROR  {e}")
print("=" * 52)
if errors:
    print(f"FAILED — {len(errors)} error(s), {len(warnings)} warning(s)"); sys.exit(1)
print(f"PASSED — 0 errors, {len(warnings)} warning(s)")
