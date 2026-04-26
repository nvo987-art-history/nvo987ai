#!/usr/bin/env python3
# ==========================================================
# FILE: tools/generate_india_prompts_json.py
# NVO987 AI – India Prompt Database Generator
# Generates 1000 India-targeted prompts into data/prompts.json
# Categories: career + business ONLY (safe SEO topics)
# ==========================================================

import os
import json
import random
import re


# ----------------------------
# CONFIG
# ----------------------------
OUTPUT_FILE = "data/prompts.json"
TOTAL_PROMPTS = 1000

BASE_SLUG_DIR = "/prompts/"


# ----------------------------
# HELPERS
# ----------------------------
def slugify(text: str) -> str:
    text = text.lower().strip()
    text = text.replace("–", "-").replace("—", "-")
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def unique_slug(existing_slugs: set, base_slug: str) -> str:
    slug = base_slug
    i = 2
    while slug in existing_slugs:
        slug = f"{base_slug}-{i}"
        i += 1
    existing_slugs.add(slug)
    return slug


# ----------------------------
# DATA SOURCES
# ----------------------------
INDIAN_CITIES = [
    "Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai", "Pune", "Kolkata",
    "Ahmedabad", "Jaipur", "Lucknow", "Noida", "Gurgaon", "Indore", "Bhopal",
    "Surat", "Nagpur", "Patna", "Chandigarh", "Kochi", "Coimbatore",
    "Visakhapatnam", "Vadodara", "Nashik", "Thane", "Mysore", "Bhubaneswar"
]

CAREER_ROLES = [
    "Software Engineer", "Frontend Developer", "Backend Developer", "Full Stack Developer",
    "Data Analyst", "Data Scientist", "DevOps Engineer", "Cloud Engineer",
    "Cybersecurity Analyst", "UI/UX Designer", "Product Manager",
    "QA Engineer", "Mobile App Developer", "Business Analyst",
    "HR Executive", "Customer Support Executive", "Accountant",
    "Digital Marketing Specialist", "SEO Specialist", "Content Writer",
    "Graphic Designer", "Sales Executive", "Operations Manager"
]

EXPERIENCE_LEVELS = [
    "Fresher", "0-1 years", "1-3 years", "3-5 years", "5+ years"
]

BUSINESS_TYPES = [
    "MSME Business", "E-commerce Store", "Restaurant", "Cafe", "Digital Agency",
    "SaaS Startup", "FinTech Startup", "EdTech Startup", "HealthTech Startup",
    "Logistics Business", "Manufacturing Unit", "Retail Shop", "Freelance Business",
    "Coaching Institute", "Real Estate Agency"
]

BUSINESS_TASKS = [
    "Business Plan", "Pitch Deck Outline", "Investor Email",
    "GST Invoice Template", "Marketing Strategy", "Branding Strategy",
    "Customer Support Script", "Sales Pitch Script",
    "LinkedIn Company Page Copy", "Website Landing Page Copy",
    "Instagram Reel Script", "YouTube Script", "SEO Blog Outline",
    "Cold Email Campaign", "WhatsApp Marketing Message",
    "Competitor Analysis Report", "Pricing Strategy",
    "Product Launch Plan", "Hiring Plan"
]


# ----------------------------
# PROMPT BUILDERS
# ----------------------------
def build_career_prompt(role: str, city: str, level: str) -> dict:
    title = f"ATS Resume Prompt – {role} ({city}, India)"
    description = f"Generate an ATS-friendly {role} resume optimized for recruiters in {city}, India."

    prompt_text = f"""You are an expert ATS resume writer for the Indian job market.

Create a modern ATS-optimized resume for the following candidate:

Role Target: {role}
Location Target: {city}, India
Experience Level: {level}

Candidate Inputs (user will fill):
- Full Name: [FULL_NAME]
- Phone: [PHONE]
- Email: [EMAIL]
- LinkedIn: [LINKEDIN_URL]
- GitHub/Portfolio: [PORTFOLIO_URL]
- Skills: [SKILLS_LIST]
- Tools/Tech Stack: [TOOLS_LIST]
- Work Experience: [EXPERIENCE_DETAILS]
- Projects: [PROJECT_DETAILS]
- Education: [DEGREE + COLLEGE]
- Certifications: [CERTIFICATIONS]
- Achievements: [ACHIEVEMENTS]
- Languages: [LANGUAGES]
- Current CTC (INR): [CURRENT_CTC]
- Expected CTC (INR): [EXPECTED_CTC]
- Notice Period: [NOTICE_PERIOD]
- Preferred Job Type: [FULL_TIME / INTERNSHIP / REMOTE / HYBRID]

Requirements:
- Output in clean resume format (NO tables).
- Use strong India-relevant keywords.
- Include a professional summary.
- Include measurable achievements with numbers.
- Include a projects section with bullet points.
- Optimize for ATS parsing (simple formatting).
- Add a dedicated Skills section with grouped skills.
- Keep it 1 page if Fresher, 1-2 pages if experienced.

Return the final resume text only.
"""

    tags = ["resume", "ats", "india", role.lower(), city.lower(), "job"]

    slug_base = slugify(f"ats-resume-prompt-{role}-{city}-india")

    return {
        "title": title,
        "description": description,
        "category": "career",
        "slug": f"{BASE_SLUG_DIR}{slug_base}.html",
        "tags": tags,
        "prompt": prompt_text
    }


