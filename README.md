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

#### Dataset object

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

#### Links

The [`links`](https://vizztools.github.io/vizzToolsCore/json-schema/links) property is an Array of [`DataDownload`](https://vizztools.github.io/vizzToolsCore/json-schema/DataDownload) objects providing the URLs of the dataset resources, such as a machine-readable version of it's `metadata`, a long text `description`, and individual `data` packages or files.

The aim of this property is to provide URIs to access the original data; usually stored remotely (although it can also be used for local resources). Using these links maybe the first step in a data processing pipeline, were the original data is downloaded and transformed to a standardized format. If the data is already in a suitable format and publicly available it may make more sense to directly define the `dataProviders` property.

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

#### Metadata

A JSON-LD description of the ORIGINAL dataset, using schema.org Dataset, and following the Google Dataset guide. The aim here is to support easy importation and mapping of a limited number of standard metadata formats. This information can be used for getting links to data and for display.

>DISCUSS: Here there is an issue with potentially having the original metadata and metadata after some transformation. Which should be stored here? Maybe just having a link to original could be enough. So far have been thinking that this is a store for the original metadata, often imported from a source and maybe enriched (a bit). Could get messy?

#### dataProviders

A list of DataProvider configuration objects, which follow the structure of `pygeoapi` [resources.providers configuration](https://docs.pygeoapi.io/en/latest/configuration.html#resources). The aim of providers is to store configurations for accessing a (limited) number of optimized data storage formats. The general workflow could be to examine the original datasets, do any pre-processing needed (such as fixing geometries or transformations), add the transformed data to a (remote) storage location, and log the configurations for accessing this optimized data.

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
    }
]
```

>DISCUSS: Do we want ultimate flexibility of data formats or should we aim to limit to a specific types; Table=CSV(Parquet), Features=GeoJSON(MVT), Coverage=GeoTIFF(ZARR)?

#### Context

This is used by `pygeoapi` to give context to fields (properties or variables) in data files. In theory it could be a neat mechanism for reducing ambiguity, and could be linked to "any" describing resource, potentially such as CF standard names. Note it does not imply any validation!

For example, we could define a field in a data file called `datetime` as `https://schema.org/DateTime` by adding an entry like:

```json
{"datetime": "https://schema.org/DateTime"}
```

#### Lineage

The purpose of the `lineage` object is to keep a record of the data processing history of the collection. Here the idea would be that each of process (vizzTool) returns a concise statement about an action applied to the collection object (WHAT, WHEN, WHO). We should also allow custom comments! For example, a user creates the collection, downloads the data from a url, and transforms and repairs a FeatureCollection.

```json
{
    "@context": "https://schema.org",
    "@type": "ItemList",
    "itemListElement": [
        "Collection created at 2020-10-18T20:48:57Z by user 123234.",
        "Data files retrieved from URL at 2020-10-18T20:48:57Z by user 123234.",
        "SHP file converted to GeoJSON, geometries repaired, and exported to URL using VIZZTOOL version X.X.X at 2020-10-18T20:48:57Z by user 123234."
    ],
    "itemListOrder": "https://schema.org/ItemListOrderDescending",
    "name": "Data processing history"
  }
```

### Pseudo user/code examples

#### It's all about the metadata

