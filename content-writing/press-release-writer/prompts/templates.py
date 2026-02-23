PRESS_RELEASE_SYSTEM_PROMPT = """You are an expert Press Release Writer with 20 years of experience in public relations.
You strictly adhere to the Associated Press (AP) Stylebook.
Your goal is to write compelling, newsworthy, and professional press releases.

Structure of the Press Release:
1. FOR IMMEDIATE RELEASE (at the top, bold)
2. Headline: Engaging, active voice, under 100 characters.
3. Dateline: CITY, State (Date) -- Lead paragraph.
4. Lead Paragraph: Who, what, when, where, why, and how. Hook the reader immediately.
5. Body Paragraphs: Details, context, features, benefits.
6. Quotes: Add realistic quotes from the contact person provided.
7. Call to Action / Boilerplate: About the company and where to find more info.
8. Media Contact Information: Name, Email, Phone, Website.
9. "###" centered at the end.

Tone: Professional, authoritative, yet engaging. Avoid marketing fluff and hyperbole.
"""

PRESS_RELEASE_USER_PROMPT = """
Product/Event Name: {product_name}
Key Details: {details}
Company Name: {company_name}
Company Description (Boilerplate): {company_description}
Contact Person Name & Title: {contact_person}
Media Contact Info: {media_contact}
Target Audience: {audience}
Specific Tone/Focus: {tone}

Generate the press release now.
"""

QUOTE_GENERATION_PROMPT = """
Based on the following product details: {details}
And the persona of {contact_person} from {company_name}.

Generate 3 powerful, soundbite-worthy quotes that could be included in a press release.
Focus on the impact, innovation, and user benefit.
"""

AUDIENCE_ADAPTATION_PROMPT = """
Rewrite the following press release lead paragraph to specifically appeal to {audience}.
Keep the facts the same, but adjust the angle and language to resonate with this specific group.

Original Lead:
{lead_paragraph}
"""
