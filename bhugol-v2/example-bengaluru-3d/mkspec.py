import json
L = [
 ("Almost every lake you see in Bengaluru was built by hand.", ["ALMOST EVERY *LAKE*", "YOU SEE IN|*BENGALURU*", "WAS BUILT|*BY HAND.*"]),
 ("Over 1,100 years. Then the city lost most of them.", ["OVER *1,100 YEARS.*", "THEN THE CITY|LOST *MOST OF THEM.*"]),
 ("So why build lakes at all?", ["SO WHY BUILD|*LAKES* AT ALL?"]),
 ("Look at the map. Bengaluru sits on a ridge, about 920 metres up.", ["LOOK AT THE MAP.", "*BENGALURU* SITS|ON A *RIDGE,*", "ABOUT *920 METRES* UP."]),
 ("No big river flows here. Rivers run downhill. Bengaluru is the hill.", ["NO BIG *RIVER*|FLOWS HERE.", "RIVERS RUN *DOWNHILL.*", "BENGALURU|*IS THE HILL.*"]),
 ("So how do you fill lakes, with no river?", ["SO HOW DO YOU|FILL *LAKES,*", "WITH *NO RIVER?*"]),
 ("Rewind to the 800s.", ["REWIND TO|THE *800s.*"]),
 ("People built earth walls across the valleys, to trap the rain.", ["PEOPLE BUILT|*EARTH WALLS*", "ACROSS THE *VALLEYS,*", "TO TRAP|THE *RAIN.*"]),
 ("Rain fills one lake. It spills into the next. Then the next.", ["RAIN FILLS|*ONE LAKE.*", "IT *SPILLS*|INTO THE NEXT.", "THEN *THE NEXT.*"]),
 ("Wheee! Lake number seven!", ["*WHEEE!*", "LAKE NUMBER|*SEVEN!*"], "drop"),
 ("Canals linked them into six chains, stepping down three valleys.", ["*CANALS* LINKED THEM|INTO *SIX CHAINS,*", "STEPPING DOWN|*THREE VALLEYS.*"]),
 ("In 1537, Kempegowda founded the city, and kept building more.", ["IN *1537,*", "*KEMPEGOWDA*|FOUNDED THE CITY,", "AND KEPT|BUILDING *MORE.*"]),
 ("Then the city grew. And grew. And grew.", ["THEN THE CITY|*GREW.*", "AND *GREW.*", "AND *GREW.*"]),
 ("From 1973 to 2013, about 79% of its water bodies vanished.", ["FROM *1973*|TO *2013,*", "ABOUT *79%*|OF ITS WATER BODIES", "*VANISHED.*"]),
 ("So today, water is pumped about 100 km from the Kaveri, and lifted 300 metres uphill.", ["SO TODAY, WATER|IS *PUMPED*", "ABOUT *100 KM*|FROM THE *KAVERI,*", "AND LIFTED|*300 METRES* UPHILL."]),
 ("The city that built its own lakes now borrows a river.", ["THE CITY THAT BUILT|ITS OWN *LAKES*", "NOW *BORROWS*|A *RIVER.*"]),
 ("And the lost lakes? Many are hiding in plain sight.", ["AND THE|*LOST LAKES?*", "MANY ARE HIDING|IN *PLAIN SIGHT.*"]),
 ("Kanteerava Stadium? Sampangi Lake.", ["KANTEERAVA STADIUM?", "*SAMPANGI LAKE.*"]),
 ("KR Market? Siddikatte Lake.", ["KR MARKET?", "*SIDDIKATTE LAKE.*"]),
 ("Majestic bus stand? Dharmambudhi Lake.", ["MAJESTIC BUS STAND?", "*DHARMAMBUDHI LAKE.*"]),
 ("Technically, I'm parked in a lake.", ["*TECHNICALLY,*", "I'M PARKED|IN A *LAKE.*"], "bus"),
 ("Bengaluru never had a big river. So it made lakes instead.", ["BENGALURU NEVER HAD|A BIG *RIVER.*", "SO IT MADE|*LAKES* INSTEAD."]),
 ("This is BHUGOL. Follow for more Geography Fun Facts.", ["THIS IS *BHUGOL.*", "FOLLOW FOR MORE|GEOGRAPHY FUN FACTS."]),
]
lines = []
for i, x in enumerate(L):
    t, ch = x[0], x[1]; n = len(t.split()); m = sum(len(c.replace('|', ' ').split(' ')) for c in ch)
    assert n == m, (i, n, m, t)
    d = {"o": 0, "text": t, "chunks": ch}
    if len(x) > 2: d["speaker"] = x[2]
    lines.append(d)
S = {"slug": "bengaluru", "lines": lines,
     "voices": {"drop": {"semitones": 4, "formant": "shifted"}, "bus": {"semitones": -3, "formant": "preserved"}},
     "align": {"offset": 0.3, "cap": 0.42, "tempo": 1.05, "long_before": {"9": 0.55, "12": 0.5, "15": 0.7, "16": 0.5, "20": 0.6, "21": 0.6, "22": 0.5}, "line_tempo": {"9": 1.0, "20": 1.0}},
     "tail": 2.3}
json.dump(S, open('bengaluru.base.json', 'w'), ensure_ascii=False, indent=1)
print('ok', sum(len(l['text'].split()) for l in lines), 'words')
