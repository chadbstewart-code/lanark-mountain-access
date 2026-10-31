# Parcel 21 preliminary terrain, canopy and wind exposure analysis

Date: 2026-10-31. Derived from committed USGS 3DEP terrain mesh `3d/viewer/terrain.json` and owner approximate GPS polygon `3d/data/parcel21-preliminary.geojson`. No legal parcel survey, lidar canopy-height raster or site-specific wind measurements have been incorporated.

## Terrain sampling method
160×160 grid; 877 interior sample cells after polygon mask. Slope from central differences of adjacent mesh elevations in horizontal meters. Resolution is roughly 14m east-west ×19m north-south; small pads, ditches and trees are not resolved.

## Preliminary parcel figures
- Sample elevation min: 2064.62 m (~6774 ft); max: 2129.41 m (~6986 ft); difference ~64.79 m (~213 ft).
- Median sampled slope: 9.9185 degrees (~17.5% grade).
- Slope <5°: 131/877 (14.9%).
- Slope 5–10°: 315/877 (35.9%).
- Slope 10–15°: 247/877 (28.2%).
- Slope >=15°: 184/877 (21.0%).
- Aspect bins (approximate counts): N 220, NE 133, E 59, SE 155, S 219, SW 35, W 18, NW 38. Aspect near-flat terrain is inherently unstable; treat bins cautiously.

## Tree cover
Owner aerial photographs/video show mixed open and wooded terrain, but **no tree positions or canopy heights have been georeferenced or measured**. Do not label individual trees or canopy boundaries as verified. Next: acquire suitable aerial orthophoto and, if available, lidar point cloud/canopy-height model; digitize canopy polygons and compare against owner footage.

## Windward/leeward
A ridge is generally windward on its upwind face and leeward on its downwind face, but actual exposure depends on incoming wind direction, season, channeling and local topography. **No verified local wind rose or site anemometer record** yet. Next: retrieve representative station winds with coordinates/elevation, assess representativeness, and compute direction-specific topographic shelter indices (e.g., N, NE, E, SE, S, SW, W, NW). Do not use generic regional winds as a definitive parcel wind direction.

## Design implication
Screen contiguous gentle terrain near existing road for 4–8 clustered cabins and a cul-de-sac; optimize water-main lengths and account for septic setbacks, drainage, snow, wind and wildfire exposure. No site approved or selected.

## Source limitations
All numbers are exploratory, based on approximate parcel geometry and resampled elevation mesh, not a field topographic survey. Recompute once county polygon and higher-resolution DEM are available.
