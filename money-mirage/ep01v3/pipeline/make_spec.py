# script_marked.md -> spec.json lines (text, caption chunks with *keywords*, speaker, chapter) + the Gemini TTS job.
# Captions: 2-6 words per chunk, broken at punctuation, one line each (long-form subtitles, not Shorts stacks).
import json, re, os
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'script_marked.md')).read()
secs = re.split(r'^# ', src, flags=re.M)[1:]
lines = []
for ci, s in enumerate(secs):
    title = s.split('\n')[0].strip()
    for l in s.split('\n')[1:]:
        l = l.strip()
        if not l: continue
        who, _, txt = l.partition(': ')
        tag = re.match(r'^\[([^\]]*)\] ', txt); tag = tag.group(1) if tag else None
        txt = re.sub(r'^\[[^\]]*\] ', '', txt)
        lines.append({'ch': ci, 'chapter': title, 'speaker': None if who == 'N' else who.lower(), 'tag': tag, 'marked': txt})

def chunk(marked):
    toks = marked.split(' '); out = []; cur = []; i = 0
    P = lambda w: re.search(r'[.,!?;:]["*\']*$', w) is not None
    while i < len(toks):
        w = toks[i]; cur.append(w); i += 1
        open_key = sum(x.count('*') for x in cur) % 2 == 1
        if open_key: continue
        if P(w) and len(cur) >= 2: out.append(' '.join(cur)); cur = []; continue
        if len(cur) >= 6:
            j = next((k for k in range(i, min(len(toks), i + 3)) if P(toks[k])), None)
            if j is not None and sum(x.count('*') for x in toks[i:j + 1]) % 2 == 0: cur += toks[i:j + 1]; i = j + 1
            out.append(' '.join(cur)); cur = []
    if cur:
        if out and len(cur) == 1: out[-1] += ' ' + cur[0]
        else: out.append(' '.join(cur))
    return out

spec = {'slug': 'mm-ep01-v3', 'lines': [], 'voices': {'goldie': {'semitones': -3, 'formant': 'preserved'}, 'bill': {'semitones': 4, 'formant': 'shifted'}},
        'align': {'offset': 0.3, 'cap': 0.42, 'tempo': 1.0, 'long_before': {}}, 'tail': 3.0}
for i, L in enumerate(lines):
    plain = L['marked'].replace('*', '')
    spec['lines'].append({'o': 0, 'text': plain, 'chunks': chunk(L['marked']), 'ch': L['ch'], 'chapter': L['chapter'], **({'speaker': L['speaker']} if L['speaker'] else {})})
    if L['speaker'] and i > 0 and not lines[i - 1]['speaker']: spec['align']['long_before'][str(i)] = 0.55   # comic beat before a character line
# sanity: chunk words == text words
for L in spec['lines']:
    assert sum(len(c.split(' ')) for c in L['chunks']) == len(L['text'].split()), L
json.dump(spec, open(os.path.join(HERE, 'spec.json'), 'w'), ensure_ascii=False, indent=1)

# TTS: 4 parts (Gemini quality stays steady over ~2.5 min), Narrator Sadaltager, both characters on Chars (Puck), re-pitched later
DIR = ("Narrate this for a premium documentary YouTube channel about money, history and the tricks behind them. The Narrator is a deep, "
       "warm, confident storyteller with a hint of mystery: curious, quietly amused, never slow, never announcer-like. Natural emphasis on dates and "
       "numbers, a short pause before each question, a beat of comic timing before and after each light joke. Energetic and punchy on the opening "
       "lines. Keep the same voice, pace and energy from start to finish. Chars voices two funny cartoon characters (a smug gold bar and a nervous "
       "banknote), short and punchy, performed exactly as described in each bracket.")
parts = [(0, 1), (2, 3), (4, 5), (6, 7)]
items = []
for k, (c0, c1) in enumerate(parts):
    ls = []
    for L, raw in zip(spec['lines'], lines):
        if c0 <= L['ch'] <= c1:
            ls.append(['Chars', f"[{raw['tag']}] {L['text']}" if raw['tag'] else L['text']] if raw['speaker'] else ['Narrator', L['text']])
    items.append({'name': f'part_{k + 1}', 'direction': DIR, 'speakers': {'Narrator': 'Sadaltager', 'Chars': 'Puck'}, 'lines': ls})
json.dump({'id': 'mm3-ep01-sadaltager', 'models': ['gemini-3.1-flash-tts-preview', 'gemini-2.5-flash-preview-tts'], 'items': items},
          open(os.path.join(HERE, 'tts_job.json'), 'w'), ensure_ascii=False, indent=1)
print(len(spec['lines']), 'lines;', sum(len(L['chunks']) for L in spec['lines']), 'caption chunks;', [len(i['lines']) for i in items], 'lines per TTS part')
for L in spec['lines'][:3]: print(L['chunks'])
