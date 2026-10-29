#!/usr/bin/env python3
"""India script markdown -> Gemini TTS job, chunked to <= ~330 words per request (longer takes degrade).
Usage: ttsjob.py script.md job_id [max_words]
Sections: '# HOOK', '# CHAPTER N: ...', '# ENDING'. Chunks break at line boundaries, preferring the end of a skit or a narrator line.
Writes jobs/tts/<job_id>.json and <script dir>/<job_id>_speakers.json (line index -> skit speaker, per chunk).
"""
import json, re, sys, os
DIR = ("Narrate this as a popular, witty long-form history YouTube documentary about India. The Narrator is a deep, warm, confident storyteller: "
       "relaxed and conversational, curious, lightly funny, with a short comic pause before each punchline and before chapter turns. "
       "Chars voices funny cartoon characters (a cheeky time-traveller, city inspectors, brick-makers, engineers, kings, emperors, sultans, merchants, soldiers): "
       "short, punchy, expressive, following the bracketed style tags. Pronounce Indian names and places naturally, the way an Indian speaker would.")
src, jid = sys.argv[1], sys.argv[2]; MAXW = int(sys.argv[3]) if len(sys.argv) > 3 else 330
lines, sec = [], None
for ln in open(src, encoding="utf-8"):
    ln = ln.strip()
    if ln.startswith("# HOOK") or ln.startswith("# ENDING") or re.match(r"# CHAPTER \d+", ln): sec = ln[2:]; continue
    if ln.startswith("[SKIT"): lines.append(("SKIT", None, sec)); continue
    m = re.match(r"^([A-Z][A-Z0-9 .&']*?):\s*(.+)$", ln)
    if sec and m: lines.append((m.group(1), m.group(2).replace("*", ""), sec))
chunks, cur, w = [], [], 0
def wc(t): return len(t.split())
i = 0
while i < len(lines):
    who, txt, sec = lines[i]
    if who == "SKIT":                                  # keep a whole skit together
        j = i + 1
        while j < len(lines) and lines[j][0] not in ("N", "SKIT"): j += 1
        block = [l for l in lines[i + 1:j]]; i = j
    else: block = [lines[i]]; i += 1
    bw = sum(wc(t) for _, t, _ in block)
    if cur and (w + bw > MAXW or (block[0][2] != cur[-1][2] and w > MAXW * .6)): chunks.append(cur); cur, w = [], 0
    cur += block; w += bw
if cur: chunks.append(cur)
items, spk = [], {}
for k, ch in enumerate(chunks, 1):
    name = f"p{k:02d}"
    spk[name] = {str(n): who for n, (who, _, _) in enumerate(ch) if who != "N"}
    items.append({"name": name, "direction": DIR, "speakers": {"Narrator": "Sadaltager", "Chars": "Puck"},
                  "lines": [["Narrator" if who == "N" else "Chars", t] for who, t, _ in ch]})
    print(name, ch[0][2][:28], "->", ch[-1][2][:28], len(ch), "lines", sum(wc(t) for _, t, _ in ch), "words")
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
json.dump({"id": jid, "key": "longform", "models": ["gemini-3.1-flash-tts-preview"], "items": items},
          open(os.path.join(root, "jobs/tts", jid + ".json"), "w"), indent=1, ensure_ascii=False)
json.dump(spk, open(os.path.join(os.path.dirname(os.path.abspath(src)), jid + "_speakers.json"), "w"), indent=1)
