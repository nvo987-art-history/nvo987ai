#!/usr/bin/env python3
# ==========================================================
# FILE: tools/generate_prompts.py
# NVO987 AI – Safe Static Prompt Generator
#
# Generates exactly 1500 static prompt pages:
#   300 career
#   300 business
#   300 education
#   300 marketing
#   300 indian-food
#
# IMPORTANT:
# - No external AI API
# - No free-form topic generation
# - Whitelisted categories only
# - Controlled templates only
# - Generated prompt pages are NOINDEX
# - Generated prompt pages are NOT added to sitemap.xml
# - One-time GitHub Pages generation
# ==========================================================

import html
import math
import os
import re
from datetime import datetime, timezone


# ----------------------------------------------------------
# CONFIG
# ----------------------------------------------------------

BASE_URL = "https://nvo987.ai.in"

TEMPLATE_FILE = "prompts/template.html"

OUTPUT_DIR = "prompts"
PAGES_DIR = "prompts/page"

SITEMAP_FILE = "sitemap.xml"
ROBOTS_FILE = "robots.txt"

TOTAL_PER_CATEGORY = 300
PROMPTS_PER_INDEX_PAGE = 25

TOTAL_PROMPTS = 1500

ALLOWED_CATEGORIES = {
    "career",
    "business",
    "education",
    "marketing",
    "indian-food",
}


# ----------------------------------------------------------
# SAFETY
# ----------------------------------------------------------

# These are deliberately narrow.
# The generator never accepts arbitrary categories or topics.

BLOCKED_TERMS = {
    "weapon",
    "weapons",
    "explosive",
    "explosives",
    "bomb",
    "terrorist",
    "terrorism",
    "malware",
    "ransomware",
    "phishing",
    "credential",
    "password stealing",
    "credit card theft",
    "fraud",
    "drug",
    "drugs",
    "poison",
    "suicide",
    "self harm",
    "self-harm",
    "violent attack",
}


def validate_category(category: str):
    if category not in ALLOWED_CATEGORIES:
        raise ValueError(
            f"Unsafe or unsupported category rejected: {category}"
        )


def validate_text(text: str):
    """
    Basic defensive validation.

    This is NOT the primary safety mechanism.
    The primary safety mechanism is the strict whitelist
    and controlled templates below.
    """

    lowered = str(text).lower()

    for term in BLOCKED_TERMS:
        if term in lowered:
            raise ValueError(
                f"Blocked term detected in generated content: {term}"
            )


# ----------------------------------------------------------
# HELPERS
# ----------------------------------------------------------

def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def safe_html(text: str) -> str:
    return html.escape(str(text), quote=True)


def write_file(path: str, content: str):
    directory = os.path.dirname(path)

    if directory:
        os.makedirs(directory, exist_ok=True)

    with open(path, "w", encoding="utf-8") as file:
        file.write(content)


def utc_today():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


# ----------------------------------------------------------
# CONTROLLED DATA
# ----------------------------------------------------------

CAREER_ROLES = [
    "Business Analyst",
    "Project Coordinator",
    "Project Manager",
    "Data Analyst",
    "Software Developer",
    "Web Developer",
    "UX Designer",
    "Graphic Designer",
    "Product Manager",
    "Operations Manager",
    "Customer Success Specialist",
    "Sales Specialist",
    "Marketing Specialist",
    "Digital Marketing Manager",
    "Content Writer",
    "Technical Writer",
    "HR Specialist",
    "Recruitment Specialist",
    "Finance Analyst",
    "Accountant",
    "Administrative Assistant",
    "Office Manager",
    "Supply Chain Coordinator",
    "Procurement Specialist",
    "Quality Assurance Specialist",
]

CAREER_LEVELS = [
    "entry-level",
    "junior",
    "mid-level",
    "senior",
]

