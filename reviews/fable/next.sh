#!/bin/bash
# Fable: print the pending request (no hash list), hash check, check/replay summary, diff, and draft.
cd ~/git/exdev; date -u
python3 -c "import json;d=json.load(open('reports/teacher-walk-001.json'));print(d['status'],d['next_position'],len(d['approved_entries']))"
F=$(for f in reviews/requests/*.md; do b=$(basename $f); [ -e reviews/verdicts/$b ] || echo $f; done | head -1); echo "PENDING: $F"
[ -z "$F" ] && { ls -lt --time-style=+%H:%M:%S .teacher/runs | sed -n 2p; exit 0; }
echo "bad hashes: $(grep -E '^- .*: `' $F | sed -E 's/^- `?([^`:]*)`?: `(.*)`/\2  \1/' | sha256sum -c 2>/dev/null | grep -vc ': OK')"; grep -vE '^- .*: `[0-9a-f]{64}`' $F | cut -c1-1200
R=$(grep -oE '\.teacher/runs/commit-[0-9]+-[0-9]+' $F | head -1); [ -f "$R/draft.md" ] || exit 0
echo ====REVIEW; bash reviews/fable/review.sh 2>&1 | grep -E '^(impl |evidence |final==|anc |blobs |replayed|REVISION )'
sha=$(grep Upstream $F | grep -oE '[0-9a-f]{40}' | head -1); echo ====DIFF $sha; git --git-dir=.sources/exllamav3.git show $sha | cut -c1-220 | head -${1:-150}
echo ====DRAFT; sed -n '/^## Problem/,$p' $R/draft.md | sed -E 's/call_([0-9a-f]{6})[0-9a-f]+/c\1/g' | grep -vE '^(Source evidence|Locations):' | cut -c1-1400
