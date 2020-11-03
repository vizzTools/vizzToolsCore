---
title: vizzToolsCore JSON Schema
---

# Core data models

These documents describe the vizzTools core data models as [JSON Schema](https://json-schema.org/understanding-json-schema/) with [JSON-LD](https://json-ld.org/) examples.

The URL `https://vizztools.github.io/vizzToolsCore/json-schema` can be used as the JSON-LD `@context` property.

Check out this [guide to using JSON schema in VSCode](https://omkarmore.wordpress.com/2017/04/07/json-schema/).

---

{% for item in site.data.index %}
<h2><a href="json-schema/{{ item.title }}.html">{{ item.title }}</a></h2>

{{ item.description }}

<a class="btn--info" href="json-schema/{{ item.title }}.schema.json">JSON Schema</a>
<a class="btn--success" href="json-schema/{{ item.title }}.jsonld">JSON-LD Example</a>

<br/>
{% endfor %}
