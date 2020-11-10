import importlib.util
 
spec = importlib.util.spec_from_file_location("VtcDataset", "vizzToolsCore/VtcDataset.py")
models = importlib.util.module_from_spec(spec)
spec.loader.exec_module(models)

import json
import pprint

# Load and view Person
with open("./jsonld-examples/Person.jsonld") as f:
    result = models.Person.from_dict(json.load(f))
print("\nTest Person\n")
pprint.pprint(result.to_dict())

# Load and view Organization
with open("./jsonld-examples/Organization.jsonld") as f:
    result = models.Organization.from_dict(json.load(f))
print("\nTest Organization\n")
pprint.pprint(result.to_dict())

# Load and view PropertyValue
with open("./jsonld-examples/PropertyValue.jsonld") as f:
    result = models.PropertyValue.from_dict(json.load(f))
print("\nTest PropertyValue\n")
pprint.pprint(result.to_dict())

# Load and view Dataset
with open("./jsonld-examples/Dataset.jsonld") as f:
    result = models.Dataset.from_dict(json.load(f))
print("\nTest Dataset\n")
pprint.pprint(result.to_dict())

# Load and view VtcDataset
with open("./jsonld-examples/VtcDataset.jsonld") as f:
    result = models.VtcDataset.from_dict(json.load(f))
print("\nTest VtcDataset\n")
pprint.pprint(result.to_dict())

# Load and add links
with open("./jsonld-examples/links.jsonld") as f:
    result.links = json.load(f)
print("\nTest add links to VtcDataset\n")
pprint.pprint(result.links)