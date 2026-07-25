---
layout: default
title: Publications
---

<h2 class="section-title">Publications</h2>

<p class="muted">
Full list of publications. Also see my
<a href="https://scholar.google.com/citations?user=SmL7oMQAAAAJ&hl=en">Google Scholar</a> profile
(2,200+ citations).
</p>

{% assign pubs = site.data.publications %}
{% assign years = pubs | map: "year" | uniq | sort | reverse %}

{% for y in years %}
<h3 class="pub-year">{{ y }}</h3>
{% for pub in pubs %}
{% if pub.year == y %}
<div class="pub-entry">
  <div class="pub-badge{% if pub.preprint %} preprint{% endif %}"><span>{{ pub.venue_short }}</span></div>
  <div class="pub-body">
    {% if pub.link %}<a class="pub-title" href="{{ pub.link }}">{{ pub.title }}</a>{% else %}<span class="pub-title">{{ pub.title }}</span>{% endif %}
    <p class="pub-authors">{{ pub.authors | replace: 'Jiaming Liu', '<span class="me">Jiaming Liu</span>' }}</p>
    <p class="pub-venue">{{ pub.venue }}</p>
    <div class="pub-links">
      {% if pub.link %}<a href="{{ pub.link }}">Paper</a>{% endif %}
      {% if pub.project %}<a href="{{ pub.project }}">Project</a>{% endif %}
      {% if pub.code %}<a href="{{ pub.code }}">Code</a>{% endif %}
      {% if pub.demo %}<a href="{{ pub.demo }}">Demo</a>{% endif %}
    </div>
  </div>
</div>
{% endif %}
{% endfor %}
{% endfor %}

<h2 class="section-title">Selected US Patents</h2>

<ul>
{% for patent in site.data.patents %}
  <li style="margin-bottom: 10px;">
    <strong>{{ patent.title }}</strong><br>
    <span class="muted">{{ patent.authors }}. {{ patent.number }}, {{ patent.year }}.</span>
  </li>
{% endfor %}
</ul>
