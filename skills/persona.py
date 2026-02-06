from __future__ import annotations
import os
import re
import asyncio
from typing import List, Any, Optional
from pydantic import BaseModel

try:
    import yaml
except Exception:  # pragma: no cover - yaml optional
    yaml = None


class AgentPersona(BaseModel):
    name: str
    id: str
    voice_traits: List[str] = []
    directives: List[str] = []
    backstory: str = ""


def _find_soul_paths(agent_id: str) -> List[str]:
    candidates = []
    # per-agent SOUL file
    candidates.append(os.path.join("skills", agent_id, "SOUL.md"))
    # repo-level fallback
    candidates.append("SOUL.md")
    return candidates


def load_agent_persona(agent_id: str) -> AgentPersona:
    """Load and parse an agent's SOUL.md frontmatter into AgentPersona.

    Looks for `skills/{agent_id}/SOUL.md` first, then `SOUL.md` at repo root.
    Frontmatter should be YAML between `---` separators. The markdown body
    becomes `backstory`.
    """
    paths = _find_soul_paths(agent_id)
    content = None
    for p in paths:
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                content = f.read()
            break
    if content is None:
        raise FileNotFoundError(f"SOUL.md not found for agent '{agent_id}' (looked: {paths})")

    m = re.match(r"^---\s*\n(.*?\n)---\s*\n(.*)$", content, re.S)
    front = {}
    body = content
    if m:
        fm_text = m.group(1)
        body = m.group(2).strip()
        if yaml:
            try:
                front = yaml.safe_load(fm_text) or {}
            except Exception:
                front = {}
        else:
            # naive YAML-ish parser: key: value lines
            for line in fm_text.splitlines():
                line = line.strip()
                if not line or ":" not in line:
                    continue
                k, v = line.split(":", 1)
                val = v.strip()
                # lists separated by commas
                if val.startswith("[") and val.endswith("]"):
                    val = [x.strip().strip('"\'') for x in val[1:-1].split(",") if x.strip()]
                front[k.strip()] = val

    # Normalize fields
    persona_data = {
        "name": front.get("name") or agent_id,
        "id": front.get("id") or agent_id,
        "voice_traits": front.get("voice_traits") or front.get("voice_traits", []) or [],
        "directives": front.get("directives") or front.get("directives", []) or [],
        "backstory": body,
    }
    return AgentPersona(**persona_data)


async def assemble_context(agent_id: str, input_query: str, mcp_client: Optional[Any] = None) -> str:
    """Assemble a system prompt string containing persona and retrieved memories.

    - Loads the `AgentPersona` from SOUL.md
    - Calls `mcp_client.call_tool('mcp-server-weaviate','search_memory', {...})` to retrieve 5 memories
    - Returns a formatted prompt with 'Who You Are' and 'What You Remember'
    """
    persona = load_agent_persona(agent_id)
    memories = []
    if mcp_client is not None:
        try:
            call = None
            if hasattr(mcp_client, "call_tool"):
                call = mcp_client.call_tool("mcp-server-weaviate", "search_memory", {"query": input_query, "limit": 5})
            elif hasattr(mcp_client, "call"):
                call = mcp_client.call("mcp-server-weaviate", "search_memory", {"query": input_query, "limit": 5})

            if asyncio.iscoroutine(call):
                memories = await call
            else:
                memories = call or []
        except Exception:
            memories = []

    # Normalize memories into text lines
    mem_lines = []
    for m in memories:
        if isinstance(m, dict):
            t = m.get("text") or m.get("snippet") or m.get("content") or str(m)
        else:
            t = str(m)
        mem_lines.append(t)

    prompt = []
    prompt.append("Who You Are:\n")
    prompt.append(f"Name: {persona.name}\n")
    prompt.append(f"ID: {persona.id}\n")
    if persona.voice_traits:
        prompt.append("Voice Traits: " + ", ".join(persona.voice_traits) + "\n")
    if persona.directives:
        prompt.append("Directives: " + ", ".join(persona.directives) + "\n")
    prompt.append("Backstory:\n" + persona.backstory + "\n\n")

    prompt.append("What You Remember:\n")
    if mem_lines:
        for i, line in enumerate(mem_lines[:5], 1):
            prompt.append(f"{i}. {line}\n")
    else:
        prompt.append("(No relevant memories found)\n")

    return "\n".join(prompt)
