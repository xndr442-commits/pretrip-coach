#!/usr/bin/env python3
"""Generate a printable 64-item content sign-off sheet.

Alexandre reads every callout and confirms it is what Fenix teaches. Nothing ships
to students until this is signed. Output: review/content_signoff.html (print to PDF).
"""
import json, os, html

ROOT = os.path.expanduser("~/Projects/PreTripCoach")
os.makedirs(f"{ROOT}/review", exist_ok=True)
d = json.load(open(f"{ROOT}/content/pretrip.en.json"))
a = json.load(open(f"{ROOT}/content/airbrakes.en.json"))

CSS = """
@page { size: letter; margin: 14mm; }
* { box-sizing: border-box; }
body { font: 11pt/1.45 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;
       color:#111318; margin:0; }
h1 { font-size:20pt; margin:0 0 2mm; }
.sub { color:#555; font-size:9.5pt; margin-bottom:5mm; }
.bar { height:4px; background:#E11B22; margin:0 0 6mm; }
.sec { margin:7mm 0 3mm; padding:2mm 3mm; background:#111318; color:#fff;
       font-weight:700; font-size:11.5pt; border-radius:2px; }
.sec .cat { display:block; font-weight:400; font-size:8.5pt; color:#bbb; margin-top:1mm; }
.af { background:#E11B22; }
.item { border-bottom:1px solid #ddd; padding:2.5mm 0; page-break-inside:avoid; }
.hd { display:flex; align-items:baseline; gap:3mm; }
.n { font-weight:700; min-width:9mm; }
.lb { font-weight:700; }
.flag { font-size:7.5pt; background:#E11B22; color:#fff; padding:0.5mm 1.5mm;
        border-radius:2px; margin-left:2mm; vertical-align:1px; }
.script { margin:1.5mm 0 0 12mm; font-style:italic; color:#222; }
.cx { margin:1.5mm 0 0 12mm; font-size:8.5pt; color:#666; }
.row { margin:2mm 0 0 12mm; font-size:9pt; display:flex; gap:6mm; align-items:center; }
.box { display:inline-block; width:3.6mm; height:3.6mm; border:1.2px solid #111;
       vertical-align:-0.6mm; margin-right:1.5mm; }
.note { flex:1; border-bottom:1px dotted #999; height:4mm; }
.sign { margin-top:10mm; padding-top:4mm; border-top:2px solid #111; font-size:10pt; }
.sign div { margin-top:7mm; }
.line { display:inline-block; border-bottom:1px solid #111; width:70mm; }
"""

# resolve {{template}} vars so the printed sheet shows real numbers, not placeholders
STD = d["standards"][d["default_vehicle_class"]]
VARS = {k: v for k, v in STD.items() if isinstance(v, (int, float, str))}
for k, v in a.get("variables", {}).items():
    if isinstance(v, dict) and d["default_vehicle_class"] in v:
        VARS[k] = v[d["default_vehicle_class"]]

def resolve(t):
    import re
    def sub(m):
        k = m.group(1)
        if k not in VARS:
            raise SystemExit(f"unresolved template var {{{{{k}}}}} — fix the content builder")
        return str(VARS[k])
    return re.sub(r"\{\{(\w+)\}\}", sub, t or "")

def esc(x): return html.escape(resolve(x))

out = [f"<!doctype html><meta charset=utf-8><title>Content Sign-Off</title><style>{CSS}</style>",
       "<h1>Pre-Trip Coach — Content Sign-Off</h1>",
       f"<div class=sub>Fenix Truck School &middot; content version {d['content_version']} &middot; "
       f"{sum(len(s.get('items',[])) for s in d['sections'])} items"
       "<br>Confirm each callout is what this school teaches. Tick <b>OK</b>, or write the correction.<br>"
       "<b>Nothing ships to students until this is signed.</b></div><div class=bar></div>"]

n = 0
for s in d["sections"]:
    af = s.get("auto_fail_section")
    cls = "sec af" if af else "sec"
    suffix = " — AUTOMATIC FAILURE SECTION" if af else ""
    out.append(f"<div class='{cls}'>{esc(s['title'])}{suffix}"
               f"<span class=cat>Official checklist: {esc(s.get('checklist_category','—'))}"
               f" &middot; booklet p.{', '.join(map(str,s.get('book_pages',[])))}</span></div>")
    for it in s.get("items", []):
        n += 1
        req = [c['label'] for c in it['concepts'] if c.get('required', True)]
        out.append(
          "<div class=item><div class=hd>"
          f"<span class=n>{n}.</span><span class=lb>{esc(it['label'])}</span>"
          f"{'<span class=flag>AUTO-FAIL</span>' if it.get('auto_fail') else ''}</div>"
          f"<div class=script>&ldquo;{esc(it['script'])}&rdquo;</div>"
          f"<div class=cx><b>Graded on ({len(req)}):</b> {esc(' &middot; '.join(req))}</div>"
          "<div class=row><span><span class=box></span>OK as written</span>"
          "<span><span class=box></span>Change:</span><span class=note></span></div></div>")

out.append("<div class=sec>Air Brake Test — spoken procedure</div>")
out.append("<div class=sub style='margin:2mm 0 3mm'>Ordered procedure, "
           f"{sum(len(p['steps']) for p in a['phases'])} steps across {len(a['phases'])} phases. "
           "Review phase by phase; note any step that is out of order for this school.</div>")
for ph in a["phases"]:
    out.append(f"<div class=item><div class=hd><span class=n>{ph['order']}.</span>"
               f"<span class=lb>{esc(ph['title'])}</span>"
               f"{'<span class=flag>AUTO-FAIL</span>' if ph.get('auto_fail') else ''}</div>"
               f"<div class=cx><b>Preconditions:</b> {esc(', '.join(ph.get('preconditions',[])))}"
               f" &middot; <b>{len(ph['steps'])} steps</b></div>"
               "<div class=row><span><span class=box></span>OK as written</span>"
               "<span><span class=box></span>Change:</span><span class=note></span></div></div>")

out.append("<div class=sign><b>Sign-off</b> — I confirm the callouts above are what Fenix Truck "
           "School teaches, and that the air-brake thresholds match the current examiner sheet."
           "<div>Name <span class=line></span>&nbsp;&nbsp; Role <span class=line></span></div>"
           "<div>Signature <span class=line></span>&nbsp;&nbsp; Date <span class=line></span></div></div>")

p = f"{ROOT}/review/content_signoff.html"
open(p, "w").write("\n".join(out))
print(f"wrote {p}  ({n} walk-around items + {len(a['phases'])} air-brake phases)")
print("open it in a browser and print to PDF")
