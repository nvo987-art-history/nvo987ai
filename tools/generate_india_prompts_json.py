#!/usr/bin/env python3
# ==========================================================
# FILE: tools/generate_india_prompts_json.py
# NVO987 AI – India Prompt Database Generator
# Generates data/prompts.json with 1000+ India-targeted prompts
# Privacy-first / static site compatible
# ==========================================================

import os
import json
import re
import random
from datetime import datetime

OUTPUT_FILE = "data/prompts.json"
TOTAL_PROMPTS = 1000

BASE_SLUG_DIR = "/prompts/"


# ----------------------------
# HELPERS
# ----------------------------
def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def safe_write_json(path: str, data):
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def build_slug(title: str) -> str:
    return f"{BASE_SLUG_DIR}{slugify(title)}.html"


def uniq_slug(slug: str, used: set) -> str:
    """Ensure slug is unique"""
    if slug not in used:
        used.add(slug)
        return slug

    i = 2
    while True:
        new_slug = slug.replace(".html", f"-{i}.html")
        if new_slug not in used:
            used.add(new_slug)
            return new_slug
        i += 1


# ----------------------------
# INDIA DATA
# ----------------------------
INDIA_CITIES = [
    "Bengaluru", "Mumbai", "Delhi", "Hyderabad", "Chennai", "Pune", "Kolkata",
    "Ahmedabad", "Jaipur", "Surat", "Lucknow", "Indore", "Nagpur", "Noida", "Gurgaon"
]

INDIA_DOMAINS = [
    "FinTech", "EdTech", "HealthTech", "E-commerce", "IT Services", "SaaS",
    "Logistics", "Retail", "Manufacturing", "Real Estate", "Legal Services",
    "Banking", "Insurance", "Telecom", "Media", "Hospitality"
]

INDIA_EXAMS = [
    "UPSC", "SSC", "IBPS PO", "CAT", "GATE", "JEE", "NEET",
    "CLAT", "GRE", "IELTS", "TOEFL", "NDA"
]

INDIA_TAX_TERMS = [
    "GST", "PAN", "Aadhaar", "ITR filing", "TDS", "HRA exemption",
    "Section 80C", "capital gains tax", "income tax slab", "Form 16"
]

INDIA_PAYMENT_TERMS = [
    "UPI", "Paytm", "PhonePe", "Google Pay", "NEFT", "IMPS", "RTGS"
]

LANGUAGES = ["English", "Hindi", "Tamil", "Telugu", "Kannada", "Marathi", "Bengali"]

JOB_ROLES = [
    "Software Engineer", "Frontend Developer", "Backend Developer",
    "Full Stack Developer", "DevOps Engineer", "Data Analyst", "Data Scientist",
    "Product Manager", "QA Engineer", "HR Executive", "Marketing Manager",
    "Sales Executive", "Business Analyst", "UI/UX Designer", "Chartered Accountant",
    "Legal Associate", "Customer Support Executive", "Operations Manager"
]


# ----------------------------
# PROMPT TEMPLATE BUILDERS
# ----------------------------
def prompt_resume(role: str, city: str) -> dict:
    title = f"ATS Resume Prompt – {role} ({city}, India)"
    description = f"Generate an ATS-friendly {role} resume optimized for recruiters in {city}, India."
    category = "career"
    tags = ["resume", "ats", "india", role.lower(), city.lower()]

    prompt = f"""You are an expert ATS resume writer for the Indian job market.

Create a modern ATS-optimized resume for the following candidate:

Role Target: {role}
Location Target: {city}, India
Experience Level: [Fresher / 1-3 yrs / 3-6 yrs / 6+ yrs]
Tech Stack / Skills: [LIST]
Projects: [LIST]
Education: [DEGREE + COLLEGE]
Certifications: [CERTIFICATIONS]
Achievements: [ACHIEVEMENTS]

Requirements:
- Output in clean resume format (no tables).
- Use Indian recruiter-friendly keywords.
- Add a strong summary section.
- Include measurable achievements with numbers.
- Include projects section with bullet points.
- Ensure ATS keyword density is high but natural.
- Add LinkedIn + GitHub placeholders.
- Include notice period and current CTC / expected CTC placeholders (India standard).

Return the final resume text only."""
    return {
        "title": title,
        "description": description,
        "category": category,
        "tags": tags,
        "prompt": prompt
    }


