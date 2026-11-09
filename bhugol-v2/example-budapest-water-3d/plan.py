# Shot plan + beats for the Budapest water Short (the whole script, to the end card). Merged into bp.json by mkspec.py.
SHOTS = [
 {"scene": "MP", "at": [0, 0, 0]},
 {"scene": "XS", "at": [1, 0, -0.15], "cut": "zoom"},
 {"scene": "CV", "at": [2, 0, -0.15]},
 {"scene": "XS", "at": [3, 0, -0.15]},
 {"scene": "CV", "at": [3, 2, -0.15]},
 {"scene": "MP", "at": [4, 0, -0.15]},
 {"scene": "MQ", "at": [5, 0, -0.15], "cut": "whip"},
 {"scene": "CV", "at": [7, 0, -0.15]},
 {"scene": "XS", "at": [8, 0, -0.15]},
 {"scene": "CV", "at": [8, 1, -0.15]},
 {"scene": "XS", "at": [9, 0, -0.15]},
 {"scene": "CV", "at": [10, 0, -0.15], "cut": "zoom"},
 {"scene": "MQ", "at": [11, 2, -0.15]},
 {"scene": "CV", "at": [12, 0, -0.15]},
 {"scene": "MQ", "at": [13, 1, -0.15]},
 {"scene": "XS", "at": [14, 0, -0.15], "cut": "flash"},
 {"scene": "CV", "at": [15, 0, -0.15]},
 {"scene": "XS", "at": [16, 0, 1.4]},
 {"scene": "MP", "at": [16, 3, 0.45], "cut": "zoom"},
]
Y, R, B = "#FFC23A", "#FF3B30", "#4FB3FF"
BEATS = [
 # hook: title letters, the 70 million litres number, rising punch-ins
 {"kind": "charslam", "at": [0, 0, -0.13]},
 {"kind": "grow", "at": [0, 0, 0.0], "until": [0, 2, -0.1], "to": 70, "unit": "MILLION L / DAY", "y": 430},
 {"kind": "punch", "scene": "MP", "at": [0, 1, 0.05], "level": 1.15},
 {"kind": "punch", "scene": "MP", "at": [0, 3, 0.0], "level": 1.28},
 {"kind": "punch", "scene": "MP", "at": [0, 4, 0.0], "level": 1.4},
 # L1 where does it come from: arrow down into the hot deep
 {"kind": "arrow", "scene": "XS", "at": [1, 0, 0.25], "until": [2, 0, -0.25], "qf": {"u": 0.50, "y": 0.18}, "qt": {"u": 0.50, "y": -0.80}, "col": Y},
 # L2 thermometer: +1 C ... / 20 m
 {"kind": "moment", "at": [2, 0, 0.2], "what": "3D thermometer pops in"},
 {"kind": "count", "at": [2, 1, 0.0]},
 {"kind": "count", "at": [2, 2, -0.05]},
 # L3 rain sinks, rises through the fault
 {"kind": "arrow", "scene": "XS", "at": [3, 0, 0.3], "until": [3, 2, -0.25], "qf": {"u": 0.30, "y": 0.34}, "qt": {"u": 0.36, "y": -0.55}, "col": B},
 {"kind": "moment", "at": [3, 1, 0.0], "what": "rain path reaches the hot deep"},
 {"kind": "circle", "scene": "CV", "at": [3, 2, 0.15], "until": [4, 0, -0.25], "q": {"u": 0.665, "y": -0.24}, "r": [120, 260], "col": Y},
 # L4 the 123 card
 {"kind": "card", "scene": "MP", "at": [4, 1, 0.4], "until": [5, 0, -0.2], "flag": "🇭🇺", "name": "BUDAPEST", "to": 123, "unit": "", "tag": "HOT SPRINGS + WELLS"},
 {"kind": "moment", "at": [4, 2, 0.0], "what": "card holds, map push-in"},
 # L5 Romans 14 baths, Ottomans 500 years
 {"kind": "grow", "at": [5, 0, 0.0], "until": [5, 1, -0.1], "to": 14, "unit": "BATHS", "y": 300},
 {"kind": "circle", "scene": "MQ", "at": [5, 0, 0.3], "until": [5, 1, -0.15], "q": {"lon": 19.0494, "lat": 47.5636}, "r": [110, 80], "col": R},
 {"kind": "moment", "at": [5, 1, 0.05], "what": "RUDAS + KIRALY pins"},
 {"kind": "grow", "at": [5, 2, -0.2], "until": [6, 0, -0.1], "to": 500, "unit": "YEARS", "y": 300},
 # L6 joke
 {"kind": "moment", "at": [6, 0, 0.05], "what": "hot-spring emoji"},
 {"kind": "punch", "scene": "MQ", "at": [6, 1, 0.0], "level": 1.18},
 # L7 eating rock: caves start dissolving (CV)
 {"kind": "moment", "at": [7, 1, -0.2], "what": "caves dissolve in the section"},
 # L8 from above / from below
 {"kind": "arrow", "scene": "XS", "at": [8, 0, 0.15], "until": [8, 1, -0.1], "qf": {"u": 0.30, "y": 0.36}, "qt": {"u": 0.33, "y": -0.10}, "col": B},
 {"kind": "arrow", "scene": "CV", "at": [8, 2, -0.05], "until": [9, 0, -0.1], "qf": {"u": 0.645, "y": -0.48}, "qt": {"u": 0.63, "y": -0.14}, "col": R},
 {"kind": "punch", "scene": "CV", "at": [8, 2, 0.0], "level": 1.16},
 # L9 so what's down there
 {"kind": "circle", "scene": "XS", "at": [9, 0, 0.1], "until": [10, 0, -0.25], "q": {"u": 0.63, "y": -0.15}, "r": [150, 150], "col": Y},
 # L10 door, flooded cave, 6 km
 {"kind": "moment", "at": [10, 0, 0.1], "what": "door emoji at the cave entrance"},
 {"kind": "circle", "scene": "CV", "at": [10, 0, 0.25], "until": [10, 1, -0.1], "q": {"lon": 19.0359, "lat": 47.5181}, "r": [95, 95], "col": R},
 {"kind": "moment", "at": [10, 1, 0.0], "what": "passages flood cyan"},
 {"kind": "grow", "at": [10, 2, 0.0], "until": [11, 0, -0.1], "to": 6, "unit": "KM", "y": 300},
 # L11 divers, hill full of houses (map of Rozsadomb)
 {"kind": "slam", "at": [11, 0, 0.05], "emo": "diver"},
 {"kind": "circle", "scene": "MQ", "at": [11, 2, 0.15], "until": [12, 0, -0.25], "q": {"lon": 19.018, "lat": 47.524}, "r": [170, 110], "col": R},
 # L12 joke on CV with the diver light
 {"kind": "moment", "at": [12, 1, 0.0], "what": "torch light passes"},
 # L13 fossil shark teeth; Hungary has no sea... now
 {"kind": "slam", "at": [13, 0, 0.25], "emo": "shark"},
 {"kind": "punch", "scene": "MQ", "at": [13, 2, 0.0], "level": 1.2},
 # L14 payoff (flash hero), L15 twist
 {"kind": "moment", "at": [14, 1, -0.1], "what": "city glows over the reservoir"},
 {"kind": "punch", "scene": "CV", "at": [15, 1, 0.0], "level": 1.18},
 # L16 still dissolving... very very slowly (snail slam)
 {"kind": "circle", "scene": "XS", "at": [16, 0, 0.3], "until": [16, 2, -0.1], "q": {"u": 0.62, "y": -0.16}, "r": [170, 160], "col": Y},
 {"kind": "moment", "at": [16, 1, 0.0], "what": "growing edge pulses"},
 {"kind": "slam", "at": [16, 3, 0.0], "emo": "snail"},
]
