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

This site is deployed with **GitHub Pages** and the custom domain `jiamingliu.xyz`.

- Repository: https://github.com/jmliu88/homepage
- Live site: https://jiamingliu.xyz

Pushing to `main` triggers the GitHub Actions workflow in `.github/workflows/pages.yml`.

### DNS records

For the apex domain `jiamingliu.xyz`, add these A records at your registrar
(Namecheap → Domain List → Manage → Advanced DNS → Host Records):

| Type | Host | Value |
|------|------|-------|
| A Record | `@` | `185.199.108.153` |
| A Record | `@` | `185.199.109.153` |
| A Record | `@` | `185.199.110.153` |
| A Record | `@` | `185.199.111.153` |

In the GitHub repository settings, enable **Pages** with source **GitHub Actions**,
and set the custom domain to `jiamingliu.xyz`.