def prompt_interview(role: str) -> dict:
    title = f"HR Interview Prompt – {role} (India)"
    description = f"Generate HR interview questions and best answers for a {role} job interview in India."
    category = "career"
    tags = ["interview", "india", "hr", role.lower()]

    prompt = f"""You are an HR interview coach specialized in Indian hiring processes.

Generate:
1) 20 HR interview questions for a {role} interview in India
2) Best example answers (Indian context)
3) Common red flags recruiters watch for
4) Salary negotiation tips (CTC-based)
5) Notice period strategy and professional responses
6) How to explain job gaps in India

Candidate details:
- Experience: [YEARS]
- Domain: [DOMAIN]
- Strengths: [STRENGTHS]
- Weaknesses: [WEAKNESSES]

Output in a structured format with headings and bullet points."""
    return {
        "title": title,
        "description": description,
        "category": category,
        "tags": tags,
        "prompt": prompt
    }


def prompt_gst_business(domain: str) -> dict:
    title = f"GST Compliance Prompt – {domain} Business (India)"
    description = f"Generate GST compliance checklist and invoicing guidance for a {domain} business in India."
    category = "business"
    tags = ["gst", "india", "tax", domain.lower()]

    prompt = f"""You are a GST compliance consultant in India.

Create a GST compliance and invoicing guide for a {domain} business in India.

Include:
- GST registration requirements
- GST invoice format template
- HSN/SAC guidance
- GST return filing schedule (GSTR-1, GSTR-3B, annual return)
- Input tax credit checklist
- Common GST mistakes and penalties
- Example invoice text
- Record keeping best practices

Assume the business operates in: [STATE]
Annual turnover: [TURNOVER]
Type: [B2B / B2C / Mixed]

Output should be clear and actionable."""
    return {
        "title": title,
        "description": description,
        "category": "business",
        "tags": tags,
        "prompt": prompt
    }


def prompt_upsc() -> dict:
    title = "UPSC Study Plan Prompt (India)"
    description = "Generate a complete UPSC study plan with timetable, revision strategy and test series schedule."
    category = "education"
    tags = ["upsc", "study plan", "india", "education"]

    prompt = """You are an expert UPSC mentor.

Create a complete UPSC preparation plan for a student.

Inputs:
- Attempt number: [1st/2nd/3rd]
- Daily study hours: [HOURS]
- Optional subject: [OPTIONAL]
- Current level: [Beginner / Intermediate / Advanced]
- Exam year: [YEAR]

Plan must include:
- 12 month strategy
- monthly targets
- weekly timetable
- daily timetable
- booklist + resources
- revision cycles
- mock test schedule
- answer writing strategy
- current affairs strategy (The Hindu / PIB / monthly magazine)
- last 60 days final revision plan

Output in structured sections with bullet points."""
    return {
        "title": title,
        "description": description,
        "category": category,
        "tags": tags,
        "prompt": prompt
    }


def prompt_exam(exam: str) -> dict:
    title = f"{exam} Study Strategy Prompt (India)"
    description = f"Generate a complete study strategy and revision timetable for {exam} exam preparation."
    category = "education"
    tags = ["exam", "india", exam.lower(), "study plan"]

    prompt = f"""You are a top mentor for Indian competitive exams.

Create a complete preparation strategy for {exam}.

Inputs:
- Target score/rank: [TARGET]
- Exam date: [DATE]
- Daily hours available: [HOURS]
- Current preparation level: [BEGINNER/INTERMEDIATE/ADVANCED]

Include:
- topic-wise roadmap
- weekly schedule
- daily timetable
- revision plan
- mock test plan
- recommended books and online resources
- time management strategy
- exam day strategy

Output should be realistic and highly actionable."""
    return {
        "title": title,
        "description": description,
        "category": category,
        "tags": tags,
        "prompt": prompt
    }


def prompt_finance_personal(city: str) -> dict:
    title = f"Personal Budget Planning Prompt – Middle Class ({city}, India)"
    description = f"Create a monthly personal budget plan for a middle-class family living in {city}, India."
    category = "finance"
    tags = ["budget", "india", "personal finance", city.lower()]

    prompt = f"""You are a personal finance advisor for Indian households.

Create a monthly budget plan for a middle-class family living in {city}, India.

Inputs:
- Monthly income: [INCOME]
- Rent: [RENT]
- EMI loans: [EMI]
- Family size: [SIZE]
- Lifestyle: [LOW/MEDIUM/HIGH]
- Savings goal: [GOAL]

Include:
- budget categories (rent, groceries, transport, school, medical, insurance, entertainment)
- suggested allocation percentages
- emergency fund plan
- SIP investment plan (India)
- tax-saving suggestions (80C, ELSS, PPF)
- example budget table in plain text
- cost-cutting tips

Output must be practical and India-specific."""
    return {
        "title": title,
        "description": description,
        "category": category,
        "tags": tags,
        "prompt": prompt
    }


