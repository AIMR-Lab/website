---
title: Grants
nav:
  order: 2
  tooltip: Active, pending, and past funding
---

# Grants

Below is an overview of the grants supporting the lab’s research efforts. Each entry includes the project’s duration, goals, and funding source. These initiatives reflect the lab’s commitment to innovation and collaboration across multiple disciplines, enabled by invaluable support from funding agencies.

{% include tags.html tags="nih, neurology, foundation, breast-cancer" %}
{% include search-info.html %}

## Current
{% for grant in site.data.grants %}
{% if grant.group == "current" %}
### {{ grant.title }}
**Subtitle:** {{ grant.subtitle }}  
{% if grant.link %}_[View More]({{ grant.link }})_{% endif %}  
  
{{ grant.description }}

---
{% endif %}
{% endfor %}

## Pending
{% for grant in site.data.grants %}
{% if grant.group == "pending" %}
### {{ grant.title }}
**Subtitle:** {{ grant.subtitle }}  
{% if grant.link %}_[View More]({{ grant.link }})_{% endif %}  
 
{{ grant.description }}

---
{% endif %}
{% endfor %}

## Past
{% for grant in site.data.grants %}
{% if grant.group == "past" %}
### {{ grant.title }}
**Subtitle:** {{ grant.subtitle }}  
{% if grant.link %}_[View More]({{ grant.link }})_{% endif %}  

{{ grant.description }}

---
{% endif %}
{% endfor %}