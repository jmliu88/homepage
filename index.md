---
layout: default
---

<h2 class="section-title">About Me</h2>

<p class="lead">
I lead content generation for the <strong>Qwen App</strong> at <strong>Alibaba Group</strong>,
building systems that connect <strong>AI agents</strong>, <strong>image generation</strong>,
and <strong>interactive video generation</strong> into a single intelligent creation experience.
</p>

<p>
My work sits at the intersection of generative models and real-world products. Over the
past years I have focused on several closely related topics:
controllable diffusion models, subject-driven personalization, human-centric video
and talking-avatar generation, visual editing (makeup / hair / garment / font / face),
efficient inference, and agentic creation workflows.
My publications have received <strong>2,200+ citations</strong> according to
<a href="https://scholar.google.com/citations?user=SmL7oMQAAAAJ&hl=en">Google Scholar</a>.
</p>

<p>
Previously, I was <strong>Head of AI at Tiamat AI</strong>, where I built the full-stack
generative pipeline for a virtual-companion app; led the <strong>AIGC &amp; Optical Flow</strong>
team at <strong>Xiaohongshu</strong> to power content creation; and led the
<strong>GAN team</strong> at <strong>Baidu</strong> on intelligent font production and
virtual-human technologies after starting in Baidu IDL's OCR team. Several works have
been widely adopted by the open-source community, including
<a href="https://github.com/Alibaba-Quark/LiveAvatar">LiveAvatar</a>
(Hugging Face #1 Paper of the Day, 2k+ GitHub stars) and
<a href="https://github.com/Xiaojiu-z/EasyControl">EasyControl</a>
(Hugging Face #1 trending Space).
</p>

<h2 class="section-title">News</h2>

<ul class="news-list">
  <li>
    <span class="news-date">Jun 2026</span>
    <span class="news-body"><a href="https://github.com/Alibaba-Quark/LiveAvatar">LiveAvatar</a> accepted to <strong>ECCV 2026</strong>.</span>
  </li>
  <li>
    <span class="news-date">2026</span>
    <span class="news-body"><a href="https://arxiv.org/abs/2604.11626">RationalRewards</a> released — Hugging Face <strong>#2 Paper of the Day</strong>. EasyText published at <strong>AAAI 2026</strong>; Stable-Hair V2 published in <strong>IEEE TVCG</strong>.</span>
  </li>
  <li>
    <span class="news-date">Dec 2025</span>
    <span class="news-body"><a href="https://arxiv.org/abs/2512.04677">LiveAvatar</a> released — a 14B-parameter real-time streaming avatar model running at 45 FPS on 5&times;H800. Hugging Face <strong>#1 Paper of the Day</strong>, 2k+ GitHub stars.</span>
  </li>
  <li>
    <span class="news-date">Oct 2025</span>
    <span class="news-body">Three papers presented at <strong>ICCV 2025</strong>: <a href="https://arxiv.org/abs/2503.07027">EasyControl</a>, <a href="https://arxiv.org/abs/2501.15891">Any2AnyTryOn</a>, and Fonts.</span>
  </li>
  <li>
    <span class="news-date">Aug 2025</span>
    <span class="news-body"><a href="https://arxiv.org/abs/2403.07764">StableMakeup</a> presented at <strong>SIGGRAPH 2025</strong>.</span>
  </li>
  <li>
    <span class="news-date">Apr 2025</span>
    <span class="news-body"><a href="https://huggingface.co/spaces/jamesliu1217/EasyControl_Ghibli">EasyControl Ghibli</a> became the <strong>#1 trending Space</strong> on Hugging Face.</span>
  </li>
  <li>
    <span class="news-date">Feb 2025</span>
    <span class="news-body"><a href="https://arxiv.org/abs/2407.14078">Stable-Hair</a> published at <strong>AAAI 2025</strong>.</span>
  </li>
</ul>

<h2 class="section-title">Selected Publications</h2>

{% assign selected = site.data.publications | where: "selected", true %}
{% for pub in selected %}
<div class="pub-entry">
  <div class="pub-badge{% if pub.preprint %} preprint{% endif %}"><span>{{ pub.venue_short }} {{ pub.year }}</span></div>
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
{% endfor %}

<p style="margin-top: 18px;">
  <a href="{{ '/publications/' | relative_url }}">→ Full publication list</a>
</p>

<h2 class="section-title">Experience</h2>

<dl class="cv-list">
  <dt>2025 – Present</dt>
  <dd><span class="title">Content Generation Lead</span>, <span class="org">Qwen App, Alibaba Group</span></dd>
  <dt>2024 – 2025</dt>
  <dd><span class="title">Head of AI</span>, <span class="org">Tiamat AI</span></dd>
  <dt>2022 – 2024</dt>
  <dd><span class="title">AIGC &amp; Optical Flow Lead</span>, <span class="org">Xiaohongshu</span></dd>
  <dt>2019 – 2022</dt>
  <dd><span class="title">Tech Lead, GAN Team</span>, <span class="org">Baidu, Vision Technology Department</span></dd>
  <dt>2017 – 2019</dt>
  <dd><span class="title">Research Engineer, OCR Team</span>, <span class="org">Baidu IDL</span></dd>
</dl>

<h2 class="section-title">Education</h2>

<dl class="cv-list">
  <dt>2012 – 2017</dt>
  <dd><span class="title">Ph.D., Pattern Recognition and Intelligent Systems</span>, <span class="org">Tongji University</span><br>
  <span class="muted">Advisors: Prof. Guo-Zheng Li (IEEE Senior Member) &amp; Prof. Mingyu You</span></dd>
  <dt>2014 – 2015</dt>
  <dd><span class="title">Joint Ph.D. Training, Department of Electrical Engineering</span>, <span class="org">Columbia University</span><br>
  <span class="muted">Advisor: Prof. Dan Ellis</span></dd>
</dl>

<h2 class="section-title">Honors &amp; Awards</h2>

<ul>
  <li>Silver Medal, China National Patent Award</li>
  <li>5&times; First Place, ICDAR 2018 / 2019 Robust Reading Competitions (detection, recognition, end-to-end)</li>
  <li>Champion, Baidu 25th Hackathon (face-swap virtual idol group)</li>
  <li>Champion, Xiaohongshu 3rd Hackathon</li>
  <li>Hugging Face #1 Paper of the Day (LiveAvatar), #2 Paper of the Day (RationalRewards)</li>
</ul>
