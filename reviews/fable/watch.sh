#!/bin/bash
# Fable's watch: exits on a request without a verdict, a stalled cycle, or a new notify-failure file.
cd ~/git/exdev
base=$(ls reports/cycle-notify-failed-* 2>/dev/null | wc -l); stall=0
while true; do
  for f in reviews/requests/*.md; do b=$(basename $f); [ -e reviews/verdicts/$b ] || { echo "PENDING $b"; exit 0; }; done
  [ $(ls reports/cycle-notify-failed-* 2>/dev/null | wc -l) -gt $base ] && { echo "NOTIFY-FAILED $(ls -t reports/cycle-notify-failed-* | head -1)"; exit 0; }
  st=$(python3 -c "import json;print(json.load(open('reports/teacher-walk-001.json')).get('status'))" 2>/dev/null)
  if [ "$st" = running ] && ! pgrep -f 'teacher.(cycle|walk)|orchestration.(run_ahead|notify)|exdev-.*.py|codex app-server' >/dev/null; then stall=$((stall+1)); else stall=0; fi
  [ $stall -ge 24 ] && { echo "STALL journal says running, no cycle process for 2 minutes"; exit 0; }
  sleep 5
done
