#!/usr/bin/env python3
"""
Export _data/publications.yml to _data/publications.bib.

Workflow:
1. Read the current YAML list (which may already contain corrections).
2. For each paper, query Crossref by title. If a match with Jiaming Liu as author is
   found, use its metadata (title, authors, year, venue, DOI).
3. Otherwise, fall back to the arXiv API for papers with an arXiv link.
4. If neither works, keep the YAML entry as-is.
5. Preserve custom fields (selected, code, project, demo, preprint, venue_short).

Run with:
    uv run --with bibtexparser --with pyyaml --with requests scripts/export_bib.py
"""

import re
import time
import xml.etree.ElementTree as ET
from pathlib import Path

import requests
import yaml
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bwriter import BibTexWriter

ROOT = Path(__file__).resolve().parent.parent
PUBS_YML = ROOT / "_data" / "publications.yml"
BIB_OUT = ROOT / "_data" / "publications.bib"
USER_AGENT = "JiamingLiuHomepageBot/1.0 (mailto:james.liu.n1@gmail.com)"


def load_yml():
    with open(PUBS_YML, encoding="utf-8") as f:
        return yaml.safe_load(f) or []


def clean_text(s):
    if not s:
        return ""
    s = s.replace("\n", " ").strip()
    # Remove XML/HTML tags (Crossref sometimes returns <scp>...</scp>)
    s = re.sub(r"<[^>]+>", "", s)
    # Decode common HTML entities
    s = s.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    # Collapse multiple spaces
    s = re.sub(r"\s+", " ", s)
    return s


def extract_arxiv_id(link):
    if not link:
        return None
    m = re.search(r"arxiv\.org/abs/(\d+\.\d+)", link)
    return m.group(1) if m else None


def build_author_name(a):
    if "given" in a and "family" in a:
        return f"{a['given']} {a['family']}".strip()
    return a.get("name", "").strip()


def last_name(full_name):
    if not full_name:
        return ""
    parts = full_name.strip().split()
    return parts[-1].lower() if parts else ""


def crossref_search(title):
    url = "https://api.crossref.org/works"
    params = {"query.title": title, "rows": 5, "mailto": "james.liu.n1@gmail.com"}
    headers = {"User-Agent": USER_AGENT}
    r = requests.get(url, params=params, headers=headers, timeout=20)
    r.raise_for_status()
    items = r.json()["message"]["items"]

    for item in items:
        item_title = item.get("title", [None])[0]
        if not item_title:
            continue

        authors = [build_author_name(a) for a in item.get("author", [])]
        # Require that Jiaming Liu appears exactly as an author
        if "Jiaming Liu" not in authors:
            continue

        year = (
            item.get("published-print", {}).get("date-parts", [[None]])[0][0]
            or item.get("published-online", {}).get("date-parts", [[None]])[0][0]
        )
        venue = item.get("container-title", [None])[0]
        doi = item.get("DOI")

        return {
            "title": clean_text(item_title),
            "authors": authors,
            "year": int(year) if year else None,
            "venue": clean_text(venue),
            "doi": doi,
            "url": f"https://doi.org/{doi}" if doi else None,
        }
    return None


def arxiv_fetch(ids):
    if not ids:
        return {}
    url = "http://export.arxiv.org/api/query?id_list=" + ",".join(ids)
    headers = {"User-Agent": USER_AGENT}
    r = requests.get(url, headers=headers, timeout=40)
    r.raise_for_status()

    root = ET.fromstring(r.text)
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    out = {}
    for entry in root.findall("atom:entry", ns):
        title = clean_text(entry.find("atom:title", ns).text)
        authors = [a.find("atom:name", ns).text for a in entry.findall("atom:author", ns)]
        year = int(entry.find("atom:published", ns).text[:4])
        raw_id = entry.find("atom:id", ns).text.split("/abs/")[-1]
        arxiv_id = re.sub(r"v\d+$", "", raw_id)  # strip version suffix
        comment = entry.find("atom:comment", ns)
        comment = clean_text(comment.text) if comment is not None else ""
        out[arxiv_id] = {
            "title": title,
            "authors": authors,
            "year": year,
            "venue": comment or "arXiv preprint",
            "doi": None,
            "url": f"https://arxiv.org/abs/{arxiv_id}",
        }
    return out


