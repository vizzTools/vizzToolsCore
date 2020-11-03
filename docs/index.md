---
title: vizzToolsCore JSON Schema
---

These documents describe the vizzTools core data models using [JSON schema](https://json-schema.org/understanding-json-schema/).

Click on the object name for a detailed HTML description, you can also view the JSON schema or JSON-LD Example.

The URL `https://vizztools.github.io/vizzToolsCore/json-schema` can be used for the JSON-LD `@context` property.

Check out this [guide to using JSON schema in VSCode](https://omkarmore.wordpress.com/2017/04/07/json-schema/).

{% for item in site.data.index %}
<h2><a href="json-schema/{{ item.title }}.html">{{ item.title }}</a></h2>

{{ item.description }}

<a href="json-schema/{{ item.title }}.schema.json">JSON Schema</a>
<a href="json-schema/{{ item.title }}.jsonld">JSON-LD Example</a>

<br/>
{% endfor %}
