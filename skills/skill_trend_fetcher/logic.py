# skills/skill_trend_fetcher/logic.py

class TrendFetcher:
    def __init__(self, niche: str):
        self.niche = niche

    def execute(self) -> dict:
        # Returning mock data that aligns with your Technical Spec schema
        return {
            "niche": self.niche,
            "trends": [
                {"topic": "On-chain Identity", "score": 92},
                {"topic": "Autonomous Agents", "score": 85}
            ]
        }