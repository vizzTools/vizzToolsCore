# vizzToolsCore

`vizzToolsCore` is set of standardized Data Structure definitions with a Python library interface.

Currently this is a under early development.

See the [Data model documentation](https://vizztools.github.io/vizzToolsCore/)

## Roadmap

~~+ add JSON schema of vtcDataset~~
+ add JSON-LD examples
+ convert to Pydantic
+ add methods
  + export
  + convert
  + add_links
  + add_metadata
  + get_user_config
+ add Visualization object?
+ add Lineage object?

## Design principles (draft)

1. The aim of `vizzToolsCore` is provide a standardized set of data structures to facilitate inter-change between various specific vizzTools data processing packages.

1. `vizzToolsCore` ONLY deals with defining data structures. Input and output (IO), as well as transformations, should be dealt with in other packages.

1. Every data structure Class MUST have a JSON-LD example and a JSON Schema. These can be generated from the Python Class or vice versa.

1. `vizzToolsCore` will use a "strict" Type mechanism, based on the standard Types defined in [Pydantic](https://pydantic-docs.helpmanual.io/).

1. The naming of JSON schema Types and properties should attempt to follow the [schema.org style guide](https://schema.org/docs/styleguide.html);

    + Types (or Classes) should be CamelCase.
    + Properties of Types should be snakeCase.

1. When possible always try to reuse Types and properties when creating new Data structures. It is ok to use Types and properites with slightly different meanings within the context of the new Type; just be sure to add a more specific `description` in the JSON Schema.

## Main Data Structure definitions

### VtcDataset

[`VtcDataset`](https://vizztools.github.io/vizzToolsCore/json-schema/VtcDataset.html) objects define configuration information related to a specific [dataset](https://en.wikipedia.org/wiki/Data_set).

Key features:

+ `VtcDataset` objects are an interface for documenting and interacting with remote and local resources. They define the origin and format information about the dataset, rather than actual the data itself. The actual data may be in variety of formats (see [dataProviders](https://vizztools.github.io/vizzToolsCore/json-schema/dataProviders)).
+ The primary purpose of a `VtcDataset` is to easily maintain metadata and traceability during data processing Actions, and enable standardized transfer of information between libraries and services. 
+ `VtcDataset` methods ONLY deal with transformations of Data structures; it is intended to be used by other libraries and services to keep track of changes in dataset metadata and configurations.
+  `VtcDataset` is represented as `JSON-LD`, allowing the context of each Type and property to be linked to URIs.
+ `VtcDataset` is agnostic to the type or format of the data, it only stores the necessary configuration information required for other libraries to access the data.
+ `io.export()` manages the metadata, rather than the data itself. The data first has to be uploaded to GEE (in this step we create provider metadata). Then the io.export() saves this metadata along with the reference to this provider in the RW-API or as a json object in cloud storage.

#### VtcDataset object

Below is the basic top-level structure of a `VtcDataset` object, which uses [JSON-LD](https://json-ld.org/) to provide context to the meaning of each property i.e., to find the definition of a property just follow the link.

`@type` MUST be "VtcDataset" and `@id` is the unique identifer for the dataset. This can be any string value; we recommend using unique, lower-case, 'slugs' based on the dataset provider, name, and version e.g., "gmw-mangrove-total-carbon-version-1-0-0".

`sdPublisher` represents the Organization (or Person) who creates this structured data object; default values for this can set in the `vtc_config` [TODO:implement this]. `dateCreated` and `dateModified` are automatically set by the system.

The other (optional) properties are objects, which are described in detail below.

> Example JSON-LD

```json
{
            "$schema": "https://vizztools.github.io/vizzToolsCore/json-schema/VtcDataset",
            "@context": "https://vizztools.github.io/vizzToolsCore/json-schema",
            "@type": "VtcDataset",
            "@id": "gmw-mangrove-total-carbon-version-1-0-0",
            "sdPublisher": {
                "@type": "Organization",
                "@id": "https://ror.org/02a809t02",
                "sameAs": "https://ror.org/02a809t02",
                "name": "Vizzuality"
            },
            "dateCreated": "2020-10-18T20:48:57Z",
            "dateModified": "2020-10-18T20:48:57Z",
            "links": {},
            "metadata": {},
            "dataProviders": {}
}
```

#### links

The [`links`](https://vizztools.github.io/vizzToolsCore/json-schema/links) property is an Array of [`DataDownload`](https://vizztools.github.io/vizzToolsCore/json-schema/DataDownload) objects providing the URLs of the dataset resources, such as a machine-readable version of it's `metadata`, a long text `description`, and individual `data` packages or files.

The aim of this property is to provide URIs to access the original data; usually stored remotely (although it can also be used for local resources).

An example workflow could be to use these links to download the original data, and then transform the data to a standardized format. They may also enable access to metadata and extended written documentation, which can be incorporated into the objects `metadata`.

Note, if the data is already in a suitable format, ready to use, and publicly available it may make more sense to directly define any number of [`DataProvider`](https://vizztools.github.io/vizzToolsCore/json-schema/DataProvider.html) objects in the `dataProviders` property.

> Example JSON-LD

```json
 [
            {
                "@type": "DataDownload",
                "name": "Description",
                "contentUrl": "https://zenodo.org/api/files/8399ce4c-250d-4d89-bebb-cdc43afe8ead/data description.docx",
                "encodingFormat": "application/docx"
            },
            {
                "@type": "DataDownload",
                "name": "Metadata",
                "contentUrl": "https://zenodo.org/record/1346097/export/schemaorg_jsonld",
                "encodingFormat": "application/html"
            },
            {
                "contentUrl": "https://zenodo.org/api/files/8399ce4c-250d-4d89-bebb-cdc43afe8ead/input_maps.zip",
                "encodingFormat": "zip",
                "@type": "DataDownload",
                "name": "Data"
            },
            {
                "contentUrl": "https://zenodo.org/api/files/8399ce4c-250d-4d89-bebb-cdc43afe8ead/input_tables.zip",
                "encodingFormat": "zip",
                "@type": "DataDownload",
                "name": "Data"
            }
        ]
```

#### metadata

An Array of [Google Dataset](https://developers.google.com/search/docs/data-types/dataset?hl=uk) [schema.org](https://schema.org/) [`DataSet`](https://vizztools.github.io/vizzToolsCore/json-schema/DataSet.html) metadata objects.

The aim of this property is to store metadata about the specific dataset. At present this is only `DataSet` objects but could be extended to other structures. Any number of objects maybe stored, hence there maybe different languages, metadata structured-data sources, and potentially versions. There is still an open question as to how best to deal with original metadata objects, and the potentially adjusted metadata object for the `VtcDataset`, hence this property may be adjusted soon.

In terms of the `DataSet` object the minimum required properties are `name` and `description`. A large variety of metadata properties maybe considered, we recommend trying to follow the [Google Dataset guide](https://developers.google.com/search/docs/data-types/dataset?hl=uk). In general the idea is to reuse, harvest and harmonize metadata, reducing the burden on the user.

Please check out the [`DataSet` definitions and examples](https://vizztools.github.io/vizzToolsCore/json-schema/DataSet.html) for more information.

> Example JSON-LD

```json
{
    "$schema": "https://vizztools.github.io/vizzToolsCore/json-schema/Dataset.schema.json",
    "@context": "https://vizztools.github.io/vizzToolsCore/json-schema/",
    "@type": "Dataset",
    "@id": "<collection-id>",
    "name": "Example collection",
    "description": "The summary must be between 50 and 5000 characters long. The summary may include Markdown syntax. Embedded images need to use absolute path URLs (instead of relative paths). When using the JSON-LD format, denote new lines with two characters: backslash and lower case letter 'n'.",
    "version": "0.0.1",
    "datePublished": "2018-05-08",
    "isBasedOn": "https://doi.org/XXXXXX",
    "sameAs": "https://doi.org/XXXXXX",
    "creator": [
        {
            "@type": "Person",
            "@id": "https://orcid.org/0000-0002-5011-6744",
            "sameAs": "https://orcid.org/0000-0002-5011-6744",
            "affiliation": "Vizzuality, Madrid, Spain",
            "name": "Edward P. Morris"
        },
        {
            "@type": "Organization",
            "@id": "https://ror.org/02a809t02",
            "sameAs": "https://ror.org/02a809t02",
            "name": "Vizzuality"
        }
    ],
    "identifier": "https://doi.org/XXXXXX",
    "keywords": [
        "keyword1",
        "keyword2",
        "keyword3"
    ],
    "citation": "Identifies academic articles that are recommended by the data provider be cited in addition to the dataset itself.",
    "license": "https://creativecommons.org/licenses/by/4.0",
    "url": "https://zenodo.org/XXXXXX",
    "inLanguage": "en",
    "alternateName": "Example version 0.0.1",
    "variableMeasured": "The variable that this dataset measures. For example, temperature or pressure.",
    "measurementTechnique": "The technique, technology, or methodology used in a dataset, which can correspond to the variable(s) described in variableMeasured.",
    "unitText": "t OC / ha",
    "spatialCoverage": "Global tropics",
    "temporalCoverage": "1996--2016",
    "thumbnailUrl": "https://dataset-thumbnail.jpeg",
    "provider": {
        "@type": "Organization",
        "@id": "https://ror.org/02a809t02",
        "sameAs": "https://ror.org/02a809t02",
        "name": "Vizzuality"
    },
    "funder": [
        {
            "@type": "Organization",
            "@id": "https://ror.org/02a809t02",
            "sameAs": "https://ror.org/02a809t02",
            "name": "Vizzuality"
        }
    ],
    "distribution": [{
        "@type": "DataDownload",
        "name": "Description",
        "contentUrl": "https://zenodo.org/api/files/8399ce4c-250d-4d89-bebb-cdc43afe8ead/data description.docx", 
        "encodingFormat": "docx"
      }, 
      {
        "@type": "DataDownload",
        "name": "Data",
        "contentUrl": "https://zenodo.org/api/files/8399ce4c-250d-4d89-bebb-cdc43afe8ead/input_maps.zip", 
        "encodingFormat": "zip"
      }] 
}
```

#### dataProviders

An Array of [`DataProvider`](https://vizztools.github.io/vizzToolsCore/json-schema/DataProvider.html) configuration objects, which can be extended to provide configurations for a variety of data formats. 

These are grouped into sub-types based on the OGC definitions of Geospatial data types, and further defined by either the data format or processing library; [`FeatureProvider`](https://vizztools.github.io/vizzToolsCore/json-schema/FeatureProvider.html), [`CoverageProvider`](https://vizztools.github.io/vizzToolsCore/json-schema/CoverageProvider.html), and [`TileProvider`](https://vizztools.github.io/vizzToolsCore/json-schema/TileProvider.html).  

The aim of the `dataProviders` property is to store configurations for accessing a (limited) number of optimized data storage formats.

An example workflow could be to examine the original datasets, do any pre-processing needed (such as fixing geometries or transformations), add the transformed data to a (remote) storage location, and log the `DataProvider` configuration(s) for accessing this optimized data, either in further processing steps or for transfer to an API.

> Example JSON-LD

```json
[
     {
            "type": "feature",
            "name": "CSV",
            "data": "tests/data/obs.csv",
            "id_field": "id",
            "geometry": {
                "x_field": "long",
                "y_field": "lat"
            }
        },
        {
            "type": "feature",
            "name": "GeoJSON",
            "data": "tests/data/obs.json",
            "id_field": "id"
        },
        {
            "type": "feature",
            "name": "Elasticsearch",
            "data": "http://localhost:9200/ne_110m_populated_places_simple",
            "id_field": "id",
            "time_field": "datetimefield"
        },
        {
            "type": "feature",
            "name": "PostgreSQL",
            "data": {
                "host": "127.0.0.1",
                "dbname": "test",
                "user": "postgres",
                "password": "postgres",
                "search_path": [
                    "osm",
                    "public"
                ]
            },
            "id_field": "osm_id",
            "table": "hotosm_bdi_waterways",
            "geom_field": "foo_geom"
        },
        {
            "type": "coverage",
            "name": "rasterio",
            "data": "tests/data/CMC_glb_TMP_TGL_2_latlon.15x.15_2020081000_P000.grib2",
            "options": {
                "DATA_ENCODING": "COMPLEX_PACKING"
            },
            "format": {
                "name": "GRIB",
                "mimetype": "application/x-grib2"
            }
        },
        {
            "type": "coverage",
            "name": "xarray",
            "data": "tests/data/coads_sst.nc",
            "x_field": "lon",
            "time_field": "time",
            "format": {
                "name": "netcdf",
                "mimetype": "application/x-netcdf"
            }
        },
        {
            "type": "coverage",
            "name": "xarray",
            "data": "tests/data/analysed_sst.zarr",
            "format": {
                "name": "zarr",
                "mimetype": "application/zip"
            }
        },
        {
            "type": "tile",
            "name": "MVT",
            "data": "tests/data/tiles/ne_110m_lakes",
            "options": {
                "metadata_format": "raw",
                "zoom": {
                    "min": 0,
                    "max": 5
                },
                "schemes": [
                    "WorldCRS84Quad"
                ]
            },
            "format": {
                "name": "pbf",
                "mimetype": "application/vnd.mapbox-vector-tile"
            }
        }
]
```

## Inspiration (further reading)

+ [pygeoapi](https://pygeoapi.io/)
+ [schema.org](https://schema.org/)
+ [Pydantic](https://pydantic-docs.helpmanual.io/)
+ [JSON Schema](http://json-schema.org/understanding-json-schema/)
+ [JSON-LD](https://json-ld.org/)
+ [quick-type](https://app.quicktype.io/)
+ [Google Dataset JSON-LD](https://developers.google.com/search/docs/data-types/dataset?hl=uk)
+ [CF Standard Names](http://cfconventions.org/standard-names.html)
