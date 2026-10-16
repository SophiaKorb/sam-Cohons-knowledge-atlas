#!/usr/bin/env python3
"""Bounded, append-only legacy audio link checks. Python 3.10+; no external packages."""
import argparse, datetime, json, pathlib, time, urllib.error, urllib.request

def probe(url, timeout):
    req=urllib.request.Request(url,headers={"User-Agent":"Cohon-Archive-QA/1.0","Range":"bytes=0-1023","Accept-Encoding":"identity"},method="GET")
    try:
        with urllib.request.urlopen(req,timeout=timeout) as r:
            buf=r.read(1024); mime=r.headers.get("Content-Type","").lower()
            magic=buf.startswith(b"ID3") or buf[:2] in (b"\xff\xfb",b"\xff\xf3",b"\xff\xf2")
            candidate=(r.status in (200,206) and (magic or mime.startswith("audio/")))
            return {"result":"audio_candidate" if candidate else "non_audio_or_uncertain","http_status":r.status,"final_url":r.url,"content_type":mime,"sample_bytes":len(buf),"mp3_signature":magic,"range_supported":r.status==206}
    except urllib.error.HTTPError as e:
        return {"result":"http_error","http_status":e.code,"final_url":e.url}
    except Exception as e:
        return {"result":"network_error","error_type":type(e).__name__,"error":str(e)[:200]}

def main():
    a=argparse.ArgumentParser()
    a.add_argument("--episodes",required=True,help="Repository file data/episodes-by-year/YYYY.json")
    a.add_argument("--ledger",required=True,help="Append-only JSONL output")
    a.add_argument("--limit",type=int,default=10)
    a.add_argument("--timeout",type=int,default=12)
    a.add_argument("--delay",type=float,default=0.5)
    x=a.parse_args()
    if not (1<=x.limit<=100 and 1<=x.timeout<=30 and x.delay>=0):a.error("invalid safety bounds")
    rows=json.loads(pathlib.Path(x.episodes).read_text(encoding="utf-8"))
    failed=[r for r in rows if r.get("official_link_status")=="dead" and r.get("official_audio_url")][:x.limit]
    dest=pathlib.Path(x.ledger);dest.parent.mkdir(parents=True,exist_ok=True)
    with dest.open("a",encoding="utf-8") as f:
        for i,row in enumerate(failed):
            record={"checked_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"id":row["id"],"original_url":row["official_audio_url"],"historical_status":"dead","method":"bounded GET, Range 0-1023","observation":probe(row["official_audio_url"],x.timeout)}
            f.write(json.dumps(record,ensure_ascii=False)+"\n");f.flush()
            print(row["id"],record["observation"]["result"])
            if i+1<len(failed):time.sleep(x.delay)

if __name__=="__main__":main()
