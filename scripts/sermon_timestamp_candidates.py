#!/usr/bin/env python3
"""Locate candidate sermon passages in timestamped SRT/VTT transcripts.

Suggests review windows, NEVER certifies sermon boundaries. Standard library only.
Usage: python scripts/sermon_timestamp_candidates.py service.vtt --markers "choice is" "choose well"
"""
import argparse
import json
import re
from pathlib import Path
from difflib import SequenceMatcher

TIME_RE = re.compile(r"(\d\d):([0-5]\d):([0-5]\d)(?:[.,](\d{1,3}))?")
RANGE_RE = re.compile(r"(\d\d:\d\d:\d\d[.,]\d+)\s*-->\s*(\d\d:\d\d:\d\d[.,]\d+)")
def seconds(s):
    m=TIME_RE.fullmatch(s.strip())
    if not m: raise ValueError("Unsupported timestamp "+s)
    h,mi,sec,ms=m.groups()
    return int(h)*3600+int(mi)*60+int(sec)+int((ms or "0").ljust(3,"0"))/1000

def norm(s):
    return re.sub(r"[^a-z0-9 ]","",re.sub(r"\s+"," ",s.lower())).strip()

def parse(path):
    lines=Path(path).read_text(encoding="utf-8-sig").splitlines()
    cues=[]; i=0
    while i<len(lines):
        m=RANGE_RE.search(lines[i])
        if not m:
            i+=1;continue
        start,end=map(seconds,m.groups());i+=1;chunk=[]
        while i<len(lines) and lines[i].strip():
            if "-->" in lines[i]:break
            chunk.append(re.sub(r"<[^>]*>","",lines[i]))
            i+=1
        if chunk:cues.append({"start":start,"end":end,"text":" ".join(chunk)})
        i+=1
    return cues

def main():
    p=argparse.ArgumentParser()
    p.add_argument("transcript")
    p.add_argument("--markers",nargs="+",required=True)
    p.add_argument("--threshold",type=float,default=.62)
    args=p.parse_args()
    cues=parse(args.transcript);hits=[]
    for marker in args.markers:
        target=norm(marker)
        for i,c in enumerate(cues):
            window=" ".join(x["text"] for x in cues[i:i+4])
            cleaned=norm(window)
            if not cleaned:continue
            if target in cleaned: score=1.0
            else: score=SequenceMatcher(None,target,cleaned[:max(len(target)*2,40)]).ratio()
            if score>=args.threshold:
                hits.append({"marker":marker,"candidate_start_seconds":c["start"],"candidate_end_seconds":cues[min(i+3,len(cues)-1)]["end"],"score":round(score,3),"excerpt":window[:220]})
    hits=sorted(hits,key=lambda x:(-x["score"],x["candidate_start_seconds"]))[:30]
    print(json.dumps({"transcript":args.transcript,"cues":len(cues),"status":"UNVERIFIED_CANDIDATES_NOT_SERMON_BOUNDARIES","matches":hits},indent=2))
if __name__=="__main__":main()
