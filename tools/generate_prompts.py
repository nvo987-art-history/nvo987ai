#!/usr/bin/env python3
# ==========================================================
# FILE: tools/generate_prompts.py
# NVO987 AI – Prompt Generator (India)
# Generates static prompt pages from data/prompts.json
# Uses prompts/template.html placeholders
# Generates paginated index pages (25 per page)
# Generates sitemap.xml + robots.txt in root
# GitHub Pages compatible / Privacy-first
# ==========================================================

import os
import json
import math
from datetime import datetime


# ----------------------------
# CONFIG
# ----------------------------
BASE_URL = "https://nvo987.ai.in"

DATA_FILE = "data/prompts.json"
TEMPLATE_FILE = "prompts/template.html"

OUTPUT_DIR = "prompts"
PAGES_DIR = "prompts/page"

SITEMAP_FILE = "sitemap.xml"
ROBOTS_FILE = "robots.txt"

PROMPTS_PER_PAGE = 25


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
    """
    if not slug:
        return ""

    slug = slug.strip()
    slug = slug.replace(BASE_URL, "")

    if not slug.startswith("/"):
        slug = "/" + slug

    if not slug.startswith("/prompts/"):
        cleaned = slug.lstrip("/")
        if cleaned.startswith("prompts/"):
            cleaned = cleaned.replace("prompts/", "", 1)
        slug = "/prompts/" + cleaned

    if not slug.endswith(".html"):
        slug += ".html"

    return slug


def extract_filename_from_slug(slug: str) -> str:
    """ /prompts/example.html -> example.html """
    return slug.split("/")[-1]


def extract_slug_id_from_filename(filename: str) -> str:
    """ example.html -> example """
    if filename.endswith(".html"):
        return filename[:-5]
    return filename


def build_keywords(item: dict) -> str:
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
    if not tags:
        return ""
    return ", ".join([str(t) for t in tags])


def write_file(path: str, content: str):
    """
    Safe write file.
    Fix: if path has no folder (example: sitemap.xml),
    do NOT call os.makedirs("").
    """
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


# ----------------------------
# SITEMAP.XML
# ----------------------------
def generate_sitemap(urls: list) -> str:
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
    return f"""User-agent: *
Allow: /

Disallow: /prompts/template.html

Sitemap: {BASE_URL}/sitemap.xml
"""


# ----------------------------
# INDEX PAGE GENERATOR (SEARCH + PAGINATION)
# ----------------------------
def build_prompt_index_page(prompts, page_num, total_pages, today):
    cards = []

    for item in prompts:
        title = safe_escape_html(item.get("title", "Untitled"))
        description = safe_escape_html(item.get("description", ""))
        category = safe_escape_html(item.get("category", "prompt"))
        tags = item.get("tags", [])
        tags_str = safe_escape_html(", ".join(tags)) if tags else ""

        slug = normalize_slug(item.get("slug", ""))

        # slug is /prompts/example.html
        # from /prompts/page/1.html we need ../example.html
        local_filename = extract_filename_from_slug(slug)

        cards.append(f"""
        <article class="place-card prompt-card"
          data-title="{title.lower()}"
          data-description="{description.lower()}"
          data-category="{category.lower()}"
          data-tags="{tags_str.lower()}">

          <div class="place-type">{category.upper()}</div>
          <h3>{title}</h3>
          <p class="place-desc">{description}</p>
          <p class="small-note muted">Tags: {tags_str}</p>

          <div class="place-actions">
            <a class="btn" href="../{local_filename}">Open Prompt</a>
          </div>
        </article>
        """)

    cards_html = "\n".join(cards)

    pagination_links = []

    if page_num > 1:
        pagination_links.append(f'<a class="btn secondary" href="{page_num-1}.html">← Previous</a>')
    else:
        pagination_links.append(f'<span class="btn secondary disabled">← Previous</span>')

    pagination_links.append(f'<span class="page-indicator">Page {page_num} / {total_pages}</span>')

    if page_num < total_pages:
        pagination_links.append(f'<a class="btn secondary" href="{page_num+1}.html">Next →</a>')
    else:
        pagination_links.append(f'<span class="btn secondary disabled">Next →</span>')

    pagination_html = "\n".join(pagination_links)

    html = f"""<!DOCTYPE html>
