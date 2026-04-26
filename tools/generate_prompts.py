import os
import json
from datetime import datetime

BASE_URL = "https://nvo987.ai.in"
OUTPUT_DIR = "prompts"
DATA_FILE = "data/prompts.json"

STYLE_PATH = "../style.css"
BANNER_IMAGE = "https://nvo987.ai.in/banner.jpg"


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta http-equiv="x-ua-compatible" content="ie=edge" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />

  <title>{title} | NVO987 AI Prompt Library</title>

  <meta name="description" content="{meta_description}" />
  <meta name="robots" content="index, follow" />
  <meta name="referrer" content="no-referrer" />
  <meta name="color-scheme" content="light" />
  <meta name="format-detection" content="telephone=no" />

  <link rel="canonical" href="{canonical}" />

  <meta property="og:site_name" content="NVO987 AI Prompt Library (India)" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{meta_description}" />
  <meta property="og:type" content="article" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:image" content="{banner_image}" />
  <meta property="og:locale" content="en_IN" />

  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{title}" />
  <meta name="twitter:description" content="{meta_description}" />
  <meta name="twitter:image" content="{banner_image}" />

  <link rel="stylesheet" href="{style_path}" />
  <link rel="icon" href="/favicon.ico" sizes="any" />

  <!-- JSON-LD Schema -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "TechArticle",
    "headline": "{title}",
    "description": "{meta_description}",
    "author": {{
      "@type": "Organization",
      "name": "NVO987"
    }},
    "publisher": {{
      "@type": "Organization",
      "name": "NVO987",
      "url": "https://nvo987.ai.in"
    }},
    "datePublished": "{date_published}",
    "mainEntityOfPage": "{canonical}"
  }}
  </script>
</head>

<body>

  <div class="topbar">
    <div class="container">
      <div class="topbar-inner">

        <div class="brand">
          <span class="brand-name">NVO987 AI</span>
          <span class="brand-tag">Prompt Library (India)</span>
        </div>

        <nav class="nav">
          <a href="/index.html">Home</a>
          <a href="/prompts/index.html">Prompts</a>
          <a href="/legal.html">Legal</a>
          <a href="/contact.html">Contact</a>
        </nav>

      </div>
    </div>
  </div>

  <main class="main">
    <div class="container">

      <section class="section">
        <div class="section-header">
          <h2>{title}</h2>
          <p>{description}</p>
        </div>

        <div class="legal-card">

          <div class="tag-row">
            <span class="pill">{category}</span>
            <span class="pill highlight">NVO987 • Privacy-first</span>
          </div>

          <div class="tag-row">
            {tags_html}
          </div>

          <h3>Prompt Template</h3>

          <textarea class="prompt-box" id="promptBox" readonly>{prompt_text}</textarea>

          <div class="button-row">
            <button class="btn" onclick="copyPrompt()">Copy Prompt</button>
            <a class="btn secondary" href="{chatgpt_link}" target="_blank" rel="noopener noreferrer">Open ChatGPT</a>
            <a class="btn secondary" href="{gemini_link}" target="_blank" rel="noopener noreferrer">Open Gemini</a>
          </div>

          <p class="small-note">
            This page is part of the NVO987 AI Prompt Library (India). Replace placeholders like [PASTE HERE] before use.
          </p>

          <p class="small-note muted">
            Disclaimer: prompts are informational templates only. Always verify outputs. No cookies, no tracking, no user data collection.
          </p>

        </div>
      </section>

      <section class="section">
        <div class="sources-card">
          <h3>Legal / Compliance</h3>
          <ul>
            <li>No registration, no user accounts.</li>
            <li>No analytics (Google Analytics, Meta Pixel, etc.).</li>
            <li>No advertising cookies.</li>
            <li>Static hosting via GitHub Pages.</li>
            <li>GDPR-friendly by design (no intentional personal data processing).</li>
          </ul>

          <p class="small-note">
            © {year} NVO987. Code licensed under MIT. Content: prompt templates only.
          </p>
        </div>
      </section>

    </div>
  </main>

  <footer class="footer">
    <div class="container footer-inner">
      <p>© {year} NVO987 – AI Prompt Library (India)</p>
      <p class="muted">No cookies • No tracking • Privacy-first static website</p>
      <p><a href="/legal.html">Legal</a> • <a href="/contact.html">Contact</a></p>
    </div>
  </footer>

  <script>
    function copyPrompt() {{
      const box = document.getElementById("promptBox");
      box.select();
      box.setSelectionRange(0, 999999);
      navigator.clipboard.writeText(box.value);
      alert("Prompt copied.");
    }}
  </script>

</body>
</html>
"""


def build_tags(tags):
    out = []
    for t in tags:
        out.append(f'<span class="pill">{t}</span>')
    return "\n            ".join(out)


def main():
    if not os.path.exists(DATA_FILE):
        raise FileNotFoundError(f"Missing {DATA_FILE}")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        prompts = json.load(f)

    today = datetime.utcnow().strftime("%Y-%m-%d")
    year = datetime.utcnow().strftime("%Y")

    generated_urls = []

    for item in prompts:
        slug = item["slug"].strip()
        filename = slug + ".html"
        out_path = os.path.join(OUTPUT_DIR, filename)

        canonical = f"{BASE_URL}/prompts/{filename}"

        tags_html = build_tags(item.get("tags", []))

        chatgpt_link = "https://chat.openai.com/"
        gemini_link = "https://gemini.google.com/"

        html = HTML_TEMPLATE.format(
            title=item["title"],
            meta_description=item["description"],
            description=item["description"],
            canonical=canonical,
            banner_image=BANNER_IMAGE,
            style_path=STYLE_PATH,
            date_published=today,
            year=year,
            category=item.get("category", "Prompt"),
            tags_html=tags_html,
            prompt_text=item.get("prompt", "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"),
            chatgpt_link=chatgpt_link,
            gemini_link=gemini_link
        )

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)

        generated_urls.append(canonical)

    # sitemap.xml
    sitemap_path = "sitemap.xml"
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        f.write(f"  <url><loc>{BASE_URL}/</loc></url>\n")
        f.write(f"  <url><loc>{BASE_URL}/prompts/index.html</loc></url>\n")
        for url in generated_urls:
            f.write(f"  <url><loc>{url}</loc></url>\n")
        f.write("</urlset>\n")

    print(f"Generated {len(prompts)} prompt pages.")
    print("Updated sitemap.xml")


if __name__ == "__main__":
    main()
