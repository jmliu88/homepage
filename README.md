# Jiaming Liu — Academic Homepage

A clean, minimal, academic-style personal homepage built with [Jekyll](https://jekyllrb.com/).
No plugins required — it builds cleanly both locally and on GitHub Pages.

## Quick start

```bash
bundle install --path vendor/bundle
bundle exec jekyll serve
# open http://localhost:4000
```

## Structure

```
├── _config.yml            # Personal info & links (email, Scholar, LinkedIn, ...)
├── _data/
│   ├── publications.yml   # Publications (add new papers here)
│   └── patents.yml        # Granted patents
├── _layouts/default.html  # Page layout
├── _includes/             # Sidebar & footer
├── assets/
│   ├── css/style.scss     # All styles
│   └── img/photo.jpg      # <-- put your portrait photo here
├── index.md               # Home page (About / News / Selected Publications)
├── publications.md        # Full publication list (auto-generated from _data)
└── projects.md            # Open-source projects
```

## Updating content

- **New paper**: add an entry to `_data/publications.yml` (see the field comments at the
  top of the file). Set `selected: true` to feature it on the home page.
- **News**: edit the `<ul class="news-list">` block in `index.md`.
- **Personal info / links**: edit `_config.yml`.
- **Photo**: replace `assets/img/photo.jpg` (a square image works best; until then an
  initials placeholder is shown).

## Deploy

Build produces a fully static site in `_site/` — host it anywhere:

```bash
bundle exec jekyll build
# upload _site/ to your server, e.g.:
rsync -avz _site/ user@your-server:/var/www/homepage/
```

Set `url` in `_config.yml` to your domain before deploying.
