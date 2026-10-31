# Lanark 3D digital twin — phased development

**Status:** foundational architecture only. No verified elevation mesh or georeferenced aerial orthomosaic has been produced yet.

## Data hierarchy
1. `data/source-manifest.json`: source catalog and provenance.
2. `data/parcel21-preliminary.geojson`: user GPS approximations; NOT surveyed.
3. `data/cabin-concept.geojson`: future proposed footprints; separate from measured geometry.
4. `data/terrain/`: USGS 3DEP clipped DEM, derived mesh, hillshade, slope and aspect; **not yet populated**.
5. `data/imagery/`: selected orthophotos and georeferenced aerial assets; **not yet populated**.
6. `data/flights/`: flight metadata, camera pose estimates and frame indexes; **not yet populated**.
7. `viewer/`: future interactive 3D viewer; do not present placeholder terrain as measured.

## Intake protocol
Add one flight or photo set at a time. Preserve original filenames, capture timestamps, camera position/heading when known, source, license, hash, and georeferencing confidence. Never warp the source photo or assert corner positions from visual resemblance alone. Annotate approximate versus verified geometry.

## Accuracy gates
A. Official parcel GIS polygon matched to PIN RP13S43E185400.
B. Real USGS 3DEP DEM clipped with a buffer around parcel.
C. Check terrain vertical datum, resolution and elevations.
D. Create scale-correct mesh and roads.
E. Position 16×20 ft cabin footprints and cul-de-sac only as conceptual features.
F. Register imagery to ground control and validate residual errors before texture mapping.

## Deployment
Existing 2D `index.html` stays the public entrypoint. A future 3D viewer can be hosted at `/3d/viewer/` once measured terrain is available. GitHub Pages is public: do not publish private family imagery or sensitive information without review.
