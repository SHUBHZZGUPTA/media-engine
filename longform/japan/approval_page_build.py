import html, json
import sys; sys.path.insert(0,'/home/claude/japan'); from hooks_section import hooks_html
E=html.escape
L=[]  # (kind, ...)
def ch(t): L.append(('ch',t))
def ln(tag,en,hi,scr,cut): L.append(('ln',tag,en,hi,scr,cut))

ch("Hook · the $100 bet (0:00–0:28)")
ln("HOOK: dare","I bet you *$100* you won't believe these are *real*.","मैं हंड्रेड डॉलर की शर्त लगाता हूँ, आपको यक़ीन नहीं होगा कि ये सच हैं।","Frame 0 = cover (title on bright 3D globe over Japan). <b>$100</b> chip slams in; title SOUND FAKE? letters slam in at 0.1 s","charslam · slam · punch 1.15")
ln("TRAILER 1 (stakes)","A train station in Japan where, if you get off, you could *never walk out*.","जापान का एक रेलवे स्टेशन, जहाँ उतर गए तो शायद कभी पैदल बाहर न निकल पाओ।","3D gorge: platform on a cliff, train pulls away. Label <b>NO EXIT</b>","whip · punch 1.3 · arrow on platform end")
ln("TRAILER 2","A village on a volcano that has *another volcano* inside it.","ज्वालामुखी पर बसा एक गाँव, जिसके अंदर एक और ज्वालामुखी है।","3D diorama of Aogashima's double crater","curve · circle on inner cone")
ln("TRAILER 3 + 4","A city with *ash* in its weather forecast. And a summit with *no address*.","एक शहर, जिसके मौसम के हाल में राख भी आती है। और एक चोटी, जिसका कोई पता नहीं।","Ash plume over a city (forecast icon ☀️🌋), then Fuji summit pin <b>📍 ???</b>","curve · curve · punch 1.4")
ln("OPEN LOOP","Plus two more I'm *not telling you* yet.","और दो और, जो मैं अभी नहीं बताऊँगा।","Two pins on the map stay dark with a ? on each","moment: hidden pins")
ln("PROOF PROMISE","But every single one *is*. And I'll show you the *proof*.","पर हर एक सच है। और मैं सबूत दिखाऊँगा।","Stamp <b>REAL ✓</b> lands on the map","stamp")
ln("PARADOX","So how does one of the best-mapped countries on Earth keep getting its own map *wrong*?","तो दुनिया के सबसे अच्छे से मैप किए गए देशों में से एक, अपना ही नक्शा बार-बार ग़लत कैसे कर देता है?","Pull back to the full paper map of Japan","zoom")
ln("SYMBOL","Grab a red pen. We're fixing the map of Japan. *Six times.*","लाल पेन उठाओ। हम जापान का नक्शा ठीक करने वाले हैं। छह बार।","Red pen enters; tracker <b>FIXED 0/6</b> appears top-left (stays all video)","zoomIn · moment: pen")

