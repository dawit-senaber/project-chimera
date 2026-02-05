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

    async def fetch_trends(self) -> dict:
        """Async compatibility wrapper expected by the planner.

        Delegates to the existing synchronous `execute()` method so
        callers can `await` the result without changing core logic.
        """
        data = self.execute()
        # Return a list of trend topics (planner expects a list it can slice)
        return [t.get("topic") for t in data.get("trends", [])]

    def fetch_interface(self) -> dict:
        """Return a machine-readable description of the expected input contract.

        This small helper is intended for spec-checking and documentation.
        It should list the input properties the skill expects.
        """
        return {
            "title": "TrendFetcher Input Contract",
            "type": "object",
            "properties": {
                "niche": {"type": "string"},
                "lookback_hours": {"type": "integer"},
                "min_relevance": {"type": "number"}
            },
            "required": ["niche"]
        }