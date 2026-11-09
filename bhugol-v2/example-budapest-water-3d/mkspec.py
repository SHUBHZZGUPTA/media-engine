import json, sys
sys.path.insert(0, '.'); from plan import SHOTS, BEATS
en = json.load(open('lines_en.json')); hi = json.load(open('lines_hi.json'))
spec = {'slug': 'budapest-water', 'lines': en['lines'], 'voices': {},
        'align': {'offset': .3, 'cap': .42, 'tempo': 1.05, 'long_before': {'6': .6, '9': .55, '12': .6, '14': .75, '15': .6, '17': .8}},
        'tail': 2.3, 'shots': SHOTS, 'beats': BEATS}
json.dump(spec, open('bp.json', 'w'), ensure_ascii=False, indent=1)
hi['align'] = {'tempo': 1.08}
json.dump(hi, open('bp.hi.json', 'w'), ensure_ascii=False, indent=1)
print('spec ok', len(spec['lines']), 'lines', len(SHOTS), 'shots', len(BEATS), 'beats')
import os
if os.path.exists('en/timing.json'):
    t = json.load(open('en/timing.json'))
    for L, T in zip(spec['lines'], t['lines']): L['o'] = T['start']
    spec['old_end'] = round((t['lines'][-1]['end'] + 2.3) * 30) / 30
    json.dump(spec, open('bp.json', 'w'), ensure_ascii=False, indent=1); print('o set from en/timing.json')
