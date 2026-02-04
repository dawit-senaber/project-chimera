import os

class MediaGenerator:
    def __init__(self, persona_path="SOUL.md"):
        self.persona_path = persona_path
        self.persona_context = self._load_persona()

    def _load_persona(self) -> str:
        """Reads the influencer's persona/soul to guide generation."""
        if os.path.exists(self.persona_path):
            with open(self.persona_path, "r", encoding="utf-8") as f:
                return f.read()
        return "Standard AI Influencer Persona"

    def generate_post(self, trend_data: dict) -> dict:
        """
        Transforms raw trend data into a structured social media post.
        In a production environment, this would call an LLM (like GPT-4 or Claude).
        """
        # Extract the primary trend found by the TrendFetcher
        trends = trend_data.get("trends", [])
        primary_trend = trends[0].get("topic", "Digital Innovation") if trends else "General"
        
        # Crafting the content based on the trend
        # Note: Logic here simulates the 'Brain' processing the SOUL.md context
        caption = f"Exploring the intersection of {primary_trend} and local heritage. #ProjectChimera #FutureAddis"
        
        return {
            "status": "draft",
            "platform": "X/Twitter",
            "content": caption,
            "image_prompt": f"A high-fidelity cinematic shot of {primary_trend}, ultra-realistic, neon accents, 8k resolution",
            "metadata": {
                "trend_source": primary_trend,
                "persona_aligned": True
            }
        }

if __name__ == "__main__":
    # Quick local test
    gen = MediaGenerator()
    mock_trend = {"trends": [{"topic": "Ethio-Jazz Revival", "score": 95}]}
    print(gen.generate_post(mock_trend))