ch("Fact 1 · The islands nobody counted (0:24–0:50)")
ln("RE-ENTRY","Fact one. *Rewind to 1987.*","फ़ैक्ट one. चलो, nineteen eighty-seven में।","Card <b>FACT 1 · ISLANDS</b>; paper map turns sepia","whip")
ln("SETUP","Japan's coast guard counts its islands. *By hand*, on paper maps.","जापान का कोस्ट गार्ड अपने द्वीप गिनता है। हाथ से, काग़ज़ के नक्शों पर।","Pencil ticks islands one by one","moment: tally marks")
ln("NUMBER","Total: *6,852.*","टोटल: six thousand eight hundred fifty-two.","<b>6,852</b> counts up and stamps on the map","count · slam")
ln("EXPLAIN","But on paper, two islands close together look like *one*. An island hugging the shore looks like *mainland*.","लेकिन काग़ज़ पर, पास-पास के दो द्वीप एक ही लगते हैं। किनारे से सटा द्वीप, ज़मीन का हिस्सा लगता है।","Close-up of the Seto Inland Sea: two islets blur into one","circle on the two islets · circle on shore islet")
ln("TURN","So Japan recounts, with *digital maps*.","तो जापान दोबारा गिनता है, डिजिटल मैप्स से।","Paper peels back to a sharp satellite 3D view; islands light up one by one","curve")
ln("PAYOFF 1","The new total, in 2023? *14,125.* More than double.","twenty twenty-three का नया टोटल? fourteen thousand one hundred twenty-five. दोगुने से भी ज़्यादा।","<b>14,125</b> counts up and slams; red pen strikes 6,852; tracker 1/6","count · slam + shake (climax 1)")
ln("JOKE","Zero new land. Japan just *looked closer*.","नई ज़मीन ज़ीरो। जापान ने बस ग़ौर से देखा।","Magnifying glass over the map; card <b>+0 km²</b>","moment: magnifier")
ln("BRIDGE","But Japan does make brand-new land. *From nothing.*","लेकिन जापान सच में नई ज़मीन बनाता है। शून्य से।","Camera races south over open ocean; steam on the horizon","whip")

ch("Fact 2 · The island that grows (0:50–1:20)")
ln("RE-ENTRY","Fact two. *Nishinoshima*, about 1,000 kilometres south of Tokyo.","फ़ैक्ट two. निशिनोशिमा, टोक्यो से करीब one thousand किलोमीटर दक्षिण।","Card <b>FACT 2 · NISHINOSHIMA</b>; 3D map flyover; pin <b>NISHINOSHIMA</b>; dotted line from TOKYO with card <b>~1,000 KM</b>","zoom · card")
ln("WOW","In 2013, the sea beside it started *steaming*, and a new island rose out of the water.","twenty thirteen में, इसके पास का समंदर भाप छोड़ने लगा, और पानी से एक नया द्वीप निकल आया।","Depth plate: sea steams, a black islet rises, embers","curve · live steam + embers")
ln("TWIST","Weeks later, it crashed into Nishinoshima. The two became *one*.","कुछ हफ़्तों बाद, ये निशिनोशिमा से जा टकराया। दोनों एक हो गए।","Before→after reveal: the islet's lava joins the old island","moment: merge reveal")
ln("SCALE","The lava kept coming. Today the island is more than *ten times* its old size.","लावा आता रहा। आज ये द्वीप अपने पुराने साइज़ से ten गुना से भी बड़ा है।","Old outline vs today's outline; <b>10×</b> grows","grow · arrow")
ln("JOKE","Officially, it's part of *Tokyo*. So the capital is growing. *By volcano.*","ऑफ़िशियली, ये टोक्यो का हिस्सा है। यानी राजधानी बढ़ रही है। ज्वालामुखी से।","Tokyo's flag fills the island; tracker 2/6","punch")
ln("SETUP","Of course, nobody lives there. Living on a volcano would be *ridiculous*.","बेशक, वहाँ कोई नहीं रहता। ज्वालामुखी पर रहना तो बेवकूफ़ी होगी।","Empty smoking island, no buildings","curve · jitter hold")
ln("BEAT","*Right?*","है ना?","Hard cut to a green island with houses","hard cut")