We would like to include Mangrove soil organic carbon on the Global Mangrove Watch platform, and we find that this dataset is available on [Zenodo](https://zenodo.org/record/2536803).

> How to prepare a dataset stored in a large data repository for query, processing, and web visualization.

Checking the zenodo site we see can see the different linked data resources and get a JSON-LD metadata version of the dataset. Unfortunately, we do not seem to be able to download the JSON-LD metadata; but we can just copy it to file.

Great! Lets fire up our `vizzTools` and make a collection.

```python
import vizzToolsCore as vtc

# Define a basic collection links dict
links = {
    metadata :  {
      "contentUrl": "https://storage.googleapis.com/mangrove_atlas/mangrove-properties/mangroves_SOC30m_0_100cm.jsonld",
      "encodingFormat": "application/jsonld",
      "@type": "DataDownload"
    },
    data :  {
      "contentUrl": "https://zenodo.org/api/files/826b6287-7c3d-4a49-a1d5-cbecb5d0496d/mangroves_SOC30m_0_100cm.zip",
      "encodingFormat": "application/zip",
      "@type": "DataDownload"
    }

# Create a new collection
# metadata file is parsed and is automagically added to `metadata`
collection = vtc.Collection(
    id = "mangrove-soc-30m-tha-0to100cm-version02",
    links = links
)

# Inspect the metadata of our bare-bones collection
collection.metadata.json()
```

> Output

```json
{
    "description": "<p>This is an update of maps produced by&nbsp;<a href=\"https://doi.org/10.1088/1748-9326/aabe1c\">Sanderman et al (2018)</a>. The improvements to the 3D spatial prediction include:</p>\n\n<ul>\n\t<li>\n\t<p>new updated global mangrove coverage map (contact Thomas Worthington),</p>\n\t</li>\n\t<li>\n\t<p>new ALOS-based DEM of the world AW3D30 v18.04,</p>\n\t</li>\n\t<li>\n\t<p>new radar ALOS-based PALSAR radar images of the world,</p>\n\t</li>\n\t<li>\n\t<p>additional SOC points (ca 550) <a href=\"https://static-content.springer.com/esm/art%3A10.1038%2Fs41558-018-0162-5/MediaObjects/41558_2018_162_MOESM2_ESM.xlsx\">published in Rovai et al. (2018)</a>&nbsp;used in model training (see gpkg file).</p>\n\t</li>\n</ul>\n\n<p>To open map in QGIS or similar, drag and drop the &quot;mangroves_dSOC_0_100cm_30m.vrt&quot; file. You can than add also the gpkg file contain the training points.&nbsp;A preview (WMS) of the predictions is available <a href=\"https://www.arcgis.com/apps/MapSeries/index.html?appid=fe214a492f114bde8b3aa1d54ef23224\">here</a>.</p>\n\n<p>Production steps (ensemble predictions using SuperLearner) are explained in detail at:&nbsp;</p>\n\n<ul>\n\t<li>R code:&nbsp;<a href=\"https://github.com/whrc/Mangrove-Soil-Carbon/\">https://github.com/whrc/Mangrove-Soil-Carbon/</a>&nbsp;(see &quot;R_code/GMW_mangroves_SOC_30m.R&quot;)</li>\n\t<li>Tutorial:&nbsp;<a href=\"https://envirometrix.github.io/PredictiveSoilMapping/soilmapping-using-mla.html#ensemble-predictions-using-superlearner-package\">&quot;Predictive Soil Mapping with R&quot;</a></li>\n</ul>\n\n<p>Produced&nbsp;for the purpose of Mangrove Restoration Potential Map funded by The&nbsp;Nature Conservancy and IUCN. Contact TNC: Emily Landis&nbsp;&lt;<a href=\"mailto:elandis@TNC.ORG\">elandis@TNC.ORG</a>&gt;.&nbsp;Contact IUCN / University of Cambridge: Thomas Worthington &lt;<a href=\"mailto:taw52@cam.ac.uk\">taw52@cam.ac.uk</a>&gt;.</p>",
    "license": "https://creativecommons.org/licenses/by-sa/4.0/legalcode",
    "creator": [
        {
            "affiliation": "Envirometrix Ltd",
            "@id": "https://orcid.org/0000-0002-9921-5129",
            "@type": "Person",
            "name": "Tomislav Hengl"
        }
    ],
    "url": "https://zenodo.org/record/2536803",
    "datePublished": "2018-10-23",
    "version": "0.2",
    "keywords": [
        "mangroves",
        "soil carbon",
        "machine learning",
        "superlearner package"
    ],
    "@context": "https://schema.org/",
    "distribution": [
        {
            "contentUrl": "https://zenodo.org/api/files/826b6287-7c3d-4a49-a1d5-cbecb5d0496d/mangroves_SOC30m_0_100cm.zip",
            "encodingFormat": "zip",
            "@type": "DataDownload"
        },
        {
            "contentUrl": "https://zenodo.org/api/files/826b6287-7c3d-4a49-a1d5-cbecb5d0496d/mangroves_SOC_points.gpkg",
            "encodingFormat": "gpkg",
            "@type": "DataDownload"
        },
        {
            "contentUrl": "https://zenodo.org/api/files/826b6287-7c3d-4a49-a1d5-cbecb5d0496d/preview_mangroves_soil_carbon_QGIS.png",
            "encodingFormat": "png",
            "@type": "DataDownload"
        }
    ],
    "identifier": "https://doi.org/10.5281/zenodo.2536803",
    "@id": "https://doi.org/10.5281/zenodo.2536803",
    "@type": "Dataset",
    "name": "Predicted soil organic carbon stock at 30 m in t/ha for 0-100 cm depth global / update of the map of mangrove forest soil carbon"
}
```

Now we want to use the vizzTools to download the data, transform it into a standard format, enrich the metadata, push the processed data to (various) remote storage locations, and update our collection with `providers`.

```python

import vizzTools as vtc
import vizzToolsIO as io
import geeUtils

# Download and unpack the zip file to dir "dataset"
ds = io.get(collection.links.data).unpack("dataset")

# Transform and add to Google Earth Engine
gee_collection_params = {
    collection_id: collection.id,
    data_path: ds.path,
    collection_metadata: collection.metadata
}
# Imagine this does all the adding, and returns a Provider object.
gee_provider_object = geeUtils.addImageCollection(gee_collection_params)

# Add the provider object to the collection
collection = collection.addProvider(gee_provider)

# Export the collection
io.export(collection, "gs://mangrove_atlas/mangrove-properties/mangroves_SOC30m_0_100cm.collection.jsonld")

# Add to an API
# automagically converting to appropriate API payload
io.export(collection, "https://api.resourcewatch.org/v1/dataset")

```

And thats it! We have now pre-processed the dataset using a number of standardized tools, added it to our remote storage solution, and made the configuration available in our favorite API. Time to take *another* coffee.

## Inspiration (further reading)

+ [pygeoapi](https://pygeoapi.io/)
+ [schema.org](https://schema.org/)
+ [Pydantic](https://pydantic-docs.helpmanual.io/)
+ [JSON Schema](http://json-schema.org/understanding-json-schema/)
+ [JSON-LD](https://json-ld.org/)
+ [quick-type](https://app.quicktype.io/)
+ [Google Dataset JSON-LD](https://developers.google.com/search/docs/data-types/dataset?hl=uk)
