"""Step 0 for bhugol-geo: our analytics vs the GeoGlobeTales findings -> topic shortlist evidence. Read-only.

Usage: python3 bhugol-v2/research/ggt/rank_topics.py [outputs/ytdeep/<id>/report.json]
       (default: newest outputs/ytdeep/mon-*/report.json; check its age, re-pull if > 24 h old)
Prints:
  1. our baseline per channel (median / top 5 views, likes + comments per 1K views, uploads)
  2. views by country with avg % viewed (where the audience is, and who watches longest)
  3. traffic sources
  4. topic-type table: GeoGlobeTales median x-cohort and 2x+ rate vs OUR median views per type
  5. every GeoGlobeTales Short ranked by x-cohort with a 'maybe done' flag (word overlap with our titles)
Topic types are keyword-tagged: rough, check by eye. Claude still judges audience fit and freshness.
"""
import json, sys, glob, os, re, statistics as st
HERE = os.path.dirname(os.path.abspath(__file__))
FAM = {
 'Record journey': r'walk around|swim|80 days|migration|longest flight|on foot|sail',
 'Name confusion': r'difference|vs northern|called holland|two new yorks|2 portlands|two virginias|greenland is ice|regions|not a country| vs ',
 'Strange border / enclave': r'border|surrounded|inside|recursive|neighbo|baarle|märket|in south america|own president|enclave',
 'Why no X': r"no bridge|don't fly|no bridges|aren.t connected|radars|isn.t covered|can't pass|no road",
 'Shape of the map': r'panhandle|so long|rectangle|got its borders|so small|shape',
 'Extreme place / record': r'middle of nowhere|darien|closest to|loudest|longest|smallest|remote|loneliest|snowiest|highest|haunted|deepest|most dangerous|forbidden|on fire|tallest|biggest',
 'True size': r'bigger than you think|true size|really huge|real size|how huge|so huge|not this small|size of',
 'History deal / conflict': r'bought|war|invade|declared|british|owns|divided|defeat|split into|avoided invasion|fought|history',
 'Invisible line / where people live': r'invisible|line|east of|empty|nobody lives|equator|date line',
 'Present-day news': r'yemen|hotspot|arctic war|panama canal|51st|newest country|hurricane milton|air strike',
}
def fam(t): return [k for k, p in FAM.items() if re.search(p, t, re.I)] or ['Other']
def words(t): return {w for w in re.findall(r'[a-zà-ÿ]{4,}', t.lower())} - {'with','that','this','from','have','your','what','they','into','than','more','most','world','country','countries','there','their','about','why','really','shorts','geography'}

path = sys.argv[1] if len(sys.argv) > 1 else sorted(glob.glob('outputs/ytdeep/mon-*/report.json'))[-1]
R = json.load(open(path)); print('analytics file:', path, '| checked', R.get('checked'))
ours = []
for c in R['channels']:
    V = [v for v in c['videos'] if (v.get('duration_s') or 0) <= 180]
    vw = sorted((v.get('views') or 0) for v in V)
    if not vw: continue
    med = st.median(vw); ours += [(c['title'], v) for v in V]
    lk = sum(v.get('likes') or 0 for v in V); cm = sum(v.get('comments') or 0 for v in V); tv = sum(vw) or 1
    print(f"\n== {c['title']} ({c.get('handle')}) subs {c.get('subscribers')} | Shorts {len(V)} | median {med:.0f} | top5 {vw[::-1][:5]} | likes/1K {1000*lk/tv:.1f} | comments/1K {1000*cm/tv:.2f}")
    A = c.get('audience') or {}
    rows = A.get('country') or []; tot = sum(r['views'] for r in rows) or 1
    print('  country (share, avg % viewed):', ', '.join(f"{r['country']} {100*r['views']/tot:.0f}% ({r.get('averageViewPercentage', 0):.0f})" for r in rows[:8]))
    tr = A.get('traffic') or []; tt = sum(r['views'] for r in tr) or 1
    print('  traffic:', ', '.join(f"{r['insightTrafficSourceType']} {100*r['views']/tt:.0f}%" for r in tr[:6]))
    by = {}
    for v in V:
        for f in fam(v.get('title') or ''): by.setdefault(f, []).append((v.get('views') or 0) / med if med else 0)
    c['_by'] = by

G = json.load(open(os.path.join(HERE, 'invS.json')))
gby = {}
for x in G:
    for f in fam(x['title']): gby.setdefault(f, []).append(x['rel'])
print('\n== Topic types: GeoGlobeTales (x their cohort) vs ours (x our median)')
hdr = ' | '.join(c['title'] for c in R['channels'] if '_by' in c)
print(f"{'type':36} GGT med  2x+   n | ours ({hdr}): median x, n")
for f, r in sorted(gby.items(), key=lambda kv: -st.median(kv[1])):
    o = ' | '.join((f"{st.median(c['_by'][f]):.2f}x n={len(c['_by'][f])}" if f in c['_by'] else '—') for c in R['channels'] if '_by' in c)
    print(f"{f:36} {st.median(r):5.2f} {100*sum(v>=2 for v in r)/len(r):4.0f}% {len(r):3} | {o}")

print('\n== GeoGlobeTales Shorts by x-cohort (remake / re-angle candidates); MAYBE DONE = shares 2+ words with one of our titles')
for x in sorted(G, key=lambda x: -x['rel']):
    w = words(x['title']); hit = max(((len(w & words(v.get('title') or '')), v.get('title')) for _, v in ours), default=(0, ''))
    flag = f"MAYBE DONE: {hit[1][:40]}" if hit[0] >= 2 else ''
    print(f"{x['rel']:5.2f}x {x['views']/1e6:5.1f}M {x['date']} {x['id']} {'/'.join(fam(x['title']))[:28]:28} {x['title'][:60]}  {flag}")