ch("Fact 3 · A volcano inside a volcano (1:20–1:48)")
ln("RE-ENTRY + JOKE","Fact three. *Aogashima.* Also... *Tokyo.*","फ़ैक्ट three. आओगाशिमा। ये भी... टोक्यो।","Card <b>FACT 3 · AOGASHIMA</b>; pin; TOKYO label stamps on","zoom · card")
ln("WOW","The whole island is a volcano. And inside its crater sits a *second, smaller one*.","पूरा द्वीप एक ज्वालामुखी है। और उसके क्रेटर के अंदर बैठा है एक दूसरा, छोटा ज्वालामुखी।","Camera dives into the 3D double crater","zoomIn · circle on inner cone")
ln("FACT","About *160* people live here. Japan's smallest village.","यहाँ करीब one hundred sixty लोग रहते हैं। जापान का सबसे छोटा गाँव।","Houses on the northern edge light up; <b>160</b> counts up","count")
ln("STAKES","In *1785*, an eruption emptied the island for about *50 years*. Then people came back. *On purpose.*","seventeen eighty-five में एक विस्फोट ने द्वीप को करीब fifty साल के लिए ख़ाली कर दिया। फिर लोग लौट आए। जान-बूझकर।","Rewind plate: lava glow, then boats returning to a green island; <b>1785</b>, <b>50 YEARS</b>","whip · count · zoomIn")
ln("DETAIL","Today the volcano heats the village *sauna* and steams their *eggs*.","आज ये ज्वालामुखी गाँव का सॉना गर्म करता है, और उनके अंडे पकाता है।","Steam vent → ♨️ 🥚 pop; tracker 3/6","moment: emoji pop")
ln("BRIDGE","Our next volcano isn't so *calm*.","हमारा अगला ज्वालामुखी इतना शांत नहीं।","Fast flight west over Japan","whip")

ch("Fact 4 · The ash forecast (1:48–2:12)")
ln("RE-ENTRY","Fact four. *Kagoshima*, a city of about *600,000*.","फ़ैक्ट four. कागोशिमा, करीब six hundred thousand लोगों का शहर।","Card <b>FACT 4 · KAGOSHIMA</b>; city lights; <b>600,000</b>","zoom · card · count")
ln("WOW","Right across the bay sits *Sakurajima*, the most active volcano in Japan.","खाड़ी के ठीक उस पार है साकुराजिमा, जापान का सबसे ऐक्टिव ज्वालामुखी।","Volcano across the bay with a live ash plume","zoomIn · arrow")
ln("NUMBER","In 2011, it erupted more than *1,000 times*. Over three a day.","twenty eleven में ये one thousand से ज़्यादा बार फटा। रोज़ three से भी ज़्यादा बार।","<b>1,000+</b> counts up with ticks","count · slam (climax 2)")
ln("PAYOFF 3","So here, the weather report also tells you *where the ash will fall*.","इसलिए यहाँ का मौसम का हाल ये भी बताता है कि राख कहाँ गिरेगी।","Weather-map card: wind arrow carries the plume over the city","moment: forecast card")
ln("DETAIL","People check it before doing *laundry*.","लोग कपड़े धोने से पहले इसे चेक करते हैं।","Washing line, ash flakes drifting","curve")
ln("JOKE","Forecast for today: sunny, with a chance of *volcano*.","आज का फ़ोरकास्ट: धूप खिली रहेगी, और ज्वालामुखी की संभावना।","☀️ + 🌋 icons; tracker 4/6","punch")
ln("BRIDGE","So surely Japan's most famous volcano belongs to Japan? Well... *not the top*.","तो जापान का सबसे मशहूर ज्वालामुखी तो पक्का जापान का होगा? ख़ैर... चोटी नहीं।","Fuji in the distance; red circle on the summit","curve · circle")

