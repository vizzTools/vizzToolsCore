"""Run this to populate the json-schema html docs"""

import os
import shutil
import sys
import json
import yaml
import pprint

sys.path.insert(0, os.path.abspath(".."))

from json_schema_for_humans.generate import generate_from_filename, GenerationConfiguration

# Create site directory structure
schema_source_dir =  "/vizzToolsCore/json-schema"
jsonld_source_dir =  "/vizzToolsCore/jsonld-examples"
schema_dir = os.path.join(os.getcwd(), "docs", "json-schema")
print("schema_dir", schema_dir)
os.makedirs(schema_dir, exist_ok=True)
#schema_includes_dir = os.path.join(os.getcwd(), "docs", "_includes", "json-schema")
#print("schema_includes_dir", schema_includes_dir)
#os.makedirs(schema_includes_dir, exist_ok=True)
#jsonld_includes_dir = os.path.join(os.getcwd(), "docs", "_includes", "jsonld")
#print("jsonld_includes_dir", jsonld_includes_dir)
#os.makedirs(jsonld_includes_dir, exist_ok=True)
#schema_html_dir = os.path.join(os.getcwd(), "docs", "json-schema")
#print("schema_html_dir", schema_html_dir)
#os.makedirs(schema_html_dir, exist_ok=True)

# Add JSON-LD
print("\nProcessing JSON-LD")
for case_name in os.listdir(jsonld_source_dir):
    print(f"Processing {case_name}")
    name, ext = os.path.splitext(case_name)
    case_source = os.path.abspath(os.path.join(jsonld_source_dir, case_name))
    if not os.path.isfile(case_source) or ext != ".jsonld":
        continue
    shutil.copyfile(case_source, os.path.join(schema_dir, case_name))
    #shutil.copyfile(case_source, os.path.join(jsonld_includes_dir, case_name))

# Convert Schema to HTML
print("\nProcessing JSON Schema")
out = []
fl = os.listdir(schema_source_dir)
pprint.pprint(fl)
for case_name in sorted(fl):
    print(f"Processing {case_name}")
    name, ext = os.path.splitext(case_name)
    name, _ = os.path.splitext(name)
    case_source = os.path.abspath(os.path.join(schema_source_dir, case_name))
    if not os.path.isfile(case_source) or ext != ".json":
        continue

    shutil.copyfile(case_source, os.path.join(schema_dir, case_name))
    #shutil.copyfile(case_source, os.path.join(schema_includes_dir, case_name))
    

    print(f"Generating example {name}")

    config = GenerationConfiguration(recursive_detection_depth=10000, expand_buttons=True, deprecated_from_description=True)
    generate_from_filename(
        case_source,
        os.path.join(schema_dir, f"{name}.html"),
        config=config
    )

    # Add to index list
    print("Writing to index")
    with open(case_source, "r") as f:
        obj = json.load(f)
        #print(obj)
        yaml_data_dict = {'title': obj["title"], 'description': obj["description"]}
        out.append(yaml_data_dict)

# Write site index YAML
pprint.pprint(out)        
with open(os.path.join(os.getcwd(), "docs", "_data", "index.yml"),'w') as yamlfile:
    yaml.safe_dump(out, yamlfile) # Also note the safe_dump


