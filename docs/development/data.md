# Data Integration Plan

A key aspect of the platform will be the need to regularly ingest third-party day for use as models within the database.
This includes:

- Governing body records (legislative and executive; possibly judicial at some point)
- Legislative session records (committees, bills, votes)
- Voter records (ideally the entire state)
- Geographic boundaries (initially state legislative districts, as well as state borders and other base map details)

## Data Integration Roadmap

### Phase One

The initial focus is exclusively on Pennsylvania, and the data sources for the first phase of development will be sourced
from:
- [PA General Assembly website](https://www.palegis.us) for governing body and legislative session records. The site is
under redevelopment and provides new RSS feeds of some of this information. The initial scrapers are functional as well.
- [PA Department of State website](https://www.pavoterservices.pa.gov/Pages/PurchasePAFullVoterExport.aspx) for full exports
of voter registration data. This data appears to be published weekly, and will likely be refreshed in the platform
quarterly.
- [Pennsylvania Spatial Data Access website] for state boundaries (using recent redistricting maps), and Mapbox for base map
details.
