# Data Integration Plan

A key aspect of the platform will be the need to regularly ingest third-party day for use as models within the database.
This includes:

- Governing body records (legislative and executive; possibly judicial at some point)
- Legislative session records (committees, bills, votes)
- Voter records (ideally the entire state)
- Campaign finance records
- Lobbying registration and activity records
- Geographic boundaries (initially state legislative districts, as well as state borders and other base map details)

## Data Integration Roadmap

### Phase One

The initial focus is exclusively on (1) the development and launch of the platform and (2) field testing of the
platform in Pennsylvania, and the data for the first phase of development will be sourced from:

- [PA General Assembly website](https://www.palegis.us) for governing body data. The site is under redevelopment and
provides new RSS feeds of some of this information. The initial scrapers are functional as well.
- [Plural Policy (formerly Open States)](https://pluralpolicy.com/) for legislative session (and possibly also governing body) data.
- [PA Department of State website](https://www.pavoterservices.pa.gov/Pages/PurchasePAFullVoterExport.aspx) for full exports
of voter registration data. This data appears to be published weekly, and will likely be refreshed in the platform
quarterly.
- [PA Department of State website](https://www.pa.gov/en/agencies/dos/resources/voting-and-elections-resources/campaign-finance-data.html) for campaign finance data.
- [PA Department of State website](https://www.electionreturns.pa.gov/) for official election returns.
for political campaign finance reports.
- [PA Department of State website](https://www.pa.gov/en/services/dos/search-lobbying-disclosure-reports.html)
for lobbying registration and expense report exports. Searchable online database
[available here](https://www.palobbyingservices.pa.gov/Public/wfSearch.aspx).
- [Pennsylvania Spatial Data Access website](https://www.pasda.psu.edu/) for state boundaries (using recent redistricting maps),
and possibly [Mapbox](https://www.mapbox.com) for base map details.

### Phase Two

The next steps after Pennsylvania will be developed in coordination with partners in other states in 2025.
