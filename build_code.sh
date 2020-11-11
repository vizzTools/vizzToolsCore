#!/bin/bash

# Get the working directory
#DIR="$(dirname "${BASH_SOURCE[0]}")"  # get the directory name
#DIR="$(realpath "${DIR}")"    # resolve its full path if need be
#echo $DIR

SCHEMA_DIR=./json-schema/
SCHEMA_EXT=.schema.json
CODE_DIR=./vizzToolsCore/
CODE_EXT=.py

# Declare a string array with type
declare -a StringArray=("Dataset" "Person" "Organization" "PropertyValue" "Place"  "TileProvider" "CoverageProvider" "FeatureProvider" "DataDownload" "DataProvider" "GeoCoordinates" "GeoShape" "Iso6391LanguageCodes" "ContactPoint")

# Read the array values with space
for val in "${StringArray[@]}"; do
    #rm $CODE_DIR$val$CODE_EXT
    echo "Processing $val"
    echo "from .$val import  $val" >> $CODE_DIR"__init__.py"
    quicktype -s schema $SCHEMA_DIR$val$SCHEMA_EXT -o $CODE_DIR$val$CODE_EXT
done