ch("Fact 5 · The summit with no address (2:12–2:42)")
ln("RE-ENTRY","Fact five. *Mount Fuji.*","फ़ैक्ट five. माउंट फ़ूजी।","Card <b>FACT 5 · MOUNT FUJI</b>; 3D terrain flyover; <b>3,776 M</b>","zoom · card · count")
ln("WOW","Above the *8th station*, the summit isn't government land. It belongs to a *shrine*.","eighth स्टेशन के ऊपर, चोटी सरकारी ज़मीन नहीं है। वो एक श्राइन की है।","Gold ring at the 8th station; land above it fills gold; label <b>8TH STATION</b>","moment: gold fill")
ln("STORY","The state took it once. The shrine *sued* to get it back, and *won*.","सरकार ने एक बार इसे ले लिया था। श्राइन ने वापस पाने के लिए केस किया, और जीत गया।","Court scales tip; ✓ stamp","moment: scales")
ln("TWIST","And here's the twist. Two prefectures share Fuji, and they've *never drawn the border* across the top.","और ट्विस्ट ये है। फ़ूजी दो प्रीफ़ेक्चर्स के बीच है, और उन्होंने चोटी पर बॉर्डर कभी खींचा ही नहीं।","Shizuoka and Yamanashi each filled with their own flag; border line stops short of the crater. Labels <b>SHIZUOKA</b> / <b>YAMANASHI</b>","curve · arrow at the gap")
ln("PAYOFF 4","So Japan's mapping agency took the summit's *address* off its online map.","इसलिए जापान की मैपिंग एजेंसी ने अपने ऑनलाइन मैप से चोटी का पता ही हटा दिया।","Map pin card; its address text deletes letter by letter","moment: address deletes")
ln("JOKE","Japan's highest point. Address: *unknown.*","जापान का सबसे ऊँचा पॉइंट। पता: मालूम नहीं।","<b>📍 ???</b>; tracker 5/6","slam")
ln("BRIDGE","But at least you can *leave* Mount Fuji. Our last stop, *you can't*.","लेकिन माउंट फ़ूजी से कम से कम आप जा तो सकते हो। हमारे आख़िरी स्टॉप से नहीं।","Train speeds west through hills","whip")

ch("Fact 6 · The station with no exit (2:42–3:08)")
ln("RE-ENTRY","Fact six. A quiet valley in *western Japan*.","फ़ैक्ट six. पश्चिमी जापान की एक शांत घाटी।","Card <b>FACT 6 · NO EXIT</b>; pin in Yamaguchi; label <b>NISHIKI RIVER</b>","zoom · card")
ln("SETUP","In *2019*, a railway opens a station here, above a river.","twenty nineteen में, एक रेलवे यहाँ एक नदी के ऊपर स्टेशन खोलती है।","3D depth plate: river gorge, small platform on the cliff, train arriving","curve")
ln("LIST","It has a platform. A sign. A view.","इसमें एक प्लैटफ़ॉर्म है। एक बोर्ड। एक नज़ारा।","Three quick framings: platform, sign, river view","hard · hard · hard")
ln("PAYOFF 1","What it doesn't have is a *road*. Or a *path*. Or an *exit*.","जो इसमें नहीं है, वो है सड़क। या रास्ता। या कोई एग्ज़िट।","Red X on each as named; <b>NO EXIT</b>","hard cuts · circles")
ln("DETAIL","Even its building materials came in *by train*, at night.","इसे बनाने का सामान तक ट्रेन से आया, रात में।","Night train carrying beams to the empty cliff","whip (rewind)")
ln("EXPLAIN","It's called *Seiryu Miharashi*, \"clear stream viewpoint.\" Only special trains stop.","इसका नाम है सेइर्यू मिहाराशी, यानी \"साफ़ नदी का व्यूपॉइंट\"। यहाँ सिर्फ़ स्पेशल ट्रेनें रुकती हैं।","Name board <b>SEIRYU MIHARASHI · 清流みはらし</b>","zoomIn")
ln("IMAGE","You step off, look at the river, and *wait* for the train back.","आप उतरते हो, नदी देखते हो, और वापसी की ट्रेन का इंतज़ार करते हो।","Train leaves; you alone on the platform; tracker 6/6","curve · jitter hold")

