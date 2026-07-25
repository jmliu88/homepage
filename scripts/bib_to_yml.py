#!/usr/bin/env python3
"""
Convert _data/publications.bib back to _data/publications.yml for Jekyll.

Run with:
    uv run --with bibtexparser --with pyyaml scripts/bib_to_yml.py
"""

import re
from pathlib import Path

import bibtexparser
import yaml

ROOT = Path(__file__).resolve().parent.parent
BIB = ROOT / "_data" / "publications.bib"
YML = ROOT / "_data" / "publications.yml"

VENUE_PATTERNS = {
    "computer vision and pattern recognition": "CVPR",
    "international conference on computer vision": "ICCV",
    "european conference on computer vision": "ECCV",
    "neural information processing systems": "NeurIPS",
    "advances in neural information processing": "NeurIPS",
    "aaai conference on artificial intelligence": "AAAI",
    "acm siggraph": "SIGGRAPH",
    "special interest group on computer graphics": "SIGGRAPH",
    "acm international conference on multimedia": "ACM MM",
    "international conference on document analysis and recognition": "ICDAR",
    "asian conference on computer vision": "ACCV",
    "transactions on visualization and computer graphics": "TVCG",
    "circuits and systems for video technology": "TCSVT",
    "ieee international conference on bioinformatics and biomedicine": "IEEE BIBM",
    "bmc medical informatics and decision making": "BMC MIDM",
    "bmvc": "BMVC",
    "iet signal processing": "IET SP",
}


def clean_text(s):
    if not s:
        return ""
    s = s.replace("\n", " ").strip()
    s = re.sub(r"\s+", " ", s)
    return s


def infer_venue_short(venue):
    if not venue:
        return "arXiv"
    v = venue.lower()
    if "arxiv" in v:
        return "arXiv"
    for pat, short in VENUE_PATTERNS.items():
        if pat in v:
            return short
    # Fallback: acronym in parentheses, e.g. "(ICCV)"
    m = re.search(r"\(([A-Za-z][A-Za-z0-9\-]{1,})\)", venue)
    if m:
        return m.group(1).upper()
    return venue.split()[0]


def to_bool(v):
    if isinstance(v, bool):
        return v
    if isinstance(v, str):
        return v.lower() in ("true", "yes", "1")
    return False


def main():
    parser = bibtexparser.bparser.BibTexParser(common_strings=True)
    parser.ignore_nonstandard_types = False

    with open(BIB, encoding="utf-8") as f:
        db = bibtexparser.load(f, parser=parser)

    entries = []
    for e in db.entries:
        venue = e.get("booktitle") or e.get("journal") or ""
        is_arxiv = "arxiv" in venue.lower()
        url = e.get("url", "")
        doi = e.get("doi", "")
        if not url and doi:
            url = f"https://doi.org/{doi}"

        entry = {
            "title": clean_text(e.get("title", "")),
            "authors": e.get("author", "").replace(" and ", ", ").strip(),
            "venue": clean_text(venue),
            "venue_short": e.get("venue_short") or infer_venue_short(venue),
            "year": int(e.get("year", 0)),
        }

        if is_arxiv or to_bool(e.get("preprint")):
            entry["preprint"] = True
        if url:
            entry["link"] = url
        if doi:
            entry["doi"] = doi

        for k in ["code", "project", "demo"]:
            if e.get(k):
                entry[k] = e[k]

        if to_bool(e.get("selected")):
            entry["selected"] = True

        entries.append(entry)

    # Sort by year desc, then title
    entries.sort(key=lambda x: (-x["year"], x["title"]))

    with open(YML, "w", encoding="utf-8") as f:
        f.write("# Auto-generated from publications.bib.\n")
        f.write("# Edit publications.bib, then run: uv run --with bibtexparser --with pyyaml scripts/bib_to_yml.py\n")
        yaml.dump(entries, f, allow_unicode=True, sort_keys=False, default_flow_style=False)

    print(f"Wrote {len(entries)} entries to {YML}")


if __name__ == "__main__":
    main()
