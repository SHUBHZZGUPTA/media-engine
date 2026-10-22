"""Fail the build when a shader source string contains a `//` line comment (22 Oct 2026: one such comment inside a
one-line GLSL string commented out the rest of the shader, so three scenes rendered black in a delivered video).
Usage: python3 shader_lint.py <template.html>   (exit 1 on a hit). build.py / build3d.py call it automatically."""
import re, sys
t = open(sys.argv[1]).read(); bad = []
for m in re.finditer(r'`([^`]*)`', t):
    body = re.sub(r'/\*.*?\*/', '', m.group(1), flags=re.S)
    if ('gl_FragColor' in body or 'gl_Position' in body) and re.search(r'(?<![:"\'])//', body): bad.append(t[:m.start()].count('\n') + 1)
if bad: sys.exit(f'SHADER LINT FAIL: `//` comment inside a shader string starting on line(s) {bad}. Use /* */ instead.')
print('shader lint: ok')
