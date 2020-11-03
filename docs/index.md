---
title: vizzToolsCore JSON Schema
---

These documents describe the vizzTools core data models as [JSON Schema](https://json-schema.org/understanding-json-schema/) with [JSON-LD](https://json-ld.org/).

The URL `https://vizztools.github.io/vizzToolsCore/json-schema` can be used as the JSON-LD `@context` property.

Check out this [guide to using JSON schema in VSCode](https://omkarmore.wordpress.com/2017/04/07/json-schema/).

# Core data models

{% for item in site.data.index %}
<h2><a href="json-schema/{{ item.title }}.html">{{ item.title }}</a></h2>

{{ item.description }}

<span class="w3-tag w3-padding w3-round-large w3-red w3-center"><a href="json-schema/{{ item.title }}.schema.json">JSON Schema</a></span>
<span class="w3-tag w3-padding w3-round-large w3-red w3-center"><a href="json-schema/{{ item.title }}.jsonld">JSON-LD Example</a></span>

<br/>
{% endfor %}
