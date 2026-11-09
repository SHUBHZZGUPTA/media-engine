/* ---------- titles + captions ---------- */
const TT = {};
for (const t of D.titles) { const g = mk('div', { class: 'ttl', id: t.id }, $('titles')); const lines = [];
  t.lines.forEach((ln0, i) => { const small = ln0.startsWith('~'); const ln = small ? ln0.slice(1) : ln0; const size = small ? 58 : 132;
    const d = mk('div', { class: 'tl ' + (small ? 'small' : 'big') }, g); const base = 300 + (i === 0 ? 0 : (small ? 74 : 124));
    Object.assign(d.style, { fontSize: size + 'px', top: (base - size * .8) + 'px', webkitTextStrokeWidth: (size * .14) + 'px' }); markup(ln, d); lines.push(d); });
  TT[t.id] = { g, t, lines }; }
const CAPS = D.chunks.map(c => { const g = mk('div', { class: 'cap' }, $('caps'));
  const lines = c.txt.split('|').map(ln => { const d = mk('div', { class: 'cl' }, g); markup(ln, d); return d; });
  return { c, g, lines, words: [...g.querySelectorAll('span')] }; });
$('folTxt').textContent = D.end.button; $('folTxt2').textContent = '✓ ' + D.end.following;
function layout() {
  for (const K of CAPS) { let fs = 92; K.g.style.opacity = 1;
    for (const d of K.lines) { d.style.fontSize = '92px'; const w = d.scrollWidth; if (w > 740) fs = Math.min(fs, 92 * 740 / w); }
    K.g.style.opacity = 0; const n = K.lines.length;
    K.lines.forEach((d, i) => Object.assign(d.style, { fontSize: fs.toFixed(1) + 'px', webkitTextStrokeWidth: (fs * .17).toFixed(1) + 'px', top: (1385 + (i - (n - 1) / 2) * fs - fs * .5).toFixed(1) + 'px' })); }
  for (const id in TT) { const { g, lines } = TT[id]; g.style.opacity = 1;
    for (const d of lines) { const w = d.scrollWidth, fs = parseFloat(d.style.fontSize); if (w > 960) d.style.fontSize = (fs * 960 / w).toFixed(1) + 'px'; }
    g.style.opacity = 0; }
}

