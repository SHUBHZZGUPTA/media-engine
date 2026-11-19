import json,glob,collections,statistics as st
S={r['id']:r for r in json.load(open('/home/claude/thumb_study/sample.json'))}
C={}
for f in glob.glob('/home/claude/thumb_study/out/b*.json'):
    for o in json.load(open(f)): C[o['id']]=o
print('coded',len(C),'of',len(S))
G={g:[(S[i],C[i]) for i in C if S.get(i,{}).get('group')==g] for g in ['winner','loser','philippines']}
# core-only winners for a cleaner comparison
G['winner_core']=[(r,c) for r,c in G['winner'] if r['src']=='core']
def pct(rows,f): return round(100*sum(1 for r,c in rows if f(c))/max(len(rows),1))
def mean(rows,k): 
    v=[c[k] for r,c in rows if isinstance(c.get(k),(int,float))]; return round(st.mean(v),1) if v else None
feats={
 'map present':lambda c:c['map_present'],
 'satellite/3d map':lambda c:c['main_visual'] in('satellite_map','3d_map'),
 'flat map':lambda c:c['main_visual']=='flat_map',
 'country solid red/fill':lambda c:c['country_highlight']=='solid_fill',
 'flag fill':lambda c:c['country_highlight']=='flag_fill',
 'flag anywhere':lambda c:c['flag_present'],
 'human face':lambda c:c['face'].startswith('human'),
 'shocked face':lambda c:c['face']=='human_shocked',
 'creature/character':lambda c:c['face']=='creature_or_character',
 'photo main visual':lambda c:c['main_visual'].startswith('photo'),
 'split comparison':lambda c:c['main_visual']=='split_comparison',
 'any arrow':lambda c:c['arrows']>0,
 'circles/rings':lambda c:c['circles_or_rings']>0,
 'callout labels':lambda c:c['callout_labels']>0,
 'yellow box':lambda c:c['highlight_box']=='yellow',
 'any highlight box':lambda c:c['highlight_box']!='none',
 'text huge':lambda c:c['text_size']=='huge',
 'text top/top-left':lambda c:c['text_position'] in('top','top-left'),
 'has number':lambda c:c['has_number'],
 'bold claim':lambda c:c['curiosity_device']=='bold_claim',
 'question':lambda c:c['curiosity_device']=='question',
 'mystery tease':lambda c:c['curiosity_device']=='mystery_tease',
 'number list':lambda c:c['curiosity_device']=='number_list',
 'bright':lambda c:c['brightness']=='bright',
 'dark':lambda c:c['brightness']=='dark',
 'high saturation':lambda c:c['saturation']=='high',
 'no text':lambda c:c['word_count']==0,
 '1-4 words':lambda c:1<=c['word_count']<=4,
 '5+ words':lambda c:c['word_count']>=5,
}
print(f"{'feature':26s}"+''.join(f'{g:>14s}' for g in G))
print(f"{'n':26s}"+''.join(f'{len(v):>14d}' for v in G.values()))
for k,f in feats.items(): print(f'{k:26s}'+''.join(f'{pct(v,f):>13d}%' for v in G.values()))
for k in ['word_count','clutter','small_size_readability','focal_points','arrows','callout_labels']:
    print(f'{k:26s}'+''.join(f'{str(mean(v,k)):>14s}' for v in G.values()))