ch("Ending · recap → verdict → loop (3:08–3:35)")
ln("RECAP","So, our map.","तो, हमारा नक्शा।","Pull back to the paper map of Japan, now covered in red pen","zoom")
ln("RECAP LIST","Uncounted islands. Growing land. A volcano in a volcano. Ash forecasts. A summit with no address. A station with no exit.","बिना गिने द्वीप। बढ़ती ज़मीन। ज्वालामुखी में ज्वालामुखी। राख का फ़ोरकास्ट। बिना पते की चोटी। बिना एग्ज़िट का स्टेशन।","Each of the 6 red marks pulses as it's named","6 rapid beats")
ln("VERDICT","Japan's map was never really wrong. Japan just *won't sit still*.","जापान का नक्शा कभी सच में ग़लत था ही नहीं। जापान बस टिककर बैठता नहीं।","The red marks breathe; the islands drift slightly, as if alive","flash (hero, payoff)")
ln("LOOP","Which leaves you on that platform, with plenty of time to count islands. So, how many did you believe? Be honest. *Because*","यानी आप उस प्लैटफ़ॉर्म पर हो, और द्वीप गिनने के लिए ढेर सारा टाइम है। तो, कितनों पर यक़ीन हुआ? सच बताना। क्योंकि","Platform → camera rises → globe, landing on the exact frame-0 picture; cover title eases in over the last 0.4 s","zoom · loop seam to frame 0")

def mark(s): 
    s=E(s)
    import re
    return re.sub(r'\*(.+?)\*',r'<b class="k">\1</b>',s)
rows=[];n=0
for it in L:
    if it[0]=='ch': rows.append(f'<tr class="ch"><td colspan="5">{E(it[1])}</td></tr>')
    else:
        n+=1;_,tag,en,hi,scr,cut=it
        rows.append(f'<tr><td class="n">{n}</td><td class="line">{mark(en)}<small>{E(tag)}</small></td><td class="hi">{E(hi)}</td><td class="vis">{scr}</td><td class="cut">{E(cut)}</td></tr>')
en_words=sum(len(it[2].replace("*","").split()) for it in L if it[0]=='ln')
json.dump([{'en':it[2],'hi':it[3]} for it in L if it[0]=='ln'],open('script_v1.json','w'),ensure_ascii=False,indent=1)

src=[("Island recount: 6,852 (1987, Coast Guard, by hand on paper maps) → 14,125 (GSI, digital maps); no change to land area","https://www.nippon.com/en/japan-data/h01615","Nippon.com"),
("Same, Kyodo report (hand-listed 1987, islands thought joined to land or merged)","https://blog.geogarage.com/2023/02/recount-with-digital-map-leads-to.html","Kyodo via GeoGarage"),
("Nishinoshima: eruption began Nov 2013 just off the island; new islet merged 26 Dec 2013","https://en.wikipedia.org/wiki/Nishinoshima_(Ogasawara)","Wikipedia (JCG/ERI cited)"),
("Nishinoshima now ~4 km² (Asahi, Nov 2023); old island ~0.3 km² → over 10× (13×)","https://www.asiae.co.kr/en/article/2023112017294676461","Asia Economy / Asahi"),
("Aogashima: part of Tokyo, double caldera, ~156–170 people, least-populated municipality, empty ~50 years after 1785","https://www.gotokyo.org/en/destinations/izu-and-ogasawara-islands/aogashima-island/index.html","GO TOKYO (official)"),
("Aogashima: residents in northern hamlets; geothermal 'hingya' runs the sauna and a steam cooker","https://seasia.co/2026/07/27/aogashima-japans-remote-island-in-an-active-volcanic-crater","Seasia (2026)"),
("Kagoshima ~600,000 people beside Sakurajima","https://www.mlit.go.jp/tagengo-db/H30-01413.html","Japan Tourism Agency (MLIT)"),
("Sakurajima 'the most active volcano in Japan'","https://repository.kulib.kyoto-u.ac.jp/dspace/bitstream/2433/281719/1/jdr.2020.p0174.pdf","Kyoto Univ., J. Disaster Research 2020"),
("2011: 1,353 eruptions at Showa crater + 2 at Minamidake (996 explosive)","https://gbank.gsj.jp/ld/resource/volcano/k20","Geological Survey of Japan"),
("JMA ash-fall forecasts; residents check them before laundry","https://www.morethantokyo.com/sakurajima-active-volcano/","More Than Tokyo"),
("Fuji above the 8th station = precinct of Fujisan Hongū Sengen Taisha","https://www.nippon.com/en/guide-to-japan/gu009003/","Nippon.com"),
("Nationalised 1871; shrine won in court 1974; land handed over 2004","https://japanupclose.web-japan.org/spot/s20230224_1.html","Japan Up Close (MOFA)"),
("Summit border between Shizuoka and Yamanashi left undefined; GSI removed the summit address from its online map","https://geospatialworld.net/news/japan-shows-signs-of-truce-by-making-mt-fuji-summit-address-less-on-official-maps","Geospatial World"),
("Seiryu Miharashi: opened 19 Mar 2019, Nishikigawa Railway, no road or path, materials carried by train at night, special trains only","https://en.wikipedia.org/wiki/Seiryu_Miharashi_Station","Wikipedia (Yomiuri cited)"),
("'Clear Stream Viewing Platform' name meaning","https://soranews24.com/2019/03/19/new-japanese-train-station-has-no-entrance-or-exit-only-used-to-admire-the-scenery/","SoraNews24"),
]
srch="".join(f'<li>{E(a)}: <a href="{u}">{E(t)}</a></li>' for a,u,t in src)

