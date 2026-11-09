import json, sys, os
sys.path.insert(0, '.'); from plan import SHOTS, BEATS
en = json.load(open('lines_en.json')); hi = json.load(open('lines_hi.json'))
spec = {'slug': 'danube', 'lines': en['lines'], 'voices': {},
        'align': {'offset': .3, 'cap': .42, 'tempo': 1.05, 'long_before': {'3': .5, '6': .5, '9': .6, '12': .5, '14': .6, '15': .5, '16': .7}},
        'tail': 2.3, 'shots': SHOTS, 'beats': BEATS}
if os.path.exists('en/timing.json'):
    t = json.load(open('en/timing.json'))
    for L, T in zip(spec['lines'], t['lines']): L['o'] = T['start']
    spec['old_end'] = round((t['lines'][-1]['end'] + 2.3) * 30) / 30; print('o set from en/timing.json')
json.dump(spec, open('dn.json', 'w'), ensure_ascii=False, indent=1)
hi['align'] = {'tempo': 1.08}
json.dump(hi, open('dn.hi.json', 'w'), ensure_ascii=False, indent=1)
print('spec ok', len(spec['lines']), 'lines', len(SHOTS), 'shots', len(BEATS), 'beats')
