---
title: vizzToolsCore JSON Schema
---

These documents describe the vizzTools core data models described using [JSON schema](https://json-schema.org/understanding-json-schema/).
Note, only high level objects are shown in the index (click on the object name for a detailed description), however all objects and properties are also available using the URL `https://vizztools.github.io/vizzToolsCore/json-schema/<name>`; hence this URL can be used for the JSON-LD `@context` property.

Check out this [guide to using JSON schema in VSCode](https://omkarmore.wordpress.com/2017/04/07/json-schema/).

{% for item in site.data.index %}
<h2><a href="json-schema/{{ item.title }}.html">{{ item.title }}</a></h2>

{{ item.description }}

<a href="json-schema/{{ item.title }}.schema.json">JSON Schema</a>
<details><summary style="font-size:12px; cursor:pointer; text-decoration: underline">Click here to expand source JSON Schema...</summary>
<p>
{% highlight json %}
{% include json-schema/{{ item.title }}.schema.json %}
{% endhighlight %}
</p>
</details>


<br/>
{% endfor %}