def build_interview_prompt(role: str, city: str, level: str) -> dict:
    title = f"HR Interview Prompt – {role} ({city}, India)"
    description = f"Generate HR interview questions and best answers for {role} candidates in {city}, India."

    prompt_text = f"""You are a professional HR interview coach specialized in Indian hiring.

Create a structured HR interview preparation guide for this candidate:

Role: {role}
Location: {city}, India
Experience Level: {level}

Include:
1. Top 20 HR interview questions for this role in India.
2. Best sample answers in a professional tone.
3. Salary expectation answer examples in INR.
4. Notice period negotiation answer examples.
5. Strengths/weaknesses answers (India-friendly).
6. Common red flags to avoid.
7. A final "2-minute self introduction" script.

Format cleanly with headings and bullet points.
Return only the interview guide.
"""

    tags = ["interview", "hr", "india", role.lower(), city.lower(), "job"]

    slug_base = slugify(f"hr-interview-prompt-{role}-{city}-india")

    return {
        "title": title,
        "description": description,
        "category": "career",
        "slug": f"{BASE_SLUG_DIR}{slug_base}.html",
        "tags": tags,
        "prompt": prompt_text
    }


def build_cover_letter_prompt(role: str, city: str) -> dict:
    title = f"Cover Letter Prompt – {role} ({city}, India)"
    description = f"Generate a professional cover letter for {role} job applications in {city}, India."

    prompt_text = f"""You are a professional cover letter writer specialized in Indian job applications.

Write a high-quality cover letter for this candidate:

Role Target: {role}
Location Target: {city}, India

Candidate Inputs:
- Full Name: [FULL_NAME]
- Company Name: [COMPANY_NAME]
- Job Posting Link: [JOB_LINK]
- Years of Experience: [YEARS]
- Key Skills: [SKILLS]
- Biggest Achievement: [ACHIEVEMENT]
- Why this company: [WHY_COMPANY]

Rules:
- Keep it concise (250-350 words).
- Use a professional Indian corporate tone.
- Mention ATS-friendly keywords.
- End with a clear call-to-action.
- Do NOT use generic filler lines.

Return the final cover letter only.
"""

    tags = ["cover letter", "india", role.lower(), city.lower(), "job"]

    slug_base = slugify(f"cover-letter-prompt-{role}-{city}-india")

    return {
        "title": title,
        "description": description,
        "category": "career",
        "slug": f"{BASE_SLUG_DIR}{slug_base}.html",
        "tags": tags,
        "prompt": prompt_text
    }


def build_business_prompt(business_type: str, city: str, task: str) -> dict:
    title = f"{task} Prompt – {business_type} ({city}, India)"
    description = f"Generate a {task.lower()} optimized for a {business_type.lower()} operating in {city}, India."

    prompt_text = f"""You are a business consultant specialized in Indian markets.

Create a professional {task} for this business:

Business Type: {business_type}
Target Location: {city}, India

Business Inputs (user will fill):
- Business Name: [BUSINESS_NAME]
- Product/Service: [PRODUCT_SERVICE]
- Target Audience: [TARGET_AUDIENCE]
- Pricing Range: [PRICING]
- Competitors: [COMPETITORS]
- Business Stage: [IDEA / EARLY / GROWTH]
- Monthly Budget (INR): [BUDGET]
- Revenue Goal (INR): [REVENUE_GOAL]
- USP (Unique Selling Point): [USP]

Requirements:
- Use India-specific context (local customer behavior, INR pricing).
- Keep structure clean and actionable.
- Provide step-by-step execution plan.
- Include realistic suggestions for Indian market conditions.
- Use bullet points and headings.

Return the final {task} only.
"""

    tags = ["business", "india", task.lower(), business_type.lower(), city.lower()]

    slug_base = slugify(f"{task}-{business_type}-{city}-india")

    return {
        "title": title,
        "description": description,
        "category": "business",
        "slug": f"{BASE_SLUG_DIR}{slug_base}.html",
        "tags": tags,
        "prompt": prompt_text
    }


# ----------------------------
# MAIN GENERATOR
# ----------------------------
def main():
    random.seed(987)

    prompts = []
    existing_slugs = set()

    # We will generate a balanced mix:
    # 60% career, 40% business
    career_target = int(TOTAL_PROMPTS * 0.6)
    business_target = TOTAL_PROMPTS - career_target

    # ----------------------------
    # CAREER PROMPTS
    # ----------------------------
    while len([p for p in prompts if p["category"] == "career"]) < career_target:
        role = random.choice(CAREER_ROLES)
        city = random.choice(INDIAN_CITIES)
        level = random.choice(EXPERIENCE_LEVELS)

        mode = random.choice(["resume", "interview", "coverletter"])

        if mode == "resume":
            item = build_career_prompt(role, city, level)
        elif mode == "interview":
            item = build_interview_prompt(role, city, level)
        else:
            item = build_cover_letter_prompt(role, city)

        slug = item["slug"].replace(".html", "")
        slug = unique_slug(existing_slugs, slug)
        item["slug"] = slug + ".html"

        prompts.append(item)

    # ----------------------------
    # BUSINESS PROMPTS
    # ----------------------------
    while len([p for p in prompts if p["category"] == "business"]) < business_target:
        business_type = random.choice(BUSINESS_TYPES)
        city = random.choice(INDIAN_CITIES)
        task = random.choice(BUSINESS_TASKS)

        item = build_business_prompt(business_type, city, task)

        slug = item["slug"].replace(".html", "")
        slug = unique_slug(existing_slugs, slug)
        item["slug"] = slug + ".html"

        prompts.append(item)

    # Shuffle final dataset for variety
    random.shuffle(prompts)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    # Save JSON
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(prompts, f, indent=2, ensure_ascii=False)

    print("=====================================")
    print(f"Generated prompts: {len(prompts)}")
    print(f"Saved to: {OUTPUT_FILE}")
    print("Categories:")
    print(f"- career: {len([p for p in prompts if p['category']=='career'])}")
    print(f"- business: {len([p for p in prompts if p['category']=='business'])}")
    print("=====================================")


if __name__ == "__main__":
    main()
