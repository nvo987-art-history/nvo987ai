# NVO987 AI Prompt Library (India)

**Website:** https://nvo987.ai.in  
**Brand:** NVO987 AI

A privacy-first AI prompt library optimized for Indian job seekers, students, freelancers and content creators.

This project is designed for **SEO indexing in India** (Google India and regional search engines) using static HTML pages generated from a structured JSON database.

---

## What does the user get?

Users get:

- ready-to-copy AI prompt templates
- dedicated prompt pages with clean UI
- quick "Copy Prompt" button
- links to ChatGPT and Gemini
- India-optimized prompts (freshers, placements, TCS, Infosys, Hinglish content, INR references)

---

## How it works

### 1) prompts.json
All prompts are stored in:

`prompts.json`

Each prompt entry contains:

- slug
- title
- category
- description
- prompt text
- tags

### 2) generate_site.py
A Python script automatically generates:

- `index.html`
- `/prompts/*.html`
- `sitemap.xml`
- `robots.txt`

This allows scaling to thousands of pages without manual work.

---

## Automation (GitHub Actions)

A workflow builds the entire site automatically:

- on every push
- daily (cron schedule)
- on manual trigger

Generated pages are committed automatically.

---

## Compliance / Privacy / GDPR

This project is designed to be privacy-first:

- no cookies
- no analytics
- no tracking pixels
- no user accounts
- no server-side processing
- no personal data collection

Hosting is provided via GitHub Pages.
Technical logs may exist at infrastructure level (GitHub / CDN), but no tracking is intentionally implemented by NVO987.

---

## Legal disclaimer

This website provides AI prompt templates for educational and productivity purposes only.

It is not affiliated with OpenAI, Google, or any AI provider.

Users must verify all generated outputs before using them in professional, legal, financial, academic or hiring contexts.

---

## License

### Code
MIT License.

### Prompt content
Prompt content is published by NVO987 (unless otherwise stated).

---

## Contact

Email: contact@nvo987.eu  
Official legal mentions: https://www.nvo987.fr  
DID: did:web:identity.nvo987.us 
