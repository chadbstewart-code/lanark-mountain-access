#!/usr/bin/env python3
"""Index public Bear Lake County planning minutes with page-level provenance.
Use official linked PDFs only. Missing/unreadable documents are reported, never silently omitted.
"""
import argparse,datetime,hashlib,json,pathlib,re,sqlite3,urllib.parse
import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader
from io import BytesIO

ROOT="https://www.bearlakecounty.info/"
SOURCES={"planning":"planning-and-zoning.html","commissioners":"meetings.html"}
HEADERS={"User-Agent":"LanarkResearchIndexer/0.1 (public county records; research)"}
def fetch(url):
 r=requests.get(url,headers=HEADERS,timeout=45);r.raise_for_status();return r.content
def discover(group,years):
 html=fetch(urllib.parse.urljoin(ROOT,SOURCES[group])).decode("utf-8","replace")
 soup=BeautifulSoup(html,"html.parser")
 found=[];seen=set()
 for a in soup.select("a[href]"):
  href=urllib.parse.urljoin(ROOT,a["href"]);label=a.get_text(" ",strip=True)
  if not href.lower().split("?")[0].endswith(".pdf"):continue
  if "bearlakecounty.info" not in urllib.parse.urlparse(href).netloc:continue
  context=a.parent.get_text(" ",strip=True)[:250] if a.parent else label
  context_years=set(re.findall(r"20(?:1[7-9]|2[0-6])",context+" "+href))
  if years and not (context_years & years):continue
  if group=="planning" and not any(k in (href+" "+label).lower() for k in ["minute","p_z","planning","p&z"]):continue
  if href in seen:continue
  seen.add(href);found.append({"url":href,"label":label,"context":context})
 return found
def setup(db):
 db.executescript("""
 CREATE TABLE IF NOT EXISTS documents(id TEXT PRIMARY KEY, source_group TEXT, url TEXT UNIQUE, title TEXT, sha256 TEXT, pages INTEGER, fetched_utc TEXT, status TEXT, error TEXT);
 CREATE TABLE IF NOT EXISTS pages(doc_id TEXT,page INTEGER,body TEXT,PRIMARY KEY(doc_id,page));
 CREATE VIRTUAL TABLE IF NOT EXISTS page_search USING fts5(doc_id UNINDEXED,page UNINDEXED,body);
 """)
def run(args):
 out=pathlib.Path(args.output);out.mkdir(parents=True,exist_ok=True)
 db=sqlite3.connect(out/"minutes.sqlite");setup(db)
 manifest={"generated_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"scope":{"groups":args.groups,"years":args.years},"documents":[]}
 for group in args.groups:
  try:links=discover(group,set(map(str,args.years)))
  except Exception as e:manifest["documents"].append({"source_group":group,"status":"discovery_error","error":str(e)});continue
  for item in links[:args.max_per_group]:
   url=item["url"];docid=hashlib.sha256(url.encode()).hexdigest()[:16]
   record={"id":docid,"source_group":group,**item}
   try:
    raw=fetch(url)
    if not raw.startswith(b"%PDF"):raise ValueError("Not a PDF")
    sha=hashlib.sha256(raw).hexdigest()
    reader=PdfReader(BytesIO(raw),strict=False)
    texts=[(p.extract_text(extraction_mode="layout") or "").strip() for p in reader.pages]
    if not any(texts):raise ValueError("No extractable text; needs manual review/OCR")
    with db:
     db.execute("DELETE FROM page_search WHERE doc_id=?",(docid,))
     db.execute("DELETE FROM pages WHERE doc_id=?",(docid,))
     for i,t in enumerate(texts,1):
      db.execute("INSERT INTO pages VALUES(?,?,?)",(docid,i,t))
      db.execute("INSERT INTO page_search VALUES(?,?,?)",(docid,i,t))
     db.execute("INSERT OR REPLACE INTO documents VALUES(?,?,?,?,?,?,?,?,?)",(docid,group,url,item["label"],sha,len(texts),manifest["generated_utc"],"indexed",None))
    record.update({"status":"indexed","pages":len(texts),"sha256":sha,"text_characters":sum(map(len,texts))})
   except Exception as e:
    record.update({"status":"error","error":str(e)})
    with db:db.execute("INSERT OR REPLACE INTO documents VALUES(?,?,?,?,?,?,?,?,?)",(docid,group,url,item["label"],None,None,manifest["generated_utc"],"error",str(e)))
   manifest["documents"].append(record)
 db.close()
 (out/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
 print("Indexed",sum(x["status"]=="indexed" for x in manifest["documents"]),"documents; errors",sum(x["status"]=="error" for x in manifest["documents"]))
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--groups",nargs="+",choices=list(SOURCES),default=["planning"]);p.add_argument("--years",nargs="+",type=int,default=[2024,2025,2026]);p.add_argument("--max-per-group",type=int,default=60);p.add_argument("--output",default="research/county-minutes/data");run(p.parse_args())
