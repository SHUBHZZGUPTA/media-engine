import asyncio, glob, json, os
from shazamio import Shazam
async def main():
    sh = Shazam(); out = {}
    for f in sorted(glob.glob('snips/*.mp3')):
        r = None
        for attempt in range(3):
            try:
                r = await sh.recognize(f); break
            except Exception as e:
                r = {'error': str(e)[:200]}; await asyncio.sleep(5)
        t = (r or {}).get('track') or {}
        out[os.path.basename(f)] = {'title': t.get('title'), 'artist': t.get('subtitle'), 'url': t.get('url'),
                                    'label': next((m.get('text') for s in t.get('sections', []) for m in s.get('metadata', []) if m.get('title') == 'Label'), None),
                                    'error': (r or {}).get('error')}
        print(os.path.basename(f), out[os.path.basename(f)]['title'], '-', out[os.path.basename(f)]['artist'])
        await asyncio.sleep(1.5)
    json.dump(out, open('results.json', 'w'), indent=1)
asyncio.run(main())
