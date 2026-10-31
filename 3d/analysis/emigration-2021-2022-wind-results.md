# Emigration Canyon wind archive — first quantified results

Computed 2026-10-31 from ITD historical RWIS station 10021. Source data and script:
- `3d/data/weather/emigration-10021-wind-raw.json`
- `3d/data/weather/emigration-10021-wind-summary.json`
- `3d/scripts/analyze_emigration_winds.py`

## Coverage and cleaning
46,920 records retrieved; 45,973 unique UTC timestamps after 947 duplicate timestamps removed. Historical coverage 2021-04-05 to 2022-08-11. 95th-percentile available gust 22.6 mph. **Not a design wind speed or long-term climate normal.**

## Direction frequency (meteorological FROM direction)
N 2,835 (6.2%), NE 1,261 (2.7%), E 1,884 (4.1%), SE 5,328 (11.6%), S 3,462 (7.5%), SW 4,237 (9.2%), W 12,511 (27.2%), NW 14,455 (31.4%). Denominator 45,973 unique records. W+NW = 58.7% of observations.

## Strong gust counts (gust >= 22.6 mph; counted by mean wind direction)
N 7, NE 3, E 1, SE 49, S 251, SW 402, W 1,044, NW 577. W is most common high-gust direction. Note: this script bins by `winddirectiondeg`, not `maxwinddirectiondeg`, so it describes prevailing direction during high-gust observations, not necessarily instantaneous gust bearing.

## Seasonal high-gust leading directions
- Winter: W 278, SW 110, NW 68
- Spring: W 430, NW 339, S 136
- Summer: W 199, SW 146, NW 132
- Fall: W 137, NW 38, SW 24

## Limitations and next analysis
- Verify sensor heights, station siting, missing intervals and coverage before claiming climatological representativeness.
- 2021–2022 only; incomplete years and seasonal imbalance.
- Separate wind direction during gust events from instantaneous gust direction when `maxwinddirectiondeg` is valid.
- Pin cabin candidate A and B geographic coordinates, then weight terrain shelter by directional gust-event frequencies.
- Georeference conifer stand and measure canopy height before predicting tree windbreak effect.
- Use on-property instruments to validate local flow.

Conclusion: West and northwest directions dominate this station's observed record; west leads high-gust events. Does not prove Site A or B windstorm-safe.
