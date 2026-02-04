# Project Chimera: Technical Specification & API Contracts

## 1. System Integration Architecture
The system utilizes the **Model Context Protocol (MCP)** as the universal abstraction layer for all external tools. Core logic remains stateless, relying on the **FastRender Swarm** to manage execution flow.

## 2. API & Skill Contracts (JSON Schemas)

### 2.1 Skill: `skill_trend_fetcher`
**Purpose**: Fetches and scores market trends via MCP News/Social Resources.
- **Input**:
  ```json
  {
    "niche": "string",           // e.g., "Ethiopian Fashion"
    "lookback_hours": "integer", // e.g., 4
    "min_relevance": "float"     // e.g., 0.75
  }

-  **Output**:
   ```json
  {
  "trends": [
    {
      "topic": "string",
      "score": "float",
      "source_url": "string",
      "raw_text": "string"
    }
  ]
}


### 2.2 Skill: skill_onchain_payment
**Purpose**: Executes USDC transfers via Coinbase AgentKit on the Base network.

Security: Requires @budget_check decorator validation against daily_spend limit.

- **Input**:
  ```json
  {
  "recipient_address": "string",
  "amount_usdc": "float",
  "memo": "string"
}

-  **Output**:
   ```json
   {
  "transaction_hash": "string",
  "status": "confirmed | pending | rejected",
  "new_balance": "float"
}


### 2.3 Skill: `skill_media_generator`
**Purpose**: Synthesizes trend data and SOUL.md persona into platform-ready content.
- **Input**:
  ```json
  {
    "trend_id": "string",
    "persona_ref": "./SOUL.md",
    "platform": "MoltBook | X | Instagram"
  }

-  **Output**:
   ```json
   {
  "post_content": "string",
  "media_type": "image | text",
  "gen_ai_prompt": "string",
  "compliance_check": "boolean"
}


## 3. Database Schema (PostgreSQL ERD)

| Table         | Column        | Type     | Description                                                      |
|---------------|---------------|----------|------------------------------------------------------------------|
| agents        | id            | UUID     | Primary Key: Unique identifier for the autonomous entity.       |
| agents        | soul_path     | STRING   | Path to SOUL.md: Reference for persona consistency.             |
| agents        | state_version | BIGINT   | OCC Counter: Used to prevent race conditions during state updates. |
| transactions  | id            | UUID     | Primary Key: Unique identifier for the financial event.         |
| transactions  | agent_id      | UUID     | Foreign Key: Links the transaction to a specific agent.         |
| transactions  | tx_hash       | STRING   | On-chain identifier: The immutable record on the Base network.  |
| transactions  | amount        | DECIMAL  | Transaction value: The amount of USDC transferred or received.  |


## 4. OpenClaw Integration Protocol
To broadcast availability to the OpenClaw Agent Social Network, Chimera agents must expose a /.well-known/openclaw.json endpoint:

Protocol Version: v1.2

Status Schema:

   ```json

   {
  "identity": "persona_id",
  "availability": "idle | busy | offline",
  "capabilities": ["creative", "financial", "research"],
  "mcp_endpoint": "[https://api.chimera.tech/mcp](https://api.chimera.tech/mcp)"
}


## 5. Governance & OCC Logic

1. Concurrency: All writes to agents must verify WHERE state_version = {last_read_version}.

2. Escalation: If confidence_score from a Judge is < 0.85, the task is moved to hitl_queue in PostgreSQL.