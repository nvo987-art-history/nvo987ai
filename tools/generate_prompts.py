#!/usr/bin/env python3
# ==========================================================
# FILE: tools/generate_prompts.py
# NVO987 AI – Prompt Generator (India)
# Generates 1000+ static prompt pages from data/prompts.json
# Uses prompts/template.html placeholders
# Also generates sitemap.xml + robots.txt in root
# 100% static / GitHub Pages compatible / Privacy-first
# ==========================================================

import os
import json
from datetime import datetime


# ----------------------------
# CONFIG
# ----------------------------
BASE_URL = "https://nvo987.ai.in"

DATA_FILE = "data/prompts.json"
TEMPLATE_FILE = "prompts/template.html"

OUTPUT_DIR = "prompts"
SITEMAP_FILE = "sitemap.xml"
ROBOTS_FILE = "robots.txt"

BANNER_IMAGE = "https://nvo987.ai.in/banner.jpg"


# ----------------------------
# HELPERS
# ----------------------------
def safe_escape_html(text: str) -> str:
    """Escape HTML special chars safely for inserting into HTML."""
    if text is None:
        return ""
    return (
        text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
    )


def normalize_slug(slug: str) -> str:
    """
    Slug must be like:
      /prompts/bug-fixing-assistant.html

    This function ensures:
      - starts with /
      - contains /prompts/
      - ends with .html
    """
    slug = slug.strip()

    if not slug.startswith("/"):
        slug = "/" + slug

    if not slug.startswith("/prompts/"):
        # If user provided only filename like bug-fixing.html
        if slug.endswith(".html"):
            slug = "/prompts/" + slug.lstrip("/")
        else:
            slug = "/prompts/" + slug.lstrip("/") + ".html"

    if not slug.endswith(".html"):
        slug += ".html"

    return slug


def extract_filename_from_slug(slug: str) -> str:
    """
    /prompts/bug-fixing-assistant.html -> bug-fixing-assistant.html
    """
    return slug.split("/")[-1]


def build_keywords(item: dict) -> str:
    """
    Generate keywords meta field.
    Uses title + category + tags.
    """
    tags = item.get("tags", [])
    category = item.get("category", "")
    title = item.get("title", "")

    keywords = ["NVO987", "NVO987 AI", "AI prompt", "prompt library", "India"]

    if category:
        keywords.append(category)

    if title:
        keywords.append(title)

    for t in tags:
        keywords.append(str(t))

    # remove duplicates
    seen = set()
    cleaned = []
    for k in keywords:
        k = k.strip()
        if k and k.lower() not in seen:
            seen.add(k.lower())
            cleaned.append(k)

    return ", ".join(cleaned)


def build_tags_string(tags) -> str:
    """Return tags as readable string: coding, debug, bugs"""
    if not tags:
        return ""
    return ", ".join([str(t) for t in tags])


def write_file(path: str, content: str):
    """Write UTF-8 file safely."""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


# ----------------------------
# GENERATE SITEMAP.XML
# ----------------------------
def generate_sitemap(urls: list) -> str:
    """
    Generate sitemap.xml content.
    """
    now = datetime.utcnow().strftime("%Y-%m-%d")

    out = []
    out.append('<?xml version="1.0" encoding="UTF-8"?>')
    out.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    for u in urls:
        out.append("  <url>")
        out.append(f"    <loc>{u}</loc>")
        out.append(f"    <lastmod>{now}</lastmod>")
        out.append("  </url>")

    out.append("</urlset>")
    out.append("")
    return "\n".join(out)


# ----------------------------
# GENERATE ROBOTS.TXT
# ----------------------------
def generate_robots() -> str:
    """
    Generate robots.txt for indexing.
    Allows everything, blocks template.html only.
    """
    return f"""User-agent: *
Allow: /

Disallow: /prompts/template.html

Sitemap: {BASE_URL}/sitemap.xml
"""


