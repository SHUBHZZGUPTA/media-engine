#!/usr/bin/env python3
"""India script markdown -> Gemini TTS job, chunked to <= ~330 words per request (longer takes degrade).
Usage: ttsjob.py script.md job_id [max_words]
Sections: '# HOOK', '# CHAPTER N: ...', '# ENDING'. Takes break only at a chapter start or right after a character line (hidden switch points).
Writes jobs/tts/<job_id>.json and <script dir>/<job_id>_speakers.json (line index -> skit speaker, per chunk).
"""
import json, re, sys, os
DIR = ("Narrate this as a popular, witty long-form history YouTube documentary about India. The Narrator is a deep, warm, confident storyteller: "
       "relaxed and conversational, curious, lightly funny, with a short comic pause before each punchline and before chapter turns. "
       "Chars voices funny cartoon characters (a cheeky time-traveller, city inspectors, brick-makers, engineers, kings, emperors, sultans, merchants, soldiers): "
       "short, punchy, expressive, following the bracketed style tags. Pronounce Indian names and places naturally, the way an Indian speaker would."
       ' VOICE IDENTITY (most important): the Narrator is always the same person: a low, warm baritone documentary host. Keep his voice identity and natural speaking pitch the same from the first line to the last, so it never sounds like a different or younger narrator. Emotion is welcome: show it freely through emphasis, energy, pace, louder and softer moments and dramatic pauses, as a real storyteller would. Never whisper or go breathy.')
src, jid = sys.argv[1], sys.argv[2]; MAXW = int(sys.argv[3]) if len(sys.argv) > 3 else 330
lines, sec = [], None
for ln in open(src, encoding="utf-8"):
    ln = ln.strip()
    if ln.startswith("# HOOK") or ln.startswith("# ENDING") or re.match(r"# CHAPTER \d+", ln): sec = ln[2:]; continue
    if ln.startswith("[SKIT"): lines.append(("SKIT", None, sec)); continue
    m = re.match(r"^([A-Z][A-Z0-9 .&']*?):\s*(.+)$", ln)
    if sec and m: lines.append((m.group(1), m.group(2).replace("*", ""), sec))
# Takes break ONLY at hidden points (BHUGOL rule, Oct 2026): a section start (chapter card) or right after a character
# line / skit (other voices + a scene change cover the narrator's take-to-take voice difference). Within a section the
# break is the hidden point that best balances the take lengths, each <= MAXW words.
def wc(t): return len(t.split())
secs = []
for who, txt, sec in lines:
    if not secs or secs[-1][0] != sec: secs.append((sec, []))
    secs[-1][1].append((who, txt, sec))
chunks = []
for sec, ls in secs:
    ls = [l for l in ls if l[0] != "SKIT"]
    def split(ls):
        tot = sum(wc(t) for _, t, _ in ls)
        if tot <= MAXW: return [ls]
        cand = [k for k in range(1, len(ls)) if ls[k - 1][0] != "N" and ls[k][0] == "N"]      # after a character line, before narration
        cand = [k for k in cand if sum(wc(t) for _, t, _ in ls[:k]) <= MAXW] or cand
        if not cand: raise SystemExit(f"{sec}: no hidden break point (add a skit or traveller line) - section is {tot} words")
        k = min(cand, key=lambda k: abs(sum(wc(t) for _, t, _ in ls[:k]) - tot / 2) + (1e4 if sum(wc(t) for _, t, _ in ls[:k]) > MAXW else 0))
        return split(ls[:k]) + split(ls[k:])
    chunks += split(ls)
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
