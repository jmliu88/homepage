#!/usr/bin/env python3
"""
Recheck _data/publications.bib against the arXiv API.

For every entry that has an arXiv URL, fetch the author list from arXiv and compare
with the .bib entry. Print any mismatches so they can be reviewed manually.

Run with:
    uv run --with bibtexparser --with requests scripts/check_bib.py
"""

import re
import xml.etree.ElementTree as ET
from pathlib import Path

import bibtexparser
import requests

ROOT = Path(__file__).resolve().parent.parent
BIB = ROOT / "_data" / "publications.bib"
USER_AGENT = "JiamingLiuHomepageBot/1.0 (mailto:james.liu.n1@gmail.com)"


def extract_arxiv_id(url):
    if not url:
        return None
    m = re.search(r"arxiv\.org/abs/(\d+\.\d+)", url)
    return m.group(1) if m else None


def last_name(full_name):
    if not full_name:
        return ""
    parts = full_name.strip().split()
    return parts[-1].lower() if parts else ""


def first_name(full_name):
    if not full_name:
        return ""
    parts = full_name.strip().split()
    return parts[0].lower() if parts else ""


def normalize(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


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
        raw_id = entry.find("atom:id", ns).text.split("/abs/")[-1]
        arxiv_id = re.sub(r"v\d+$", "", raw_id)  # strip version suffix
        out[arxiv_id] = {
            "title": entry.find("atom:title", ns).text.strip().replace("\n", " "),
            "authors": [a.find("atom:name", ns).text for a in entry.findall("atom:author", ns)],
            "year": int(entry.find("atom:published", ns).text[:4]),
        }
    return out


def compare_authors(bib_authors, arxiv_authors, title):
    issues = []
    if len(bib_authors) != len(arxiv_authors):
        issues.append(f"author count differs: bib={len(bib_authors)} arxiv={len(arxiv_authors)}")

    for i, (ba, aa) in enumerate(zip(bib_authors, arxiv_authors)):
        if last_name(ba) != last_name(aa):
            issues.append(f"author #{i+1} last name differs: bib='{ba}' arxiv='{aa}'")
        elif normalize(first_name(ba)) != normalize(first_name(aa)):
            issues.append(f"author #{i+1} first name differs: bib='{ba}' arxiv='{aa}'")
    return issues


def main():
    parser = bibtexparser.bparser.BibTexParser(common_strings=True)
    parser.ignore_nonstandard_types = False
    with open(BIB, encoding="utf-8") as f:
        db = bibtexparser.load(f, parser=parser)

    id_to_entry = {}
    for e in db.entries:
        aid = extract_arxiv_id(e.get("url", ""))
        if aid:
            id_to_entry[aid] = e

    arxiv_meta = arxiv_fetch(list(id_to_entry.keys()))

    problems = 0
    for aid, e in id_to_entry.items():
        meta = arxiv_meta.get(aid)
        if not meta:
            print(f"MISSING: arXiv {aid} not found for {e['ID']}")
            problems += 1
            continue

        bib_authors = [a.strip() for a in e["author"].split(" and ")]
        issues = compare_authors(bib_authors, meta["authors"], e["title"])
        if issues:
            problems += 1
            print(f"MISMATCH {e['ID']} (arXiv:{aid}):")
            for issue in issues:
                print(f"  - {issue}")

    if problems == 0:
        print(f"All {len(id_to_entry)} arXiv entries look good.")
    else:
        print(f"\n{problems} problem(s) found. Please review the .bib file.")


if __name__ == "__main__":
    main()
