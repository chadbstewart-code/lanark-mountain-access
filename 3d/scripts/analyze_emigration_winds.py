#!/usr/bin/env python3
"""Fetch ITD Emigration Canyon historical wind records in object-ID pages and compute wind roses.
Station ID and date coverage discovered from official ArcGIS metadata.
"""
import requests,json,math,collections,datetime,pathlib,time
BASE="https://gisp.itd.idaho.gov/hosting/rest/services/Hosted/RWIS_HistoricData/FeatureServer/0/query"
OUT=pathlib.Path("3d/data/weather");OUT.mkdir(parents=True,exist_ok=True)
SID=10021
FIELDS="objectid,stationid,stationname,sensorvaluedatetimeutc,winddirectiondeg,windspeedmph,maxwinddirectiondeg,maxwindspeedmph"
def get(p):
 for attempt in range(4):
  try:
   r=requests.get(BASE,params={"f":"json",**p},timeout=90);r.raise_for_status();j=r.json()
   if "error" in j:raise RuntimeError(str(j["error"]))
   return j
  except (requests.RequestException,RuntimeError):
   if attempt==3:raise
   time.sleep(2**attempt)
ids=get({"where":f"stationid={SID}","returnIdsOnly":"true"})["objectIds"]
if not ids:raise RuntimeError("No records for Emigration Canyon")
ids=sorted(ids)
rows=[]
for k in range(0,len(ids),500):
 batch=ids[k:k+500]
 j=get({"objectIds":",".join(map(str,batch)),"outFields":FIELDS,"returnGeometry":"false"})
 rows.extend(x["attributes"] for x in j.get("features",[]))
print("Retrieved",len(rows),"of",len(ids))
if len(rows)<len(ids)*.99:raise RuntimeError("Incomplete retrieval; refusing summary")
# Preserve raw records in compact JSON; source provenance explicit
(OUT/"emigration-10021-wind-raw.json").write_text(json.dumps({"station_id":SID,"source":BASE,"retrieved_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"records":rows},separators=(",",":")))
# Deduplicate by timestamp, selecting maximum available gust if multiple records
dedup={}
for row in rows:
 t=row.get("sensorvaluedatetimeutc")
 if not isinstance(t,(int,float)):continue
 old=dedup.get(t)
 if old is None or (row.get("maxwindspeedmph") or -1)>(old.get("maxwindspeedmph") or -1):dedup[t]=row
clean=list(dedup.values())
dirs=["N","NE","E","SE","S","SW","W","NW"]
def sector(deg):
 if not isinstance(deg,(int,float)) or not math.isfinite(deg) or deg<0 or deg>360:return None
 return dirs[int(((deg%360)+22.5)//45)%8]
gusts=sorted([r["maxwindspeedmph"] for r in clean if isinstance(r.get("maxwindspeedmph"),(int,float)) and r["maxwindspeedmph"]>=0])
threshold=gusts[int(.95*(len(gusts)-1))] if gusts else None
summary={"station":"Emigration Canyon","stationid":SID,"source":BASE,"retrieved_records":len(rows),"unique_timestamps":len(clean),"duplicates_removed":len(rows)-len(clean),"gust_p95_mph":threshold,"sectors":{},"seasonal":{},"notes":["Directions are meteorological FROM bearings","Only 2021-2022 available in this source","Do not extrapolate to Lanark without local validation"]}
def tally(records):
 out={x:{"count":0,"high_gust_count":0} for x in dirs}
 for r in records:
  sec=sector(r.get("winddirectiondeg"))
  if sec is None:continue
  out[sec]["count"]+=1
  if threshold is not None and isinstance(r.get("maxwindspeedmph"),(int,float)) and r["maxwindspeedmph"]>=threshold:out[sec]["high_gust_count"]+=1
 return out
summary["sectors"]=tally(clean)
for season,months in {"winter":[12,1,2],"spring":[3,4,5],"summer":[6,7,8],"fall":[9,10,11]}.items():
 subset=[r for r in clean if datetime.datetime.fromtimestamp(r["sensorvaluedatetimeutc"]/1000,datetime.timezone.utc).month in months]
 summary["seasonal"][season]={"observations":len(subset),"sectors":tally(subset)}
(OUT/"emigration-10021-wind-summary.json").write_text(json.dumps(summary,indent=2)+"\n")
print(json.dumps({k:v for k,v in summary.items() if k!="seasonal"},indent=2))
