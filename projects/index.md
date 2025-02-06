---
title: Projects
nav:
  order: 3
  tooltip: Software, datasets, and more
---

# {% include icon.html icon="fa-solid fa-wrench" %}Projects

Our lab harnesses advanced deep learning and image processing techniques to push the boundaries of medical diagnostics. Through multidisciplinary projects, we develop cutting-edge solutions that enhance image quality, automate feature detection, and improve early disease diagnosis, paving the way for smarter, more accurate clinical decision-making.

{% include tags.html tags="publication, resource, website" %}

{% include search-info.html %}

{% include section.html %}

## Featured

{% include list.html component="card" data="projects" filter="group == 'featured'" %}

{% include section.html %}

## More

{% include list.html component="card" data="projects" filter="!group" style="small" %}
