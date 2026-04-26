#!/usr/bin/env python3
# ==========================================================
# FILE: tools/generate_prompts.py
# NVO987 AI – Prompt Generator (India)
#
# Generates:
#   - /prompts/*.html pages from data/prompts.json
#   - /prompts/index.html (prompt directory)
#   - /index.html Quick Access section (auto updated)
#   - sitemap.xml (root)
#   - robots.txt (root)
#
# GitHub Pages compatible / 100% static / Privacy-first
# ==========================================================

import os
import json
import re
from datetime import datetime


# ----------------------------
# CONFIG
# ----------------------------
BASE_URL = "https://nvo987.ai.in"

DATA_FILE = "data/prompts.json"
TEMPLATE_FILE = "prompts/template.html"

OUTPUT_DIR = "prompts"
PROMPTS_INDEX_FILE = "prompts/index.html"

ROOT_INDEX_FILE = "index.html"
SITEMAP_FILE = "sitemap.xml"
ROBOTS_FILE = "robots.txt"


# ----------------------------
# HELPERS
# ----------------------------
def safe_escape_html(text: str) -> str:
    """Escape HTML special chars safely for inserting into HTML."""
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
    Ensures slug is always in this format:
      /prompts/filename.html

    Accepts:
      - "bug-fixing.html"
      - "/bug-fixing.html"
      - "/prompts/bug-fixing.html"
      - "prompts/bug-fixing.html"
      - full URL with domain
    """
    if not slug:
        return ""

    slug = slug.strip()
    slug = slug.replace(BASE_URL, "")

    if not slug.startswith("/"):
        slug = "/" + slug

    if slug.startswith("/prompts/"):
        pass
    else:
        cleaned = slug.lstrip("/")
        if cleaned.startswith("prompts/"):
            cleaned = cleaned.replace("prompts/", "", 1)
        slug = "/prompts/" + cleaned

    if not slug.endswith(".html"):
        slug += ".html"

    return slug


def extract_filename_from_slug(slug: str) -> str:
    """ /prompts/bug-fixing-assistant.html -> bug-fixing-assistant.html """
    return slug.split("/")[-1]


def extract_slug_id_from_filename(filename: str) -> str:
    """ bug-fixing-assistant.html -> bug-fixing-assistant """
    if filename.endswith(".html"):
        return filename[:-5]
    return filename


def build_keywords(item: dict) -> str:
    """Generate keywords meta field from title + category + tags."""
    tags = item.get("tags", [])
    category = item.get("category", "")
    title = item.get("title", "")

    keywords = [
        "NVO987",
        "NVO987 AI",
        "AI prompt",
        "prompt library",
        "India",
        "ChatGPT prompts",
        "Gemini prompts",
        "Claude prompts"
    ]

    if category:
        keywords.append(str(category))

    if title:
        keywords.append(str(title))

    for t in tags:
        keywords.append(str(t))

    seen = set()
    cleaned = []
    for k in keywords:
        k = k.strip()
        if k and k.lower() not in seen:
            seen.add(k.lower())
            cleaned.append(k)

    return ", ".join(cleaned)


def build_tags_string(tags) -> str:
    """Return tags as readable string."""
    if not tags:
        return ""
    return ", ".join([str(t) for t in tags])


def write_file(path: str, content: str):
    """Write UTF-8 file safely."""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def read_file(path: str) -> str:
    """Read UTF-8 file safely."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# ----------------------------
# SITEMAP.XML
# ----------------------------
def generate_sitemap(urls: list) -> str:
    """Generate sitemap.xml content."""
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
# ROBOTS.TXT
# ----------------------------
def generate_robots() -> str:
    """Generate robots.txt for indexing."""
    return f"""User-agent: *
Allow: /

Disallow: /prompts/template.html

Sitemap: {BASE_URL}/sitemap.xml
"""


