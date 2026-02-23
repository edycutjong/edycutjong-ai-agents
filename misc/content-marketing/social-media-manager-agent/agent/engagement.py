from .generator import ContentGenerator

class EngagementManager:
    def __init__(self, content_generator: ContentGenerator):
        self.generator = content_generator
        # Mock comments
        self.mock_comments = [
            {"id": 1, "user": "@tech_fan", "text": "This is amazing! When is it launching?", "platform": "Twitter", "sentiment": "Positive"},
            {"id": 2, "user": "@skeptic_dev", "text": "I'm not sure about the privacy implications.", "platform": "LinkedIn", "sentiment": "Neutral"},
            {"id": 3, "user": "@early_adopter", "text": "Can I get early access?", "platform": "Instagram", "sentiment": "Positive"},
            {"id": 4, "user": "@troll_bot", "text": "This looks like vaporware.", "platform": "Twitter", "sentiment": "Negative"},
        ]

    def get_pending_comments(self):
        # In a real app, this would fetch from APIs
        return self.mock_comments

    def suggest_reply(self, comment):
        """Generates a reply suggestion based on the comment sentiment and brand voice."""
        prompt = f"Reply to this comment: '{comment['text']}' from {comment['user']} on {comment['platform']}."

        # Use the existing generator but customized for replies
        if not self.generator.llm:
            sentiment = comment.get("sentiment", "Neutral")
            if sentiment == "Positive":
                return f"Thanks {comment['user']}! We're glad you're excited! Stay tuned for updates."
            elif sentiment == "Negative":
                return f"Hi {comment['user']}, we appreciate your feedback and are working hard to address these concerns."
            else:
                return f"Thanks for sharing your thoughts, {comment['user']}!"

        try:
            # We can use the generator's LLM directly if we expose it or add a method
            # Ideally, we should add a method to ContentGenerator or use it here if accessible
            # Since we passed the instance, let's use a specific method if it existed, or just mock it for now
            # to avoid modifying generator.py again unless necessary.
            # Actually, let's add a helper method to EngagementManager that uses the generator's llm attribute if available.

            from langchain_core.prompts import PromptTemplate

            template = """
            You are a social media manager.
            Brand Voice: {voice}

            Task: Write a reply to this comment:
            User: {user}
            Comment: "{text}"
            Platform: {platform}
            Sentiment: {sentiment}

            Requirements:
            - Be polite and professional.
            - Address the user's point directly.
            - Keep it under 280 chars for Twitter.

            Reply:
            """

            prompt_template = PromptTemplate(
                input_variables=["voice", "user", "text", "platform", "sentiment"],
                template=template
            )

            chain = prompt_template | self.generator.llm
            response = chain.invoke({
                "voice": self.generator.brand_voice,
                "user": comment['user'],
                "text": comment['text'],
                "platform": comment['platform'],
                "sentiment": comment['sentiment']
            })
            return response.content.strip()

        except Exception as e:
            return f"Error generating reply: {e}"
