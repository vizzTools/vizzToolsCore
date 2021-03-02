# vizzToolsCore

`vizzToolsCore` is a set of standardized Data Structure definitions as JSON Schema each with an HTML page for easy linking, for example using JSON-LD, and a Python client library for interacting with the data structures. Currently, this project is under early development. See the [Data model documentation](https://vizztools.github.io/vizzToolsCore/)

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

## Design principles

1. The aim of `vizzToolsCore` is provide a standardized set of data structures to facilitate inter-change between various specific vizzTools data processing packages.

1. `vizzToolsCore` ONLY deals with defining data structures. Input and output (IO), as well as transformations, should be dealt with in other packages.

1. Every data structure Class MUST have a JSON-LD example and a JSON Schema. These can be generated from the Python Class or vice versa.

1. `vizzToolsCore` will use a "strict" Type mechanism, based on the standard Types defined in [Pydantic](https://pydantic-docs.helpmanual.io/).

1. The naming of JSON schema Types and properties should attempt to follow the [schema.org style guide](https://schema.org/docs/styleguide.html);

    + Types (or Classes) should be CamelCase.
    + Properties of Types should be snakeCase.

1. When possible always try to reuse Types and properties when creating new Data structures. It is ok to use Types and properites with slightly different meanings within the context of the new Type; just be sure to add a more specific `description` in the JSON Schema.

## Main Data Structure definitions

### Dataset

[`Dataset`](https://vizztools.github.io/vizzToolsCore/Dataset.html) objects define both metadata and configuration information related to a specific [dataset](https://en.wikipedia.org/wiki/Data_set).

Key features:

+ `Dataset` objects are an interface for documenting and interacting with remote and local resources. They define the origin and format information about the dataset, rather than actual the data itself. The actual data may be in variety of formats (see [dataProviders](https://vizztools.github.io/vizzToolsCore/json-schema/dataProviders)).
+ The primary purpose of a `Dataset` is to easily maintain metadata and traceability during data processing Actions, and enable standardized transfer of information between libraries and services.
+ `Dataset` methods ONLY deal with transformations of Data structures; it is intended to be used by other libraries and services to keep track of changes in dataset metadata and configurations.
+ `Dataset` is represented as `JSON-LD`, allowing the context of each Type and property to be linked to URIs.
+ `Dataset` is agnostic to the type or format of the data, it only stores the necessary configuration information required for other libraries to access the data.

#### Dataset object

Below is the structure of a `Dataset` object, which is an adaptation of the schema.org [Dataset](schema.org/Dataset) following the [Google structured data Dataset guidelines](https://developers.google.com/search/docs/data-types/dataset). A number of non-standard properties are also used; such as `dataProviders`, `lineage`, and `visualization`, which are explained in more detail below.

Whilst `Dataset` objects allow extensive metadata descriptions, the minimum requirements are `@type`, which must be "Dataset" and `@id`, the unique identifer for the dataset. This may be any string value; we recommend using unique, lower-case, 'slugs' based on the dataset provider, name, and version e.g., "gmw-mangrove-total-carbon-version-1-0-0" or a DOI. We also automatically add `sdPublisher`, which represents the Organization (or Person) who creates this structured data object, as well as `dateCreated` and `dateModified` both set by the system.

Details about the other (optional) properties can be found in the [data model documentation](https://vizztools.github.io/vizzToolsCore/), and via in the examples below.

> Example JSON-LD

```json
{
    "$schema": "https://vizztools.github.io/vizzToolsCore/json-schema/Dataset.schema.json",
    "@context": "https://vizztools.github.io/vizzToolsCore",
    "@id": "gmw-mangrove-total-carbon-version-1-0-0",
    "@type": "Dataset",
    "name": "Example collection",
    "description": "The summary must be between 50 and 5000 characters long. The summary may include Markdown syntax. Embedded images need to use absolute path URLs (instead of relative paths). When using the JSON-LD format, denote new lines with two characters: backslash and lower case letter 'n'.",
    "alternateName": "Example version 0.0.1",
    "citation": "Identifies academic articles that are recommended by the data provider be cited in addition to the dataset itself.",
    "creator": [
        {
            "@id": "https://orcid.org/0000-0002-5011-6744",
            "@type": "Person",
            "name": "Edward P. Morris",
            "affiliation": "Vizzuality, Madrid, Spain",
            "sameAs": "https://orcid.org/0000-0002-5011-6744"
        },
        {
            "@id": "https://ror.org/02a809t02",
            "@type": "Organization",
            "name": "Vizzuality",
            "sameAs": "https://ror.org/02a809t02"
        }
    ],
    "dataProviders": [
        {
            "name": "CSV",
            "type": "feature",
            "data": "file:///tests/data/obs.csv",
            "id_field": "id",
            "x_field": "long",
            "y_field": "lat"
        }
    ],
    "dateCreated": "2020-10-18T20:48:57Z",
    "dateModified": "2020-10-18T20:48:57Z",
    "datePublished": "2018-05-08",
    "distribution": [
        {
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
        }
    ],
    "funder": [
        {
            "@id": "https://ror.org/02a809t02",
            "@type": "Organization",
            "name": "Vizzuality",
            "sameAs": "https://ror.org/02a809t02"
        }
    ],
    "identifier": "https://doi.org/XXXXXX",
    "inLanguage": "en",
    "isBasedOn": "https://doi.org/XXXXXX",
    "keywords": [
        "keyword1",
        "keyword2",
        "keyword3"
    ],
    "license": "https://creativecommons.org/licenses/by/4.0",
    "measurementTechnique": "The technique, technology, or methodology used in a dataset, which can correspond to the variable(s) described in variableMeasured.",
    "provider": [
        {
            "@id": "https://ror.org/02a809t02",
            "@type": "Organization",
            "name": "Vizzuality",
            "sameAs": "https://ror.org/02a809t02"
        }
    ],
    "sameAs": "https://doi.org/XXXXXX",
    "sdPublisher": [
        {
            "@id": "https://ror.org/02a809t02",
            "@type": "Organization",
            "name": "Vizzuality",
            "sameAs": "https://ror.org/02a809t02"
        }
    ],
    "spatialCoverage": "Global tropics",
    "temporalCoverage": "1950-01-01/2013-12-18",
    "thumbnailUrl": "https://dataset-thumbnail.jpeg",
    "unitText": "t OC / ha",
    "url": "https://zenodo.org/XXXXXX",
    "variableMeasured": "The variable that this dataset measures. For example, temperature or pressure.",
    "version": "0.0.1"
}
```

## How to use

You can use the JSON schemas, for example during linting or validation by adding the `"$schema"` property to your JSON, such as: 

```json
{
    "$schema": "https://vizztools.github.io/vizzToolsCore/Person.schema.json",
    "name": "Jane Doe"
}
```

If you would like to check the definition of a property visit the [HTML site](https://vizztools.github.io/vizzToolsCore) adding the type or property name to the URL. If creating new JSON schema it can be useful to use these core models via referencing, such as;

```json
{
    "artist": {
        "$ref": "https://vizztools.github.io/vizzToolsCore/Person.schema.json",
        "description": "A person who makes creative things"
        }
}
```

### Installation of the  Python client

To install from PyPi.

```shell
pip3 install vizzToolsCore
```

To build the package using this repository see the build instructions below.

## Getting started

Import the package

```python
import VizzToolsCore as vtc
```

To create a Dataset object:

```python
# Create empty dataset
import json
ds = vtc.dataset_from_dict({"@id": "my-test-dataset"})
print(json.dumps(ds.to_dict(), indent=2, sort_keys=True))
```

To load a JSONLD dataset object from file

```python
# Load JSONLD Dataset
import json
with open("https://vizztools.github.io/vizzToolsCore/jsonld-examples/Dataset.jsonld") as f:
    ds = vtc.dataset_from_dict(json.load(f))
    print(json.dumps(ds.to_dict(), indent=2, sort_keys=True))
```

## Build

`VizzToolsCore` is automatically built using JSON schema (`./data/json-schema`); these are intended to be the "single source of truth" for the data structures.

The [data structure documentation site](https://vizztools.github.io/vizzToolsCore) is generated using [`json_schema_for_humans`](https://github.com/coveooss/json-schema-for-humans); using this [script](https://github.com/vizzTools/ci-scripts/blob/master/generate_schema_docs.py). This creates HTML pages for every JSON schema file in `./json-schema`, and adds the JSON schema and JSONLD examples to the site. Configuration of this process can be found in `./docs`.  

Python classes (`./VizzToolsCore/Models.py`) and simple access functions are generated using [`quicktype`](quicktype.io); using this [script](https://github.com/vizzTools/ci-scripts/blob/master/json_schema_to_python.sh). The list of Types to convert is defined in `.data/src-urls.json`; note all properties and objects of higher level objects are converted, however it is often useful to specifically define the order these are passed. Further methods to interact with these base classes are added manually.

Tests are carried out against JSONLD examples (`./data/jsonld-examples`). TODO: Add more info about tests. Finally the updated JSON schema docs and Python package are deployed to `gh-pages` and `PyPi` respectively.

Local build...

The full CI build process is defined by the `.travis.yml` config. Note this relies on [vizzTools common CI scripts](https://github.com/vizzTools/ci-scripts).

## Inspiration (further reading)

+ [pygeoapi](https://pygeoapi.io/)
+ [schema.org](https://schema.org/)
+ [Pydantic](https://pydantic-docs.helpmanual.io/)
+ [JSON Schema](http://json-schema.org/understanding-json-schema/)
+ [JSON-LD](https://json-ld.org/)
+ [quick-type](https://app.quicktype.io/)
+ [Google Dataset JSON-LD](https://developers.google.com/search/docs/data-types/dataset?hl=uk)
+ [CF Standard Names](http://cfconventions.org/standard-names.html)