CAREER_TASKS = [
    "resume improvement",
    "CV structure",
    "interview preparation",
    "cover letter writing",
    "professional summary",
    "skills presentation",
    "career planning",
    "job application organization",
    "professional development planning",
    "work experience presentation",
    "achievement presentation",
    "portfolio planning",
    "career goal setting",
    "personal professional branding",
    "job-search planning",
]

BUSINESS_TYPES = [
    "small retail business",
    "local service business",
    "online store",
    "consulting business",
    "creative agency",
    "technology startup",
    "education business",
    "hospitality business",
    "food business",
    "professional service business",
    "family business",
    "freelance business",
    "small manufacturing business",
    "subscription business",
    "local tourism business",
]

BUSINESS_TASKS = [
    "business plan structure",
    "market research planning",
    "customer profile development",
    "value proposition development",
    "competitor analysis",
    "customer service improvement",
    "operations planning",
    "pricing strategy",
    "sales process improvement",
    "business goal planning",
    "monthly planning",
    "workflow organization",
    "customer feedback analysis",
    "service improvement",
    "business presentation planning",
    "small business content planning",
    "basic financial planning",
    "product launch planning",
    "business process documentation",
    "growth planning",
]

EDUCATION_SUBJECTS = [
    "mathematics",
    "history",
    "geography",
    "biology",
    "physics",
    "chemistry",
    "computer science",
    "economics",
    "literature",
    "language learning",
    "business studies",
    "art history",
    "general science",
    "social studies",
    "environmental studies",
]

EDUCATION_TASKS = [
    "study plan",
    "revision schedule",
    "lesson planning",
    "topic summary",
    "concept explanation",
    "flashcard creation",
    "practice question planning",
    "exam preparation",
    "note organization",
    "learning goal planning",
    "study session structure",
    "beginner learning roadmap",
    "intermediate learning roadmap",
    "advanced learning roadmap",
    "research organization",
    "reading plan",
    "vocabulary practice",
    "project planning",
    "learning progress review",
    "educational presentation planning",
]

MARKETING_TYPES = [
    "content marketing",
    "search marketing",
    "social media marketing",
    "email marketing",
    "local marketing",
    "brand marketing",
    "product marketing",
    "B2B marketing",
    "e-commerce marketing",
    "small business marketing",
    "creative marketing",
    "community marketing",
    "customer retention marketing",
    "launch marketing",
    "digital brand strategy",
]

MARKETING_TASKS = [
    "content calendar",
    "blog topic planning",
    "SEO content planning",
    "social media calendar",
    "email campaign planning",
    "customer persona development",
    "brand messaging",
    "campaign planning",
    "product launch messaging",
    "local marketing plan",
    "content repurposing",
    "audience research",
    "marketing KPI planning",
    "campaign review",
    "newsletter planning",
    "landing page content",
    "brand voice development",
    "customer journey mapping",
    "marketing strategy outline",
    "editorial planning",
]

INDIAN_REGIONS = [
    "North Indian",
    "South Indian",
    "East Indian",
    "West Indian",
    "Central Indian",
    "Coastal Indian",
    "Punjabi",
    "Gujarati",
    "Bengali",
    "Maharashtrian",
    "Rajasthani",
    "Tamil",
    "Kerala",
    "Andhra",
    "Karnataka",
]

INDIAN_FOOD_TYPES = [
    "vegetarian dinner",
    "vegetarian lunch",
    "family meal",
    "quick weekday meal",
    "festive meal",
    "breakfast",
    "snack",
    "rice dish",
    "flatbread meal",
    "lentil dish",
    "vegetable dish",
    "curry",
    "soup",
    "chutney",
    "dessert",
    "street-food inspired meal",
    "regional meal",
    "beginner-friendly dish",
    "one-pot meal",
    "meal-prep dish",
]

