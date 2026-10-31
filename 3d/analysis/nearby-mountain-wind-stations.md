# Nearby mountain wind stations — priority evidence

Updated 2026-10-31. Parcel approximate center 42.2905,-111.482. Straight-line distances approximate; station placement and sensor heights need validation.

## Priority 1: Emigration Canyon
- PacifiCorp ITDB9: coordinates 42.3617,-111.4974, roughly 8 km north. Published maximum gust 55.7 mph, 99th percentile 43.18 mph, 95th percentile 35.79 mph; period and instrument metadata not yet confirmed. Source: https://pacificorpweather.com/station/ITDB9
- Idaho Transportation Department ITDD4 (D5 Emigration Canyon): Iowa Environmental Mesonet archives quarter-hourly direction/speed/gust, example 2026-09-14 W/WSW gusts to 33 mph. Source: https://www.mesonet.agron.iastate.edu/sites/obhistory.php?network=ID_RWIS&station=ITDD4
- ITD historical ArcGIS dataset: https://gisp.itd.idaho.gov/hosting/rest/services/Hosted/RWIS_HistoricData/FeatureServer/0
- **Do not assume ITDB9 and ITDD4 share an exact location or sensor.** Verify before merging.

## Secondary: EW3600
- APRS reported location 42.3000,-111.4000, approximately 6.8 km east of parcel. Private station; placement and calibration unknown.
- Source: https://aprs.fi/weather/a/EW3600
- Windfinder statistics page explicitly says no statistical weather data available: https://www.windfinder.com/windstatistics/ew3600_grace_idaho_united_states
- Thus, not yet suitable as sole historical climatology source.

## Mountain weather context
- Emigrant Summit SNOTEL 471: 42°22'N,111°34'W, 7390 ft. Primarily snow, precipitation and temperature; wind sensor availability not verified. https://wcc.sc.egov.usda.gov/nwcc/site?sitenum=471
- Bear Lake Airport K1U7 is lower valley baseline, not primary parcel wind proxy.

## Analysis pipeline next
1. Obtain at least 2-5 years of hourly/15-minute ITDD4 observations where available, plus ITDB9 records if exportable.
2. Verify completeness, duplicate observations, station coordinates/elevation and sensor height.
3. Produce wind roses by season and day/night; separate top 5% gust events from ordinary winds.
4. Compare station directions with owner-observed west-to-east drainage winds and the parcel's measured terrain shelter index.
5. Collect onsite wind measurements at candidate A, B and an exposed reference location before asserting wind-speed reduction.

## Interpretation limits
Wind speed reduction at A/B is not calculated. Nearby stations cannot capture all local ridge turbulence and canopy effects. Do not claim either site storm-safe based solely on terrain heatmap or one station.
