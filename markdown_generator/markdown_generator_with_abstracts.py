#!/usr/bin/env python
# coding: utf-8

"""
Markdown generator for publications with abstracts (Jekyll-compatible)
Run from:
C:\Users\Olivia\Dropbox\Applications\Github\OliviaBrtl.github.io\markdown_generator
"""

from pybtex.database.input import bibtex
from time import strptime
import html
import os
import re

publist = {
    "article": {
        "file": "../files/Publications.bib",
        "venuekey": "journal",
        "venue-pretext": "",
        "collection": {
            "name": "publications",
            "permalink": "/publication/"
        }
    }
}

html_escape_table = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;"
}

def html_escape(text):
    return "".join(html_escape_table.get(c, c) for c in text)

for pubsource in publist:
    parser = bibtex.Parser()
    bibdata = parser.parse_file(publist[pubsource]["file"])

    for bib_id, entry in bibdata.entries.items():
        pub_year, pub_month, pub_day = "1900", "01", "01"
        b = entry.fields

        try:
            pub_year = f'{b["year"]}'
            if "month" in b:
                if len(b["month"]) < 3:
                    pub_month = "0" + b["month"]
                    pub_month = pub_month[-2:]
                elif not b["month"].isdigit():
                    tmnth = strptime(b["month"][:3], "%b").tm_mon
                    pub_month = f"{tmnth:02d}"
                else:
                    pub_month = b["month"]
            if "day" in b:
                pub_day = b["day"]

            pub_date = f"{pub_year}-{pub_month}-{pub_day}"
            clean_title = b["title"].translate(str.maketrans("", "", "{}\")).replace(" ", "-")
            url_slug = re.sub(r"\[.*\]|[^a-zA-Z0-9_-]", "", clean_title).replace("--", "-")
            md_filename = f"{pub_date}-{url_slug}.md".replace("--", "-")
            html_filename = f"{pub_date}-{url_slug}".replace("--", "-")

            citation = ""
            for author in entry.persons["author"]:
                citation += f"{author.first_names[0]} {author.last_names[0]}, "
            citation = citation.rstrip(", ") + ". ""
            citation += html_escape(b["title"].translate(str.maketrans("", "", "{}\"))) + ""."
            venue = publist[pubsource]["venue-pretext"] + b[publist[pubsource]["venuekey"]].translate(str.maketrans("", "", "{}\"))
            citation += " " + html_escape(venue) + ", " + pub_year + "."

            md = "---\n"
            md += f'title: "{html_escape(b["title"].translate(str.maketrans("", "", "{}\")))}"\n'
            md += f'collection: {publist[pubsource]["collection"]["name"]}\n'
            md += f'permalink: {publist[pubsource]["collection"]["permalink"]}{html_filename}\n'
            md += f'date: {pub_date}\n'
            md += f'venue: "{html_escape(venue)}"\n'
            md += f'citation: "{html_escape(citation)}"\n'

            if "abstract" in b and len(b["abstract"]) > 10:
                abstract = html_escape(b["abstract"])
                md += f'abstract: "{abstract}"\n'

            if "note" in b and len(b["note"]) > 5:
                md += f'excerpt: "{html_escape(b["note"])}"\n'

            if "url" in b and len(b["url"]) > 5:
                md += f'paperurl: "{b["url"]}"\n'

            md += "---\n"

            if "abstract" in b and len(b["abstract"]) > 10:
                md += f"**Abstract:** {abstract}\n\n"

            if "note" in b:
                md += html_escape(b["note"]) + "\n"

            if "url" in b:
                md += f'[Access paper here]({b["url"]}){{:target="_blank"}}\n'
            else:
                search_title = clean_title.replace("-", "+")
                md += f'Use [Google Scholar](https://scholar.google.com/scholar?q={search_title}){{:target="_blank"}}\n'

            os.makedirs("../_publications", exist_ok=True)
            with open(f"../_publications/{md_filename}", "w", encoding="utf-8") as f:
                f.write(md)
            print(f"✓ Parsed {bib_id}: {b['title'][:60]}" + ("..." if len(b['title']) > 60 else ""))

        except KeyError as e:
            print(f"⚠ Missing field {e} in {bib_id}: {b.get('title', 'UNKNOWN TITLE')[:30]}...")
            continue
