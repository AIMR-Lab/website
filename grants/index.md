---
title: Grants
nav:
  order: 2
  tooltip: Active, pending, and past funding
---

# {% include icon.html icon="fa-solid fa-hand-holding-dollar" %} Grants

{% include tags.html tags="nih, neurology, foundation, breast-cancer" %}
{% include search-info.html %}

{% include section.html %}

## Current
{% include list.html component="card" data="grants" filter="group == 'current'" %}

{% include section.html %}

## Pending
{% include list.html component="card" data="grants" filter="group == 'pending'" style="small" %}

{% include section.html %}

## Past
{% include list.html component="card" data="grants" filter="group == 'past'" style="small" %}