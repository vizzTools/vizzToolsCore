# vizzToolsCore

vizzToolsCore is an internal Python library to manage some of our the day-to-day tasks.

Currently this is a skeleton under development.

## Design principles (draft)

1. The aim of `vizzToolsCore` is provide a standardised set of data structures to faciliate inter-change between various specific vizzTools data processing packages.

1. `vizzToolsCore` ONLY deals with defining data structures, input and output, as well as transformations, should be dealt with in other packages.

1. Every data structure Class MUST have a JSON example and a JSON Schema. These can be generated from the Python Class or vice versa.

1. `vizzToolsCore` will use a "strict" Type mechanism, based on the standard Types defined in [Pydantic](https://pydantic-docs.helpmanual.io/).

