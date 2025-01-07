---
title: Grant
nav:
  order: 2
  tooltip: Email, address, and location
---

# {% include icon.html icon="fa-solid fa-wrench" %}Grant

{% for grant in site.data.grant.current %}
  <h2>{{ grant.id }}</h2>
  <p><strong>Project Period:</strong> {{ grant.project_period }}</p>
  <p><strong>Funding Agency:</strong> {{ grant.funding_agency }}</p>
  ...
{% endfor %}