# ----------------------------
# MAIN
# ----------------------------
def main():
    # Check required files
    if not os.path.exists(DATA_FILE):
        raise FileNotFoundError(f"Missing: {DATA_FILE}")

    if not os.path.exists(TEMPLATE_FILE):
        raise FileNotFoundError(f"Missing: {TEMPLATE_FILE}")

    # Load template
    with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
        template_html = f.read()

    # Load prompts database
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        prompts = json.load(f)

    if not isinstance(prompts, list):
        raise ValueError("prompts.json must be a JSON array")

    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Dates
    today = datetime.utcnow().strftime("%Y-%m-%d")
    year = datetime.utcnow().strftime("%Y")

    generated_urls = []

    # Generate each prompt page
    for item in prompts:
        title = item.get("title", "").strip()
        description = item.get("description", "").strip()
        category = item.get("category", "prompt").strip()
        tags = item.get("tags", [])
        prompt_text = item.get("prompt", "").strip()

        if not title:
            print("Skipping item: missing title")
            continue

        if not description:
            description = f"Prompt template: {title}"

        # Slug must be full path: /prompts/name.html
        slug = normalize_slug(item.get("slug", ""))

        filename = extract_filename_from_slug(slug)
        out_path = os.path.join(OUTPUT_DIR, filename)

        canonical_url = f"{BASE_URL}{slug}"
        generated_urls.append(canonical_url)

        # keywords and tags
        keywords = build_keywords(item)
        tags_string = build_tags_string(tags)

        # HTML-safe content
        safe_title = safe_escape_html(title)
        safe_description = safe_escape_html(description)
        safe_keywords = safe_escape_html(keywords)
        safe_category = safe_escape_html(category)
        safe_tags = safe_escape_html(tags_string)
        safe_prompt_text = safe_escape_html(prompt_text)

        # Fill template placeholders
        html = template_html

        html = html.replace("{{TITLE}}", safe_title)
        html = html.replace("{{DESCRIPTION}}", safe_description)
        html = html.replace("{{KEYWORDS}}", safe_keywords)
        html = html.replace("{{CATEGORY}}", safe_category)
        html = html.replace("{{TAGS}}", safe_tags)
        html = html.replace("{{PROMPT_TEXT}}", safe_prompt_text)

        # IMPORTANT: {{SLUG}} should be WITHOUT /prompts/ and WITHOUT .html in your template system
        # BUT your template currently expects {{SLUG}} in URLs.
        # We will supply slug without "/prompts/" and without ".html"
        slug_clean = filename.replace(".html", "")
        html = html.replace("{{SLUG}}", slug_clean)

        # Dates
        html = html.replace("{{DATE_PUBLISHED}}", today)
        html = html.replace("{{DATE_MODIFIED}}", today)

        # Write file
        write_file(out_path, html)

        print(f"Generated: {out_path}")

    # ----------------------------
    # SITEMAP URLS (STATIC PAGES)
    # ----------------------------
    static_urls = [
        f"{BASE_URL}/",
        f"{BASE_URL}/index.html",
        f"{BASE_URL}/prompts/",
        f"{BASE_URL}/prompts/index.html",
        f"{BASE_URL}/legal.html",
        f"{BASE_URL}/contact.html",
    ]

    all_urls = static_urls + generated_urls

    # Remove duplicates while preserving order
    seen = set()
    final_urls = []
    for u in all_urls:
        if u not in seen:
            seen.add(u)
            final_urls.append(u)

    # Generate sitemap.xml
    sitemap_content = generate_sitemap(final_urls)
    write_file(SITEMAP_FILE, sitemap_content)

    # Generate robots.txt
    robots_content = generate_robots()
    write_file(ROBOTS_FILE, robots_content)

    print(f"\nGenerated {len(generated_urls)} prompt pages.")
    print(f"Updated {SITEMAP_FILE}")
    print(f"Updated {ROBOTS_FILE}")


if __name__ == "__main__":
    main()