INDIAN_FOOD_TASKS = [
    "recipe writing",
    "ingredient planning",
    "step-by-step cooking instructions",
    "spice planning",
    "ingredient substitutions",
    "beginner cooking guide",
    "serving suggestions",
    "meal planning",
    "shopping list creation",
    "cooking timeline",
    "regional food introduction",
    "leftover planning",
    "portion planning",
    "vegetarian menu planning",
    "family menu planning",
]


# ----------------------------------------------------------
# PROMPT BUILDERS
# ----------------------------------------------------------

def build_career_prompts():
    prompts = []

    for role in CAREER_ROLES:
        for level in CAREER_LEVELS:
            for task in CAREER_TASKS:

                if len(prompts) >= TOTAL_PER_CATEGORY:
                    return prompts

                title = f"{role} {level.title()} – {task.title()}"

                prompt = (
                    f"Create a practical {task} plan for a {level} "
                    f"{role}. Keep the advice professional, clear, "
                    f"realistic, and suitable for a general job-search "
                    f"context. Organize the result into useful sections "
                    f"and include concrete examples where appropriate."
                )

                description = (
                    f"A structured AI prompt for {task} "
                    f"for a {level} {role}."
                )

                prompts.append({
                    "category": "career",
                    "title": title,
                    "description": description,
                    "prompt": prompt,
                    "tags": [
                        "career",
                        role,
                        level,
                        task,
                    ],
                })

    return prompts


def build_business_prompts():
    prompts = []

    for business_type in BUSINESS_TYPES:
        for task in BUSINESS_TASKS:

            if len(prompts) >= TOTAL_PER_CATEGORY:
                return prompts

            title = f"{business_type.title()} – {task.title()}"

            prompt = (
                f"Create a practical {task} framework for a "
                f"{business_type}. Keep the recommendations "
                f"general, ethical, realistic, and suitable for "
                f"a small or growing organization. Use clear "
                f"sections, priorities, and actionable next steps."
            )

            description = (
                f"A structured AI prompt for {task} "
                f"for a {business_type}."
            )

            prompts.append({
                "category": "business",
                "title": title,
                "description": description,
                "prompt": prompt,
                "tags": [
                    "business",
                    business_type,
                    task,
                ],
            })

    return prompts


def build_education_prompts():
    prompts = []

    for subject in EDUCATION_SUBJECTS:
        for task in EDUCATION_TASKS:

            if len(prompts) >= TOTAL_PER_CATEGORY:
                return prompts

            title = f"{subject.title()} – {task.title()}"

            prompt = (
                f"Create a clear {task} for learning {subject}. "
                f"Adapt the structure for a general learner, "
                f"explain concepts in accessible language, and "
                f"include practical study steps and review points. "
                f"Avoid unsupported claims and encourage checking "
                f"reliable educational sources when appropriate."
            )

            description = (
                f"A structured AI prompt for {task} "
                f"in {subject}."
            )

            prompts.append({
                "category": "education",
                "title": title,
                "description": description,
                "prompt": prompt,
                "tags": [
                    "education",
                    subject,
                    task,
                ],
            })

    return prompts


def build_marketing_prompts():
    prompts = []

    for marketing_type in MARKETING_TYPES:
        for task in MARKETING_TASKS:

            if len(prompts) >= TOTAL_PER_CATEGORY:
                return prompts

            title = f"{marketing_type.title()} – {task.title()}"

            prompt = (
                f"Create a practical {task} for {marketing_type}. "
                f"Focus on useful, ethical, audience-respecting "
                f"marketing practices. Structure the result with "
                f"objectives, audience considerations, content ideas, "
                f"execution steps, and measurable outcomes."
            )

            description = (
                f"A structured AI prompt for {task} "
                f"within {marketing_type}."
            )

            prompts.append({
                "category": "marketing",
                "title": title,
                "description": description,
                "prompt": prompt,
                "tags": [
                    "marketing",
                    marketing_type,
                    task,
                ],
            })

    return prompts


