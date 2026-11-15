import json
# (display chunks EN, tts chunks EN, display chunks HI, tts chunks HI)
L = [
 (["What if *Spain*", "and *Portugal*", "became one country... *again?*"], ["What if Spain", "and Portugal", "became one country... again?"],
  ["अगर *Spain*", "और *Portugal*", "फिर से *एक देश* बन जाएं?"], ["अगर Spain", "और Portugal", "फिर से एक देश बन जाएं?"]),
 (["Yes, *again.*", "They've *already*", "done it once."], ["Yes, again.", "They've already", "done it once."],
  ["हाँ, *फिर से।*", "क्योंकि ये *पहले भी*", "हो चुका है।"], ["हाँ, फिर से।", "क्योंकि ये पहले भी", "हो चुका है।"]),
 (["In *1580,*", "Portugal's royal family", "ran out of *heirs.*"], ["In fifteen eighty,", "Portugal's royal family", "ran out of heirs."],
  ["*1580* में,", "Portugal के राजघराने में", "कोई *वारिस* नहीं बचा।"], ["Fifteen eighty में,", "Portugal के राजघराने में", "कोई वारिस नहीं बचा।"]),
 (["So Spain's king", "took the *crown...*", "for *sixty years.*"], ["So Spain's king", "took the crown...", "for sixty years."],
  ["तो Spain के राजा ने", "*ताज* ले लिया...", "पूरे *sixty* साल के लिए।"], ["तो Spain के राजा ने", "ताज ले लिया...", "पूरे sixty साल के लिए।"]),
 (["So what would", "this country *get today?*"], ["So what would", "this country get today?"],
  ["तो आज ये देश", "*कैसा* होगा?"], ["तो आज ये देश", "कैसा होगा?"]),
 (["About *61 million* people...", "*more* than *Italy.*"], ["About sixty-one million people...", "more than Italy."],
  ["करीब *61 million* लोग...", "*Italy* से भी ज़्यादा।"], ["करीब sixty-one million लोग...", "Italy से भी ज़्यादा।"]),
 (["Two languages", "spoken by over", "*800 million* people."], ["Two languages", "spoken by over", "eight hundred million people."],
  ["दो भाषाएं,", "जो *800 million* से ज़्यादा", "लोग बोलते हैं।"], ["दो भाषाएं,", "जो eight hundred million से ज़्यादा", "लोग बोलते हैं।"]),
 (["And a *Nobel*-winning writer", "already picked its name:", "*Iberia.*"], ["And a Nobel-winning writer", "already picked its name:", "Iberia."],
  ["और एक *Nobel* विजेता ने", "इसका नाम भी रख दिया था:", "*Iberia.*"], ["और एक Nobel विजेता ने", "इसका नाम भी रख दिया था:", "Iberia."]),
 (["So why did", "Portugal *walk away?*"], ["So why did", "Portugal walk away?"],
  ["तो Portugal", "*अलग* क्यों हुआ?"], ["तो Portugal", "अलग क्यों हुआ?"]),
 (["Spain kept *dragging*", "Portugal into", "its *wars.*"], ["Spain kept dragging", "Portugal into", "its wars."],
  ["Spain उसे *बार-बार*", "अपनी", "*जंगों* में घसीटता रहा।"], ["Spain उसे बार-बार", "अपनी", "जंगों में घसीटता रहा।"]),
 (["So on *December 1st, 1640,*", "Portugal took", "its *crown back.*"], ["So on December first, sixteen forty,", "Portugal took", "its crown back."],
  ["तो *1 December 1640* को,", "Portugal ने अपना", "*ताज वापस* ले लिया।"], ["तो first December sixteen forty को,", "Portugal ने अपना", "ताज वापस ले लिया।"]),
 (["And it *still* gets", "a *day off* for that."], ["And it still gets", "a day off for that."],
  ["और आज *भी*", "उस दिन *छुट्टी* मिलती है।"], ["और आज भी", "उस दिन छुट्टी मिलती है।"]),
 (["But that's not even", "the *weirdest* part."], ["But that's not even", "the weirdest part."],
  ["लेकिन ये अभी", "सबसे *अजीब* बात नहीं है।"], ["लेकिन ये अभी", "सबसे अजीब बात नहीं है।"]),
 (["Cross the *border* today...", "and you travel", "*back in time.*"], ["Cross the border today...", "and you travel", "back in time."],
  ["आज *border* पार करो...", "और आप", "*time* में पीछे चले जाते हो।"], ["आज border पार करो...", "और आप", "time में पीछे चले जाते हो।"]),
 (["Spain's clocks run", "an *hour ahead.*", "Since *1940.*"], ["Spain's clocks run", "an hour ahead.", "Since nineteen forty."],
  ["Spain की घड़ियां", "*एक घंटा* आगे चलती हैं।", "*1940* से।"], ["Spain की घड़ियां", "एक घंटा आगे चलती हैं।", "Nineteen forty से।"]),
 (["Then there's the *capital.*", "*Madrid...*", "or *Lisbon?*"], ["Then there's the capital.", "Madrid...", "or Lisbon?"],
  ["फिर *capital* का झगड़ा।", "*Madrid...*", "या *Lisbon?*"], ["फिर capital का झगड़ा।", "Madrid...", "या Lisbon?"]),
 (["And Portugal has", "just *one demand.*"], ["And Portugal has", "just one demand."],
  ["और Portugal की", "बस *एक शर्त* है।"], ["और Portugal की", "बस एक शर्त है।"]),
 (["So... *one country,*", "or *two?*", "Because honestly..."], ["So... one country,", "or two?", "Because honestly..."],
  ["तो... *एक देश*", "या *दो?*", "क्योंकि सच बताऊं..."], ["तो... एक देश", "या दो?", "क्योंकि सच बताऊं..."]),
]
en = {'lines': [{'who': 'Narrator', 'chunks': a, 'tc': b, 'tts': ' '.join(b)} for a, b, c, d in L]}
hi = {'lines': [{'who': 'Narrator', 'chunks': c, 'tc': d, 'tts': ' '.join(d), 'chunks_en': a} for a, b, c, d in L]}
for a, b, c, d in L: assert len(a) == len(b) == len(c) == len(d), a
json.dump(en, open('script.json', 'w'), ensure_ascii=False, indent=1); json.dump(hi, open('script_hi.json', 'w'), ensure_ascii=False, indent=1)
print('EN words', sum(len(l['tts'].split()) for l in en['lines']), 'lines', len(L))
DIR_EN = ("Narrate this as a high-energy, feel-good 'what if' geography video for BHUGOL, a popular geography fun-facts YouTube channel. The Narrator is thrilled to be telling you this: enthusiastic, upbeat, bright and very expressive, like an excited friend who can't wait to show you something amazing. Big smile in the voice the whole way. Wide, lively pitch movement: rise with real curiosity on every question, say every number with genuine amazement, and land each punchline with a grin after a tiny comic pause. Say 'again?' in the first line with a playful, knowing lift. The last line trails off unfinished on 'Because honestly...', voice staying up, so it loops straight back into the first line. Pace is quick and bouncy, about 170 words per minute, short crisp pauses; never slow, flat, calm, sleepy or documentary-serious. Accent: native General American English narrator, neutral American accent from the first word to the last. VOICE IDENTITY: always the same warm baritone host, same person and same energy level throughout. Pronounce 'Iberia' as 'eye-BEER-ee-uh'.")
DIR_HI = ("Narrate this as a high-energy, feel-good 'what if' geography video for BHUGOL, a popular geography fun-facts YouTube channel, in natural spoken Hindi like a top Indian geography explainer channel. The Narrator is thrilled to be telling you this: enthusiastic, upbeat, bright and very expressive, like an excited friend who can't wait to show you something amazing. Big smile in the voice the whole way. Wide, lively pitch movement: rise with real curiosity on every question, say every number with genuine amazement, and land each punchline with a grin after a tiny comic pause. Say 'फिर से' in the first line with a playful, knowing lift. Numbers and English words (country and city names, million, Nobel, border, time, capital, December) are spoken in English, naturally, the way Indian creators mix them. The last line trails off unfinished on 'क्योंकि सच बताऊं...', voice staying up, so it loops straight back into the first line. Pace is quick and bouncy with short crisp pauses; never slow, flat, calm, sleepy or documentary-serious. VOICE IDENTITY: always the same warm baritone host, same person and same energy level throughout. Pronounce 'Iberia' as 'eye-BEER-ee-uh'.")
for lang, S, D in (('en', en, DIR_EN), ('hi', hi, DIR_HI)):
    job = {'id': f'iberia-{lang}-g38', 'models': ['gemini-3.8-flash-tts'], 'items': [{'name': f'narration_{lang}', 'direction': D, 'speakers': {'Narrator': 'Sadaltager', 'Chars': 'Puck'}, 'lines': [['Narrator', l['tts']] for l in S['lines']]}]}
    json.dump(job, open(f'/home/claude/media-engine/jobs/tts/iberia-{lang}-g38.json', 'w'), ensure_ascii=False, indent=1)
