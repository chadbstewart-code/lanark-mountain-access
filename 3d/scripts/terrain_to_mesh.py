#!/usr/bin/env python3
"""Convert georeferenced DEM into lightweight mesh JSON for browser 3D viewer.
Requires: pip install rasterio numpy
Uses geographic degrees projected to local meters (equirectangular at parcel latitude).
"""
import argparse,json,pathlib,math
import numpy as np
import rasterio
from rasterio.enums import Resampling
def main():
 p=argparse.ArgumentParser()
 p.add_argument("dem");p.add_argument("--output",default="3d/viewer/terrain.json")
 p.add_argument("--grid",type=int,default=160)
 args=p.parse_args()
 if not 8<=args.grid<=400:p.error("grid must be 8..400")
 with rasterio.open(args.dem) as ds:
  if ds.crs is None or ds.crs.to_epsg()!=4326:
   raise RuntimeError("Expected WGS84 EPSG:4326 DEM; reproject before conversion")
  arr=ds.read(1,out_shape=(args.grid,args.grid),resampling=Resampling.bilinear,masked=True)
  if np.ma.count_masked(arr):raise RuntimeError("DEM has missing cells; choose valid bounds or fill explicitly")
  bounds=ds.bounds
  elevations=np.asarray(arr,dtype=float)
  center_lat=(bounds.top+bounds.bottom)/2;center_lon=(bounds.left+bounds.right)/2
  mx=111320*math.cos(math.radians(center_lat));my=111132
  vertices=[]
  for i in range(args.grid):
   lat=bounds.top-(bounds.top-bounds.bottom)*i/(args.grid-1)
   for j in range(args.grid):
    lon=bounds.left+(bounds.right-bounds.left)*j/(args.grid-1)
    vertices.append([round((lon-center_lon)*mx,2),round(float(elevations[i,j]),2),round((center_lat-lat)*my,2)])
  payload={"source":str(args.dem),"center_wgs84":[center_lon,center_lat],"grid":args.grid,
           "bounds_wgs84":[bounds.left,bounds.bottom,bounds.right,bounds.top],
           "elevation_min_m":float(elevations.min()),"elevation_max_m":float(elevations.max()),
           "vertices_m":vertices,"vertical_exaggeration":1,"measured":True}
  dest=pathlib.Path(args.output);dest.parent.mkdir(parents=True,exist_ok=True)
  dest.write_text(json.dumps(payload,separators=(",",":")))
  print("Wrote",dest,"with",len(vertices),"vertices")
if __name__=="__main__":main()
