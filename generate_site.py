import os
import json
import datetime
from pathlib import Path

SITE_URL = "https://nvo987.ai.in"
OUTPUT_DIR = "prompts"
PROMPTS_FILE = "prompts.json"

BRAND_NAME = "NVO987 AI"
CONTACT_EMAIL = "contact@nvo987.eu"
LEGAL_URL = "https://www.nvo987.fr"
DID_URL = "https://identity.nvo987.us"
DID_VALUE = "did:web:identity.nvo987.us"

def safe(text):
    if text is None:
        return ""
    return str(text).strip()

def escape_html(s):
    if s is None:
        return ""
    return (
        str(s)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#039;")
    )

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def json_ld_for_prompt(title, description, canonical):
    obj = {
        "@context": "https://schema.org",
        "@type": "TechArticle",
        "headline": title,
        "description": description,
        "url": canonical,
        "datePublished": datetime.date.today().isoformat(),
        "dateModified": datetime.date.today().isoformat(),
        "publisher": {
            "@type": "Organization",
            "name": BRAND_NAME,
            "url": SITE_URL
        }
    }
    return json.dumps(obj, ensure_ascii=False)

def build_prompt_page(prompt):
    slug = safe(prompt.get("slug"))
    title = escape_html(prompt.get("title", "AI Prompt"))
    description = escape_html(prompt.get("description", ""))
    category = escape_html(prompt.get("category", "Prompt"))
    prompt_text = escape_html(prompt.get("prompt", ""))

    tags = prompt.get("tags", [])
    tags_html = ""
    if tags:
        tags_html = "".join([f"<span class='tag'>{escape_html(t)}</span>" for t in tags])

    canonical = f"{SITE_URL}/prompts/{slug}.html"
    json_ld = escape_html(json_ld_for_prompt(title, description, canonical))

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta http-equiv="x-ua-compatible" content="ie=edge" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />

  <title>{title} – {BRAND_NAME}</title>

  <meta name="description" content="{description}" />
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large" />
  <meta name="referrer" content="no-referrer" />
  <meta name="format-detection" content="telephone=no, email=no, address=no" />

  <meta http-equiv="Permissions-Policy" content="geolocation=(), microphone=(), camera=(), payment=(), interest-cohort=()" />

  <link rel="canonical" href="{canonical}" />
  <link rel="stylesheet" href="../style.css" />
  <link rel="icon" href="../favicon.ico" sizes="any" />

  <meta property="og:site_name" content="{BRAND_NAME}" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{description}" />
  <meta property="og:type" content="article" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:image" content="{SITE_URL}/banner.jpg" />

  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{title}" />
  <meta name="twitter:description" content="{description}" />
  <meta name="twitter:image" content="{SITE_URL}/banner.jpg" />

  <script type="application/ld+json">{json_ld}</script>
</head>

<body>

  <div class="topbar">
    <div class="container">
      <div class="topbar-inner">
        <div class="brand">
          <span class="brand-name">{BRAND_NAME}</span>
          <span class="brand-tag">Prompt Library (India)</span>
        </div>

        <nav class="nav">
          <a href="../index.html">Home</a>
          <a href="../index.html#prompts">Prompts</a>
          <a href="../index.html#legal">Legal</a>
          <a href="../index.html#contact">Contact</a>
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

        <div class="prompt-card">
          <div class="prompt-meta">
            <span class="pill">{category}</span>
            <span class="pill secondary">NVO987 • Privacy-first</span>
          </div>

          <div class="tags">
            {tags_html}
          </div>

          <h3>Prompt Template</h3>

          <textarea id="promptBox" class="prompt-box" readonly>{prompt_text}</textarea>

          <div class="actions">
            <button class="btn" onclick="copyPrompt()">Copy Prompt</button>
            <a class="btn secondary" href="https://chat.openai.com/" target="_blank" rel="noopener noreferrer">Open ChatGPT</a>
            <a class="btn secondary" href="https://gemini.google.com/" target="_blank" rel="noopener noreferrer">Open Gemini</a>
          </div>

          <p class="small-note">
            This page is part of the <strong>NVO987 AI Prompt Library</strong>.
            Replace placeholders like <strong>[PASTE HERE]</strong> before using.
          </p>

          <p class="small-note">
            Disclaimer: prompts are informational templates only. Always verify outputs.
          </p>
        </div>

      </section>

    </div>
  </main>

  <footer class="footer">
    <div class="container footer-inner">
      <p>© 2026 NVO987 – AI Resources</p>
      <p class="muted">No cookies • No tracking • Static website</p>
      <p>Contact: <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a></p>
      <p>DID: <a href="{DID_URL}" target="_blank" rel="noopener noreferrer">{DID_VALUE}</a></p>
    </div>
  </footer>

  <script>
    function copyPrompt() {{
      const box = document.getElementById("promptBox");
      box.select();
      box.setSelectionRange(0, 999999);
      navigator.clipboard.writeText(box.value);
      alert("Prompt copied (NVO987 AI).");
    }}
  </script>

