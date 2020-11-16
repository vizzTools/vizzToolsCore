#!/bin/bash

# Set the JSON schema source urls JSON path
# This should be of the form: 
#   {"<Type>": ["<schema-path>"], "<Type>": ["<schema-path>"]}
# where `Type` is the tope-level Type or Class name, and schema-path is a file or URL path.
# Note if using files, references ($ref) must be in same directory
# Note parsing only the top-level Type usually provides 
SCHEMA_SRC_URLS="src-urls.json" 

# Set the directory to add the generated Python code
# all Types will be added to a single file, Models.py
# and the __init__.py file updated to load all Types
CODE_DIR=./vizzToolsCore

# Update __init__.py
# TODO: add automatic semantic version
echo "from .Models import  *" >> $CODE_DIR/"__init__.py"

# Convert JSON schema to Python code
quicktype \
    --alphabetize-properties \
    --python-version 3.7 \
    --src-lang schema \
    --src-urls src-urls.json \
    -l py \
    -o $CODE_DIR/Models.py
echo "Code written to $CODE_DIR/Models.py"