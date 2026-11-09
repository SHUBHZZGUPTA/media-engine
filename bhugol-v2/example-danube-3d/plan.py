# Shot plan + beats for the Danube Short (the whole script, to the end card). Merged into dn.json by mkspec.py.
SHOTS = [
 {"scene": "MW", "at": [0, 0, 0]},
 {"scene": "MV", "at": [1, 0, -0.15]},
 {"scene": "MW", "at": [2, 0, -0.15]},
 {"scene": "MV", "at": [4, 0, -0.15]},
 {"scene": "MW", "at": [5, 0, -0.15]},
 {"scene": "MV", "at": [6, 0, -0.15]},
 {"scene": "MI", "at": [7, 0, -0.15], "cut": "whip"},
 {"scene": "XS", "at": [8, 0, -0.15], "cut": "zoom"},
 {"scene": "MI", "at": [11, 0, -0.15]},
 {"scene": "MW", "at": [12, 0, -0.15], "cut": "flash"},
 {"scene": "MV", "at": [13, 0, -0.15]},
 {"scene": "MI", "at": [14, 0, -0.15]},
 {"scene": "MW", "at": [15, 0, -0.15]},
]
Y, R, B, G = "#FFC23A", "#FF3B30", "#4FB3FF", "#5CFF8A"
SINK = {"lon": 8.733, "lat": 47.932}; SPRING = {"lon": 8.857, "lat": 47.843}
BEATS = [
 # L0 hook: title letters, Danube draws across Europe, 4 capital dots, rising punch-ins
 {"kind": "charslam", "at": [0, 0, -0.13]},
 {"kind": "moment", "at": [0, 0, 0.3], "what": "Danube draws across Europe"},
 {"kind": "punch", "scene": "MW", "at": [0, 1, 0.0], "level": 1.15},
 {"kind": "moment", "at": [0, 1, 0.05], "what": "four capital dots pop"},
 {"kind": "punch", "scene": "MW", "at": [0, 2, 0.0], "level": 1.28},
 {"kind": "punch", "scene": "MW", "at": [0, 4, 0.0], "level": 1.4},
 # L1 Black Forest -> Black Sea
 {"kind": "moment", "at": [1, 1, 0.0], "what": "BLACK FOREST label + source dot"},
 {"kind": "moment", "at": [1, 2, 0.0], "what": "camera flies with the river to the BLACK SEA label"},
 # L2 Vienna, 56 km, Bratislava
 {"kind": "card", "scene": "MW", "at": [2, 1, 0.0], "lon": 16.3738, "lat": 48.2082, "flag": "🇦🇹", "name": "VIENNA", "tag": "CAPITAL #1", "dx": 90},
 {"kind": "grow", "at": [2, 2, 0.0], "to": 56, "unit": "KM", "y": 300},
 {"kind": "card", "scene": "MW", "at": [2, 3, 0.0], "lon": 17.1077, "lat": 48.1486, "flag": "🇸🇰", "name": "BRATISLAVA", "tag": "CAPITAL #2", "dx": -160},
 # L3 commute joke
 {"kind": "moment", "at": [3, 1, 0.0], "what": "bus emoji pops"},
 {"kind": "punch", "scene": "MW", "at": [3, 1, 0.1], "level": 1.16},
 # L4 Budapest, Belgrade
 {"kind": "card", "scene": "MV", "at": [4, 0, 0.1], "lon": 19.0402, "lat": 47.4979, "flag": "🇭🇺", "name": "BUDAPEST", "tag": "CAPITAL #3"},
 {"kind": "circle", "scene": "MV", "at": [4, 0, 0.5], "until": [4, 1, 0.45], "q": {"lon": 19.05, "lat": 47.50}, "r": [120, 150], "col": R},
 {"kind": "card", "scene": "MV", "at": [4, 2, 0.7], "lon": 20.4489, "lat": 44.8125, "flag": "🇷🇸", "name": "BELGRADE", "tag": "CAPITAL #4"},
 # L5 four capitals, no river has more
 {"kind": "grow", "at": [5, 0, 0.0], "until": [5, 2, -0.1], "to": 4, "unit": "CAPITALS", "y": 300},
 {"kind": "moment", "at": [5, 1, 0.0], "what": "four capital dots pulse"},
 {"kind": "slam", "at": [5, 3, 0.05], "emo": "trophy"},
 # L6 re-ask: near its start, disappear?
 {"kind": "circle", "scene": "MV", "at": [6, 1, 0.1], "q": SINK, "r": [130, 100], "col": R},
 {"kind": "card", "scene": "MV", "at": [6, 1, 0.0], "lon": 8.733, "lat": 47.932, "flag": "🇩🇪", "name": "GERMANY", "tag": "NEAR THE SOURCE", "dx": 120},
 {"kind": "moment", "at": [6, 3, 0.0], "what": "the river near the source flickers out"},
 # L7 rewind: Immendingen, limestone, cracks
 {"kind": "card", "scene": "MI", "at": [7, 1, 0.05], "lon": 8.733, "lat": 47.932, "flag": "🇩🇪", "name": "IMMENDINGEN", "tag": "DANUBE SINKHOLE"},
 {"kind": "moment", "at": [7, 2, 0.0], "what": "camera drops toward the riverbed"},
 {"kind": "card", "scene": "MI", "at": [7, 2, 0.05], "lon": 8.70, "lat": 47.925, "flag": "🪨", "name": "LIMESTONE", "tag": "FULL OF CRACKS", "dx": -80},
 {"kind": "arrow", "scene": "MI", "at": [7, 3, 0.0], "qf": {"lon": 8.70, "lat": 47.985}, "qt": SINK, "col": Y},
 # L8 leaks into the ground; 1921; 309 days
 {"kind": "moment", "at": [8, 0, 0.1], "what": "cracks appear, water sinks into them"},
 {"kind": "arrow", "scene": "XS", "at": [8, 1, 0.0], "qf": {"lon": 8.733, "lat": 47.932}, "qt": {"u": 0.24, "y": -0.45}, "col": B},
 {"kind": "grow", "at": [8, 2, 0.0], "to": 1921, "from": 1800, "unit": "", "y": 300},
 {"kind": "moment", "at": [8, 3, 0.0], "what": "river downstream of the sink dries up"},
 {"kind": "grow", "at": [8, 4, 0.0], "to": 309, "unit": "DAYS", "y": 300},
 # L9 joke
 {"kind": "punch", "scene": "XS", "at": [9, 1, 0.0], "level": 1.18},
 # L10 1877 salt + dye; waited
 {"kind": "grow", "at": [10, 0, 0.0], "to": 1877, "from": 1800, "unit": "", "y": 300},
 {"kind": "slam", "at": [10, 1, 0.3], "emo": "salt"},
 {"kind": "moment", "at": [10, 1, 0.0], "what": "green dye at the sinkhole"},
 {"kind": "moment", "at": [10, 2, 0.0], "what": "green water runs through the conduit"},
 {"kind": "slam", "at": [10, 3, 0.05], "emo": "timer"},
 # L11 60 hours later, 12 km south, a spring, Lake Constance
 {"kind": "grow", "at": [11, 0, 0.0], "to": 60, "unit": "HOURS", "y": 300},
 {"kind": "card", "scene": "MI", "at": [11, 1, 0.1], "lon": 8.857, "lat": 47.843, "flag": "🇩🇪", "name": "AACH SPRING", "to": 12, "unit": "KM", "tag": "FROM THE SINKHOLE"},
 {"kind": "moment", "at": [11, 2, 0.0], "what": "spring glows, Aach draws"},
 {"kind": "card", "scene": "MI", "at": [11, 3, 0.1], "lon": 9.0, "lat": 47.71, "flag": "🌊", "name": "LAKE CONSTANCE", "tag": "FLOWS INTO THE RHINE", "dx": 60},
 # L12 payoff: Rhine to the North Sea, the wrong sea
 {"kind": "moment", "at": [12, 0, 0.1], "what": "Rhine draws to the North Sea"},
 {"kind": "arrow", "scene": "MW", "at": [12, 1, 0.0], "qf": {"lon": 6.3, "lat": 51.9}, "qt": {"lon": 4.9, "lat": 53.2}, "col": B},
 {"kind": "circle", "scene": "MW", "at": [12, 2, 0.0], "q": {"lon": 4.6, "lat": 53.8}, "r": [190, 130], "col": R},
 {"kind": "punch", "scene": "MW", "at": [12, 2, 0.05], "level": 1.2},
 # L13 1927 court
 {"kind": "moment", "at": [13, 0, 0.05], "what": "scales emoji pops, German flag on the map"},
 {"kind": "flap", "at": [13, 2, 0.0], "text": "1927", "y": 260},
 {"kind": "punch", "scene": "MV", "at": [13, 4, 0.0], "level": 1.18},
 # L14 twist: upper Danube may switch to the Rhine for good
 {"kind": "moment", "at": [14, 1, 0.0], "what": "underground route glows"},
 {"kind": "moment", "at": [14, 2, 0.0], "what": "upper Danube turns blue"},
 {"kind": "card", "scene": "MI", "at": [14, 2, 0.0], "lon": 8.66, "lat": 47.94, "flag": "🔀", "name": "UPPER DANUBE", "tag": "→ RHINE?", "dx": -60},
 {"kind": "arrow", "scene": "MI", "at": [14, 3, 0.0], "qf": SINK, "qt": {"lon": 8.81, "lat": 47.878}, "col": B},
 {"kind": "circle", "scene": "MI", "at": [14, 4, 0.0], "q": SINK, "r": [120, 90], "col": R},
 {"kind": "slam", "at": [14, 4, 0.1], "emo": "swap"},
 # L15 loop line
 {"kind": "moment", "at": [15, 0, 0.0], "what": "capital dots pulse"},
 {"kind": "grow", "at": [15, 1, 0.0], "to": 10, "unit": "COUNTRIES", "y": 300},
 {"kind": "moment", "at": [15, 2, 0.0], "what": "both rivers glow"},
 {"kind": "moment", "at": [15, 3, 0.0], "what": "upper Danube flickers"},
]
