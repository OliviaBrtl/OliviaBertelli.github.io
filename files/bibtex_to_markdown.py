import os
import bibtexparser

# Path to your BibTeX file and the output directory
BIBTEX_FILE = "Publications.bib"
OUTPUT_DIR = "_publications"

def sanitize_filename(s):
    return "".join(c if c.isalnum() or c in '-_.' else '_' for c in s)

def bib_entry_to_markdown(entry):
    # Build YAML front matter
    yaml = []
    yaml.append('---')
    yaml.append(f'title: "{entry.get("title","").replace("{","").replace("}","")}"')
    yaml.append(f'year: {entry.get("year","")}')
    yaml.append(f'citation: "{entry.get("author","")}, {entry.get("title","").replace("{","").replace("}","")}, {entry.get("journal", entry.get("institution",""))}, {entry.get("year","")}"')
    if "abstract" in entry:
        yaml.append('abstract: "{}"'.format(entry["abstract"].replace('"', '\\"')))
    if "journal" in entry:
        yaml.append(f'journal: "{entry["journal"]}"')
    if "author" in entry:
        yaml.append(f'author: "{entry["author"]}"')
    if "doi" in entry or "DOI" in entry:
        yaml.append(f'doi: "{entry.get("doi", entry.get("DOI",""))}"')
    if "url" in entry:
        yaml.append(f'url: "{entry["url"]}"')
    yaml.append('---')
    return "\n".join(yaml) + "\n"

def main():
    with open(BIBTEX_FILE, encoding='utf-8') as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)

   import re

def slugify(value):
    value = value.lower()
    value = re.sub(r'[^\w\s-]', '', value)
    value = re.sub(r'[\s_-]+', '-', value)
    value = value.strip('-')
    return value

for entry in bib_database.entries:
    year = entry.get('year', '1900')
    month = entry.get('month', '01').zfill(2) if 'month' in entry else '01'
    day = '01'
    title_raw = entry.get('title', 'untitled').replace('{','').replace('}','')
    title_slug = slugify(title_raw)
    filename = f"{year}-{month}-{day}-{title_slug}.md"
    md_content = bib_entry_to_markdown(entry)
    output_path = os.path.join(OUTPUT_DIR, filename)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Written: {output_path}")

if __name__ == "__main__":
    main()
