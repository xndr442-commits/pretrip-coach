#!/usr/bin/env python3
"""Reference implementation of the OFFLINE concept grader, in all three languages.

Exists so the builder does not have to invent and iterate on the matching
algorithm -- the expensive part of Phase 1. Deliberately simple, dependency-free,
and portable to TypeScript / C# / C++ in an afternoon.

  1. normalise -- lowercase, strip accents/punctuation, drop filler words
  2. expand    -- accept phrases = item's own list + shared defect vocabulary
                  + per-language item-specific list
  3. match     -- HIT if an accept phrase appears as a contiguous token run, or
                  if all its content tokens fall inside a short window (so
                  "secure and tight" matches "tight and secure")
  4. polarity  -- "no cracks" is NOT satisfied by the bare word "cracks"

Run:  python3 scripts/reference_grader.py
"""
import json, os, re, sys, unicodedata

ROOT = os.path.expanduser("~/Projects/PreTripCoach")

FILLER = {
 "en": {"um","uh","like","so","okay","ok","well","and","the","a","an","is","are",
        "my","i","it","that","this","of","to","them","they","there","just","also","on"},
 "es": {"eh","este","pues","o","sea","y","el","la","los","las","un","una","es",
        "esta","estan","mi","mis","que","de","lo","yo","en","se"},
 "pt": {"eh","tipo","entao","e","o","a","os","as","um","uma","esta","estao",
        "meu","minha","que","de","em","se"},
}
NEGATORS = {"no","not","without","never","none","nao","sem","nem","sin","ni"}


def strip_accents(s):
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn")

def normalise(text):
    t = strip_accents(text.lower())
    t = re.sub(r"[^a-z0-9/\s]", " ", t)
    return re.sub(r"\s+", " ", t).strip()

def tokens(text, lang="en"):
    out = []
    for w in normalise(text).split():
        if w in NEGATORS:
            out.append(w)
        elif w not in FILLER.get(lang, set()):
            out.append(w)
    return out

def stem(w):
    for suf in ("mente","cion","coes","ndo","adas","ados","ada","ado","ing","ed","es","as","os","s"):
        if len(w) > 4 and w.endswith(suf):
            return w[:-len(suf)]
    return w

def stems(text, lang="en"):
    return [stem(w) for w in tokens(text, lang)]

def phrase_hits(phrase, said, lang):
    p = [w for w in (stem(x) for x in tokens(phrase, lang)) if w]
    if not p:
        return False
    n = len(p)
    if n == 1:
        return p[0] in said
    for i in range(len(said) - n + 1):          # contiguous
        if said[i:i+n] == p:
            return True
    window = n + 4                              # order-independent, nearby
    for i in range(max(1, len(said) - window + 1)):
        if set(p) <= set(said[i:i+window]):
            return True
    return False

def polarity_ok(accept_phrase, said, lang):
    ap = [stem(w) for w in tokens(accept_phrase, lang)]
    if not any(w in NEGATORS for w in ap):
        return True                              # not a negative concept
    content = [w for w in ap if w not in NEGATORS]
    if not content:
        return True
    for i, w in enumerate(said):
        if w in content and any(t in NEGATORS for t in said[max(0, i-4):i+1]):
            return True
    return False


class Grader:
    def __init__(self, root=ROOT):
        self.items = {}
        for s in json.load(open(f"{root}/content/pretrip.en.json"))["sections"]:
            for it in s.get("items", []):
                self.items[it["id"]] = it
        self.vocab, self.specific = {}, {}
        for lang in ("es", "pt"):
            self.vocab[lang] = json.load(open(f"{root}/content/i18n/{lang}.json"))["defect_vocabulary"]
            self.specific[lang] = json.load(open(f"{root}/content/i18n/concepts.{lang}.json"))["concepts"]

    def accept_phrases(self, item_id, c, lang):
        out = list(c["accept"]) + [c["label"]]
        if lang in ("es", "pt"):
            out += self.vocab[lang].get(c["id"], [])
            out += self.specific[lang].get(f"{item_id}.{c['id']}", [])
        return out

    def grade(self, item_id, transcript, lang="en"):
        item = self.items[item_id]
        said = stems(transcript, lang)
        hit, missed = [], []
        for c in item["concepts"]:
            if not c.get("required", True):
                continue
            ok = any(phrase_hits(ph, said, lang) and polarity_ok(ph, said, lang)
                     for ph in self.accept_phrases(item_id, c, lang))
            (hit if ok else missed).append(c["id"])
        total = len(hit) + len(missed)
        return {"hit": hit, "missed": missed,
                "score": round(len(hit)/total, 2) if total else 0.0,
                "pips": f"{len(hit)}/{total}"}


def main():
    g = Grader()
    tests = json.load(open(f"{ROOT}/content/grader_tests.json"))["tests"]
    fails = 0
    print(f"{'':5}{'item':22} {'lang':4} {'got':6} {'want':6} transcript")
    print("-" * 94)
    for i, t in enumerate(tests, 1):
        r = g.grade(t["item"], t["transcript"], t["lang"])
        want, got = set(t["expect_hit"]), set(r["hit"])
        ok = want == got
        fails += 0 if ok else 1
        nreq = len(want) + len(t["expect_missed"])
        print(f"{'ok  ' if ok else 'FAIL'} {t['item']:22} {t['lang']:4} "
              f"{r['pips']:6} {len(want)}/{nreq:<4} {t['transcript'][:42]}")
        if not ok:
            print(f"        want {sorted(want)}")
            print(f"        got  {sorted(got)}")
    print("-" * 94)
    print(f"{len(tests)-fails}/{len(tests)} passed")
    sys.exit(1 if fails else 0)

if __name__ == "__main__":
    main()
