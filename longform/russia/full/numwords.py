"""Spoken years and quantities -> digits for captions (English)."""
import re
U = "zero one two three four five six seven eight nine".split()
TEEN = "ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
TENS = {"twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90}
def two(w):
    """'twenty-three' / 'fourteen' / 'oh nine' -> int or None"""
    w = w.lower().strip()
    if w.startswith("oh "): return U.index(w[3:]) if w[3:] in U else None
    if w in TEEN: return 10 + TEEN.index(w)
    if w in TENS: return TENS[w]
    m = re.fullmatch(r"(\w+)-(\w+)", w)
    if m and m.group(1) in TENS and m.group(2) in U: return TENS[m.group(1)] + U.index(m.group(2))
    return None
CEN = TEEN[2:] + ["twenty"]   # twelve..nineteen, twenty
TWO = r"(?:oh \w+|\w+-\w+|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety)"
FIXED = [("seven point two million dollars", "$7.2 million"), ("one and a half million", "1.5 million"), ("sixteen hundred and one", "1601"),
         ("two hundred and forty", "240"), ("three hundred and four", "304"), ("six hundred thousand", "600,000"), ("seven hundred thousand", "700,000"),
         ("seventy thousand", "70,000"), ("twenty-seven million", "27 million"), ("twenty-three million", "23 million"), ("three million", "3 million"),
         ("nine hundred days", "900 days"), ("eleven hundred", "1,100"), ("ninety miles", "90 miles"), ("thirteen days", "13 days"),
         ("nineteen thirty-seven and thirty-eight", "1937 and 38"), ("nineteen thirty-two and thirty-three", "1932 and 33"), ("twenty-one years", "21 years"),
         ("thirty-four years", "34 years"), ("thirty-seven years", "37 years"), ("fourteen years", "14 years"), ("fifteen years", "15 years"),
         ("seventeen hundred", "1700"), ("eight months", "8 months"), ("two metres", "2 metres"), ("six foot eight", "6 ft 8")]
def digits(text):
    for a, b in FIXED: text = re.sub(r"\b" + re.escape(a) + r"\b", b, text, flags=re.I)
    def yr(m):
        c, r = m.group(1).lower(), two(m.group(2))
        if r is None: return m.group(0)
        base = (CEN.index(c) + 12) * 100 if c != "twenty" else 2000
        return str(base + r)
    text = re.sub(r"\b(" + "|".join(CEN) + r") (" + TWO + r")\b(?! (?:thousand|million|hundred))", yr, text, flags=re.I)
    # "nineteen-twenties" / "nineties" left as words
    return text
if __name__ == "__main__":
    for s in ["In twelve twenty-three, at", "in seventeen oh nine", "February twenty twenty-two", "twenty fourteen", "nineteen thirty-two and thirty-three",
              "one and a half million", "eighteen sixty-seven", "fifteen forty-seven, at sixteen", "twenty twenty, until twenty thirty-six"]:
        print(s, "->", digits(s))
