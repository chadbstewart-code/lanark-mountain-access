#!/usr/bin/env python3
"""Inspect public ITD historical RWIS service and preserve metadata + limited station sample.
No conclusions about prevailing winds until station IDs, field semantics and coverage are verified.
"""
import json,pathlib,requests,datetime
BASE="https://gisp.itd.idaho.gov/hosting/rest/services/Hosted/RWIS_HistoricData/FeatureServer/0"
out=pathlib.Path("3d/data/weather");out.mkdir(parents=True,exist_ok=True)
def get(url,params):
 r=requests.get(url,params=params,timeout=60);r.raise_for_status();j=r.json()
 if "error" in j:raise RuntimeError(str(j["error"]))
 return j
metadata=get(BASE,{"f":"json"})
fields=[{"name":f.get("name"),"type":f.get("type"),"alias":f.get("alias")} for f in metadata.get("fields",[])]
if not fields:raise RuntimeError("No fields: cannot verify station identifier")
info={"retrieved_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"service":BASE,
      "record_count_unverified":True,"fields":fields,"time_info":metadata.get("timeInfo"),
      "capabilities":metadata.get("capabilities"),"object_id_field":metadata.get("objectIdField")}
(out/"itd-rwis-schema.json").write_text(json.dumps(info,indent=2)+"\n")
sample=get(BASE+"/query",{"where":"1=1","outFields":"*","returnGeometry":"false","resultRecordCount":3,"f":"json"})
(out/"itd-rwis-sample.json").write_text(json.dumps(sample,indent=2)+"\n")
print("Schema and 3 sample rows saved. Verify station and time fields before bulk download.")
print([x["name"] for x in fields])
