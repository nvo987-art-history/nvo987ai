# ==========================================================
# FILE: tools/generate_prompts.py
# NVO987 AI – Static Prompt Page Generator (India)
# Generates:
#   - /prompts/*.html from prompts/template.html
#   - sitemap.xml (auto updated)
#   - robots.txt (auto updated)
# Compatible with GitHub Actions + GitHub Pages
# ==========================================================

import os
import json
from datetime import datetime


BASE_URL = "https://nvo987.ai.in"

OUTPUT_DIR = "prompts"
DATA_FILE = "data/prompts.json"
TEMPLATE_FILE = "prompts/template.html"

SITEMAP_FILE = "sitemap.xml"
ROBOTS_FILE = "robots.txt"


def safe_html(text: str) -> str:
    if text is None:
        return ""
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def normalize_slug(slug: str) -> str:
    """
    Supports:
      "bug-fixing"
      "bug-fixing.html"
      "/prompts/bug-fixing.html"
      "prompts/bug-fixing.html"
    Returns:
      "bug-fixing"
    """
    if not slug:
        return ""

    slug = slug.strip().replace("\\", "/")

    if slug.startswith("/"):
        slug = slug[1:]

    if slug.startswith("prompts/"):
        slug = slug[len("prompts/"):]

    if slug.endswith(".html"):
        slug = slug[:-5]

    return slug


def build_tags(tags):
    if not tags:
        return ""

    out = []
    for t in tags:
        out.append(f'<span class="pill">{safe_html(t)}</span>')

    return "\n            ".join(out)


def load_template():
    if not os.path.exists(TEMPLATE_FILE):
        raise FileNotFoundError(f"Missing template file: {TEMPLATE_FILE}")

    with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
        return f.read()


def generate_page(template, item, today, year):
    title = safe_html(item.get("title", "Untitled Prompt"))
    description = safe_html(item.get("description", ""))
    category = safe_html(item.get("category", "general"))

    tags_list = item.get("tags", [])
    tags_string = ", ".join(tags_list) if isinstance(tags_list, list) else str(tags_list)
    tags_string = safe_html(tags_string)

    keywords = safe_html(item.get("keywords", tags_string))

    prompt_text_raw = item.get("prompt_text", item.get("prompt", ""))
    prompt_text = safe_html(prompt_text_raw)

    slug_clean = normalize_slug(item.get("slug", ""))

    if not slug_clean:
        raise ValueError(f"Missing or invalid slug for item: {item.get('title')}")

    canonical_url = f"{BASE_URL}/prompts/{slug_clean}.html"

    # Replace placeholders in template.html
    html = template
    html = html.replace("{{TITLE}}", title)
    html = html.replace("{{DESCRIPTION}}", description)
    html = html.replace("{{CATEGORY}}", category)
    html = html.replace("{{TAGS}}", tags_string)
    html = html.replace("{{KEYWORDS}}", keywords)
    html = html.replace("{{PROMPT_TEXT}}", prompt_text)
    html = html.replace("{{SLUG}}", slug_clean)
    html = html.replace("{{DATE_PUBLISHED}}", today)
    html = html.replace("{{DATE_MODIFIED}}", today)

    # IMPORTANT:
    # Generated pages must be indexable (template is noindex by design)
    html = html.replace(
        '<meta name="robots" content="noindex, nofollow, noarchive">',
        '<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">'
    )

    return slug_clean, canonical_url, html


def write_sitemap(urls, today):
    with open(SITEMAP_FILE, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')

        # Core pages
        f.write(f"  <url><loc>{BASE_URL}/</loc><lastmod>{today}</lastmod></url>\n")
        f.write(f"  <url><loc>{BASE_URL}/prompts/</loc><lastmod>{today}</lastmod></url>\n")
        f.write(f"  <url><loc>{BASE_URL}/prompts/index.html</loc><lastmod>{today}</lastmod></url>\n")
        f.write(f"  <url><loc>{BASE_URL}/legal.html</loc><lastmod>{today}</lastmod></url>\n")
        f.write(f"  <url><loc>{BASE_URL}/contact.html</loc><lastmod>{today}</lastmod></url>\n")

        # Prompt pages
        for url in urls:
            f.write(f"  <url><loc>{url}</loc><lastmod>{today}</lastmod></url>\n")

        f.write("</urlset>\n")


def write_robots():
    with open(ROBOTS_FILE, "w", encoding="utf-8") as f:
        f.write("User-agent: *\n")
        f.write("Allow: /\n\n")
        f.write(f"Sitemap: {BASE_URL}/sitemap.xml\n")


def main():
    if not os.path.exists(DATA_FILE):
        raise FileNotFoundError(f"Missing {DATA_FILE}")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        prompts = json.load(f)

    template = load_template()

    today = datetime.utcnow().strftime("%Y-%m-%d")
    year = datetime.utcnow().strftime("%Y")

    generated_urls = []

    for item in prompts:
        slug_clean, canonical_url, html = generate_page(template, item, today, year)

        out_file = slug_clean + ".html"
        out_path = os.path.join(OUTPUT_DIR, out_file)

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)

        generated_urls.append(canonical_url)

    write_sitemap(generated_urls, today)
    write_robots()

    print(f"Generated {len(prompts)} prompt pages.")
    print("Updated sitemap.xml")
    print("Updated robots.txt")


if __name__ == "__main__":
    main()
