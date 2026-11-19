#!/bin/bash
# Laptop: list CC-licensed candidates (30/60 fps) for each clip need. usage: bash find_clips.sh > cand.txt
Y=~/.local/bin/yt-dlp
q() { # $1 tag, $2 query
  echo "== $1 | $2"
  timeout 25 $Y --flat-playlist -J "https://www.youtube.com/results?search_query=$(echo "$2" | sed 's/ /+/g')&sp=EgIwAQ%253D%253D" 2>/dev/null |
    python3 -c "
import json,sys
d=json.load(sys.stdin)
for e in [e for e in d.get('entries',[]) if 25<(e.get('duration') or 0)<1500][:7]: print(e['id'])" > /tmp/ids.txt
  for id in $(cat /tmp/ids.txt); do
    timeout 10 $Y -q --no-warnings --print "%(id)s|%(fps)s|%(height)s|%(duration)s|%(license)s|%(channel)s|%(title).60s" "https://youtu.be/$id" 2>/dev/null
  done
}
q isl "El Nido Palawan drone 4k"
q isl2 "Coron Palawan drone"
q taal "Taal volcano drone 4k"
q taal2 "Taal lake Tagaytay drone"
q choc "Chocolate Hills Bohol drone 4k"
q tars "Philippine tarsier Bohol"
q pina "Mount Pinatubo crater lake drone"
q man "Manila drone 4k"
q man2 "Manila traffic jeepney street"
q lant "Giant Lantern Festival San Fernando"
q mall "Christmas mall Manila September"
q sea "deep sea submersible dive footage"
