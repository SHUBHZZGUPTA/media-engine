# sourced by the shell tools: run them FROM the episode folder
MM3="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; TOOLS="$MM3/tools"; ENGD="$MM3/engine"; EP="$(pwd)"
export HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1 HYPERFRAMES_NO_UPDATE_CHECK=1 HYPERFRAMES_SKIP_SKILLS=1 PYTHONDONTWRITEBYTECODE=1
export HYPERFRAMES_BROWSER_PATH="${HYPERFRAMES_BROWSER_PATH:-/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell}"
[ -d "$ENGD/node_modules/hyperframes" ] || (cd "$ENGD" && npm ci --silent)
