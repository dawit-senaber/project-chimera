import asyncio
import os
from skills.persona import AgentPersona, load_agent_persona, assemble_context


def write_soul(tmp_path, agent_id: str):
    d = tmp_path / "skills" / agent_id
    d.mkdir(parents=True)
    soul = d / "SOUL.md"
    soul.write_text("""---
name: TestAgent
id: test-agent
voice_traits: [witty, empathetic]
directives: [never_politics]
---
This is the backstory of TestAgent.
""")
    return str(d)


class MockMCP:
    async def call_tool(self, server, tool, args):
        # return a list of simple memory dicts
        await asyncio.sleep(0)
        return [{"text": "Memory A"}, {"text": "Memory B"}]


def test_load_agent_persona(tmp_path):
    agent_dir = write_soul(tmp_path, "test-agent")
    cwd = os.getcwd()
    try:
        os.chdir(str(tmp_path))
        p = load_agent_persona("test-agent")
        assert isinstance(p, AgentPersona)
        assert p.name == "TestAgent"
        assert "witty" in p.voice_traits
    finally:
        os.chdir(cwd)


def test_assemble_context_async(tmp_path):
    write_soul(tmp_path, "test-agent")
    cwd = os.getcwd()
    try:
        os.chdir(str(tmp_path))
        mock = MockMCP()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        prompt = loop.run_until_complete(assemble_context("test-agent", "query", mock))
        assert "Who You Are" in prompt
        assert "Memory A" in prompt
    finally:
        os.chdir(cwd)