def build_indian_food_prompts():
    prompts = []

    for region in INDIAN_REGIONS:
        for food_type in INDIAN_FOOD_TYPES:

            if len(prompts) >= TOTAL_PER_CATEGORY:
                return prompts

            title = f"{region} – {food_type.title()}"

            prompt = (
                f"Create a practical recipe concept for a "
                f"{region} Indian {food_type}. Include ingredients, "
                f"clear preparation steps, approximate cooking order, "
                f"serving suggestions, and reasonable ingredient "
                f"substitutions. Keep the recipe accessible to a "
                f"home cook and explain unfamiliar ingredients briefly."
            )

            description = (
                f"An AI prompt for planning a {region} "
                f"Indian {food_type} recipe."
            )

            prompts.append({
                "category": "indian-food",
                "title": title,
                "description": description,
                "prompt": prompt,
                "tags": [
                    "indian food",
                    "indian recipes",
                    region,
                    food_type,
                ],
            })

    return prompts


# ----------------------------------------------------------
# BUILD DATASET
# ----------------------------------------------------------

def build_all_prompts():

    prompts = []

    category_builders = [
        build_career_prompts,
        build_business_prompts,
        build_education_prompts,
        build_marketing_prompts,
        build_indian_food_prompts,
    ]

    for builder in category_builders:

        category_prompts = builder()

        if len(category_prompts) != TOTAL_PER_CATEGORY:
            raise ValueError(
                f"{builder.__name__} generated "
                f"{len(category_prompts)} instead of "
                f"{TOTAL_PER_CATEGORY} prompts."
            )

        prompts.extend(category_prompts)

    if len(prompts) != TOTAL_PROMPTS:
        raise ValueError(
            f"Expected {TOTAL_PROMPTS} prompts, "
            f"generated {len(prompts)}."
        )

    return prompts


# ----------------------------------------------------------
# VALIDATE DATASET
# ----------------------------------------------------------

def validate_dataset(prompts):

    if len(prompts) != TOTAL_PROMPTS:
        raise ValueError(
            "Dataset size validation failed."
        )

    category_counts = {
        category: 0
        for category in ALLOWED_CATEGORIES
    }

    slugs = set()

    for item in prompts:

        category = item["category"]

        validate_category(category)

        category_counts[category] += 1

        # Validate title, description and prompt.
        for field in [
            "title",
            "description",
            "prompt",
        ]:
            validate_text(item[field])

        # Validate tags as well.
        for tag in item.get("tags", []):
            validate_text(tag)

        slug = slugify(
            f"{category}-{item['title']}"
        )

        if not slug:
            raise ValueError(
                f"Empty slug for: {item['title']}"
            )

        if slug in slugs:
            raise ValueError(
                f"Duplicate slug: {slug}"
            )

        slugs.add(slug)

    for category in ALLOWED_CATEGORIES:

        if category_counts[category] != TOTAL_PER_CATEGORY:
            raise ValueError(
                f"{category}: expected "
                f"{TOTAL_PER_CATEGORY}, got "
                f"{category_counts[category]}"
            )

    print("Safety validation passed.")
    print("Category counts:")

    for category in sorted(category_counts):

        print(
            f"  {category}: "
            f"{category_counts[category]}"
        )


# ----------------------------------------------------------
# TEMPLATE
# ----------------------------------------------------------

