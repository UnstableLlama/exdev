# Fable: per-window token use of Astra's thread. usage: token_profile.py START_FILE END_FILE [label]
import json,glob,os,sys,datetime
f=[x for x in glob.glob(os.path.expanduser("~/.codex/sessions/2026/11/*/*.jsonl")) if "01a1da07" in x][0]
ts=lambda p: datetime.datetime.fromtimestamp(os.path.getmtime(p),datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
t0,t1=ts(sys.argv[1]),ts(sys.argv[2])
calls=inp=unc=out=0;mx=0
for l in open(f):
    if '"token_count"' not in l: continue
    try: d=json.loads(l)
    except Exception: continue
    i=(d.get("payload") or {}).get("info")
    if not i or not (t0<d["timestamp"][:19]<=t1): continue
    u=i["last_token_usage"]; calls+=1; inp+=u["input_tokens"]; unc+=u["input_tokens"]-u.get("cached_input_tokens",0); out+=u["output_tokens"]; mx=max(mx,u["input_tokens"])
print(f"{sys.argv[3] if len(sys.argv)>3 else ''} calls={calls} input={inp/1e6:.2f}M uncached={unc/1e3:.0f}k output={out/1e3:.1f}k maxctx={mx/1e3:.0f}k")
