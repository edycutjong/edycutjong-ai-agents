import os
import random
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

class ContentGenerator:
    def __init__(self, api_key=None, brand_voice="Professional, engaging, and tech-savvy"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.brand_voice = brand_voice
        self.llm = None

        if self.api_key:
            self.llm = ChatOpenAI(api_key=self.api_key, model="gpt-4o")

    def generate_draft(self, topic, platform="Twitter"):
        """Generates a social media draft for a specific platform."""
        if not self.llm:
            return f"[MOCK DRAFT] Here is a generated post about '{topic}' for {platform} in a {self.brand_voice} tone. #MockGen #AI"

        prompt_template = PromptTemplate(
            input_variables=["topic", "platform", "voice"],
            template="""
            You are a social media manager.
            Brand Voice: {voice}

            Task: Write a {platform} post about: {topic}.

            Requirements:
            - Use appropriate emojis for {platform}.
            - Include 2-3 relevant hashtags.
            - Keep it concise and engaging.
            - For Twitter/X: Max 280 characters.
            - For LinkedIn: Professional but conversational, structure with bullet points if needed.
            - For Instagram: Visual-focused caption, engaging hook.

            Draft:
            """
        )

        chain = prompt_template | self.llm
        try:
            response = chain.invoke({"topic": topic, "platform": platform, "voice": self.brand_voice})
            return response.content.strip()
        except Exception as e:
            return f"Error generating content: {str(e)}"

    def generate_image_prompt(self, topic, platform="Instagram"):
        """Generates an image generation prompt for DALL-E or Midjourney."""
        if not self.llm:
            return f"[MOCK IMAGE PROMPT] A high-quality, professional photo representing '{topic}' with a modern aesthetic suitable for {platform}."

        prompt_template = PromptTemplate(
            input_variables=["topic", "platform", "voice"],
            template="""
            You are an AI art director.
            Brand Voice: {voice}

            Task: Create a detailed image generation prompt for a post about: {topic} on {platform}.

            Requirements:
            - Describe the subject, lighting, style, and mood.
            - Optimize for high-quality, photorealistic or modern vector art style.
            - No text in the image description unless essential.

            Image Prompt:
            """
        )

        chain = prompt_template | self.llm
        try:
            response = chain.invoke({"topic": topic, "platform": platform, "voice": self.brand_voice})
            return response.content.strip()
        except Exception as e:
            return f"Error generating image prompt: {str(e)}"

if __name__ == "__main__":
    gen = ContentGenerator()
    print(gen.generate_draft("AI Agents in 2024", "LinkedIn"))
