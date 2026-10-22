#!/bin/bash
# Pre-render gates for a BHUGOL build (22 Oct 2026). Run after build.py/build3d.py, before `hyperframes render`.
# Usage: bhugol-v2/qa/gates.sh <build_dir> [<node work dir with playwright-core>]   -> exit 1 if any gate fails
set -o pipefail
B=$1; W=${2:-/home/claude/work}; Q=$(cd "$(dirname "$0")" && pwd); ok=0
export HYPERFRAMES_BROWSER_PATH=${HYPERFRAMES_BROWSER_PATH:-/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell}
cp "$Q/scene_gate.mjs" "$Q/layout_gate.mjs" "$W/" && cd "$W" || exit 1
node scene_gate.mjs "$B" | tail -20 || ok=1
node layout_gate.mjs "$B" | grep -E "^FAIL|LAYOUT" || ok=1
[ $ok = 0 ] && echo "ALL GATES PASS: render may start" || echo "GATES FAILED: fix the spec/template, rebuild, rerun gates. Do not render."
exit $ok
