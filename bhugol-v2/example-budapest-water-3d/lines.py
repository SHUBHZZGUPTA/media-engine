# Source of truth for the Budapest hot-water Short (EN + HI). Builds bp.json / bp.hi.json / TTS jobs.
# Each entry: (EN text, EN chunks, HI text, HI chunks, HI tts text or None = same as HI text)
L = [
 ("70 million litres of hot water rise under Budapest every day. And you'd never guess what it's doing down there.",
  ["*70 MILLION LITRES*", "OF *HOT WATER*|RISE UNDER *BUDAPEST*", "EVERY DAY.", "AND YOU'D NEVER GUESS", "WHAT IT'S DOING|*DOWN THERE.*"],
  "Budapest के नीचे हर दिन 70 million litres गर्म पानी ऊपर आता है। और वो नीचे क्या कर रहा है, आप सोच भी नहीं सकते।",
  ["*Budapest* के नीचे", "हर दिन *70 million litres*", "*गर्म पानी* ऊपर आता है।", "और वो नीचे|क्या कर रहा है,", "आप *सोच भी नहीं सकते।*"],
  "Budapest के नीचे हर दिन seventy million litres गर्म पानी ऊपर आता है। और वो नीचे क्या कर रहा है, आप सोच भी नहीं सकते।"),
 ("So where does all that hot water come from?",
  ["SO WHERE DOES|ALL THAT HOT WATER", "*COME FROM?*"],
  "तो इतना गर्म पानी आता कहाँ से है?",
  ["तो इतना गर्म पानी", "*आता कहाँ से है?*"], None),
 ("Here, Earth's crust is thin. It heats up about one degree every 20 metres down.",
  ["HERE, EARTH'S CRUST|IS *THIN.*", "IT HEATS UP ABOUT|*ONE DEGREE*", "EVERY *20 METRES* DOWN."],
  "यहाँ धरती की परत पतली है। नीचे करीब हर 20 metres पर एक degree गर्मी बढ़ती है।",
  ["यहाँ धरती की परत|*पतली* है।", "नीचे करीब हर|*20 metres* पर", "*एक degree*|गर्मी बढ़ती है।"],
  "यहाँ धरती की परत पतली है। नीचे करीब हर twenty metres पर एक degree गर्मी बढ़ती है।"),
 ("Rain sinks deep into the Buda Hills, heats up, and rises back through a fault line.",
  ["*RAIN* SINKS DEEP|INTO THE *BUDA HILLS,*", "HEATS UP,", "AND RISES BACK|THROUGH A *FAULT LINE.*"],
  "बारिश Buda Hills में गहराई तक जाती है, गर्म होती है, और एक fault line से वापस ऊपर आती है।",
  ["*बारिश* Buda Hills में|गहराई तक जाती है,", "गर्म होती है,", "और एक *fault line* से|वापस ऊपर आती है।"], None),
 ("Result? 123 hot springs and wells. But that's not the strange part.",
  ["RESULT?", "*123* HOT SPRINGS|AND WELLS.", "BUT THAT'S NOT|THE *STRANGE PART.*"],
  "नतीजा? 123 गर्म झरने और कुएँ। पर असली अजीब बात ये नहीं है।",
  ["नतीजा?", "*123* गर्म झरने|और कुएँ।", "पर असली *अजीब बात*|ये नहीं है।"],
  "नतीजा? one hundred twenty-three गर्म झरने और कुएँ। पर असली अजीब बात ये नहीं है।"),
 ("The Romans built 14 baths here. The Ottomans added more, still open nearly 500 years later.",
  ["THE *ROMANS* BUILT|*14* BATHS HERE.", "THE *OTTOMANS* ADDED MORE,", "STILL OPEN NEARLY|*500 YEARS* LATER."],
  "Romans ने यहाँ 14 baths बनाए। Ottomans ने और बनाए, जो करीब 500 साल बाद भी खुले हैं।",
  ["*Romans* ने यहाँ|*14 baths* बनाए।", "*Ottomans* ने और बनाए,", "जो करीब *500 साल* बाद|भी खुले हैं।"],
  "Romans ने यहाँ fourteen baths बनाए। Ottomans ने और बनाए, जो करीब five hundred साल बाद भी खुले हैं।"),
 ("Some regulars look like they never got out.",
  ["SOME REGULARS|LOOK LIKE THEY", "*NEVER GOT OUT.*"],
  "कुछ लोग तो जैसे कभी बाहर ही नहीं निकले।",
  ["कुछ लोग तो जैसे", "कभी *बाहर ही नहीं निकले।*"], None),
 ("But the water wasn't just warming people. It was eating rock.",
  ["BUT THE WATER WASN'T|JUST WARMING PEOPLE.", "IT WAS *EATING ROCK.*"],
  "पर ये पानी सिर्फ़ लोगों को गर्म नहीं कर रहा था। ये पत्थर खा रहा था।",
  ["पर ये पानी सिर्फ़|लोगों को गर्म नहीं कर रहा था।", "ये *पत्थर खा रहा था।*"], None),
 ("Most caves are dug by rain from above. These were dug by hot water... from below.",
  ["MOST CAVES ARE DUG|BY RAIN *FROM ABOVE.*", "THESE WERE DUG|BY HOT WATER...", "*FROM BELOW.*"],
  "ज़्यादातर गुफाएँ बारिश ऊपर से बनाती है। ये गुफाएँ गर्म पानी ने... नीचे से बनाईं।",
  ["ज़्यादातर गुफाएँ बारिश|*ऊपर से* बनाती है।", "ये गुफाएँ|गर्म पानी ने...", "*नीचे से* बनाईं।"], None),
 ("So what's down there now?",
  ["SO WHAT'S DOWN THERE|*NOW?*"],
  "तो अब नीचे क्या है?",
  ["तो अब नीचे|*क्या है?*"], None),
 ("Behind a metal door near a busy road: a flooded cave, about six kilometres long.",
  ["BEHIND A *METAL DOOR*|NEAR A BUSY ROAD:", "A *FLOODED CAVE,*", "ABOUT *SIX KILOMETRES* LONG."],
  "एक busy सड़क के पास, metal के दरवाज़े के पीछे: पानी से भरी गुफा, करीब 6 kilometres लंबी।",
  ["एक busy सड़क के पास,|*metal के दरवाज़े* के पीछे:", "*पानी से भरी गुफा,*", "करीब *6 kilometres* लंबी।"],
  "एक busy सड़क के पास, metal के दरवाज़े के पीछे: पानी से भरी गुफा, करीब six kilometres लंबी।"),
 ("Divers swim through it, in warm water, under a hill full of houses.",
  ["*DIVERS* SWIM THROUGH IT,", "IN WARM WATER,", "UNDER A HILL|*FULL OF HOUSES.*"],
  "Divers इसमें तैरते हैं, गर्म पानी में, घरों से भरी पहाड़ी के नीचे।",
  ["*Divers* इसमें तैरते हैं,", "गर्म पानी में,", "*घरों से भरी पहाड़ी*|के नीचे।"], None),
 ("No traffic down there. Best commute in Budapest.",
  ["NO TRAFFIC|DOWN THERE.", "*BEST COMMUTE*|IN BUDAPEST."],
  "नीचे कोई traffic नहीं। Budapest का सबसे अच्छा रास्ता।",
  ["नीचे कोई *traffic* नहीं।", "Budapest का|*सबसे अच्छा रास्ता।*"], None),
 ("Down there: fossil shark teeth. In Hungary, which has no sea... now.",
  ["DOWN THERE:|*FOSSIL SHARK TEETH.*", "IN *HUNGARY,*|WHICH HAS NO SEA...", "*NOW.*"],
  "वहाँ नीचे: shark के fossil दाँत। Hungary में, जहाँ समुद्र ही नहीं है... अब।",
  ["वहाँ नीचे:|*shark के fossil दाँत।*", "*Hungary* में, जहाँ|समुद्र ही नहीं है...", "*अब।*"], None),
 ("Budapest doesn't just have hot springs. It's sitting on one.",
  ["BUDAPEST DOESN'T JUST|HAVE HOT SPRINGS.", "IT'S *SITTING ON ONE.*"],
  "Budapest में सिर्फ़ गर्म झरने नहीं हैं। Budapest ख़ुद एक झरने पर बैठा है।",
  ["Budapest में सिर्फ़|गर्म झरने नहीं हैं।", "Budapest ख़ुद|*एक झरने पर बैठा है।*"], None),
 ("And the twist? That cave is still growing.",
  ["AND THE *TWIST?*", "THAT CAVE IS|*STILL GROWING.*"],
  "और twist? वो गुफा अब भी बढ़ रही है।",
  ["और *twist?*", "वो गुफा|*अब भी बढ़ रही है।*"], None),
 ("Right now, hot water is still dissolving the rock. Very... very... slowly.",
  ["RIGHT NOW, HOT WATER|IS STILL *DISSOLVING*|THE ROCK.", "VERY...", "VERY...", "*SLOWLY.*"],
  "अभी भी, गर्म पानी नीचे पत्थर घोल रहा है। बहुत... बहुत... धीरे।",
  ["अभी भी, गर्म पानी|नीचे पत्थर *घोल* रहा है।", "बहुत...", "बहुत...", "*धीरे।*"], None),
 ("This is Bhoogol. Follow for more Geography Fun Facts.",
  ["THIS IS *BHUGOL.*", "FOLLOW FOR MORE|GEOGRAPHY FUN FACTS."],
  "ये है भूगोल। ऐसे ही मज़ेदार जियोग्राफी फैक्ट्स के लिए फॉलो करें।",
  ["ये है *भूगोल।*", "ऐसे ही मज़ेदार जियोग्राफी|फैक्ट्स के लिए फॉलो करें।"], None),
]

