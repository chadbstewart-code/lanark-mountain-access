# USGS 3DEP terrain acquisition

Status: download procedure committed; **no DEM has yet been downloaded or validated**.

Official USGS 3DEP image service:
https://elevation.nationalmap.gov/arcgis/rest/services/3DEPElevation/ImageServer

## Workflow

On a computer with internet access:

```bash
python -m pip install requests rasterio numpy
python 3d/scripts/fetch_terrain.py
python 3d/scripts/terrain_to_mesh.py 3d/data/terrain/lanark_3dep.tif
```

This requests a buffered WGS84 raster around the approximate parcel and produces a mesh JSON. The bounding box is deliberately larger than the parcel to include nearby ridges and road approaches. It does **not** establish legal boundaries.

## Validation before publication
- Confirm request succeeded and raster CRS, nodata, source resolution and vertical datum.
- Compare representative elevations with official USGS point queries.
- Verify mesh XY spacing in meters, elevation range and vertical exaggeration = 1.
- Compare parcel and roads against imagery, then publish viewer after validation.
- Never commit huge source DEMs blindly; GitHub may require Git LFS or external object storage.

The USGS image service provides interpolated elevation, not surveyed construction elevations. If the source returns a non-TIFF error or missing data, do not substitute made-up heights.

Next: validate DEM and build interactive Three.js terrain viewer with camera presets, parcel overlay, roads and accurately scaled 16×20 ft cabin placeholders.
