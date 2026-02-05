import pytest
from skills.skill_trend_fetcher.logic import TrendFetcher

def test_trend_fetcher_output_schema():
    """Verify that the TrendFetcher returns the expected JSON structure."""
    fetcher = TrendFetcher(niche="Ethiopian Fashion")
    result = fetcher.execute()
    
    # Assertions based on the technical spec
    assert "trends" in result, "Result must contain 'trends' key"
    assert isinstance(result["trends"], list), "'trends' must be a list"
    assert len(result["trends"]) > 0, "Should find at least one trend"
    
    first_trend = result["trends"][0]
    assert "topic" in first_trend
    assert "score" in first_trend
    assert isinstance(first_trend["score"], int)


@pytest.mark.asyncio
async def test_fetch_trends_is_awaitable():
    fetcher = TrendFetcher(niche="Ethiopian Fashion")
    result = await fetcher.fetch_trends()
    assert isinstance(result, list)
    assert len(result) > 0
    assert isinstance(result[0], str)