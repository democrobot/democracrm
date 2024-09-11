# Data Source

## Description

The `data.ImportDataSource` model defines a third-party data source that is imported into the platform and used as part
of other database models. This model is responsible for documenting and managing the data source, and works with the
`data.ImportDataSet` model to track and control the lifecycle of the data source.

It can specify either a bulk upload source from a local directory or a Web API source from a remote URL. For both bulk
upload and Web API sources, a subdirectory of `BASE_DIR/data/imports` must be assigned to this source, from which individual
uploads can be stored and imported.

This directory will be monitored for new files with a specific file type, which can be specified as CSV, JSON, or Zip files.
For each new file added, the `data.ImportDataSource` model will create a `data.ImportDataSet` record and indicate that
updates are available for import from that data source.

## Fields

### Name

###
