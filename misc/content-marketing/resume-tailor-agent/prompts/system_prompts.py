try:
    from langchain.prompts import PromptTemplate
except ImportError:
    try:
        from langchain_core.prompts import PromptTemplate
    except ImportError:
        # Fallback for some weird environments
        from langchain.prompts.prompt import PromptTemplate

# 1. Analyze Job Description
JOB_ANALYSIS_PROMPT = PromptTemplate(
    input_variables=["job_description"],
    template="""
You are an expert career coach and technical recruiter.
Analyze the following job description and extract the key information needed to tailor a resume.

Job Description:
{job_description}

Output your analysis in the following format:
1. **Key Technical Skills**: List the most critical technical skills required.
2. **Soft Skills/Core Competencies**: List the important soft skills or competencies.
3. **Key Responsibilities**: Summarize the main day-to-day duties.
4. **Company Culture/Values**: Infer the company culture and values if mentioned.
5. **Keywords**: specific keywords to include in the resume for ATS optimization.
"""
)

# 2. Tailor Resume
TAILOR_RESUME_PROMPT = PromptTemplate(
    input_variables=["resume_content", "job_analysis"],
    template="""
You are an expert resume writer.
Your task is to rewrite the provided resume to better match the analyzed job requirements.

Original Resume:
{resume_content}

Job Analysis:
{job_analysis}

Instructions:
- Keep the original structure (Contact Info, Experience, Education, Skills) but optimize the content.
- Rewrite the Professional Summary to align with the job's key responsibilities and culture.
- Rewrite bullet points in the Experience section to highlight relevant achievements using the keywords from the analysis.
- Ensure the tone is professional and action-oriented.
- Do not fabricate experiences, but rephrase existing ones to emphasize relevance.
- Add a "Skills" section if missing, or update the existing one with the Key Technical Skills and Keywords.

Output the full tailored resume in Markdown format.
"""
)

# 3. Generate Cover Letter
COVER_LETTER_PROMPT = PromptTemplate(
    input_variables=["resume_content", "job_description"],
    template="""
You are a professional cover letter writer.
Write a compelling cover letter for the candidate based on their resume and the job description.

Candidate's Resume:
{resume_content}

Job Description:
{job_description}

Instructions:
- The cover letter should be addressed to the Hiring Manager (or specific name if found).
- Hook the reader in the opening paragraph.
- Body paragraphs should connect the candidate's specific achievements to the job's key challenges.
- Convey enthusiasm for the role and company.
- Professional sign-off.
- Keep it concise (under 400 words).

Output the cover letter in Markdown format.
"""
)