# ----------------------------
# PROMPTS INDEX PAGE
# ----------------------------
def generate_prompts_index_html(prompts: list) -> str:
    """Generate prompts/index.html listing page."""
    today = datetime.utcnow().strftime("%Y-%m-%d")

    cards = []

    for item in prompts:
        title = safe_escape_html(item.get("title", "Untitled"))
        description = safe_escape_html(item.get("description", ""))
        category = safe_escape_html(item.get("category", "prompt"))
        tags = item.get("tags", [])
        tags_string = safe_escape_html(build_tags_string(tags))

        slug = normalize_slug(item.get("slug", ""))
        if not slug:
            continue

        filename = extract_filename_from_slug(slug)

        cards.append(f"""
        <article class="place-card">
          <div class="place-type">{category.capitalize()}</div>
          <h3>{title}</h3>
          <p class="place-desc">{description}</p>
          <p class="small-note muted">Tags: <strong>{tags_string}</strong></p>
          <div class="place-actions">
            <a class="btn" href="{filename}">Open Prompt</a>
          </div>
        </article>
        """)

    cards_html = "\n".join(cards)

    return f"""<!DOCTYPE html>
<html lang="en-IN">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="x-ua-compatible" content="ie=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <title>Prompt Library Index | NVO987 AI</title>
  <meta name="description" content="Browse the full NVO987 AI prompt directory. 100% static and privacy-first.">
  <meta name="robots" content="index, follow">
  <meta name="theme-color" content="#f6f1e9">
  <link rel="canonical" href="{BASE_URL}/prompts/index.html">

  <link rel="icon" href="../favicon.ico" sizes="any">
  <link rel="apple-touch-icon" href="../apple-touch-icon.png">
  <link rel="stylesheet" href="../style.css">
</head>

<body>

  <div class="topbar">
    <div class="container">
      <div class="topbar-inner">

        <div class="brand">
          <span class="brand-name">NVO987 AI</span>
          <span class="brand-tag">Prompt Library · India</span>
        </div>

        <nav class="nav">
          <a href="../index.html">Home</a>
          <a href="index.html">Prompts</a>
          <a href="../legal.html">Legal</a>
          <a href="../contact.html">Contact</a>
        </nav>

      </div>
    </div>
  </div>

  <main class="main">
    <div class="container">

      <section class="section">
        <div class="section-header">
          <h1>Prompt Library Index</h1>
          <p>Browse all prompts generated from our JSON database.</p>
          <p class="small-note muted">Last updated: {today}</p>
        </div>
      </section>

      <section class="section">
        <div class="grid">
          {cards_html}
        </div>
      </section>

    </div>
  </main>

  <footer class="footer">
    <div class="container footer-inner">
      <p>
        © <span id="year"></span> NVO987 AI Prompt Library (India) ·
        <a href="../index.html">Home</a> ·
        <a href="index.html">Prompts</a> ·
        <a href="../legal.html">Legal</a> ·
        <a href="../contact.html">Contact</a>
      </p>
      <p class="small-note muted">
        100% static website. No cookies. No tracking. No analytics.
      </p>
    </div>
  </footer>

  <script>
    document.getElementById("year").textContent = new Date().getFullYear();
  </script>

</body>
</html>
"""


# ----------------------------
# ROOT INDEX QUICK ACCESS UPDATE
# ----------------------------
def build_quick_access_html(prompts: list, max_items: int = 6) -> str:
    """Generate the Quick Access card grid for index.html."""
    cards = []

    for item in prompts[:max_items]:
        title = safe_escape_html(item.get("title", "Untitled"))
        description = safe_escape_html(item.get("description", ""))
        category = safe_escape_html(item.get("category", "prompt"))

        slug = normalize_slug(item.get("slug", ""))
        if not slug:
            continue

        filename = extract_filename_from_slug(slug)

        cards.append(f"""
        <article class="place-card">
          <div class="place-type">{category.capitalize()}</div>
          <h3>{title}</h3>
          <p class="place-desc">{description}</p>
          <div class="place-actions">
            <a class="btn" href="prompts/{filename}">Open Prompt</a>
          </div>
        </article>
        """)

    return "\n".join(cards)


