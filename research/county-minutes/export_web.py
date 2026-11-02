#!/usr/bin/env python3
"""Publish OCR pages and topic matches for a static searchable county minutes viewer.
Topic hits are candidates for human review, never automatically approved decisions.
"""
import sqlite3,json,pathlib,re,datetime
root=pathlib.Path(__file__).parent
db=sqlite3.connect(root/"data/minutes.sqlite")
db.row_factory=sqlite3.Row
docs=[dict(r) for r in db.execute("SELECT id,source_group,url,title,pages,status FROM documents WHERE status='indexed' ORDER BY title")]
pages=[dict(r) for r in db.execute("SELECT doc_id,page,body FROM pages ORDER BY doc_id,page")]
topics={
 "conditional use":r"conditional\s+use|\bCUP\b",
 "agricultural zoning":r"agricultur|\bzone\s+A\b",
 "cabins and lodges":r"cabins?|lodg(e|ing)|hunting",
 "guest or dude ranch":r"guest\s+ranch|dude\s+ranch",
 "subdivision and splits":r"subdivis|lot\s+split|parcel\s+split",
 "roads and access":r"access|road|easement",
 "recreational use":r"recreat|campground|camping"
}
compiled={k:re.compile(v,re.I) for k,v in topics.items()}
hits=[]
for p in pages:
 for name,pattern in compiled.items():
  matches=list(pattern.finditer(p["body"]))
  if not matches:continue
  for m in matches[:8]:
   a=max(0,m.start()-160);b=min(len(p["body"]),m.end()+220)
   hits.append({"doc_id":p["doc_id"],"page":p["page"],"topic":name,"excerpt":" ".join(p["body"][a:b].split())})
payload={"generated_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"source":"OCR extracted county PDF minutes; text may contain errors","documents":docs,"pages":pages,"topic_hits":hits,"topics":list(topics)}
dest=root/"web"/"index-data.json";dest.parent.mkdir(parents=True,exist_ok=True)
dest.write_text(json.dumps(payload,ensure_ascii=False,separators=(",",":")))
print(f"Exported {len(docs)} documents, {len(pages)} pages, {len(hits)} candidate topic hits, {dest.stat().st_size} bytes")
