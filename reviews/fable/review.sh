#!/bin/bash
# Fable's routine pass over the pending request: request text, check.py, hashes, draft, replay, prompt diff, hindsight, catalog.
# usage: reviews/fable/review.sh [previous-run-for-prompt-compare]
cd ~/git/exdev
for f in reviews/requests/*.md; do b=$(basename $f); [ -e reviews/verdicts/$b ] || { F=$f; N=$b; }; done
[ -z "$N" ] && { echo "nothing pending"; exit 0; }
echo "== $N"; sed '/^## SHA256/,$d' $F
set -- $(echo $N | sed -E 's/commit-([0-9]+)-([0-9]+)\.md/\1 \2/') "$1"
echo ===CHECK; python3 reviews/fable/check.py $1 $2 2>&1 | grep -v '^[0-9]* {"id"' | sed -n 7,40p
echo ===HASH; grep -E '^- .*: `' $F | sed -E 's/^- (.*): `(.*)`/\2  \1/' | sha256sum -c 2>&1 | grep -v ': OK'; echo hashdone
S=$(grep -o 'Upstream: `[0-9a-f]*' $F | cut -d'`' -f2)
echo ===DRAFT; sed -n '/^## Problem/,$p' .teacher/runs/commit-$1-$2/draft.md
echo ===DIFFSTAT; git --git-dir=.sources/exllamav3.git show --stat --format='%H %ci %s' $S | tail -12
PREV=${3:-$(ls -d .teacher/runs/commit-$(printf %06d $((10#$1-1)))-* | tail -1 | xargs basename)}
python3 - $1 $2 $PREV <<'PY'
import json,sys
sys.path.insert(0,'.')
def load(r):
    acc={}
    def calls(o):
        if isinstance(o,dict):
            if "tool" in o and "arguments" in o and "id" in o: acc.setdefault("c",[]).append(o)
            if o.get("role")=="tool" and "call_id" in o: acc.setdefault("r",{})[o["call_id"]]=o["content"]
            if o.get("role") in("system","developer") and isinstance(o.get("content"),str): acc.setdefault("s",[]).append(o["content"])
            for v in o.values(): calls(v)
        elif isinstance(o,list):
            for v in o: calls(v)
    calls(json.load(open(f".teacher/runs/{r}/raw-transcript.json"))); return acc
a=load(f"commit-{sys.argv[1]}-{sys.argv[2]}"); b=load(sys.argv[3])
print("===REPLAY\nsystem same as",sys.argv[3],":",a["s"]==b["s"])
from teacher.runner import Runner
r=Runner(f".teacher/retrieval/{sys.argv[1]}-{sys.argv[2]}"); bad=0
for cl in a["c"]:
    try: got=r.invoke(cl["tool"],cl["arguments"])
    except Exception as e: got={"EXC":str(e)}
    if got!=json.loads(a["r"][cl["id"]]): bad+=1
    print(cl["tool"],json.dumps(cl["arguments"])[:170])
print("replayed",len(a["c"]),"mismatch",bad)
import os
pe=f".teacher/runs/commit-{sys.argv[1]}-{sys.argv[2]}/prior-evidence.json"
if os.path.exists(pe):
    pbad=0; recs=json.load(open(pe))
    for rec in recs:
        try: got=r.invoke(rec["tool"],rec["arguments"])
        except Exception as e: got={"EXC":str(e)}
        if json.dumps(got)!=rec["result"]: pbad+=1
    print("replayed-imported",len(recs),"mismatch",pbad)
PY
echo ===HINDSIGHT; grep -rl "reviews/verdicts\|defect-ledger" .teacher/retrieval/$1-$2 2>/dev/null | head -3; echo end
C=$(git --git-dir=.sources/exllamav3.git show -s --format=%cI $S | xargs -I{} date -u -d {} +%Y-%m-%dT%H:%M:%SZ)
echo "===OPEN AT $C"; gh api --paginate "repos/turboderp-org/exllamav3/issues?state=all&per_page=100&direction=asc&sort=created" --jq ".[] | select(.created_at < \"$C\") | select(.closed_at==null or .closed_at > \"$C\") | .number" | tr '\n' ' '; echo
