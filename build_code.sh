#!/bin/bash
quicktype -s schema json-schema/VtcDataset.schema.json -o vizzToolsCore/VtcDataset.py
quicktype -s schema json-schema/Dataset.schema.json -o vizzToolsCore/Dataset.py
quicktype -s schema json-schema/Person.schema.json -o vizzToolsCore/Person.py
quicktype -s schema json-schema/Organization.schema.json -o vizzToolsCore/Organization.py
quicktype -s schema json-schema/PropertyValue.schema.json -o vizzToolsCore/PropertyValue.py
quicktype -s schema json-schema/Place.schema.json -o vizzToolsCore/Place.py
quicktype -s schema json-schema/TileProvider.schema.json -o vizzToolsCore/TileProvider.py
quicktype -s schema json-schema/CoverageProvider.schema.json -o vizzToolsCore/CoverageProvider.py
quicktype -s schema json-schema/FeatureProvider.schema.json -o vizzToolsCore/FeatureProvider.py