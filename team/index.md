---
title: Team
nav:
  order: 4
  tooltip: About our team
---

# {% include icon.html icon="fa-solid fa-users" %}Team

Our lab is a collective of computational research investigators. We like to perform ambitious research, but operate in a fun, collaborative, and team-oriented environment, and we are strongly committed to mentoring young scientists through internship schemes.

{% include section.html %}

{% include list.html data="members" component="portrait" filter="role == 'pi'" %}
{% include list.html data="members" component="portrait" filter="role != 'pi'" %}