</body>
</html>
"""

def build_index(prompts):
    total = len(prompts)
    today = datetime.date.today().isoformat()

    cards = []
    for p in prompts:
        title = escape_html(p["title"])
        category = escape_html(p.get("category", "Prompt"))
        desc = escape_html(p.get("description", ""))
        slug = escape_html(p["slug"])
        url = f"prompts/{slug}.html"

        cards.append(f"""
        <article class="place-card">
          <div class="place-type">{category}</div>
          <h3>{title}</h3>
          <div class="place-desc">{desc}</div>
          <div class="place-actions">
            <a class="btn" href="{url}">Open Prompt</a>
          </div>
        </article>
        """)

    cards_html = "\n".join(cards)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta http-equiv="x-ua-compatible" content="ie=edge" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />

  <title>NVO987 AI – Prompt Library for India</title>

  <meta name="description" content="NVO987 AI Prompt Library: resume, job interview, freelancing, business, YouTube and study prompts optimized for India. No cookies, no tracking." />
  <meta name="keywords" content="AI prompts India, ChatGPT prompts India, resume prompt fresher, ATS resume India, TCS interview prompt, Infosys interview prompt, Hinglish YouTube script prompt, freelancing prompts India, NVO987 AI" />
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large" />
  <meta name="referrer" content="no-referrer" />
  <meta name="color-scheme" content="light" />
  <meta name="format-detection" content="telephone=no, email=no, address=no" />

  <meta http-equiv="Permissions-Policy" content="geolocation=(), microphone=(), camera=(), payment=(), interest-cohort=()" />

  <link rel="canonical" href="{SITE_URL}/" />
  <link rel="stylesheet" href="style.css" />
  <link rel="icon" href="favicon.ico" sizes="any" />

  <meta property="og:site_name" content="NVO987 AI" />
  <meta property="og:title" content="NVO987 AI Prompt Library (India)" />
  <meta property="og:description" content="Copy-ready AI prompts optimized for India. Resume, jobs, freelancing, YouTube, study. No cookies." />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="{SITE_URL}/" />
  <meta property="og:image" content="{SITE_URL}/banner.jpg" />

  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="NVO987 AI Prompt Library (India)" />
  <meta name="twitter:description" content="Copy-ready AI prompts for Indian students, job seekers and creators. Privacy-first." />
  <meta name="twitter:image" content="{SITE_URL}/banner.jpg" />

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "WebSite",
    "name": "NVO987 AI Prompt Library",
    "url": "{SITE_URL}",
    "description": "A privacy-first AI prompt library optimized for India.",
    "publisher": {{
      "@type": "Organization",
      "name": "NVO987",
      "url": "{LEGAL_URL}"
    }}
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
          <a href="#prompts">Prompts</a>
          <a href="#legal">Legal</a>
          <a href="#contact">Contact</a>
        </nav>
      </div>
    </div>
  </div>

  <div class="container">
    <header class="hero">
      <div class="hero-text">
        <h1>NVO987 AI Prompt Library</h1>
        <p class="hero-sub">India • Resume • Jobs • Freelancing • YouTube • Study</p>
        <p class="hero-note">
          Privacy-first • No cookies • No tracking • Static website
        </p>
      </div>
    </header>
  </div>

  <main class="main">
    <div class="container">

      <section id="prompts" class="section">
        <div class="section-header">
          <h2>Prompt Directory</h2>
          <p>
            Copy-ready AI prompt templates optimized for India. Use them instantly in ChatGPT or Gemini.
            Built and maintained by <strong>NVO987</strong>.
          </p>
        </div>

        <div class="status success">
          {total} prompt(s) available • Updated {today} • NVO987 AI
        </div>

        <div class="grid">
          {cards_html}
        </div>
      </section>

      <section id="legal" class="section">
        <div class="section-header">
          <h2>Legal / Privacy / Compliance</h2>
          <p>Transparency, privacy-first design, and disclaimer policy.</p>
        </div>

        <div class="legal-card">

          <h3>Publisher</h3>
          <p>
            This website <strong>{SITE_URL}</strong> is published by <strong>NVO987</strong>.
            Official legal mentions are available at:
            <a href="{LEGAL_URL}" target="_blank" rel="noopener noreferrer">{LEGAL_URL}</a>.
          </p>

          <h3>Service nature</h3>
          <p>
            This site provides a curated library of AI prompt templates for educational and productivity purposes.
            It is not an AI model, not a chatbot service, and does not provide guaranteed professional advice.
          </p>

          <h3>Privacy-first (No GDPR issues)</h3>
          <ul>
            <li>No cookies</li>
            <li>No analytics</li>
            <li>No tracking pixels</li>
            <li>No accounts / no login</li>
            <li>No personal data database</li>
            <li>No server-side processing</li>
          </ul>

          <p class="small-note">
            Hosting is provided via GitHub Pages. Standard technical logs may exist at infrastructure level.
          </p>

          <h3>Disclaimer (important)</h3>
          <p>
            Prompts and outputs are provided for informational purposes only.
            Users must verify accuracy and comply with applicable laws and employer policies.
            NVO987 is not responsible for decisions made using generated content.
          </p>

          <h3>Non-affiliation</h3>
          <p>
            This project is independent and not affiliated with OpenAI, Google, Microsoft, or any third-party AI provider.
            ChatGPT and Gemini are trademarks of their respective owners.
          </p>

        </div>
      </section>

      <section id="contact" class="section">
        <div class="section-header">
          <h2>Contact / Identity</h2>
          <p>Official contact and DID identity.</p>
        </div>

        <div class="sources-card">
          <p>Email: <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a></p>
          <p>Legal: <a href="{LEGAL_URL}" target="_blank" rel="noopener noreferrer">{LEGAL_URL}</a></p>
          <p>DID: <a href="{DID_URL}" target="_blank" rel="noopener noreferrer">{DID_VALUE}</a></p>
        </div>
      </section>

    </div>
  </main>

  <footer class="footer">
    <div class="container footer-inner">
      <p>© 2026 NVO987 – AI Resources</p>
      <p class="muted">No cookies • No tracking • Static publishing</p>
      <p>Official legal mentions: <a href="{LEGAL_URL}" target="_blank" rel="noopener noreferrer">{LEGAL_URL}</a></p>
      <p class="small-note">Brand: NVO987 AI • Domain: nvo987.ai.in</p>
    </div>
  </footer>

</body>
</html>
"""

