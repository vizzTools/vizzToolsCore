---
title: vizzToolsCore JSON Schema
---

# Core data models

These documents describe the vizzTools core data models as [JSON Schema](https://json-schema.org/understanding-json-schema/) with [JSON-LD](https://json-ld.org/) examples.

The URL `https://vizztools.github.io/vizzToolsCore/json-schema` can be used as the JSON-LD `@context` property.

Check out this [guide to using JSON schema in VSCode](https://omkarmore.wordpress.com/2017/04/07/json-schema/).

---

{% for item in site.data.index %}
<h2>{{ item.title }}</h2>

{{ item.description }}

<header><ul>
<li>::marker<a href="json-schema/{{ item.title }}.html">View <strong>HTML</strong></a></li>
<li>::marker<a href="json-schema/{{ item.title }}.schema.json">Download <strong>JSON Schema</strong></a></li>
<li>::marker<a href="json-schema/{{ item.title }}.jsonld">Download <strong>JSON-LD Example</strong></a></li>
</ul></header>

<br/>
{% endfor %}
