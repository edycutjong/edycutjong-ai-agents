import logging
from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from config import Config
from prompts.system_prompts import (
    PLANNING_PROMPT,
    SEARCH_QUERY_PROMPT,
    SYNTHESIS_PROMPT,
    FACT_CHECK_PROMPT,
    FINAL_REPORT_PROMPT
)
from agent.tools import search_tool, scrape_website

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ResearchAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model=Config.MODEL_NAME,
            temperature=0.7,
            api_key=Config.OPENAI_API_KEY
        )
        self.history = []

    def plan_research(self, topic: str, depth: str, domains: List[str]) -> List[str]:
        """
        Generates a research plan (list of sub-topics) based on the topic.
        """
        logger.info(f"Planning research for: {topic}")
        prompt = PromptTemplate.from_template(PLANNING_PROMPT)
        chain = prompt | self.llm | StrOutputParser()

        response = chain.invoke({
            "topic": topic,
            "depth": depth,
            "domains": ", ".join(domains)
        })

        # Parse the response into a list of steps
        # Assuming the LLM returns a numbered list
        steps = []
        for line in response.split('\n'):
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('-')):
                # Remove numbering/bullets
                clean_line = line.lstrip('0123456789.- ').strip()
                if clean_line:
                    steps.append(clean_line)

        # Fallback if parsing fails or LLM returns just text
        if not steps:
            steps = [topic]

        # Limit steps based on depth if needed, or just return all
        return steps[:Config.MAX_ITERATIONS]

    def generate_search_queries(self, sub_topic: str, context: str = "") -> List[str]:
        """
        Generates search queries for a sub-topic.
        """
        logger.info(f"Generating queries for: {sub_topic}")
        prompt = PromptTemplate.from_template(SEARCH_QUERY_PROMPT)
        chain = prompt | self.llm | StrOutputParser()

        response = chain.invoke({
            "sub_topic": sub_topic,
            "context": context,
            "num_queries": 3
        })

        queries = [q.strip() for q in response.split('\n') if q.strip()]
        return queries

    def synthesize_info(self, topic: str, research_data: str, focus: str) -> str:
        """
        Synthesizes research data into a report section.
        """
        logger.info(f"Synthesizing info for: {topic}")
        if not research_data:
            return "No information found."

        prompt = PromptTemplate.from_template(SYNTHESIS_PROMPT)
        chain = prompt | self.llm | StrOutputParser()

        # Truncate research data to avoid token limits if necessary
        # (Naive truncation, better to use token counting but string slicing is faster for now)
        truncated_data = research_data[:20000]

        return chain.invoke({
            "topic": topic,
            "research_data": truncated_data,
            "focus": focus
        })

    def fact_check(self, text: str) -> str:
        """
        Fact-checks the synthesized text.
        """
        logger.info("Fact checking...")
        prompt = PromptTemplate.from_template(FACT_CHECK_PROMPT)
        chain = prompt | self.llm | StrOutputParser()

        return chain.invoke({"text": text})

    def generate_final_report(self, topic: str, sections: List[str]) -> str:
        """
        Compiles sections into a final report.
        """
        logger.info("Generating final report...")
        prompt = PromptTemplate.from_template(FINAL_REPORT_PROMPT)
        chain = prompt | self.llm | StrOutputParser()

        combined_sections = "\n\n".join(sections)

        return chain.invoke({
            "topic": topic,
            "sections": combined_sections
        })

    def run_research(self, topic: str, depth: str, domains: List[str], status_callback=None) -> str:
        """
        Main execution loop.
        status_callback: function(str) -> void to update UI
        """
        def update_status(msg):
            if status_callback:
                status_callback(msg)
            logger.info(msg)

        update_status(f"Starting research on: {topic}")

        # 1. Plan
        update_status("Planning research structure...")
        plan = self.plan_research(topic, depth, domains)
        update_status(f"Plan created with {len(plan)} steps.")

        report_sections = []

        # 2. Execute per step
        for i, step in enumerate(plan):
            update_status(f"Step {i+1}/{len(plan)}: Researching '{step}'...")

            # Generate queries
            queries = self.generate_search_queries(step)

            # Search
            all_content = []
            for query in queries[:1]: # Limit to 1 query per step to save time/tokens for now
                update_status(f"Searching: {query}")
                urls = search_tool(query, num_results=Config.SEARCH_RESULTS_PER_QUERY)

                for url in urls:
                    update_status(f"Reading: {url}")
                    content = scrape_website(url)
                    if content:
                        all_content.append(f"Source: {url}\nContent: {content}\n---\n")

            combined_content = "\n".join(all_content)

            # Synthesize
            update_status(f"Synthesizing findings for '{step}'...")
            synthesis = self.synthesize_info(topic, combined_content, focus=step)

            # Fact Check
            update_status(f"Fact checking '{step}' section...")
            checked_synthesis = self.fact_check(synthesis)

            report_sections.append(checked_synthesis)

        # 3. Final Report
        update_status("Compiling final report...")
        final_report = self.generate_final_report(topic, report_sections)

        update_status("Research complete!")
        return final_report
