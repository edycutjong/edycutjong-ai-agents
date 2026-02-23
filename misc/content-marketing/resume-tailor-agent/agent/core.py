import sys
import os

# Ensure the root directory is in sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from langchain_openai import ChatOpenAI
except ImportError:
    try:
        from langchain.chat_models import ChatOpenAI
    except ImportError:
        # Last resort for some environments
        from langchain_community.chat_models import ChatOpenAI

try:
    from langchain.chains import LLMChain
except ImportError:
    try:
        from langchain_classic.chains import LLMChain
    except ImportError:
        # Even more fallback
        from langchain.chains.llm import LLMChain

# Adjusted imports assuming running from root or with PYTHONPATH set correctly
try:
    from prompts.system_prompts import (
        JOB_ANALYSIS_PROMPT,
        TAILOR_RESUME_PROMPT,
        COVER_LETTER_PROMPT
    )
    from config import Config
except ImportError:
    # Fallback for relative imports if run as a module
    from ..prompts.system_prompts import (
        JOB_ANALYSIS_PROMPT,
        TAILOR_RESUME_PROMPT,
        COVER_LETTER_PROMPT
    )
    from ..config import Config

class ResumeTailorAgent:
    def __init__(self):
        self.llm = self._get_llm()

    def _get_llm(self):
        if Config.MOCK_MODE or not Config.OPENAI_API_KEY:
            return None

        return ChatOpenAI(
            model=Config.MODEL_NAME,
            temperature=0.7,
            api_key=Config.OPENAI_API_KEY
        )

    def analyze_job(self, job_description: str) -> str:
        if self.llm is None:
            return self._mock_analyze_job(job_description)

        chain = LLMChain(llm=self.llm, prompt=JOB_ANALYSIS_PROMPT)
        result = chain.run(job_description=job_description)
        return result

    def tailor_resume(self, resume_content: str, job_analysis: str) -> str:
        if self.llm is None:
            return self._mock_tailor_resume(resume_content, job_analysis)

        chain = LLMChain(llm=self.llm, prompt=TAILOR_RESUME_PROMPT)
        result = chain.run(resume_content=resume_content, job_analysis=job_analysis)
        return result

    def generate_cover_letter(self, resume_content: str, job_description: str) -> str:
        if self.llm is None:
            return self._mock_generate_cover_letter(resume_content, job_description)

        chain = LLMChain(llm=self.llm, prompt=COVER_LETTER_PROMPT)
        result = chain.run(resume_content=resume_content, job_description=job_description)
        return result

    # --- MOCK RESPONSES ---

    def _mock_analyze_job(self, job_description):
        return f"""
**Job Analysis (MOCK)**

**Key Technical Skills**: Python, React, Cloud Computing (AWS/Azure)
**Soft Skills**: Problem Solving, Communication, Leadership
**Key Responsibilities**:
- Develop scalable web applications.
- Collaborate with cross-functional teams.
**Company Culture**: Innovative, Fast-paced, Collaborative.
**Keywords**: Full Stack, DevOps, Agile, CI/CD.
"""

    def _mock_tailor_resume(self, resume_content, job_analysis):
        return f"""
# TAILORED RESUME (MOCK)

## Professional Summary
Experienced Software Engineer with a focus on Full Stack development and Cloud technologies. Proven track record in delivering scalable solutions in agile environments.

## Experience
**Senior Developer @ Tech Corp**
- Led a team of 5 developers to build a cloud-native platform.
- Optimized CI/CD pipelines reducing deployment time by 40%.
- Utilized Python and React to enhance user experience.

## Skills
- **Languages**: Python, JavaScript, TypeScript
- **Frameworks**: React, Django, Flask
- **Tools**: Docker, Kubernetes, AWS
"""

    def _mock_generate_cover_letter(self, resume_content, job_description):
        return f"""
Dear Hiring Manager,

I am writing to express my strong interest in the Software Engineer position at your company. With my background in Python and React development, I am confident in my ability to contribute effectively to your team.

At my previous role, I successfully led key projects that aligned perfectly with the responsibilities outlined in your job description. I am particularly excited about the opportunity to work in your innovative and fast-paced environment.

Thank you for considering my application. I look forward to the possibility of discussing how my skills and experiences align with your needs.

Sincerely,
[Candidate Name]
"""
