#!/usr/bin/env python3
"""Download USGS 3DEP bare-earth elevation raster for Lanark.
Requires: pip install requests rasterio numpy
Produces a georeferenced GeoTIFF and metadata; never substitutes synthetic terrain.
"""
import argparse, json, pathlib, datetime
import requests
import rasterio
import numpy as np
from rasterio.warp import transform_bounds

SERVICE="https://elevation.nationalmap.gov/arcgis/rest/services/3DEPElevation/ImageServer/exportImage"
DEFAULT_BBOX=(-111.495,42.280,-111.468,42.301)
def main():
 p=argparse.ArgumentParser()
 p.add_argument("--output",default="3d/data/terrain/lanark_3dep.tif")
 p.add_argument("--bbox",nargs=4,type=float,default=DEFAULT_BBOX,metavar=("WEST","SOUTH","EAST","NORTH"))
 p.add_argument("--size",type=int,default=512,help="Raster width and height in pixels")
 args=p.parse_args()
 if args.size<64 or args.size>2048: p.error("size must be 64..2048")
 west,south,east,north=args.bbox
 if not(west<east and south<north):p.error("invalid bbox")
 out=pathlib.Path(args.output);out.parent.mkdir(parents=True,exist_ok=True)
 params={"bbox":",".join(map(str,args.bbox)),"bboxSR":4326,"imageSR":4326,
         "size":f"{args.size},{args.size}","format":"tiff","pixelType":"F32",
         "noData":-9999,"interpolation":"RSP_BilinearInterpolation","f":"image"}
 response=requests.get(SERVICE,params=params,timeout=120)
 response.raise_for_status()
 if not(response.content[:4] in (b"II*\x00",b"MM\x00*")):
  raise RuntimeError("USGS did not return a TIFF: "+response.text[:400])
 out.write_bytes(response.content)
 with rasterio.open(out) as ds:
  if ds.crs is None:raise RuntimeError("Raster lacks CRS; reject until resolved")
  band=ds.read(1,masked=True)
  valid=band.compressed()
  if not valid.size:raise RuntimeError("No valid elevation pixels")
  meta={"source":SERVICE,"retrieved_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "bbox_wgs84":args.bbox,"width":ds.width,"height":ds.height,"crs":str(ds.crs),
        "transform":list(ds.transform)[:6],"vertical_units":"meters (verify raster metadata)",
        "min_m":float(valid.min()),"max_m":float(valid.max()),"valid_pixels":int(valid.size),
        "caution":"Not a construction survey. Confirm vertical datum and source resolution."}
 (out.with_suffix(".json")).write_text(json.dumps(meta,indent=2)+"\n")
 print(json.dumps(meta,indent=2))
if __name__=="__main__":main()
