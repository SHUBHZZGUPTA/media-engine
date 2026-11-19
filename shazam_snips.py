import asyncio, glob, json, os, sys, time
from shazamio import Shazam
async def main():
    sh = Shazam(); out = {}
    files = sorted(glob.glob('snips/*.mp3'))
    for i, f in enumerate(files):
        k = os.path.basename(f); t0 = time.time()
        try:
            r = await asyncio.wait_for(sh.recognize(f), timeout=75)
            t = r.get('track') or {}
            out[k] = {'title': t.get('title'), 'artist': t.get('subtitle'), 'url': t.get('url'),
                      'label': next((m.get('text') for s in t.get('sections', []) for m in s.get('metadata', []) if m.get('title') == 'Label'), None)}
        except Exception as e:
            out[k] = {'error': f'{type(e).__name__}: {str(e)[:150]}'}
        print(i, k, out[k], f'{time.time() - t0:.1f}s', flush=True)
        if i % 20 == 0: json.dump(out, open('results.json', 'w'), indent=1)
        await asyncio.sleep(1.0)
    json.dump(out, open('results.json', 'w'), indent=1)
asyncio.run(main())
