#!/usr/bin/env python3
"""Discover Emigration Canyon station IDs and coverage in ITD historical RWIS.
Do not confuse station names with the IEM ITDD4 code.
"""
import requests,json,pathlib,datetime
BASE="https://gisp.itd.idaho.gov/hosting/rest/services/Hosted/RWIS_HistoricData/FeatureServer/0/query"
out=pathlib.Path("3d/data/weather");out.mkdir(parents=True,exist_ok=True)
def query(params):
 r=requests.get(BASE,params={"f":"json",**params},timeout=90);r.raise_for_status();j=r.json()
 if "error" in j:raise RuntimeError(str(j["error"]))
 return j
names=query({"where":"UPPER(stationname) LIKE '%EMIGR%'","outFields":"stationid,stationname","returnDistinctValues":"true","returnGeometry":"false","orderByFields":"stationid"})
stations=[f["attributes"] for f in names.get("features",[])]
report={"retrieved_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"source":BASE,"search":"UPPER(stationname) LIKE '%EMIGR%'","stations":[]}
for station in stations:
 sid=station["stationid"]
 where=f"stationid = {int(sid)}"
 count=query({"where":where,"returnCountOnly":"true","returnGeometry":"false"}).get("count")
 stats=query({"where":where,"outStatistics":json.dumps([
 {"statisticType":"min","onStatisticField":"sensorvaluedatetimeutc","outStatisticFieldName":"first_utc"},
 {"statisticType":"max","onStatisticField":"sensorvaluedatetimeutc","outStatisticFieldName":"last_utc"},
 {"statisticType":"count","onStatisticField":"maxwindspeedmph","outStatisticFieldName":"gust_values"}
 ]),"returnGeometry":"false"})
 report["stations"].append({**station,"records":count,"coverage":stats.get("features",[{}])[0].get("attributes",{})})
(out/"emigration-station-discovery.json").write_text(json.dumps(report,indent=2)+"\n")
print(json.dumps(report,indent=2))
if not stations:raise RuntimeError("No matching Emigration station in this table; do not proceed to climatology.")
