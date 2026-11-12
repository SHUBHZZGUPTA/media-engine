# Textures + routes + real-sun simulation for the flight Short.
import json, math, numpy as np
from PIL import Image, ImageEnhance; Image.MAX_IMAGE_PIXELS = None
F = '/home/claude/media-engine/outputs/fetch/'; A = 'art/'
def grade(im, b, c, s): return ImageEnhance.Color(ImageEnhance.Contrast(ImageEnhance.Brightness(im).enhance(b)).enhance(c)).enhance(s)
grade(Image.open(F + 'baikal-map/globe_bmng.jpg').convert('RGB').resize((4096, 2048), Image.LANCZOS), 1.42, 1.12, 1.35).save(A + 'day.jpg', quality=92)
n = np.array(Image.open(F + 'flight-night/night_bm2016.jpg').convert('RGB').resize((4096, 2048), Image.LANCZOS)).astype(float)
Image.fromarray(np.clip(n * 1.35, 0, 255).astype(np.uint8)).save(A + 'night.jpg', quality=90)
def v(lat, lon): la, lo = math.radians(lat), math.radians(lon); return np.array([math.cos(la) * math.cos(lo), math.cos(la) * math.sin(lo), math.sin(la)])
def ll(p): return [round(math.degrees(math.atan2(p[1], p[0])), 3), round(math.degrees(math.asin(max(-1, min(1, p[2])))), 3)]
def gc(a, b, step=1.0):  # a,b = (lon,lat); returns list of [lon,lat] along the great circle
    pa, pb = v(a[1], a[0]), v(b[1], b[0]); d = math.acos(max(-1, min(1, pa @ pb))); k = max(2, int(math.degrees(d) / step))
    return [ll((math.sin((1 - f) * d) * pa + math.sin(f * d) * pb) / math.sin(d)) for f in np.linspace(0, 1, k + 1)]
def path(wps):
    out = []
    for a, b in zip(wps, wps[1:]): seg = gc(a, b); out += seg if not out else seg[1:]
    return out
def length(p): return sum(6371 * math.acos(max(-1, min(1, v(a[1], a[0]) @ v(b[1], b[0])))) for a, b in zip(p, p[1:]))
P = {'MEL': (144.84, -37.67), 'SYD': (151.18, -33.95), 'LAX': (-118.41, 33.94), 'LHR': (-0.45, 51.47), 'TLS': (1.37, 43.63), 'HKG': (113.91, 22.31), 'DEN': (-104.67, 39.86)}
# Airbus AIB35LR, 27-28 Jul 2026: over Sydney, NE across the Pacific toward LA, across North America, the Atlantic, over London, to Toulouse (track approximate).
A350 = path([P['MEL'], P['SYD'], (-178, -12), (-150, 14), P['LAX'], (-100, 38), (-75, 44), (-53, 49), (-20, 53), P['LHR'], P['TLS']])
SHORT = path([P['MEL'], P['TLS']])
# Boeing 777-200LR, 9-10 Nov 2005: Hong Kong east over the North Pacific, LA, Denver, North America, mid-north Atlantic, London (approximate).
B777 = path([P['HKG'], (150, 32), (-165, 36), P['LAX'], P['DEN'], (-80, 42), (-50, 49), (-20, 52), P['LHR']])
B777S = path([P['HKG'], P['LHR']])
print('A350 km', round(length(A350)), 'short km', round(length(SHORT)), 'B777 km', round(length(B777)))
# real sun: plane at uniform progress, 07:27 UTC 27 Jul -> 07:51 UTC 28 Jul (24.4 h)
cum = np.cumsum([0] + [6371 * math.acos(max(-1, min(1, v(a[1], a[0]) @ v(b[1], b[0])))) for a, b in zip(A350, A350[1:])]); cum /= cum[-1]
def sun(h_utc, dec=19.0): return v(dec, -15 * (h_utc - 12 - 0.108))
ev = []; prev = None
for f in np.linspace(0, 1, 4000):
    i = min(len(A350) - 2, np.searchsorted(cum, f) - 1); i = max(0, i); g = (f - cum[i]) / max(1e-9, cum[i + 1] - cum[i])
    p = v(A350[i][1], A350[i][0]) * (1 - g) + v(A350[i + 1][1], A350[i + 1][0]) * g; p /= np.linalg.norm(p)
    alt = math.degrees(math.asin(p @ sun(7.45 + 24.4 * f))); day = alt > -0.83
    if prev is not None and day != prev: ev.append(['sunrise' if day else 'sunset', round(float(f), 3), ll(p)])
    prev = day
print(ev)
json.dump({'A350': A350, 'SHORT': SHORT, 'B777': B777, 'B777S': B777S, 'P': P, 'sunEvents': ev, 'dep_utc': 7.45, 'hours': 24.4, 'dec': 19.0}, open(A + 'routes.json', 'w'))
