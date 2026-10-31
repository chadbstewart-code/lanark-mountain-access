#!/usr/bin/env python3
"""Fetch a georeferenced visual basemap image for the Lanark terrain footprint.
Imagery is a visual reference, NOT an orthomosaic or survey.
"""
import pathlib,requests
BBOX=(-111.495,42.277,-111.468,42.304)
URL="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/export"
out=pathlib.Path("3d/viewer/imagery.jpg")
params={"bbox":",".join(map(str,BBOX)),"bboxSR":"4326","imageSR":"4326","size":"1024,1024","format":"jpg","f":"image"}
r=requests.get(URL,params=params,timeout=90);r.raise_for_status()
if not r.content.startswith(b"\xff\xd8\xff"):raise RuntimeError("Imagery server did not return JPEG: "+r.text[:200])
out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(r.content)
print("Downloaded visual imagery:",len(r.content),"bytes; bounds",BBOX)
