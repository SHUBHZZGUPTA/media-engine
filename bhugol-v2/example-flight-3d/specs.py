import json
EN = [
 ("From Australia, you fly west to reach Europe.", ["FROM *AUSTRALIA,*", "YOU FLY *WEST*", "TO REACH EUROPE."]),
 ("This plane flew east. Twenty-four hours, non-stop, and set the airliner world record.", ["THIS PLANE|FLEW *EAST.*", "*24 HOURS,* NON-STOP,", "AND SET THE AIRLINER|*WORLD RECORD.*"]),
 ("The short way, past India, is about seventeen thousand kilometres.", ["THE SHORT WAY,", "PAST *INDIA,*", ["IS ABOUT *17,000 KM.*", 5]]),
 ("But this jet crossed the Pacific, America and the Atlantic. Two sunsets, two sunrises.", ["BUT THIS JET CROSSED", "THE *PACIFIC,*", "*AMERICA*", "AND THE *ATLANTIC.*", "*TWO SUNSETS,*", "*TWO SUNRISES.*"]),
 ("So why the long way?", ["SO WHY THE|*LONG WAY?*"]),
 ("Because records count distance. Over twenty-three thousand kilometres, more than halfway round Earth.", ["BECAUSE RECORDS|COUNT *DISTANCE.*", ["OVER *23,000 KM,*", 4], "MORE THAN *HALFWAY*|ROUND EARTH."]),
 ("The record it broke? A Boeing, in two thousand and five. It went the long way too.", ["THE RECORD|IT BROKE?", ["A BOEING,|IN *2005.*", 7], "IT WENT THE|LONG WAY *TOO.*"]),
 ("Controllers even offered it shortcuts. The pilots said no.", ["CONTROLLERS EVEN|OFFERED IT *SHORTCUTS.*", "THE PILOTS|SAID *NO.*"]),
 ("In record books, the wrong way is the right way.", ["IN RECORD BOOKS,", "THE *WRONG WAY*", "IS THE *RIGHT WAY.*"]),
 ("This is Bhoogol.", ["THIS IS *BHUGOL.*"]),
]
HI = [
 ("Australia से Europe जाना हो, तो आप west जाते हैं।", ["*AUSTRALIA* से EUROPE|जाना हो,", "तो आप *WEST*|जाते हैं।"]),
 ("ये plane east गया। twenty-four hours non-stop, और airliner world record बना दिया।", ["ये PLANE *EAST* गया।", "*24 HOURS* NON-STOP,", "और AIRLINER *WORLD RECORD*|बना दिया।"]),
 ("India के पास से short रास्ता, करीब seventeen thousand kilometre है।", ["*INDIA* के पास से", "SHORT रास्ता,", ["करीब *17,000 KM* है।", 5]]),
 ("पर ये jet Pacific, America और Atlantic पार कर गया। दो sunset, दो sunrise।", ["पर ये JET *PACIFIC,*", "*AMERICA* और *ATLANTIC*|पार कर गया।", "दो *SUNSET,*", "दो *SUNRISE।*"]),
 ("तो लंबा रास्ता क्यों?", ["तो लंबा रास्ता|*क्यों?*"]),
 ("क्योंकि record distance गिनता है। twenty-three thousand kilometre से ज़्यादा, आधी धरती से भी लंबा।", ["क्योंकि RECORD|*DISTANCE* गिनता है।", ["*23,000 KM* से ज़्यादा,", 5], "आधी धरती से|भी *लंबा।*"]),
 ("और जो record टूटा? two thousand five का एक Boeing। वो भी लंबे रास्ते गया था।", ["और जो RECORD टूटा?", ["*2005* का एक BOEING।", 6], "वो भी लंबे रास्ते|गया *था।*"]),
 ("Controllers ने तो shortcut तक offer किए। Pilots ने मना कर दिया।", ["CONTROLLERS ने तो|*SHORTCUT* तक OFFER किए।", "PILOTS ने|*मना* कर दिया।"]),
 ("Record की दुनिया में, गलत रास्ता ही सही रास्ता है।", ["RECORD की दुनिया में,", "*गलत* रास्ता ही", "*सही* रास्ता है।"]),
 ("ये है भूगोल।", ["ये है *भूगोल।*"]),
]
for lang, L, tempo in (('en', EN, 1.05), ('hi', HI, 1.08)):
    lines = []
    for text, ch in L:
        chunks = [c if isinstance(c, list) else [c, len(c.replace('|', ' ').split())] for c in ch]
        n = sum(c[1] for c in chunks); assert n == len(text.split()), (lang, text, n, len(text.split()))
        lines.append({'text': text, 'chunks': chunks})
    json.dump({'slug': 'flight', 'lang': lang, 'lines': lines, 'align': {'cap': .38, 'tempo': tempo, 'offset': .3, 'long_before': {'8': .55}}}, open(f'flight-{lang}.base.json', 'w'), ensure_ascii=False, indent=1)
print('ok')
