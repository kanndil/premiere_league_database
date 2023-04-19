---
layout: default
title: Home
---

{% for page in site.pages %}
  - [{{ page.name }}]({{ page.path }})
{% endfor %}