def prompt_system_design() -> dict:
    title = "System Design Interview Prompt – Indian Product Companies"
    description = "Generate a full system design interview solution in Indian tech interview style."
    category = "coding"
    tags = ["system design", "interview", "india", "scalability"]

    prompt = """You are a senior system design interviewer from an Indian product company (Flipkart / Swiggy / Zomato style).

Design a scalable system for the following problem:

[PROBLEM STATEMENT]

Deliver:
- requirements gathering
- functional requirements
- non-functional requirements
- assumptions
- high-level architecture diagram description
- database schema
- API design
- caching strategy
- load balancing strategy
- queue/event-driven architecture
- scalability bottlenecks
- cost optimization
- monitoring and logging
- final summary

Explain in clear step-by-step Indian interview style."""
    return {
        "title": title,
        "description": description,
        "category": category,
        "tags": tags,
        "prompt": prompt
    }


def prompt_reel_script(language: str) -> dict:
    title = f"Instagram Reel Script Prompt – {language} Audience (India)"
    description = f"Generate viral Instagram Reel scripts targeting {language}-speaking audiences in India."
    category = "marketing"
    tags = ["instagram", "reels", "india", language.lower(), "marketing"]

    prompt = f"""You are a viral content strategist for Indian Instagram creators.

Generate 10 Instagram Reel script ideas targeting {language}-speaking audiences in India.

Inputs:
- niche: [NICHE]
- product/service: [PRODUCT]
- target audience: [AGE GROUP]
- tone: [FUNNY/INSPIRATIONAL/EDUCATIONAL]

Each script must include:
- hook (first 2 seconds)
- scene-by-scene breakdown
- captions text
- suggested hashtags (India)
- CTA line
- recommended duration

Output in a clean list format."""
    return {
        "title": title,
        "description": description,
        "category": category,
        "tags": tags,
        "prompt": prompt
    }


def prompt_startup_pitch(city: str) -> dict:
    title = f"Startup Pitch Deck Prompt – {city} (India)"
    description = f"Generate an investor-ready startup pitch deck outline for startups raising funding in {city}, India."
    category = "business"
    tags = ["startup", "pitch deck", "india", city.lower(), "investor"]

    prompt = f"""You are a startup fundraising expert for Indian venture capital ecosystem.

Create a full pitch deck outline for an Indian startup.

Inputs:
- Startup name: [NAME]
- Industry: [INDUSTRY]
- Location: {city}, India
- Target customers: [B2B/B2C]
- Business model: [MODEL]
- Revenue: [CURRENT REVENUE]
- Funding stage: [SEED/PRE-SEED/SERIES A]
- Competitors: [COMPETITORS]

Include:
- Problem slide
- Solution slide
- Market size (India TAM/SAM/SOM)
- Product demo outline
- Traction metrics
- Unit economics (CAC, LTV)
- Go-to-market plan for India
- Team slide
- Financial projections
- Funding ask + use of funds
- Risks and mitigation

Write as a professional deck outline with bullet points."""
    return {
        "title": title,
        "description": description,
        "category": category,
        "tags": tags,
        "prompt": prompt
    }


def prompt_tax_filing() -> dict:
    title = "Income Tax Filing Prompt – Salaried Employee (India)"
    description = "Generate step-by-step guidance to file income tax return for a salaried employee in India."
    category = "finance"
    tags = ["income tax", "itr", "india", "salary", "pan"]

    prompt = """You are an Indian income tax consultant.

Provide step-by-step instructions for filing income tax return (ITR) for a salaried employee in India.

Inputs:
- Annual salary: [SALARY]
- Form 16 available: [YES/NO]
- Rent paid: [RENT]
- Home loan interest: [INTEREST]
- Investments: [80C INVESTMENTS]
- Health insurance premium: [80D]
- Other income: [CAPITAL GAINS/FD INTEREST]

Include:
- which ITR form to choose
- new vs old tax regime comparison
- deduction checklist (80C, 80D, HRA, home loan)
- document checklist
- common mistakes
- refund timeline expectations

Output should be beginner-friendly."""
    return {
        "title": title,
        "description": description,
        "category": category,
        "tags": tags,
        "prompt": prompt
    }


