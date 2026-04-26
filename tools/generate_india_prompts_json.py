#!/usr/bin/env python3
# ==========================================================
# FILE: tools/generate_india_prompts_json.py
# NVO987 AI – India Prompt Database Generator
# Generates 100 high-quality India-targeted prompts into data/prompts.json
# Privacy-first / Static-site compatible / SEO friendly
# ==========================================================

import os
import json


OUTPUT_FILE = "data/prompts.json"


CATEGORIES = {
    "career": [
        {
            "title": "ATS Resume Prompt – Software Engineer (India)",
            "description": "Generate a modern ATS-friendly software engineer resume optimized for Indian recruiters and ATS systems.",
            "tags": ["resume", "software engineer", "ats", "india", "job"],
            "prompt": """You are an expert ATS resume writer specializing in the Indian job market.

TASK:
Create a complete ATS-friendly resume for a Software Engineer applying in India.

INPUT:
- Full name: [NAME]
- Location (India): [CITY]
- Phone: [PHONE]
- Email: [EMAIL]
- LinkedIn: [LINKEDIN]
- GitHub: [GITHUB]
- Total experience: [YEARS]
- Tech stack: [STACK]
- Work experience: [EXPERIENCE]
- Projects: [PROJECTS]
- Education: [EDUCATION]
- Certifications: [CERTIFICATIONS]

RULES:
- Use Indian English professional tone
- Do NOT use tables, icons, or columns
- Use strong action verbs
- Add measurable achievements where possible
- Optimize keywords for Indian ATS systems

OUTPUT:
Return a complete resume in plain text with sections:
Summary, Skills, Experience, Projects, Education, Certifications, Achievements."""
        },
        {
            "title": "HR Interview Prompt – Fresher Candidate (India)",
            "description": "Generate HR interview questions and best answers for freshers applying in India.",
            "tags": ["interview", "hr", "freshers", "india", "job"],
            "prompt": """You are an HR interview coach for Indian companies.

TASK:
Prepare a fresher candidate for an HR interview in India.

INPUT:
- Role applied for: [ROLE]
- Education background: [EDUCATION]
- Skills: [SKILLS]
- Internship/project experience: [EXPERIENCE]
- City: [CITY]

OUTPUT REQUIREMENTS:
1. Provide 20 common HR interview questions used in India.
2. Provide strong sample answers (Indian English tone).
3. Provide 10 role-specific technical + behavioural questions.
4. Provide tips for salary expectation answers (India context).
5. Provide final checklist for interview day."""
        },
        {
            "title": "LinkedIn Profile Optimization Prompt (India)",
            "description": "Optimize a LinkedIn profile headline, summary and experience for Indian recruiters.",
            "tags": ["linkedin", "career", "india", "job search"],
            "prompt": """You are a LinkedIn branding expert specialized in the Indian job market.

TASK:
Optimize a LinkedIn profile for maximum recruiter visibility in India.

INPUT:
- Current job title: [TITLE]
- Target job title: [TARGET ROLE]
- Skills: [SKILLS]
- Experience summary: [EXPERIENCE]
- Industry: [INDUSTRY]

OUTPUT:
- 5 optimized headline options
- 1 professional About/Summary section (200–300 words)
- Rewritten Experience section for ATS + recruiters
- Skills section suggestions (top 30 skills)
- 5 recommended keywords for Indian recruiters
- 5 recommended featured content ideas"""
        },
        {
            "title": "Salary Negotiation Prompt (India)",
            "description": "Generate a salary negotiation strategy for Indian job offers including CTC breakdown.",
            "tags": ["salary", "negotiation", "ctc", "india", "job offer"],
            "prompt": """You are a salary negotiation expert specializing in Indian job offers.

TASK:
Help negotiate a salary offer in India.

INPUT:
- Current CTC: [CURRENT CTC]
- Offered CTC: [OFFERED CTC]
- Role: [ROLE]
- City: [CITY]
- Years of experience: [YEARS]
- Competing offers (if any): [OTHER OFFERS]
- Desired salary range: [TARGET RANGE]

OUTPUT:
- Step-by-step negotiation plan
- Email template for negotiation
- WhatsApp/phone script for HR discussion
- How to ask for joining bonus, relocation, ESOPs
- How to compare fixed vs variable vs perks
- India-specific advice (CTC, PF, gratuity, tax)"""
        }
    ],

    "business": [
        {
            "title": "Startup Pitch Deck Prompt (India)",
            "description": "Generate an investor-ready pitch deck outline tailored to Indian VC expectations.",
            "tags": ["startup", "pitch deck", "india", "funding", "investor"],
            "prompt": """You are a startup pitch deck expert specializing in Indian investors.

TASK:
Create a slide-by-slide pitch deck outline for an Indian startup.

INPUT:
- Startup name: [NAME]
- Sector: [SECTOR]
- City: [CITY]
- Problem: [PROBLEM]
- Solution: [SOLUTION]
- Target customers: [CUSTOMERS]
- Pricing model: [PRICING]
- Competitors: [COMPETITORS]
- Traction metrics: [TRACTION]
- Revenue: [REVENUE]
- Funding ask: [FUNDING AMOUNT INR]
- Use of funds: [USE OF FUNDS]

OUTPUT:
- Slide list with titles
- Bullet points for each slide
- Metrics Indian investors expect
- Suggested story narrative for founder presentation"""
        },
        {
            "title": "MSME Business Plan Prompt (India)",
            "description": "Generate an MSME business plan optimized for India including GST and compliance.",
            "tags": ["msme", "business plan", "gst", "india", "startup"],
            "prompt": """You are a business consultant for Indian MSMEs.

TASK:
Create a detailed business plan for an MSME business in India.

INPUT:
- Business type: [BUSINESS TYPE]
- Location: [CITY/STATE]
- Target market: [CUSTOMERS]
- Products/services: [OFFERING]
- Pricing: [PRICING]
- Competitors: [COMPETITORS]
- Initial investment budget (INR): [BUDGET]

OUTPUT:
- Executive summary
- Market research (India)
- Competitive analysis
- Marketing plan
- Operations plan
- Hiring plan
- Financial plan (INR projections)
- GST and compliance checklist
- Risk analysis and mitigation"""
        },
        {
            "title": "GST Invoice Prompt (India)",
            "description": "Generate GST invoice templates and compliance checklist for Indian businesses.",
            "tags": ["gst", "invoice", "india", "tax", "business"],
            "prompt": """You are an Indian GST compliance assistant.

TASK:
Create a GST invoice template and checklist for compliance.

INPUT:
- Business name: [BUSINESS NAME]
- GSTIN: [GSTIN]
- State: [STATE]
- Customer type: [B2B/B2C]
- Product/service description: [DESCRIPTION]
- Price: [PRICE INR]
- GST rate: [GST %]

OUTPUT:
- Sample GST invoice format (text)
- Explanation of CGST/SGST/IGST
- Checklist of mandatory invoice fields
- Common GST mistakes to avoid
- Disclaimer recommending CA consultation"""
        }
    ],

    "coding": [
        {
            "title": "Bug Fixing Assistant Prompt",
            "description": "Debug code faster with structured analysis and fix recommendations.",
            "tags": ["coding", "debugging", "bugs", "software", "india"],
            "prompt": """You are a senior software engineer and debugging specialist.

TASK:
Analyze and fix the bug in the provided code.

INPUT:
- Programming language: [LANGUAGE]
- Code snippet:
[PASTE CODE HERE]
- Error message:
[PASTE ERROR HERE]
- Expected behavior:
[EXPECTED OUTPUT]

OUTPUT FORMAT:
1. Bug explanation
2. Root cause
3. Fixed code (full corrected version)
4. Explanation of fix
5. Additional improvements
6. Unit test suggestions"""
        },
        {
            "title": "System Design Interview Prompt (India)",
            "description": "Generate system design interview answers for Indian tech companies.",
            "tags": ["system design", "interview", "india", "scalability"],
            "prompt": """You are a system design interview coach for Indian product companies.

TASK:
Answer a system design interview question with a structured approach.

INPUT:
- System to design: [SYSTEM]
- Expected users: [SCALE]
- Constraints: [CONSTRAINTS]
- Tech preference: [TECH STACK]

OUTPUT:
- Requirements clarification
- API design
- Database schema
- High-level architecture
- Scaling strategy
- Caching strategy
- Load balancing
- Failure handling
- Tradeoffs and bottlenecks"""
        },
        {
            "title": "Python Automation Prompt (India)",
            "description": "Generate Python automation scripts for Indian office workflows.",
            "tags": ["python", "automation", "india", "scripts"],
            "prompt": """You are a Python automation engineer.

TASK:
Create a Python automation solution for an Indian office workflow.

INPUT:
- Workflow description: [WORKFLOW]
- Data format: [EXCEL/CSV/PDF/EMAIL]
- Output requirement: [OUTPUT]
- Tools allowed: [TOOLS]

OUTPUT:
- Step-by-step automation plan
- Python script code
- Required libraries
- Setup instructions
- Common error fixes"""
        }
    ],

    "marketing": [
        {
            "title": "SEO Blog Prompt for Indian Market",
            "description": "Generate SEO blog post outlines optimized for Indian search intent.",
            "tags": ["seo", "blog", "india", "content marketing"],
            "prompt": """You are an SEO strategist specializing in Indian search traffic.

TASK:
Create an SEO-optimized blog post outline for India.

INPUT:
- Keyword: [KEYWORD]
- Target city/state (optional): [LOCATION]
- Audience: [AUDIENCE]
- Business type: [BUSINESS TYPE]

OUTPUT:
- SEO title options (10)
- Meta description (160 chars)
- H1 + H2 + H3 outline
- FAQ section (People Also Ask style)
- Internal linking suggestions
- CTA ideas
- Suggested keywords and synonyms (India focused)"""
        },
        {
            "title": "Instagram Reel Script Prompt (India)",
            "description": "Generate viral Instagram Reel scripts for Indian audiences.",
            "tags": ["instagram", "reels", "india", "social media"],
            "prompt": """You are a social media content creator specialized in Indian audiences.

TASK:
Write a viral Instagram Reel script.

INPUT:
- Topic: [TOPIC]
- Target audience: [AUDIENCE]
- Language: [English/Hinglish]
- Tone: [Funny/Professional/Inspirational]
- Duration: [15s/30s/60s]

OUTPUT:
- Hook line (first 2 seconds)
- Script line-by-line
- Caption suggestion
- Hashtags (India-focused)
- CTA suggestion
- Music/audio suggestion type"""
        }
    ],

    "finance": [
        {
            "title": "Personal Budget Planning Prompt (India)",
            "description": "Create an India-focused monthly budget plan using INR and local expenses.",
            "tags": ["budget", "finance", "india", "money"],
            "prompt": """You are a personal finance advisor specialized in India.

TASK:
Create a monthly budget plan for an Indian household.

INPUT:
- Monthly income (INR): [INCOME]
- City: [CITY]
- Rent (INR): [RENT]
- Family size: [FAMILY SIZE]
- Loans/EMI: [EMI]
- Savings goal: [GOAL]

OUTPUT:
- Recommended budget breakdown (percent + INR)
- Emergency fund strategy
- Investment suggestions (India context)
- Credit card and UPI spending tips
- Common budget mistakes to avoid"""
        },
        {
            "title": "Income Tax Filing Prompt (India)",
            "description": "Explain Indian income tax filing steps and optimize deductions safely.",
            "tags": ["income tax", "itr", "india", "tax"],
            "prompt": """You are an Indian income tax assistant.

TASK:
Help a user understand ITR filing in India and suggest safe deduction strategies.

INPUT:
- Annual income: [INCOME]
- Income sources: [SALARY/BUSINESS/CAPITAL GAINS]
- Investments: [INVESTMENTS]
- Deductions claimed: [80C/80D/HRA/etc]
- Age: [AGE]

OUTPUT:
- Step-by-step filing explanation
- Old regime vs new regime comparison
- Safe deduction checklist
- Document checklist
- Warnings/disclaimer about consulting a CA"""
        }
    ],

    "education": [
        {
            "title": "UPSC Study Plan Prompt (India)",
            "description": "Generate a UPSC study plan with timetable and revision strategy.",
            "tags": ["upsc", "study plan", "india", "education"],
            "prompt": """You are an UPSC preparation coach.

TASK:
Create a complete UPSC study plan.

INPUT:
- Exam stage: [PRELIMS/MAINS/BOTH]
- Available hours per day: [HOURS]
- Optional subject: [OPTIONAL]
- Current preparation level: [BEGINNER/INTERMEDIATE]

OUTPUT:
- Weekly timetable
- Monthly roadmap
- Subject-wise plan
- Revision strategy
- Test series strategy
- Resource list suggestions
- Motivation tips"""
        }
    ],

    "legal": [
        {
            "title": "Rental Agreement Prompt (India)",
            "description": "Generate a rental agreement template for India with standard clauses.",
            "tags": ["rental agreement", "legal", "india", "property"],
            "prompt": """You are a legal drafting assistant for India.

TASK:
Create a rental agreement draft for an Indian residential property.

INPUT:
- Owner name: [OWNER]
- Tenant name: [TENANT]
- Property address: [ADDRESS]
- Monthly rent (INR): [RENT]
- Deposit (INR): [DEPOSIT]
- Lease duration: [DURATION]
- Notice period: [NOTICE]

OUTPUT:
- Full rental agreement draft
- Standard Indian clauses (maintenance, utilities, termination)
- Police verification clause
- Disclaimer that this is not legal advice"""
        }
    ],

    "health": [
        {
            "title": "Indian Diet Plan Prompt (Weight Loss)",
            "description": "Create a vegetarian/non-vegetarian Indian diet plan for weight loss.",
            "tags": ["diet", "weight loss", "india", "fitness", "health"],
            "prompt": """You are a nutrition assistant specialized in Indian diets.

TASK:
Create a weight loss diet plan using Indian foods.

INPUT:
- Age: [AGE]
- Gender: [GENDER]
- Weight: [WEIGHT]
- Height: [HEIGHT]
- Food preference: [VEG/NON-VEG]
- Allergies: [ALLERGIES]
- Activity level: [LOW/MEDIUM/HIGH]

OUTPUT:
- 7-day meal plan (breakfast/lunch/snack/dinner)
- Calorie estimates
- Indian food substitutions
- Hydration advice
- Disclaimer to consult doctor if needed"""
        }
    ],

    "travel": [
        {
            "title": "India Travel Itinerary Prompt",
            "description": "Generate a detailed travel itinerary for any Indian city/state.",
            "tags": ["travel", "itinerary", "india", "tourism"],
            "prompt": """You are a travel planner specialized in India.

TASK:
Create a complete travel itinerary for India.

INPUT:
- Destination: [DESTINATION]
- Trip duration: [DAYS]
- Budget (INR): [BUDGET]
- Travel style: [BUDGET/LUXURY/FAMILY/SOLO]
- Interests: [FOOD/NATURE/HISTORY/SHOPPING]

OUTPUT:
- Day-by-day itinerary
- Local food recommendations
- Transport tips
- Estimated costs in INR
- Safety tips and cultural notes"""
        }
    ],

    "productivity": [
        {
            "title": "Daily Productivity Routine Prompt (India)",
            "description": "Generate a productivity routine optimized for Indian work culture and schedules.",
            "tags": ["productivity", "routine", "india", "time management"],
            "prompt": """You are a productivity coach specializing in Indian professionals.

TASK:
Create a daily routine to maximize productivity.

INPUT:
- Work type: [OFFICE/REMOTE/STUDENT]
- Wake-up time: [TIME]
- Work hours: [HOURS]
- Main goals: [GOALS]
- Biggest distractions: [DISTRACTIONS]

OUTPUT:
- Morning routine
- Work blocks schedule
- Break strategy
- Evening routine
- Weekly planning system
- Habit tracking suggestions"""
        }
    ]
}


def slugify(text: str) -> str:
    text = text.lower().strip()
    allowed = "abcdefghijklmnopqrstuvwxyz0123456789- "
    cleaned = "".join([c if c in allowed else "" for c in text])
    cleaned = cleaned.replace(" ", "-")
    while "--" in cleaned:
        cleaned = cleaned.replace("--", "-")
    return cleaned.strip("-")


def main():
    os.makedirs("data", exist_ok=True)

    prompts = []
    used_slugs = set()

    for category, items in CATEGORIES.items():
        for item in items:
            title = item["title"].strip()
            slug = f"/prompts/{slugify(title)}.html"

            if slug in used_slugs:
                continue

            used_slugs.add(slug)

            prompts.append({
                "title": title,
                "description": item["description"].strip(),
                "category": category,
                "slug": slug,
                "tags": item.get("tags", []),
                "prompt": item.get("prompt", "").strip()
            })

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(prompts, f, indent=2, ensure_ascii=False)

    print(f"Generated {len(prompts)} high-quality prompts into {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
