# vizzToolsCore

`vizzToolsCore` is an internal Python library to manage some of our the day-to-day tasks.

Currently this is a skeleton under development.

## Design principles (draft)

1. The aim of `vizzToolsCore` is provide a standardized set of data structures to facilitate inter-change between various specific vizzTools data processing packages.

1. `vizzToolsCore` ONLY deals with defining data structures. Input and output (IO), as well as transformations, should be dealt with in other packages.

1. Every data structure Class MUST have a JSON example and a JSON Schema. These can be generated from the Python Class or vice versa.

1. `vizzToolsCore` will use a "strict" Type mechanism, based on the standard Types defined in [Pydantic](https://pydantic-docs.helpmanual.io/).

## Main data structures (draft)

### Dataset

The general aim is not to actually store any data, but provide the configurations needed for other tools to connect to these (remote) data resources. Related to this is the desire to align with 'pygeoapi` so that it is easy to export configurations to services.

To summarise:

- `Dataset` objects are an interface for documenting and interacting with remote resources and are defined with their origin and format information rather than from the data itself. The actual data it refers to can be in a variety of formats.
-  The primary purpose of a `Dataset` is to easily maintain metadata and traceability across services. `Dataset` methods wrap transformations of metadata along with IO operations.
-  `Dataset` methods parse and create `JSON-LD` (we should get used to reading/writing `JSON-LD` to manage datasets or create methods for abstracting this).
-  The `Dataset` is agnostic to the type or format of the data. So the results of `io.get(ds).unpack()` is an object referencing one or more files which may be in multiple formats.
- `io.export()` manages the metadata, rather than the data itself. The data first has to be uploaded to GEE (in this step we create provider metadata). Then the io.export() saves this metadata along with the reference to this provider in the RW-API or as a json object in cloud storage.

#### Dataset object

Below is the basic top-level structure of a `Collection` object, which uses [JSON-LD](https://json-ld.org/) to provide context on the meaning of each property i.e., to find our the definition of a property just follow the link. These can be as specific or general as you like, for example `dateCreated` links to a specific definition, whereas `providers` links to more general documentation.

`@type` MUST be "Collection" and `@id` is the unique identifer for the collection. `sdPublisher` represents the Organization (or Person) who creates this object; it could be a default or derived from a "user config". `dateCreated` and `dateModified` are automatically set by the system.

The other (optional) properties are objects, which are described in detail below.

> DISCUSS: Collection or Dataset?  In OGC circles collection seems to be the standard. "A collection of things". Dataset = "A collection of data items".
> DISCUSS: I favor human readable identifier, but how to ensure these are unique? We could use UUIDs and/or include another `identifier`?.

```json
{
    "@context": {
        "dateCreated": "http://schema.org/dateCreated",
        "dateModified": "http://schema.org/dateModified",
        "sdPublisher": "http://schema.org/sdPublisher",
        "providers": "https://docs.pygeoapi.io/en/latest/configuration.html#resources",
        "context": "https://docs.pygeoapi.io/en/latest/configuration.html#linked-data",
        "metadata": "http://schema.org/dateSet"
    },
    "@type": "Collection",
    "@id": "my-dataset",
    "sdPublisher": "vizzuality.",
    "dateCreated": "2020-10-18T20:48:57Z",
    "dateModified": "2020-10-18T20:48:57Z",
    "links": {},
    "metadata": {},
    "providers": {},
    "context": {},
    "lineage": {}
}
```

#### Links

A object for providing the URLs of the collection `metadata`, `description`, and `data`. The idea would be that using these links you can either import (or at least view and copy) each of the categories. So we could support (via a vizzTool) mapping of some common metadata schemas, which get the metadata from the URL, transform it an add a JSON-ĹD representation to `metadata`. These links would be used to get the data files and (using vizzTools) transform it to a standard format for inclusion into `providers`. If already in a "standard format", this link can be directly transferred to a Provider object. The description is a long detailed description, that is usually a bit annoying to manage in JSON and best edited in text editor.

```json
{
    "description": [
        {
            "@type": "DataDownload",
            "name": "Description",
            "contentUrl": "https://zenodo.org/api/files/8399ce4c-250d-4d89-bebb-cdc43afe8ead/data description.docx",
            "encodingFormat": "application/docx"
        }
    ],
    "metadata": [
        {
            "@type": "DataDownload",
            "name": "Metadata",
            "contentUrl": "https://zenodo.org/record/1346097/export/schemaorg_jsonld",
            "encodingFormat": "application/html"
        }
    ],
    "data": [
        {
            "contentUrl": "https://zenodo.org/api/files/8399ce4c-250d-4d89-bebb-cdc43afe8ead/input_maps.zip",
            "encodingFormat": "zip",
            "@type": "DataDownload",
            "name": "Input maps"
        },
        {
            "contentUrl": "https://zenodo.org/api/files/8399ce4c-250d-4d89-bebb-cdc43afe8ead/input_tables.zip",
            "encodingFormat": "zip",
            "@type": "DataDownload",
            "name": "Input tables"
        },
        {
            "contentUrl": "https://zenodo.org/api/files/8399ce4c-250d-4d89-bebb-cdc43afe8ead/output_global_damage.zip",
            "encodingFormat": "zip",
            "@type": "DataDownload",
            "name": "Output global damage"
        }
    ]
}
```

> DISCUSS: It seems like the first step, get the links to the data. Often this data needs to be manually examined, and then a transformation script made (using vizzTools!). Does the dict structure make sense or does it miss use cases? This is essentially similar to the metadata.distribution field, which does not try and define the link content themes.

#### Metadata

A JSON-LD description of the ORIGINAL dataset, using schema.org Dataset, and following the Google Dataset guide. The aim here is to support easy importation and mapping of a limited number of standard metadata formats. This information can be used for getting links to data and for display.

>DISCUSS: Here there is an issue with potentially having the original metadata and metadata after some transformation. Which should be stored here? Maybe just having a link to original could be enough. So far have been thinking that this is a store for the original metadata, often imported from a source and maybe enriched (a bit). Could get messy?

#### Providers

A list of Provider configuration objects, which follow the structure of `pygeoapi` [resources.providers configuration](https://docs.pygeoapi.io/en/latest/configuration.html#resources). The aim of providers is to store configurations for accessing a (limited) number of optimized data storage formats. The general workflow could be to examine the original datasets, do any pre-processing needed (such as fixing geometries or transformations), add the transformed data to a (remote) storage location, and log the configurations for accessing this optimized data.

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
