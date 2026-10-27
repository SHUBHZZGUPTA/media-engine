#!/usr/bin/env python3
"""Script markdown -> Gemini TTS job (one item per chapter group) + speaker map.
Usage: ttsjob.py script.md job_id "2,3" "4,5" ...   (groups of chapter numbers)
Writes jobs/tts/<job_id>.json and longform/russia/full/<job_id>_speakers.json
"""
import json, re, sys, os
DIR = "Narrate this as a popular, witty long-form history YouTube documentary. The Narrator is a deep, warm, confident storyteller: relaxed and conversational, curious, lightly funny, with a short comic pause before each punchline and before chapter turns. Chars voices funny cartoon characters (a cheeky time-traveller, khans, princes, tsars, servants, nobles, officers, an empress): short, punchy, expressive, following the bracketed style tags."
src, jid, groups = sys.argv[1], sys.argv[2], [[int(x) for x in g.split(",")] for g in sys.argv[3:]]
ch, chap = {}, None
for ln in open(src, encoding="utf-8"):
    ln = ln.strip()
    m = re.match(r"# CHAPTER (\d+)", ln)
    if m: chap = int(m.group(1)); ch[chap] = []; continue
    m = re.match(r"^([A-Z][A-Z .']*?):\s*(.+)$", ln)
    if chap and m:
        ch[chap].append((m.group(1), m.group(2).replace("*", "")))
items, spk = [], {}
for g in groups:
    name = "ch" + "_".join(map(str, g))
    lines = [l for c in g for l in ch[c]]
    spk[name] = {str(i): who for i, (who, _) in enumerate(lines) if who != "N"}
    items.append({"name": name, "direction": DIR, "speakers": {"Narrator": "Sadaltager", "Chars": "Puck"},
                  "lines": [["Narrator" if w == "N" else "Chars", t] for w, t in lines]})
    print(name, len(lines), "lines", sum(len(t.split()) for _, t in lines), "words")
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")
json.dump({"id": jid, "key": "longform", "models": ["gemini-3.1-flash-tts-preview"], "items": items},
          open(os.path.join(root, "jobs/tts", jid + ".json"), "w"), indent=1, ensure_ascii=False)
json.dump(spk, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), jid + "_speakers.json"), "w"), indent=1)