def load_template():

    if not os.path.exists(TEMPLATE_FILE):
        raise FileNotFoundError(
            f"Missing template: {TEMPLATE_FILE}"
        )

    with open(
        TEMPLATE_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        return file.read()


# ----------------------------------------------------------
# GENERATE PROMPT PAGES
# ----------------------------------------------------------

def generate_prompt_pages(prompts, template):

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    generated_files = []

    today = utc_today()

    for index, item in enumerate(
        prompts,
        start=1
    ):

        category = item["category"]

        title = item["title"]
        description = item["description"]
        prompt_text = item["prompt"]

        slug = slugify(
            f"{category}-{title}"
        )

        filename = f"{slug}.html"

        output_path = os.path.join(
            OUTPUT_DIR,
            filename
        )

        tags = ", ".join(
            item["tags"]
        )

        html_content = template

        replacements = {
            "{{TITLE}}": safe_html(title),
            "{{DESCRIPTION}}": safe_html(description),
            "{{CATEGORY}}": safe_html(category),
            "{{TAGS}}": safe_html(tags),
            "{{PROMPT_TEXT}}": safe_html(prompt_text),
            "{{SLUG}}": safe_html(slug),
            "{{DATE_PUBLISHED}}": today,
            "{{DATE_MODIFIED}}": today,
            "{{PROMPT_NUMBER}}": str(index),
        }

        for placeholder, value in replacements.items():

            html_content = html_content.replace(
                placeholder,
                value
            )

        write_file(
            output_path,
            html_content
        )

        generated_files.append(
            f"{BASE_URL}/prompts/{filename}"
        )

    return generated_files


# ----------------------------------------------------------
# INDEX PAGE
# ----------------------------------------------------------

def build_card(item):

    title = safe_html(
        item["title"]
    )

    description = safe_html(
        item["description"]
    )

    category = safe_html(
        item["category"]
    )

    tags = safe_html(
        ", ".join(item["tags"])
    )

    search_text = (
        item["title"]
        + " "
        + item["description"]
        + " "
        + item["category"]
        + " "
        + " ".join(item["tags"])
    ).lower()

    slug = slugify(
        f'{item["category"]}-{item["title"]}'
    )

    return f"""
<article class="prompt-card"
    data-search="{safe_html(search_text)}">

    <div class="category">{category.upper()}</div>

    <h2>{title}</h2>

    <p>{description}</p>

    <div class="tags">{tags}</div>

    <a class="button"
       href="/prompts/{slug}.html">
       Open Prompt
    </a>

</article>
"""


def build_index_page(
    page_items,
    page_number,
    total_pages,
    today
):

    cards = "\n".join(
        build_card(item)
        for item in page_items
    )

    if page_number > 1:

        previous_html = (
            f'<a href="/prompts/page/'
            f'{page_number - 1}.html">'
            f'← Previous</a>'
        )

    else:

        previous_html = (
            '<span class="disabled">'
            '← Previous'
            '</span>'
        )

    if page_number < total_pages:

        next_html = (
            f'<a href="/prompts/page/'
            f'{page_number + 1}.html">'
            f'Next →</a>'
        )

    else:

        next_html = (
            '<span class="disabled">'
            'Next →'
            '</span>'
        )

    canonical = (
        f"{BASE_URL}/prompts/index.html"
        if page_number == 1
        else
        f"{BASE_URL}/prompts/page/{page_number}.html"
    )

    return f"""<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>
NVO987 AI – Prompt Library
Page {page_number}
</title>

<meta name="description"
      content="NVO987 AI Prompt Library. "
               "Career, business, education, marketing "
               "and Indian food prompts.">

<meta name="robots"
      content="noindex, follow">

<link rel="canonical"
      href="{canonical}">

<style>

* {{
    box-sizing: border-box;
}}

html {{
    scroll-behavior: smooth;
}}

body {{
    margin: 0;
    background: #f4efe7;
    color: #202020;
    font-family:
        Inter,
        Arial,
        Helvetica,
        sans-serif;
}}

.container {{
    width: min(1180px, 92%);
    margin: 0 auto;
}}

.header {{
    background: #171513;
    color: #f5efe5;
    padding: 28px 0;
}}

.header-inner {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 25px;
    flex-wrap: wrap;
}}

.brand {{
    font-family: Georgia, serif;
    font-size: 25px;
    letter-spacing: .04em;
}}

.nav {{
    display: flex;
    gap: 18px;
    flex-wrap: wrap;
}}

.nav a {{
    color: #f5efe5;
    text-decoration: none;
}}

.nav a:hover {{
    text-decoration: underline;
}}

.hero {{
    padding: 70px 0 45px;
}}

.hero h1 {{
    margin: 0 0 12px;
    font-family: Georgia, serif;
    font-size: clamp(38px, 6vw, 68px);
    font-weight: 400;
}}

.hero p {{
    max-width: 760px;
    font-size: 18px;
    line-height: 1.7;
}}

.search {{
    margin: 10px 0 40px;
}}

.search input {{
    width: 100%;
    padding: 17px 18px;
    border: 1px solid #c9c0b4;
    border-radius: 10px;
    background: #fffdf9;
    font-size: 16px;
}}

.search input:focus {{
    outline: 2px solid #202020;
    outline-offset: 2px;
}}

.grid {{
    display: grid;
    grid-template-columns:
        repeat(auto-fit, minmax(280px, 1fr));
    gap: 22px;
}}

.prompt-card {{
    background: #fffdf9;
    border: 1px solid #ded6ca;
    border-radius: 16px;
    padding: 25px;
    box-shadow:
        0 8px 25px rgba(30, 25, 20, .05);
}}

.prompt-card:hover {{
    transform: translateY(-2px);
    box-shadow:
        0 12px 30px rgba(30, 25, 20, .08);
}}

.category {{
    font-size: 11px;
    letter-spacing: .14em;
    font-weight: 700;
    margin-bottom: 14px;
}}

.prompt-card h2 {{
    margin: 0 0 12px;
    font-family: Georgia, serif;
    font-size: 23px;
    font-weight: 400;
}}

.prompt-card p {{
    line-height: 1.65;
}}

.tags {{
    margin: 18px 0;
    color: #756e65;
    font-size: 13px;
    line-height: 1.5;
}}

.button {{
    display: inline-block;
    padding: 11px 16px;
    border-radius: 8px;
    background: #202020;
    color: #fff;
    text-decoration: none;
}}

.button:hover {{
    background: #000;
}}

.pagination {{
    margin: 45px 0 70px;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 22px;
    flex-wrap: wrap;
}}

.pagination a {{
    color: #202020;
}}

.disabled {{
    color: #aaa;
}}

.footer {{
    background: #171513;
    color: #cfc7bd;
    padding: 35px 0;
    margin-top: 50px;
}}

.footer a {{
    color: #f5efe5;
}}

@media (max-width: 650px) {{

    .hero {{
        padding: 45px 0 30px;
    }}

    .header-inner {{
        align-items: flex-start;
        flex-direction: column;
    }}

}}

@media (prefers-reduced-motion: reduce) {{

    html {{
        scroll-behavior: auto;
    }}

    .prompt-card {{
        transition: none;
    }}

}}

</style>

</head>

<body>

<header class="header">

<div class="container header-inner">

<div class="brand">
NVO987 AI
</div>

<nav class="nav">

<a href="/index.html">
Home
</a>

<a href="/prompts/index.html">
Prompts
</a>

<a href="https://nvo987.fr/mentions-legales.html">
Mentions légales
</a>

<a href="https://nvo987.fr/contact.html">
Contact
</a>

</nav>

</div>

</header>

<main class="container">

<section class="hero">

<h1>
Prompt Library
</h1>

<p>
A curated collection of 1,500 static AI prompts
covering career, business, education, marketing
and Indian food.
</p>

<p>
Page {page_number} of {total_pages}
· Updated {today}
</p>

</section>

<section class="search">

<input
    id="searchBox"
    type="search"
    placeholder="Search this page..."
    autocomplete="off"
    aria-label="Search prompts on this page">

</section>

<section
    class="grid"
    id="promptGrid">

{cards}

</section>

<nav
    class="pagination"
    aria-label="Prompt library pagination">

{previous_html}

<strong>
Page {page_number} / {total_pages}
</strong>

{next_html}

</nav>

</main>

<footer class="footer">

<div class="container">

<p>
NVO987 AI – Prompt Library
</p>

<p>
Static website · No cookies · No tracking
· Prompt pages are not indexed by search engines.
</p>

</div>

</footer>

<script>

const searchBox =
    document.getElementById("searchBox");

const cards =
    document.querySelectorAll(".prompt-card");

searchBox.addEventListener(
    "input",
    function () {{

        const query =
            this.value.toLowerCase().trim();

        cards.forEach(
            function(card) {{

                const text =
                    card.dataset.search || "";

                card.style.display =
                    text.includes(query)
                        ? ""
                        : "none";

            }}
        );

    }}
);

</script>

</body>

</html>
"""


def generate_indexes(prompts):

    os.makedirs(
        PAGES_DIR,
        exist_ok=True
    )

    total_pages = max(
        1,
        math.ceil(
            len(prompts)
            / PROMPTS_PER_INDEX_PAGE
        )
    )

    today = utc_today()

    for page_number in range(
        1,
        total_pages + 1
    ):

        start = (
            page_number - 1
        ) * PROMPTS_PER_INDEX_PAGE

        end = (
            start
            + PROMPTS_PER_INDEX_PAGE
        )

        page_items = prompts[start:end]

        content = build_index_page(
            page_items,
            page_number,
            total_pages,
            today
        )

        if page_number == 1:

            output_path = (
                f"{OUTPUT_DIR}/index.html"
            )

        else:

            output_path = (
                f"{PAGES_DIR}/"
                f"{page_number}.html"
            )

        write_file(
            output_path,
            content
        )

    return total_pages


# ----------------------------------------------------------
# SITEMAP
# ----------------------------------------------------------

def generate_sitemap():

    today = utc_today()

    urls = [
        f"{BASE_URL}/",
        f"{BASE_URL}/index.html",
        f"{BASE_URL}/prompts/index.html",
        "https://nvo987.fr/mentions-legales.html",
        "https://nvo987.fr/contact.html",
    ]

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]

    for url in urls:

        lines.append("  <url>")

        lines.append(
            f"    <loc>{safe_html(url)}</loc>"
        )

        lines.append(
            f"    <lastmod>{today}</lastmod>"
        )

        lines.append(
            "  </url>"
        )

    lines.append(
        "</urlset>"
    )

    lines.append("")

    write_file(
        SITEMAP_FILE,
        "\n".join(lines)
    )