def make_bibkey(title, year):
    first = re.sub(r"[^a-zA-Z0-9]", "", title.split()[0]).lower()
    return f"{first}{year}"


def entry_type(venue):
    v = venue.lower()
    if "arxiv" in v:
        return "article"  # journal = {arXiv preprint ...}
    if any(x in v for x in ["transaction", "journal", "bmc", "iet", "international journal"]):
        return "article"
    return "inproceedings"


def main():
    pubs = load_yml()

    # Batch arXiv lookups
    arxiv_ids = [extract_arxiv_id(p.get("link", "")) for p in pubs]
    arxiv_ids = [aid for aid in arxiv_ids if aid]
    arxiv_meta = arxiv_fetch(arxiv_ids)

    db = BibDatabase()
    db.entries = []
    warnings = []

    for p in pubs:
        title = p["title"]
        aid = extract_arxiv_id(p.get("link", ""))

        arxiv_info = arxiv_meta.get(aid) if aid else None
        crossref_info = crossref_search(title)

        # Rule: if arXiv exists, arXiv is the source of truth for authors/title/year.
        # Use Crossref venue/DOI only when the first author matches; otherwise warn.
        if arxiv_info:
            meta = arxiv_info
            if crossref_info:
                if last_name(arxiv_info["authors"][0]) == last_name(crossref_info["authors"][0]):
                    meta = {
                        **crossref_info,
                        "title": arxiv_info["title"],
                        "authors": arxiv_info["authors"],
                    }
                else:
                    warnings.append(
                        f"Author mismatch for {aid} ({title}): "
                        f"arXiv={arxiv_info['authors'][0]} vs Crossref={crossref_info['authors'][0]}"
                    )
        elif crossref_info:
            meta = crossref_info
        else:
            meta = {
                "title": title,
                "authors": [a.strip() for a in p["authors"].split(",")],
                "year": int(p["year"]),
                "venue": p.get("venue", ""),
                "doi": None,
                "url": p.get("link"),
            }
            warnings.append(f"Used YAML fallback for: {title}")

        entry = {
            "ENTRYTYPE": entry_type(meta.get("venue", "")),
            "ID": make_bibkey(meta["title"], meta["year"]),
            "title": meta["title"],
            "author": " and ".join(meta["authors"]),
            "year": str(meta["year"]),
        }

        venue = meta.get("venue", "")
        if venue:
            if entry["ENTRYTYPE"] == "article":
                entry["journal"] = venue
            else:
                entry["booktitle"] = venue

        if meta.get("doi"):
            entry["doi"] = meta["doi"]
        if meta.get("url"):
            entry["url"] = meta["url"]

        # Preserve custom fields from YAML
        for k in ["selected", "code", "project", "demo"]:
            v = p.get(k)
            if v is not None and v != "":
                entry[k] = "true" if v is True else str(v)

        # Set preprint based on the actual venue, not the old YAML
        if "arxiv" in meta.get("venue", "").lower():
            entry["preprint"] = "true"

        db.entries.append(entry)
        time.sleep(0.15)  # be polite to Crossref

    for w in warnings:
        print("WARNING:", w)
    if warnings:
        print(f"\n{len(warnings)} warning(s) above. Please review before using the .bib.")

    writer = BibTexWriter()
    writer.indent = "  "
    writer.comma_first = False

    with open(BIB_OUT, "w", encoding="utf-8") as f:
        f.write(writer.write(db))

    print(f"Wrote {len(db.entries)} entries to {BIB_OUT}")


if __name__ == "__main__":
    main()