# Spoken TTS spellings (EN). Captions keep the real spelling.
TTS_EN = {17: "This is Bhoogol. Follow for more Geography Fun Facts."}

DIR_EN = ("Narrate this as a popular geography YouTube Shorts channel. The Narrator is a deep, warm, confident storyteller: "
          "brisk and curious, with natural emphasis, a short comic pause before each punchline (\"never got out\", "
          "\"Best commute in Budapest\", \"now\"), a dramatic hush on \"from below\", and a slow, deadpan delivery of "
          "\"Very... very... slowly.\"")
DIR_HI = ("Narrate in natural spoken Hindi like an Indian geography explainer channel; numbers and English words in English. "
          "The Narrator is a deep, warm, confident storyteller: brisk and curious, a short comic pause before each punchline, "
          "a dramatic hush on \"नीचे से\", and a slow, deadpan \"बहुत... बहुत... धीरे।\"")

if __name__ == "__main__":
    import json
    for i, l in enumerate(L):
        assert len(l[1]) == len(l[3]), (i, len(l[1]), len(l[3]))
    en_lines = [{"o": 0, "text": l[0], "chunks": l[1]} for l in L]
    hi_lines = [{"text": l[2], "chunks": l[3]} for l in L]
    hi_tts = " ".join((l[4] or l[2]) for l in L)
    json.dump({"slug": "budapest-water", "lines": en_lines}, open("lines_en.json", "w"), ensure_ascii=False, indent=1)
    json.dump({"lines": hi_lines, "titles": [], "i18n": {}, "align": {"tempo": 1.08}, "tts": hi_tts},
              open("lines_hi.json", "w"), ensure_ascii=False, indent=1)
    models = ["gemini-2.5-flash-preview-tts", "gemini-3.1-flash-tts-preview"]
    for lang, d, lines in (("en", DIR_EN, [TTS_EN.get(i, l[0]) for i, l in enumerate(L)]),
                           ("hi", DIR_HI, [(l[4] or l[2]) for l in L])):
        job = {"id": f"bpwater-{lang}", "models": models, "items": [{"name": "narration", "direction": d,
               "speakers": {"Narrator": "Sadaltager"}, "lines": [["Narrator", t] for t in lines]}]}
        json.dump(job, open(f"/home/claude/media-engine/jobs/tts/bpwater-{lang}.json", "w"), ensure_ascii=False, indent=1)
    w = sum(len(l[0].split()) for l in L)
    print("lines", len(L), "EN words", w)