page=f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Japan Facts That Sound Fake — Script v1</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;800;900&family=Mukta:wght@400;600&display=swap">
<style>
:root{{--bg:#F4F1EC;--surface:#fff;--fg:#141414;--muted:#5E5A55;--rule:#DED8CF;--red:#D7261E;--sky:#1E5FD8;--gold:#E9B10C;--display:'Archivo','Arial Black',sans-serif;--body:'Archivo',system-ui,sans-serif}}
@media (prefers-color-scheme:dark){{:root{{--bg:#111;--surface:#1B1A19;--fg:#EEE9E2;--muted:#A49E96;--rule:#2F2C29;--red:#FF4F45;--sky:#6EA2FF;--gold:#F5C842;color-scheme:dark}}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 var(--body);padding:0 16px}}
main{{max-width:1240px;margin:0 auto;padding:28px 0 64px;display:grid;gap:30px}}
.eyebrow{{font:800 12px/1 var(--body);letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}}
h1{{font:900 clamp(36px,7vw,68px)/.95 var(--display);margin:10px 0 12px;letter-spacing:-.02em}} h1 em{{font-style:normal;color:var(--red)}}
h2{{font:900 22px/1.1 var(--display);margin:0 0 12px}}
.lede{{max-width:72ch;color:var(--muted);margin:0}}
.stats{{display:flex;flex-wrap:wrap;gap:8px 24px;margin-top:14px;font-size:14px}} .stats b{{color:var(--red);font:900 20px/1 var(--display);margin-right:4px}}
.two{{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:18px}}
.panel{{background:var(--surface);border:1px solid var(--rule);border-radius:6px;padding:18px 20px;min-width:0}} .panel p{{margin:0 0 10px}} .panel ul{{margin:0;padding-left:18px}} .panel li{{margin-bottom:6px}}
code.t{{display:block;font:800 16px/1.35 var(--body);background:var(--bg);padding:8px 10px;border-radius:4px;margin:4px 0 4px}} .sc{{font-size:12.5px;color:var(--muted);margin:0 0 10px}}
.thumb{{display:inline-block;background:#1E7FD0;padding:12px 16px;border-radius:4px;margin:4px 0 10px}} .thumb span{{font:900 24px/1.1 var(--display);color:#fff;-webkit-text-stroke:1.5px #000;text-transform:uppercase}} .thumb mark{{background:#FFD21F;color:#000;padding:0 6px;-webkit-text-stroke:0}}
.tablewrap{{overflow-x:auto;border:1px solid var(--rule);border-radius:6px;background:var(--surface)}}
table{{border-collapse:collapse;width:100%;min-width:1150px;font-size:14.5px}} td,th{{border-top:1px solid var(--rule);padding:9px 12px;vertical-align:top;text-align:left}}
th{{font:800 11.5px/1.2 var(--body);letter-spacing:.08em;text-transform:uppercase;color:var(--muted);background:var(--bg)}}
td.n{{color:var(--muted);width:28px}} td.line{{max-width:46ch}} td.line small{{display:block;color:var(--sky);font-weight:800;font-size:11.5px;letter-spacing:.06em;text-transform:uppercase;margin-top:3px}}
b.k{{color:var(--red)}} td.hi{{font-family:'Mukta','Noto Sans Devanagari',sans-serif;font-size:15px;max-width:40ch}} td.vis{{color:var(--muted);font-size:13.5px;width:26%}} td.vis b{{color:var(--fg)}} td.cut{{font-size:12.5px;color:var(--sky);width:12%;font-weight:700}}
tr.ch td{{background:var(--bg);font:900 13px/1 var(--display);letter-spacing:.1em;text-transform:uppercase;color:var(--red);padding:12px}}
table.f{{min-width:640px}} .src a{{color:var(--sky)}} .ok{{color:#1E9E57;font-weight:800}}
table.r{{min-width:900px}} tr.pick td{{background:color-mix(in srgb,var(--gold) 16%,var(--surface))}} td.num{{font-variant-numeric:tabular-nums;white-space:nowrap}} ol.hk{{margin:0 0 10px;padding-left:20px}} ol.hk li{{margin-bottom:4px}} .hi2{{font-family:'Mukta','Noto Sans Devanagari',sans-serif;font-size:15px;color:var(--muted);border-left:3px solid var(--rule);padding-left:10px}} .eyebrow{{margin-bottom:6px}}
</style></head><body><main>
<header><div class="eyebrow">BHUGOL long-form · script v1 (chosen) · BHUGOL fact numbering · 5 ranked hooks · 14 Nov 2026</div>
<h1>6 Japan facts that <em>sound fake</em></h1>
<p class="lede">One story, not a list: Japan is one of the best-mapped countries on Earth, yet its map keeps falling behind. We take a red pen and fix the map six times. Each fact sets up the next one, and the ending loops back into the first line.</p>
<div class="stats"><span><b>{n}</b>lines</span><span><b>{en_words}</b>words (EN)</span><span><b>~3:35</b>English</span><span><b>~3:55–4:10</b>Hindi</span><span><b>6</b>corrections = chapters</span></div></header>

<section class="two">
<div class="panel"><h2>Hooks (hookscore.py)</h2>
<p><b>A · 57 WORKABLE · "The Question"</b> (used)<br>Japan's island count was wrong for 35 years. By 7,273 islands. So what else is your map of Japan not telling you?</p>
<p><b>B · 53 · "The Question"</b><br>For 35 years, Japan's official count was missing 7,273 of its own islands. So what else is the map of Japan not telling you?</p>
<p class="sc">Both are weakest on "stakes". The trailer lines 3–6 cover that with four shocks paid off later. I turned down a 60-scoring version ("your map was missing 7,273 islands") because it overstates: the islands were always on the maps, they just weren't counted.</p></div>
<div class="panel"><h2>Story frame (Ziro playbook, shortened)</h2><ul>
<li><b>Paradox:</b> one of the best-mapped countries, and its map can't keep up</li>
<li><b>Symbol:</b> a paper map + red pen; tracker FIXED 0/6 → 6/6</li>
<li><b>Hook = trailer:</b> stat → question → 4 shocks paid off later → paradox → symbol</li>
<li><b>But/so links:</b> zero new land → but Japan makes land → nobody lives on a volcano → right? → quiet volcano → not so calm → Fuji belongs to Japan? → not the top → you can leave Fuji → not the last stop</li>
<li><b>Answer only at the end:</b> "Japan just won't sit still" (~92%)</li>
<li><b>Loop:</b> "…harder than it sounds. Because" → "Japan's island count was wrong…"</li></ul></div>
</section>

<section class="two">
<div class="panel"><h2>Titles (one per block)</h2>
<code class="t">6 Japan Facts That Sound Fake 🇯🇵</code><p class="sc">32 chars · lint 100 · matches your brief</p>
<code class="t">Japan's Map Is Wrong in 6 Ways 🗾</code><p class="sc">32 chars · lint 100 · matches the story frame</p>
<code class="t">6 Japan Facts Nobody Believes 🇯🇵</code><p class="sc">32 chars · lint 100</p></div>
<div class="panel"><h2>Thumbnail concept (sketch)</h2>
<div class="thumb"><span>6 Japan facts that sound <mark>fake</mark></span></div>
<p>Headline = the chosen title (your rule), white outlined caps, yellow box on the last word. A bright 3D satellite Japan fills the frame, with red hand-drawn circles on three insets: the no-exit platform, Fuji's summit with a 📍?, and the volcano inside a volcano. title.py flags that the thumbnail repeats the title; I followed your title-as-headline rule anyway. I'll show you the real one before burning it in.</p></div>
</section>

{hooks_html()}
<section><h2>Script, English + Hindi, with shot plan (V1 hook shown)</h2>
<p class="sc">Every line has its cut and beats up to the last frame. <b class="k">Red</b> = caption keyword (sweep bar). Hindi numbers are spoken in English. On-screen elements stay English in the Hindi video.</p>
<div class="tablewrap"><table><tr><th>#</th><th>English</th><th>Hindi</th><th>On screen</th><th>Cut / beat</th></tr>
{"".join(rows)}</table></div></section>

<section class="two">
<div class="panel"><h2>All on-screen text</h2><ul>
<li>Hook title: <b>SOUNDS FAKE?</b> · <b>+7,273 ISLANDS</b> · <b>NO EXIT</b> · <b>📍 ???</b></li>
<li>Tracker (whole video): <b>FIXED 0/6 … 6/6</b></li>
<li>Chapter cards: <b>FACT 1 · ISLANDS</b> · <b>2 · NISHINOSHIMA</b> · <b>3 · AOGASHIMA</b> · <b>4 · KAGOSHIMA</b> · <b>5 · MOUNT FUJI</b> · <b>6 · NO EXIT</b></li>
<li>Numbers (count up with the voice): 6,852 · 14,125 · +0 km² · ~1,000 KM · 10× · 160 · 1785 · 50 YEARS · 600,000 · 1,000+ · 3,776 M</li>
<li>Map labels: TOKYO · NISHINOSHIMA · AOGASHIMA · KAGOSHIMA · SAKURAJIMA · MOUNT FUJI · 8TH STATION · SHIZUOKA · YAMANASHI · NISHIKI RIVER · SEIRYU MIHARASHI 清流みはらし</li>
<li>Icons: ☀️🌋 · ♨️🥚 · court scales ✓ · red X marks</li>
<li>Karaoke captions with the keyword bars</li></ul>
<p class="sc">New since the brief, so please OK them: the FIXED 0/6 tracker and the chapter cards. Also no "subscribe" joke: the Ziro playbook wants one at 35–57%, but voice.md bans the word. Tell me if you want one.</p></div>
<div class="panel"><h2>Hedges and judgment calls</h2><ul>
<li>"Wrong for 35 years": 1987 count → recount published Feb 2023 (sources say 35).</li>
<li>"More than ten times its old size": ~0.3 km² → ~4.1 km² (about 13×).</li>
<li>"About 160 people": 156 (2025) to ~170 in other counts. They live on the northern edge, <b>not inside the crater</b>, so the wording is "on a volcano".</li>
<li>"Over three a day": 1,355 eruptions in 2011 ≈ 3.7/day.</li>
<li>Fuji: I kept the shrine fact neutral (ownership and a court case, nothing religious) and left out the dates, which take long to say. Dates are in the sources.</li>
<li>Chugoku Shimbun reported Seiryu Miharashi under 1,000 users a year, two years running. I left that out because it doesn't help the story.</li>
<li>No India-first anchors (your L27 rule).</li></ul></div>
</section>

<section class="panel src"><h2>Sources</h2><ul>{srch}</ul></section>
</main></body></html>'''
open('v1.html','w').write(page)
print(n,en_words)
