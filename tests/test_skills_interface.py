import pytest
import os

def test_skill_directory_structure():
    """Verify all required skills have their documentation and entry points."""
    required_skills = ["skill_trend_fetcher", "skill_media_generator", "skill_onchain_payment"]
    for skill in required_skills:
        skill_path = os.path.join("skills", skill)
        assert os.path.exists(skill_path), f"Missing skill directory: {skill}"
        assert os.path.exists(os.path.join(skill_path, "SKILL.md")), f"Missing SKILL.md in {skill}"

def test_mcp_heartbeat_config():
    """Verify pyproject.toml has the necessary MCP and Agentic dependencies."""
    with open("pyproject.toml", "r") as f:
        content = f.read()
        assert "mcp" in content
        assert "coinbase-agentkit" in content
        assert "weaviate-client" in content