# ----------------------------------------------------------
# ROBOTS
# ----------------------------------------------------------

def generate_robots():

    content = f"""User-agent: *
Allow: /

Disallow: /prompts/template.html

Sitemap: {BASE_URL}/sitemap.xml
"""

    write_file(
        ROBOTS_FILE,
        content
    )


# ----------------------------------------------------------
# MAIN
# ----------------------------------------------------------

def main():

    print("=" * 60)
    print("NVO987 AI – SAFE PROMPT GENERATOR")
    print("=" * 60)

    # Load the controlled HTML template.
    template = load_template()

    # Build the strictly controlled dataset.
    prompts = build_all_prompts()

    # Run safety, category, quantity and slug validation.
    validate_dataset(prompts)

    print()

    print(
        f"Generating {len(prompts)} "
        f"static prompt pages..."
    )

    generated_urls = generate_prompt_pages(
        prompts,
        template
    )

    total_pages = generate_indexes(
        prompts
    )

    generate_sitemap()

    generate_robots()

    print()

    print(
        "Generation completed successfully."
    )

    print(
        f"Prompt pages: {len(generated_urls)}"
    )

    print(
        f"Index pages:  {total_pages}"
    )

    print(
        "Sitemap:      sitemap.xml"
    )

    print(
        "Robots:       robots.txt"
    )

    print()

    print(
        "IMPORTANT: Generated prompt pages "
        "are NOINDEX and are NOT in sitemap.xml."
    )

    print("=" * 60)


if __name__ == "__main__":
    main()
