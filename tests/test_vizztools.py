import importlib.util
 
spec = importlib.util.spec_from_file_location("models", "vizzToolsCore/models.py")
models = importlib.util.module_from_spec(spec)
spec.loader.exec_module(models)

import json
with open("jsonld-examples/Dataset.jsonld") as f:
    result = models.Dataset.from_dict(json.load(f))
print(result)    