def update_root_index_html(prompts: list):
    """
    Updates ONLY the Quick Access grid in index.html.
    It searches for markers:

      <!-- QUICK_ACCESS_START -->
      ...
      <!-- QUICK_ACCESS_END -->

    Everything between them will be replaced.
    """
    if not os.path.exists(ROOT_INDEX_FILE):
        print("Skipping root index update: index.html not found.")
        return

    html = read_file(ROOT_INDEX_FILE)

    quick_access_cards = build_quick_access_html(prompts, max_items=6)

    replacement_block = f"""<!-- QUICK_ACCESS_START -->
<div class="grid">
{quick_access_cards}
</div>
<!-- QUICK_ACCESS_END -->"""

    pattern = r"<!-- QUICK_ACCESS_START -->(.*?)<!-- QUICK_ACCESS_END -->"
    if not re.search(pattern, html, flags=re.DOTALL):
        print("WARNING: index.html does not contain QUICK_ACCESS markers.")
        print("Add these markers in index.html to enable auto-update.")
        return

    html_new = re.sub(pattern, replacement_block, html, flags=re.DOTALL)
    write_file(ROOT_INDEX_FILE, html_new)
    print("Updated: index.html Quick Access section")


# ----------------------------
# MAIN
# ----------------------------
def main():
    if not os.path.exists(DATA_FILE):
        raise FileNotFoundError(f"Missing: {DATA_FILE}")

    if not os.path.exists(TEMPLATE_FILE):
        raise FileNotFoundError(f"Missing: {TEMPLATE_FILE}")

    template_html = read_file(TEMPLATE_FILE)

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        prompts = json.load(f)

    if not isinstance(prompts, list):
        raise ValueError("prompts.json must be a JSON array")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    today = datetime.utcnow().strftime("%Y-%m-%d")

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

        slug = normalize_slug(item.get("slug", ""))
        if not slug:
            print(f"Skipping item: missing slug ({title})")
            continue

        filename = extract_filename_from_slug(slug)
        slug_id = extract_slug_id_from_filename(filename)

        out_path = os.path.join(OUTPUT_DIR, filename)

        canonical_url = f"{BASE_URL}{slug}"
        generated_urls.append(canonical_url)

        keywords = build_keywords(item)
        tags_string = build_tags_string(tags)

        safe_title = safe_escape_html(title)
        safe_description = safe_escape_html(description)
        safe_keywords = safe_escape_html(keywords)
        safe_category = safe_escape_html(category)
        safe_tags = safe_escape_html(tags_string)
        safe_prompt_text = safe_escape_html(prompt_text)

        html = template_html

        html = html.replace("{{TITLE}}", safe_title)
        html = html.replace("{{DESCRIPTION}}", safe_description)
        html = html.replace("{{KEYWORDS}}", safe_keywords)
        html = html.replace("{{CATEGORY}}", safe_category)
        html = html.replace("{{TAGS}}", safe_tags)
        html = html.replace("{{PROMPT_TEXT}}", safe_prompt_text)

        # Template expects: /prompts/{{SLUG}}.html
        html = html.replace("{{SLUG}}", slug_id)

        html = html.replace("{{DATE_PUBLISHED}}", today)
        html = html.replace("{{DATE_MODIFIED}}", today)

        write_file(out_path, html)
        print(f"Generated: {out_path}")

    # Generate prompts/index.html
    prompts_index_html = generate_prompts_index_html(prompts)
    write_file(PROMPTS_INDEX_FILE, prompts_index_html)
    print(f"Generated: {PROMPTS_INDEX_FILE}")

    # Update root index.html Quick Access section
    update_root_index_html(prompts)

    # Generate sitemap.xml
    static_urls = [
        f"{BASE_URL}/",
        f"{BASE_URL}/index.html",
        f"{BASE_URL}/prompts/index.html",
        f"{BASE_URL}/legal.html",
        f"{BASE_URL}/contact.html",
    ]

    all_urls = static_urls + generated_urls

    seen = set()
    final_urls = []
    for u in all_urls:
        if u not in seen:
            seen.add(u)
            final_urls.append(u)

    sitemap_content = generate_sitemap(final_urls)
    write_file(SITEMAP_FILE, sitemap_content)

    # Generate robots.txt
    robots_content = generate_robots()
    write_file(ROBOTS_FILE, robots_content)

    print("\nDONE.")
    print(f"Generated prompt pages: {len(generated_urls)}")
    print(f"Updated: {SITEMAP_FILE}")
    print(f"Updated: {ROBOTS_FILE}")


if __name__ == "__main__":
    main()
