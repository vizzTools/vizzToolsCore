#pip3 install -e vizzToolsCore

import json
import pprint

# Load and view Person
from vizzToolsCore import Person
with open("./jsonld-examples/Person.jsonld") as f:
    result = Person.person_from_dict(json.load(f))
print("\nTest Person\n")
pprint.pprint(result.to_dict())

# Load and view Organization
from vizzToolsCore import Organization
with open("./jsonld-examples/Organization.jsonld") as f:
    result = Organization.organization_from_dict(json.load(f))
print("\nTest Organization\n")
pprint.pprint(result.to_dict())

# Load and view PropertyValue
from vizzToolsCore import PropertyValue
with open("./jsonld-examples/PropertyValue.jsonld") as f:
    result = PropertyValue.property_value_from_dict(json.load(f))
print("\nTest PropertyValue\n")
pprint.pprint(result.to_dict())

# Load and view Dataset
from vizzToolsCore import Dataset
with open("./jsonld-examples/Dataset.jsonld") as f:
    result = Dataset.dataset_from_dict(json.load(f))
print("\nTest Dataset\n")
pprint.pprint(result.to_dict())

# Load and view VtcDataset
with open("./jsonld-examples/VtcDataset.jsonld") as f:
    result = vtc.VtcDataset.from_dict(json.load(f))
print("\nTest VtcDataset\n")
pprint.pprint(result.to_dict())

# Load and add links
with open("./jsonld-examples/links.jsonld") as f:
    result.links = json.load(f)
print("\nTest add links to VtcDataset\n")
pprint.pprint(result.links)