<html lang="en-IN">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="x-ua-compatible" content="ie=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <title>Prompt Library Index – Page {page_num} | NVO987 AI</title>
  <meta name="description" content="Browse NVO987 AI prompts for India. Search by category, tags, and keywords. Page {page_num} of {total_pages}.">
  <meta name="robots" content="index, follow">
  <meta name="theme-color" content="#f6f1e9">
  <meta name="color-scheme" content="light">
  <link rel="canonical" href="{BASE_URL}/prompts/page/{page_num}.html">

  <link rel="icon" href="../../favicon.ico" sizes="any">
  <link rel="apple-touch-icon" href="../../apple-touch-icon.png">
  <link rel="stylesheet" href="../../style.css">
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
          <a href="../../index.html">Home</a>
          <a href="../index.html">Prompts</a>
          <a href="../../legal.html">Legal</a>
          <a href="../../contact.html">Contact</a>
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
        <div class="legal-card">
          <h2>Search prompts</h2>
          <input id="searchBox" type="text" placeholder="Search prompts (title, category, tags)..."
            style="width:100%; padding:14px; font-size:16px; border-radius:12px; border:1px solid #ccc;">
          <p class="small-note muted" style="margin-top:10px;">
            Works instantly. No tracking. No analytics. Search runs only in your browser.
          </p>
        </div>
      </section>

      <section class="section">
        <div class="grid" id="promptGrid">
          {cards_html}
        </div>
      </section>

      <section class="section">
        <div class="legal-card" style="display:flex; justify-content:space-between; align-items:center; gap:10px; flex-wrap:wrap;">
          {pagination_html}
        </div>
      </section>

    </div>
  </main>

  <footer class="footer">
    <div class="container footer-inner">
      <p>
        © <span id="year"></span> NVO987 AI Prompt Library (India) ·
        <a href="../../index.html">Home</a> ·
        <a href="../index.html">Prompts</a> ·
        <a href="../../legal.html">Legal</a> ·
        <a href="../../contact.html">Contact</a>
      </p>

      <p class="small-note muted">
        100% static website. No cookies. No tracking. No analytics. No profiling.
      </p>
    </div>
  </footer>

  <script>
    document.getElementById("year").textContent = new Date().getFullYear();

    const searchBox = document.getElementById("searchBox");
    const cards = document.querySelectorAll(".prompt-card");

    searchBox.addEventListener("input", () => {{
      const q = searchBox.value.toLowerCase().trim();

      cards.forEach(card => {{
        const text =
          (card.dataset.title || "") +
          " " +
          (card.dataset.description || "") +
          " " +
          (card.dataset.category || "") +
          " " +
          (card.dataset.tags || "");

        if (text.includes(q)) {{
          card.style.display = "";
        }} else {{
          card.style.display = "none";
        }}
      }});
    }});
  </script>

</body>
</html>
"""
    return html


# ----------------------------
# MAIN
# ----------------------------
def main():
    if not os.path.exists(DATA_FILE):
        raise FileNotFoundError(f"Missing: {DATA_FILE}")

    if not os.path.exists(TEMPLATE_FILE):
        raise FileNotFoundError(f"Missing: {TEMPLATE_FILE}")

    with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
        template_html = f.read()

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        prompts = json.load(f)

    if not isinstance(prompts, list):
        raise ValueError("prompts.json must be a JSON array")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(PAGES_DIR, exist_ok=True)

    today = datetime.utcnow().strftime("%Y-%m-%d")

    generated_urls = []
    generated_files = []

    # ----------------------------
    # GENERATE PROMPT PAGES
    # ----------------------------
    for item in prompts:
        title = item.get("title", "").strip()
        description = item.get("description", "").strip()
        category = item.get("category", "prompt").strip()
        tags = item.get("tags", [])

        # IMPORTANT: prompt might not exist
        prompt_text = item.get("prompt", "").strip()

        if not prompt_text:
            prompt_text = f"[PROMPT MISSING]\n\nThis prompt entry has no 'prompt' field in prompts.json.\n\nTitle: {title}\nCategory: {category}\nTags: {', '.join(tags)}\n\nFix: add a 'prompt' field to this JSON item."

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
        html = html.replace("{{SLUG}}", slug_id)

        html = html.replace("{{DATE_PUBLISHED}}", today)
        html = html.replace("{{DATE_MODIFIED}}", today)

        write_file(out_path, html)
        generated_files.append(out_path)

        print(f"Generated prompt: {out_path}")

    # ----------------------------
    # GENERATE PAGINATED INDEX
    # ----------------------------
    total_prompts = len(prompts)
    total_pages = max(1, math.ceil(total_prompts / PROMPTS_PER_PAGE))

    for page_num in range(1, total_pages + 1):
        start = (page_num - 1) * PROMPTS_PER_PAGE
        end = start + PROMPTS_PER_PAGE
        page_items = prompts[start:end]

        page_html = build_prompt_index_page(page_items, page_num, total_pages, today)

        out_page_path = os.path.join(PAGES_DIR, f"{page_num}.html")
        write_file(out_page_path, page_html)

        print(f"Generated index page: {out_page_path}")

    # prompts/index.html should match page/1.html
    index_html_path = os.path.join(OUTPUT_DIR, "index.html")
    first_page_path = os.path.join(PAGES_DIR, "1.html")

    with open(first_page_path, "r", encoding="utf-8") as f:
        first_page_html = f.read()

    first_page_html = first_page_html.replace(
        f'{BASE_URL}/prompts/page/1.html',
        f'{BASE_URL}/prompts/index.html'
    )

    write_file(index_html_path, first_page_html)

    # ----------------------------
    # STATIC URLS FOR SITEMAP
    # ----------------------------
    static_urls = [
        f"{BASE_URL}/",
        f"{BASE_URL}/index.html",
        f"{BASE_URL}/prompts/index.html",
        f"{BASE_URL}/legal.html",
        f"{BASE_URL}/contact.html",
    ]

    pagination_urls = []
    for page_num in range(1, total_pages + 1):
        pagination_urls.append(f"{BASE_URL}/prompts/page/{page_num}.html")

    all_urls = static_urls + pagination_urls + generated_urls

    seen = set()
    final_urls = []
    for u in all_urls:
        if u not in seen:
            seen.add(u)
            final_urls.append(u)

    sitemap_content = generate_sitemap(final_urls)
    write_file(SITEMAP_FILE, sitemap_content)

    robots_content = generate_robots()
    write_file(ROBOTS_FILE, robots_content)

    print("\n===============================")
    print(f"Generated prompt pages: {len(generated_urls)}")
    print(f"Generated index pages: {total_pages}")
    print(f"Updated sitemap: {SITEMAP_FILE}")
    print(f"Updated robots: {ROBOTS_FILE}")
    print("===============================")


if __name__ == "__main__":
    main()
