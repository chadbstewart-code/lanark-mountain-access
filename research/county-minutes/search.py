#!/usr/bin/env python3
import argparse,sqlite3,pathlib
p=argparse.ArgumentParser();p.add_argument("query");p.add_argument("--db",default="research/county-minutes/data/minutes.sqlite");p.add_argument("--limit",type=int,default=25);a=p.parse_args()
db=sqlite3.connect(a.db)
for row in db.execute("""SELECT d.title,d.url,p.page,snippet(page_search,2,'[',']',' … ',20)
 FROM page_search JOIN documents d ON d.id=page_search.doc_id
 JOIN pages p ON p.doc_id=d.id AND p.page=page_search.page
 WHERE page_search MATCH ? ORDER BY rank LIMIT ?""",(a.query,a.limit)):
 print(f"{row[0]} | PDF page {row[2]} | {row[1]}\n{row[3]}\n")
