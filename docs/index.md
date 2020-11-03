---
title: vizzToolsCore JSON Schema
---

{% for item in site.data.index %}
<h2><a href="assets/json-schema-html/{{ item.title }}.html">{{ item.title }}</a></h2>

{{ item.description }}

<details><summary style="font-size:20px; cursor:pointer; text-decoration: underline">Click here to expand source JSON Schema...</summary>
<p>
{% highlight json %}
{% include json-schema/{{ item.title }}.schema.json %}
{% endhighlight %}
</p>
</details>

<details><summary style="font-size:20px; cursor:pointer; text-decoration: underline">Click here to expand the rendered result...</summary>
<p>
<iframe style="width: 100%; height: 60vh" src="assets/json-schema-html/{{ item.title }}.html"></iframe>
</p>
</details>
<br/>
{% endfor %}

{% assign json_files = site.static_files | where: "json", true %}
{% for myjson in json_files %}
  {{ myjson.path }}
{% endfor %}
