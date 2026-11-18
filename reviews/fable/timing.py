#!/usr/bin/env python3
"""Fable's timing report: author turn durations by model from the Codex session log, since a UTC time.
usage: reviews/fable/timing.py [since-iso, default 2026-11-16T15:00]"""
import sys,json,glob,datetime as dt,statistics as st,collections,re
since=sys.argv[1] if len(sys.argv)>1 else '2026-11-16T15:00'
L=glob.glob('/home/brandonrabe/.codex/sessions/2026/11/14/rollout-*01a1da07*.jsonl')[0]
P=lambda s: dt.datetime.fromisoformat(s.replace('Z','+00:00'))
model=None; start=None; rows=[]; tools=0; quota=[]
for l in open(L):
    if l[14:30]<since[:16]: continue
    try: d=json.loads(l)
    except Exception: continue
    p=d.get('payload') or {}; t=p.get('type')
    if d.get('type')=='turn_context': model=p.get('model')
    elif t=='task_started': start=P(d['timestamp']); tools=0
    elif t=='custom_tool_call': tools+=1
    elif t=='task_complete' and start:
        rows.append((model,(P(d['timestamp'])-start).total_seconds(),tools,d['timestamp'])); start=None
    if '"used_percent"' in l:
        m=re.search(r'"primary":\{[^}]*"used_percent":([0-9.]+)',l)
        if m: quota.append((d.get('timestamp'),float(m.group(1)),model))
by=collections.defaultdict(list)
for r in rows: by[r[0]].append(r)
for m,rs in by.items():
    ds=[r[1] for r in rs]; work=[r for r in rs if r[2]>=3]
    per=[r[1]/r[2] for r in work]
    print(f"{m}: turns={len(rs)} total={sum(ds)/60:.0f}min median={st.median(ds):.0f}s; working turns (3+ commands)={len(work)} median={st.median([r[1] for r in work]) if work else 0:.0f}s, sec/command median={st.median(per) if per else 0:.0f}")
# quota per hour of author turn time, by model
first={}
for ts,q,m in quota:
    first.setdefault(m,[ts,q,ts,q]); first[m][2]=ts; first[m][3]=q
for m,(a,qa,b,qb) in first.items():
    h=(P(b)-P(a)).total_seconds()/3600
    if h>0: print(f"quota while {m}: {qa:.0f}% -> {qb:.0f}% over {h:.1f}h wall = {(qb-qa)/h:.1f}%/h")