def prompt_customer_support(domain: str) -> dict:
    title = f"Customer Support Reply Prompt – {domain} Company (India)"
    description = f"Generate professional customer support email replies for a {domain} company serving Indian customers."
    category = "business"
    tags = ["customer support", "email", "india", domain.lower()]

    prompt = f"""You are a customer support manager in India.

Generate 15 professional customer support email templates for a {domain} company in India.

Include:
- refund request reply
- late delivery apology
- payment failed (UPI/NEFT/IMPS)
- account verification (PAN/Aadhaar)
- escalation handling
- angry customer response
- subscription cancellation
- invoice request (GST invoice)
- technical issue troubleshooting
- product damaged delivery

Tone: polite, professional, Indian English.
Output must be copy-paste ready."""
    return {
        "title": title,
        "description": description,
        "category": category,
        "tags": tags,
        "prompt": prompt
    }


def prompt_legal_agreement() -> dict:
    title = "Rental Agreement Draft Prompt (India)"
    description = "Generate a rental agreement draft for tenants and landlords in India."
    category = "legal"
    tags = ["rental agreement", "india", "legal", "property"]

    prompt = """You are a legal drafting assistant specialized in Indian rental agreements.

Draft a rental agreement for India.

Inputs:
- Landlord name: [LANDLORD]
- Tenant name: [TENANT]
- Property address: [ADDRESS]
- Monthly rent: [RENT]
- Security deposit: [DEPOSIT]
- Lease duration: [DURATION]
- Notice period: [NOTICE]
- Maintenance rules: [RULES]

Include:
- parties and definitions
- rent payment terms
- deposit clause
- termination clause
- maintenance responsibilities
- subletting restrictions
- dispute resolution
- jurisdiction clause
- signature block

Output should be formatted as a formal agreement document."""
    return {
        "title": title,
        "description": description,
        "category": category,
        "tags": tags,
        "prompt": prompt
    }


# ----------------------------
# GENERATION PLAN
# ----------------------------
def generate_prompt_objects():
    prompts = []
    used_slugs = set()

    # Core templates pool
    builders = []

    # Resume prompts
    for role in JOB_ROLES:
        for city in random.sample(INDIA_CITIES, 5):
            builders.append(lambda r=role, c=city: prompt_resume(r, c))

    # Interview prompts
    for role in JOB_ROLES:
        builders.append(lambda r=role: prompt_interview(r))

    # Startup pitch prompts
    for city in INDIA_CITIES:
        builders.append(lambda c=city: prompt_startup_pitch(c))

    # GST prompts
    for domain in INDIA_DOMAINS:
        builders.append(lambda d=domain: prompt_gst_business(d))

    # Exam prompts
    builders.append(lambda: prompt_upsc())
    for exam in INDIA_EXAMS:
        builders.append(lambda e=exam: prompt_exam(e))

    # Finance prompts
    for city in INDIA_CITIES:
        builders.append(lambda c=city: prompt_finance_personal(c))
    builders.append(lambda: prompt_tax_filing())

    # Coding prompts
    builders.append(lambda: prompt_system_design())

    # Marketing prompts
    for lang in LANGUAGES:
        builders.append(lambda l=lang: prompt_reel_script(l))

    # Legal prompts
    builders.append(lambda: prompt_legal_agreement())

    # Customer support prompts
    for domain in INDIA_DOMAINS:
        builders.append(lambda d=domain: prompt_customer_support(d))

    # Shuffle to avoid grouping
    random.shuffle(builders)

    # Expand until TOTAL_PROMPTS
    i = 0
    while len(prompts) < TOTAL_PROMPTS:
        builder = builders[i % len(builders)]
        obj = builder()

        title = obj["title"]
        slug = build_slug(title)
        slug = uniq_slug(slug, used_slugs)

        obj["slug"] = slug

        # Ensure prompt exists always
        if "prompt" not in obj or not obj["prompt"].strip():
            obj["prompt"] = f"Write a helpful AI prompt for: {title} (India)."

        # Ensure tags list
        if "tags" not in obj or not isinstance(obj["tags"], list):
            obj["tags"] = ["india"]

        # Normalize tags (lowercase)
        obj["tags"] = [str(t).strip().lower() for t in obj["tags"] if str(t).strip()]

        prompts.append(obj)
        i += 1

    return prompts


# ----------------------------
# MAIN
# ----------------------------
def main():
    random.seed(987)  # deterministic output
    generated = generate_prompt_objects()

    safe_write_json(OUTPUT_FILE, generated)

    print("========================================")
    print("NVO987 AI – India Prompt Database Built")
    print("----------------------------------------")
    print(f"Output file: {OUTPUT_FILE}")
    print(f"Total prompts: {len(generated)}")
    print(f"Generated date: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print("========================================")


if __name__ == "__main__":
    main()
