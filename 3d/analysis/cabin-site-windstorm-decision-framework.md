# Lanark cabin site windstorm decision framework

Status: awaiting verified Emigration Canyon historical wind summary. No A/B site coordinates have yet been saved to the repository. Do not fabricate rankings.

## Inputs
- USGS 3DEP terrain mesh and directional terrain-horizon screening.
- ITD Emigration Canyon station 10021, 2021-04-05 to 2022-08-11, archive in process.
- Owner observations: Site A red circle almost always sheltered; Site B green circle usually sheltered. Coordinates pending.
- Conifer stand marked by owner in aerial photograph. No verified tree height or polygon.
- Owner reports frequent downslope west-to-east winds.

## Calculation plan
1. Deduplicate wind observations by timestamp and report missing intervals.
2. Compute sector frequencies by season, nighttime/daytime, and high-gust subset.
3. Pin A/B geographic coordinates from 3D viewer. Reject comparisons without pins.
4. Sample directional terrain index at each pin. Do not interpret it as a wind-speed percentage.
5. Use gust-direction frequencies as scenario weights for screening; disclose station transferability uncertainty.
6. Add canopy-height and windbreak-distance screening only when stand polygon and lidar heights are available.
7. Compare slope, drainage, treefall setbacks, snow drifting, wildfire exposure and access before choosing a site.

## Stop conditions
No exact site coordinates: cannot calculate site-specific scores.
No reliable gust directions: cannot weight storm scenarios.
No canopy heights: cannot quantify tree shelter.
No site wind loggers: cannot claim measured wind-speed reductions or storm safety.

## Outputs to build
- Seasonal wind rose and strongest-gust direction chart.
- A/B directional table with terrain-only shelter indices and evidence confidence.
- 3D overlay distinguishing observed sheltered sites from model estimates.
- Site measurement protocol: 2 candidate sensors + 1 exposed reference, comparable heights and sampling cadence.
