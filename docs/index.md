---
title: vizzToolsCore JSON Schema
---

# Examples
{% for example in site.data.examples %}
## {{ example.display_name }}

{{ example.description }}

<details><summary style="font-size:20px; cursor:pointer; text-decoration: underline">Click here to expand source JSON Schema...</summary>
<p>
{% highlight json %}
{% include examples/{{ example.name }}.schema.json %}
{% endhighlight %}
</p>
</details>

<details><summary style="font-size:20px; cursor:pointer; text-decoration: underline">Click here to expand the rendered result...</summary>
<p>
[ {{example.display_name}} ](assets/examples/{{ example.name }}.html)

<iframe style="width: 100%; height: 60vh" src="assets/examples/{{ example.name }}.html"></iframe>
</p>
</details>
<br/>
{% endfor %}