#pip3 install -e vizzToolsCore

import json
import pprint

# Load and view Person
from vizzToolsCore import Person
with open("./jsonld-examples/Person.jsonld") as f:
    person = Person.person_from_dict(json.load(f))
print("\nTest Person\n")
pprint.pprint(person.to_dict())

# Load and view Organization
from vizzToolsCore import Organization
with open("./jsonld-examples/Organization.jsonld") as f:
    org = Organization.organization_from_dict(json.load(f))
print("\nTest Organization\n")
pprint.pprint(org.to_dict())

# Load and view PropertyValue
from vizzToolsCore import PropertyValue
with open("./jsonld-examples/PropertyValue.jsonld") as f:
    pv = PropertyValue.property_value_from_dict(json.load(f))
print("\nTest PropertyValue\n")
pprint.pprint(pv.to_dict())

# Load and view Dataset
from vizzToolsCore import Dataset
with open("./jsonld-examples/Dataset.jsonld") as f:
    metadata = Dataset.dataset_from_dict(json.load(f))
print("\nTest Dataset\n")
pprint.pprint(metadata.to_dict())

# Load and view VtcDataset
from vizzToolsCore import VtcDataset
with open("./jsonld-examples/VtcDataset.jsonld") as f:
    ds = VtcDataset.vtc_dataset_from_dict(json.load(f))
print("\nTest VtcDataset\n")
pprint.pprint(ds.to_dict())

# Load add metadata and links
with open("./jsonld-examples/links.jsonld") as f:
    ds_dict = ds.to_dict()
    ds_dict["metadata"] = [metadata.to_dict()]
    ds_dict["links"] = json.load(f)
print("\nTest add metadata and links to VtcDataset\n")
pprint.pprint(VtcDataset.vtc_dataset_from_dict(ds_dict).to_dict())
