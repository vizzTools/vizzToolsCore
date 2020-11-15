#!/bin/bash

# Get the working directory
#DIR="$(dirname "${BASH_SOURCE[0]}")"  # get the directory name
#DIR="$(realpath "${DIR}")"    # resolve its full path if need be
#echo $DIR

SCHEMA_DIR="https://vizztools.github.io/vizzToolsCore/json-schema/DataProvider.schema.json"
SCHEMA_EXT=.schema.json
SCHEMA_NAME="DataProvider"
CODE_DIR=./vizzToolsCore
CODE_EXT=.py

# Declare a string array with type
# "Person" "Organization" "PropertyValue" "Place"  "TileProvider" "CoverageProvider" "FeatureProvider" "DataDownload" "GeoCoordinates" "GeoShape" "Iso6391LanguageCodes" "ContactPoint"
#declare -a StringArray=("Dataset")

# Read the array values with space
#for val in "${StringArray[@]}"; do
#rm $CODE_DIR$val$CODE_EXT
#echo "Processing $SCHEMA_DIR"
echo "from .Models import  *" >> $CODE_DIR/"__init__.py"
quicktype \
    --alphabetize-properties \
    --python-version 3.7 \
    --src-lang schema \
    --src-urls src-urls.json \
    -l py \
    -o $CODE_DIR/Models.py
echo "Code written to $CODE_DIR/Models.py"