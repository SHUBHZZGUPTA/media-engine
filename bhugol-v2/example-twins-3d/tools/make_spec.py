# Writes twins.base.json (EN) and twins-hi.base.json (HI): line text = the caption chunks joined, so tokens always match.
import json
EN = [
 ["I BET *$100*", "YOU DIDN'T KNOW|THERE ARE SOME COUNTRIES", "THAT LOOK|*COMPLETELY DIFFERENT,*", "BUT ARE ALMOST|EXACTLY THE *SAME SIZE!*"],
 ["LET'S START WITH|*NUMBER FIVE:*", "*NEPAL* AND *BANGLADESH.*"],
 ["THEY ARE ONLY|*22 KM* APART,", "BUT ONE TOUCHES|THE *SKY*", "WITH *MOUNT EVEREST,*", "WHILE THE OTHER|TOUCHES THE *OCEAN*", "WITH ITS *RIVERS!*"],
 ["*NUMBER FOUR* IS", "*GUINEA* AND THE|*UNITED KINGDOM.*"],
 ["YOU WON'T|BELIEVE IT.", "ONCE THE *BIGGEST*|*EMPIRE* IN THE WORLD,", "IT NOW HAS AN AREA", "AS SMALL AS *GUINEA.*"],
 ["*SO SAD.*"],
 ["*NUMBER THREE* IS", "*CHILE* AND *ZAMBIA.*"],
 ["IF YOU PULL *ZAMBIA*", "LIKE *CHEWING GUM,*", "THEN YOU WOULD GET|ANOTHER *CHILE*", "OF THE *SAME SIZE.*"],
 ["*NUMBER TWO* IS", "*ITALY* AND THE|*PHILIPPINES.*"],
 ["ONE LOOKS|LIKE A *BOOT,*", "WHILE THE OTHER LOOKS|LIKE A *SITTING MAN.*"],
 ["BUT PUT THEM|*TOGETHER,*", "AND THEY FORM A|*COMPLETE HUMAN BODY.*"],
 ["AND *NUMBER ONE...*", "IS *MALAYSIA*|AND *VIETNAM!*"],
 ["BOTH ARE IN|*SOUTHEAST ASIA,*", "HAVE LONG *COASTLINES,*", "AND ARE ALMOST|THE *SAME SIZE.*"],
 ["I THINK THEY WERE|*MADE FOR EACH OTHER.*"],
 ["WANT TO GO|*DOUBLE OR NOTHING?*", "*BECAUSE...*"]]
HI = [
 ["मैं *$100* की|शर्त लगाता हूँ,", "आपको नहीं पता था कि|कुछ कंट्रीज़", "दिखने में *बिल्कुल अलग* हैं,", "पर साइज़ में|लगभग *एक जैसी* हैं!"],
 ["शुरू करते हैं|*नंबर फाइव* से:", "*नेपाल* और *बांग्लादेश।*"],
 ["दोनों बस *22 km*|दूर हैं,", "पर एक *माउंट एवरेस्ट* से", "*आसमान* छूता है,", "और दूसरा अपनी|*नदियों* से", "*समंदर!*"],
 ["*नंबर फोर:*", "*गिनी* और|*यूनाइटेड किंगडम।*"],
 ["*यकीन नहीं होगा।*", "कभी दुनिया का|*सबसे बड़ा* एम्पायर,", "आज उसका एरिया", "बस *गिनी* जितना है।"],
 ["*कितना दुखद।*"],
 ["*नंबर थ्री:*", "*चिली* और *ज़ाम्बिया।*"],
 ["*ज़ाम्बिया* को", "*च्युइंग गम* की तरह|खींचो,", "तो उतनी ही बड़ी|एक और *चिली*", "*बन जाएगी।*"],
 ["*नंबर टू:*", "*इटली* और|*फिलीपींस।*"],
 ["एक *जूते* जैसा|दिखता है,", "और दूसरा|*बैठे हुए आदमी* जैसा।"],
 ["पर दोनों को|*जोड़ दो,*", "तो *पूरा इंसान*|बन जाता है।"],
 ["और *नंबर वन* है...", "*मलेशिया* और|*वियतनाम!*"],
 ["दोनों *साउथईस्ट एशिया*|में हैं,", "दोनों के लंबे|*कोस्टलाइन्स* हैं,", "और साइज़|*लगभग बराबर।*"],
 ["लगता है, ये *एक-दूसरे*|*के लिए ही बने* हैं।"],
 ["*डबल ऑर नथिंग* करें?", "*क्योंकि...*"]]
assert [len(x) for x in EN] == [len(x) for x in HI]
def txt(ch): return ' '.join(' '.join(c.replace('|', ' ').replace('*', '').split()) for c in ch)
def lines(L, lang):
    out = []
    for i, ch in enumerate(L):
        t = txt(ch); t = t if lang == 'hi' else t[0] + t[1:].lower()
        d = {'o': 0, 'text': t, 'chunks': ch}
        if i == 5: d['speaker'] = 'uk'
        out.append(d)
    return out
base = {'voices': {'uk': {'semitones': 3, 'formant': 'preserved'}}, 'tail': .35,
        'align': {'offset': .25, 'cap': .42, 'tempo': 1.06, 'long_before': {'1': .45, '3': .45, '5': .4, '6': .45, '8': .45, '11': .5, '13': .35}, 'line_tempo': {'5': 1.0, '13': 1.0}}}
en = dict(base, slug='twins', lines=lines(EN, 'en'))
hi = dict(base, slug='twins-hi', lines=lines(HI, 'hi')); hi['align'] = dict(base['align'], tempo=1.08); hi['tts'] = ' '.join(l['text'] for l in hi['lines'])
json.dump(en, open('/home/claude/work/twins/twins.base.json', 'w'), ensure_ascii=False, indent=1)
json.dump(hi, open('/home/claude/work/twins/twins-hi.base.json', 'w'), ensure_ascii=False, indent=1)
for a, b in zip(en['lines'], hi['lines']): print(len(a['text'].split()), len(b['text'].split()), a['text'][:60])
