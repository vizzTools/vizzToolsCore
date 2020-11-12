"""Run this to populate the json-schema html docs"""

import os
import shutil
import sys
import json
import yaml
import pprint
from json_schema_for_humans.generate import generate_from_filename, GenerationConfiguration

# Set path when run in docs
sys.path.insert(0, os.path.abspath(".."))

# Define directory names of schema and examples
URL_PATH = "https://vizztools.github.io/vizzToolsCore"
SCHEMA_DIR =  "json-schema"
JSONLD_DIR =  "jsonld-examples"
DOCS_DIR = "docs"

# Make directories in docs
DOCS_SCHEMA_PATH = os.path.join(os.getcwd(), DOCS_DIR, SCHEMA_DIR)
DOCS_JSONLD_PATH = os.path.join(os.getcwd(), DOCS_DIR, JSONLD_DIR)
DOCS_PATH = os.path.join(os.getcwd(), DOCS_DIR)
os.makedirs(DOCS_SCHEMA_PATH, exist_ok=True)
os.makedirs(DOCS_JSONLD_PATH, exist_ok=True)

#schema_includes_dir = os.path.join(os.getcwd(), "docs", "_includes", "json-schema")
#print("schema_includes_dir", schema_includes_dir)
#os.makedirs(schema_includes_dir, exist_ok=True)
#jsonld_includes_dir = os.path.join(os.getcwd(), "docs", "_includes", "jsonld")
#print("jsonld_includes_dir", jsonld_includes_dir)
#os.makedirs(jsonld_includes_dir, exist_ok=True)
#schema_html_dir = os.path.join(os.getcwd(), "docs", "json-schema")
#print("schema_html_dir", schema_html_dir)
#os.makedirs(schema_html_dir, exist_ok=True)

# Add JSON-LD examples
print("\nProcessing JSON-LD")
for case_name in os.listdir(JSONLD_DIR):
    print(f"Processing {case_name}")
    name, ext = os.path.splitext(case_name)
    case_source = os.path.abspath(os.path.join(JSONLD_DIR, case_name))
    if os.path.isfile(case_source) and ext == ".jsonld":
        print(case_source)
        # replace @id with URL_PATH + basename
        with open(case_source, "r") as f:
            obj = json.load(f)
            obj['$schema'] = os.path.join(URL_PATH,os.path.basename(obj['$schema']))
            obj['@context'] = URL_PATH
            print(obj['$schema'])
            print(obj['@context'])
            print("Writing to: ", os.path.join(DOCS_JSONLD_PATH, case_name), "\n")
        with open(os.path.join(DOCS_JSONLD_PATH, case_name), 'w') as f:
            json.dump(obj, f, indent=4, sort_keys=True)

# Convert Schema to HTML
print("\nProcessing JSON Schema")
out = []
fl = os.listdir(SCHEMA_DIR)
#pprint.pprint(fl)
for case_name in sorted(fl):
    print(f"Processing {case_name}")
    name, ext = os.path.splitext(case_name)
    name, _ = os.path.splitext(name)
    case_source = os.path.abspath(os.path.join(SCHEMA_DIR, case_name))
    if os.path.isfile(case_source) and ext == ".json":
        # replace @id with URL_PATH + basename
        with open(case_source, "r") as f:
            obj = json.load(f)
            obj["$id"] = f"{URL_PATH}/{SCHEMA_DIR}/{obj['$id']}"
            print("Updated $id: ", obj["$id"])
            print("Writing to index")
            yaml_data_dict = {'title': obj["title"], 'description': obj["description"]}
            out.append(yaml_data_dict)
            print("Writing to: ", os.path.join(DOCS_SCHEMA_PATH, case_name))
            with open(os.path.join(DOCS_SCHEMA_PATH, case_name), 'w') as f:
                json.dump(obj, f, indent=4, sort_keys=True)
        
            print(f"Generating example {name}")
            config = GenerationConfiguration(recursive_detection_depth=10000, expand_buttons=True, deprecated_from_description=True)
            generate_from_filename(
                os.path.join(SCHEMA_DIR, case_name),
                os.path.join(DOCS_PATH, f"{name}.html"),
                config=config
            )

# Write site index YAML
#pprint.pprint(out)        
with open(os.path.join(DOCS_PATH, "_data", "index.yml"),'w') as yamlfile:
    yaml.safe_dump(out, yamlfile)