def build_sitemap(prompts):
    today = datetime.date.today().isoformat()

    urls = []
    urls.append(f"""
  <url>
    <loc>{SITE_URL}/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
""")

    for p in prompts:
        slug = safe(p.get("slug"))
        if not slug:
            continue

        urls.append(f"""
  <url>
    <loc>{SITE_URL}/prompts/{slug}.html</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
""")

    urls_xml = "\n".join(urls)

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls_xml}
</urlset>
"""

def build_robots():
    return f"""User-agent: *
Allow: /

Sitemap: {SITE_URL}/sitemap.xml
"""

def main():
    if not os.path.exists(PROMPTS_FILE):
        raise Exception("Missing prompts.json file")

    with open(PROMPTS_FILE, "r", encoding="utf-8") as f:
        prompts = json.load(f)

    if not isinstance(prompts, list):
        raise Exception("prompts.json must contain a JSON list")

    ensure_dir(OUTPUT_DIR)

    print("Generating prompt pages...")

    valid_prompts = []
    for p in prompts:
        slug = safe(p.get("slug"))
        title = safe(p.get("title"))

        if not slug or not title:
            print("Skipping invalid prompt entry:", p)
            continue

        valid_prompts.append(p)

        html = build_prompt_page(p)
        out_path = Path(OUTPUT_DIR) / f"{slug}.html"

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)

    print("Generating index.html...")
    index_html = build_index(valid_prompts)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(index_html)

    print("Generating sitemap.xml...")
    sitemap = build_sitemap(valid_prompts)
    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write(sitemap)

    print("Generating robots.txt...")
    robots = build_robots()
    with open("robots.txt", "w", encoding="utf-8") as f:
        f.write(robots)

    print("Done. Generated", len(valid_prompts), "prompt pages for NVO987 AI.")

if __name__ == "__main__":
    main()
