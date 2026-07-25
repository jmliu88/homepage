# Content Guide & Changelog

This file tracks what each part of the homepage says, why, and where to edit it.

## Where to edit what

| Section | File to edit |
|---------|--------------|
| Name, email, social links, SEO description | `_config.yml` |
| Portrait photo | `assets/img/photo.jpg` |
| About / bio, News, Experience, Education, Honors | `index.md` |
| **Publication metadata (single source of truth)** | **`_data/publications.bib`** |
| Publications page template | `publications.md` |
| Patents | `_data/patents.yml` |
| Open-source project cards | `projects.md` |
| Styles (colors, fonts, layout) | `assets/css/style.scss` |
| Layout / sidebar / footer | `_layouts/default.html`, `_includes/sidebar.html`, `_includes/footer.html` |

## Publication workflow

We now use `_data/publications.bib` as the single source of truth for papers.
The Jekyll site reads `_data/publications.yml`, which is auto-generated from the `.bib` file.

### To update publications

1. Edit `_data/publications.bib` (fix authors, venue, year, add a new entry, etc.).
   - `selected = {true}` puts the paper on the home page.
   - `code`, `project`, `demo` are optional custom fields for links.
   - `venue_short` is optional; if omitted it is inferred from the venue name.
2. Regenerate `_data/publications.yml`:

```bash
uv run --with bibtexparser --with pyyaml scripts/bib_to_yml.py
```

3. Rebuild the site:

```bash
bundle exec jekyll build
```

### To re-fetch metadata from arXiv / Crossref

If you want to re-import all papers from the web (e.g., after adding several arXiv IDs):

```bash
uv run --with bibtexparser --with pyyaml --with requests scripts/export_bib.py
```

This script:
- Queries **Crossref** by title (preferred, gives accurate conference/journal metadata).
- Falls back to the **arXiv API** for papers with an arXiv link.
- Preserves your custom fields (`selected`, `code`, `project`, `demo`, `preprint`, `venue_short`).

Always review the generated `.bib` before committing — Crossref/arXiv titles sometimes have
odd casing or stray whitespace.

### Recheck workflow (mandatory after export)

After running `export_bib.py`, always run the recheck script:

```bash
uv run --with bibtexparser --with requests scripts/check_bib.py
```

It verifies every arXiv-linked entry against the arXiv API and prints author/name
mismatches. Fix any reported issues in the `.bib` before running `bib_to_yml.py`.

**Lesson learned (2026-07-25):** Do NOT manually expand abbreviated author names from
Google Scholar (e.g., `H Wang` → `Haofan Wang`). Always fetch full names from arXiv or
Crossref. If both are unavailable, keep the abbreviation or mark it for manual review.

## Content principles

- **Academic tone, high-level bio.** Avoid internal level codes (P8, T7, R6). Focus on topics, products, and impact.
- **Publications drive the page.** Add or edit a paper in `_data/publications.bib`; set `selected = {true}` to feature it on the home page.
- **Verified links only.** Paper links come from DOI or arXiv.

## Changelog

### 2026-07-25
- Switched publications to a `.bib`-first workflow.
- Added `scripts/export_bib.py` (Crossref + arXiv import) and `scripts/bib_to_yml.py` (convert to Jekyll data).
- Regenerated `_data/publications.yml` from `_data/publications.bib` with corrected author lists and venues.
- Fixed titles/venues: Any2AnyTryOn casing, EditWorld whitespace, WordCon (TCSVT), cough2015 (BMC journal), Stable-Hair V2 (TVCG).
- **Bug fix:** Corrected RationalRewards authors (Haozhe Wang, Cong Wei, Weiming Ren, Fangzhen Lin, Wenhu Chen).
- **Root cause:** Initial YAML manually expanded Google Scholar abbreviations incorrectly; export script fell back to that YAML when Crossref had no record.
- **Improvement:** `export_bib.py` now prefers arXiv API for author lists when an arXiv ID exists, and warns on mismatches.
- **Added recheck:** `scripts/check_bib.py` validates all arXiv-linked entries against the arXiv API after export.

### 2026-07-24
- Added portrait photo.
- Rewrote bio to high-level narrative covering Alibaba (Qwen App), Tiamat AI, Xiaohongshu, Baidu OCR/GAN.
- Removed internal ranks (P8 / T7 / R6) from bio and Experience section.
- Added full career timeline, education, and Honors & Awards.
- Updated LiveAvatar to ECCV 2026 and added official repo/project links.
- Added 2026 papers: RationalRewards, CollectionLoRA, EasyText, Stable-Hair V2.

### 2026-07-24 (initial)
- Initial Jekyll homepage with About, News, Publications, Projects.
- Imported publications from Google Scholar and verified key arXiv links.
