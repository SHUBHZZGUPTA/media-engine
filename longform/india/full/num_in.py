"""Spoken numbers -> digits for the India subtitles ("eleven ninety-one" -> 1191, "a hundred and seventy million" -> 170 million).
Numbers below ten stay as words ("one place", "two princes"). Ordinals stay as words."""
import re
U = {w: i for i, w in enumerate("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen "
                                  "eighteen nineteen".split())}
T = {w: 10 * i for i, w in enumerate("_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()) if w != "_"}
SC = {"hundred": 100, "thousand": 1000}
BIG = ("million", "billion")
TEENC = "eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen"
TENS = "twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety"
UNITS = "one|two|three|four|five|six|seven|eight|nine"
TWO = rf"(?:(?:{TENS})(?:-(?:{UNITS}))?|ten|{TEENC})"          # 10..99 spoken

def _two(s):
    s = s.lower()
    if "-" in s: a, b = s.split("-"); return T[a] + U[b]
    return T.get(s, U.get(s))

def digits(text):
    # 1850s
    text = re.sub(rf"\b({TEENC})[- ]({TENS[:]})\b(?=s)", lambda m: str(U[m.group(1).lower()] * 100 + T[m.group(2).lower().rstrip('s')]), text, flags=re.I)
    text = re.sub(rf"\b({TEENC})[- ](twenties|thirties|forties|fifties|sixties|seventies|eighties|nineties)\b",
                  lambda m: f"{U[m.group(1).lower()] * 100 + T[m.group(2).lower()[:-3] + 'y']}s", text, flags=re.I)
    # years: "eleven ninety-one", "twelve oh six", "sixteen hundred"
    text = re.sub(rf"\b({TEENC}) ({TWO})\b(?! (?:hundred|thousand|million))", lambda m: str(U[m.group(1).lower()] * 100 + _two(m.group(2))), text, flags=re.I)
    text = re.sub(rf"\b({TEENC}) oh ({UNITS})\b", lambda m: str(U[m.group(1).lower()] * 100 + U[m.group(2).lower()]), text, flags=re.I)
    text = re.sub(rf"\b({TEENC}) hundred\b(?! and| (?:{UNITS}|{TENS}))", lambda m: str(U[m.group(1).lower()] * 100), text, flags=re.I)
    # "two thousand fourteen" (years 2000-2099)
    text = re.sub(rf"\btwo thousand (?:and )?({TWO}|{UNITS})\b", lambda m: str(2000 + (_two(m.group(1)) if _two(m.group(1)) is not None else 0)), text, flags=re.I)
    # "three twenty-six BCE"
    text = re.sub(rf"\b({UNITS}) ({TWO}) (BCE|CE)\b", lambda m: f"{U[m.group(1).lower()] * 100 + _two(m.group(2))} {m.group(3)}", text, flags=re.I)
    # "three point one four one six"
    text = re.sub(rf"\b({UNITS}) point((?: (?:{UNITS}|zero))+)\b",
                  lambda m: f"{U[m.group(1).lower()]}." + "".join(str(U[w]) for w in m.group(2).lower().split()), text, flags=re.I)
    # "two and a half million"
    text = re.sub(rf"\b({UNITS}) and a half (million|billion)\b", lambda m: f"{U[m.group(1).lower()]}.5 {m.group(2)}", text, flags=re.I)
    # general cardinals
    W = rf"(?:{TENS}|{TEENC}|ten|{UNITS}|zero)(?:-(?:{UNITS}))?"
    pat = rf"\b(?:a |{W} )?(?:(?:{W}|hundred|thousand)(?: and | |-))*(?:{W}|hundred|thousand)\b"
    def conv(m):
        s = m.group(0); toks = re.split(r"[ -]", s.lower()); total, cur, n = 0, 0, 0
        for t in toks:
            if t == "and": continue
            if t == "a": cur = 1; continue
            if t in U: cur += U[t]; n += 1
            elif t in T: cur += T[t]; n += 1
            elif t == "hundred": cur = max(cur, 1) * 100; n += 1
            elif t == "thousand": total += max(cur, 1) * 1000; cur = 0; n += 1
            else: return s
        v = total + cur
        if v < 10 or (n == 1 and v < 10): return s
        out = f"{v:,}"
        return out if not s[0].isupper() or not s[0].isalpha() else out
    text = re.sub(pat, conv, text, flags=re.I)
    return text

if __name__ == "__main__":
    for s in ["In three twenty-six BCE, he", "In eleven ninety-one, at", "twelve oh six", "In nineteen forty-seven", "two thousand fourteen",
              "In the eighteen-fifties", "a hundred and seventy million", "two and a half million", "forty-seven tonnes", "three point one four one six",
              "On the last day of sixteen hundred,", "five hundred and sixty", "three twenty-one BCE", "two sixty-one BCE", "six hundred BCE",
              "three hundred twenty CE", "the fifteenth of August, nineteen forty-seven", "two thousand twenty-three", "three hundred and seventy-nine",
              "one place on Earth", "two princes", "twenty thousand workers", "a hundred and fifty years later", "about two hundred thousand",
              "nineteen hundred BCE", "for more than three thousand years", "twenty-nine", "By nineteen fifty, India", "four hundred million",
              "Day four hundred.", "thirty-two", "eight years", "in twenty-four days"]:
        print(f"{s:50s} -> {digits(s)}")
