import asyncio
# NOTE: Email notifications use `dry_run=True` by default for safety.
import os
from skills.skill_trend_fetcher.logic import TrendFetcher
from skills.skill_email_sender import EmailSender
from skills import db_adapter
# Import your other skills here (e.g., MediaGenerator, PostScheduler)

class ChimeraOrchestrator:
    def __init__(self):
        self.name = "Chimera Lead Orchestrator"
        self.version = "2026.1.0"
        self.is_running = True

    async def planner_step(self):
        print("🔍 [PLANNER] Scanning MCP Resources for trends...")
        # Added the 'niche' argument required by your specific logic.py
        fetcher = TrendFetcher(niche="AI and Web3") 
        try:
            trends = await fetcher.fetch_trends()
            # If fetch_trends returns a list of objects, we extract the text
            return trends[:3] 
        except Exception as e:
            print(f"⚠️ [PLANNER ERROR] Could not fetch trends: {e}")
            return ["No recent trends found"] # Fallback to keep the loop moving
        
    async def worker_step(self, task):
        print(f"⚙️ [WORKER] Executing task: {task}")
        # Logic to call your specific skills
        result = f"Draft content for: {task}"
        return {"content": result, "confidence": 0.95}

    async def judge_step(self, result):
        print(f"⚖️ [JUDGE] Auditing result (Confidence: {result['confidence']})")
        # SRS NFR 1.1: Confidence Logic
        if result['confidence'] > 0.90:
            print("✅ [JUDGE] Approved for autonomous publishing.")
            return True
        else:
            print("❌ [JUDGE] Rejected. Escalating to HITL Queue.")
            try:
                # Push to HITL queue (DB adapter stub)
                db_adapter.push_hitl(result)
            except Exception as e:
                print(f"⚠️ [JUDGE] Failed to push to HITL queue: {e}")
            return False

    async def run_swarm_loop(self):
        print(f"🚀 Project Chimera Online | {self.version}")
        while self.is_running:
            # 1. PLAN
            tasks = await self.planner_step()

            # Keep track of published items this loop to send a single summary email
            published_items = []

            # 2. WORK & JUDGE
            for task in tasks:
                worker_output = await self.worker_step(task)
                approved = await self.judge_step(worker_output)

                if approved:
                    print(f"📡 [POSTING] Content live: {worker_output['content']}")
                    published_items.append(worker_output['content'])

            # 3. NOTIFY (batch, dry-run by default)
            try:
                email_notify_to = os.getenv("EMAIL_NOTIFY_TO", "you@example.com")
                email_dry_run = os.getenv("EMAIL_DRY_RUN", "true").lower() != "false"
                if published_items:
                    sender = EmailSender()
                    subject = f"Chimera Digest: {len(published_items)} published items"
                    body_lines = ["Published items:"] + [f"- {p}" for p in published_items]
                    body = "\n".join(body_lines)
                    notify_res = sender.send(subject=subject, body=body, to=[email_notify_to], dry_run=email_dry_run)
                    print(f"✉️ [NOTIFY] Summary send result: {notify_res}")
            except Exception as e:
                print(f"⚠️ [NOTIFY ERROR] Failed to send summary: {e}")
            
            print("😴 [SLEEP] Loop complete. Resting for 60 seconds...")
            await asyncio.sleep(60)
            # self.is_running = False # Uncomment for a single-run demo

if __name__ == "__main__":
    orchestrator = ChimeraOrchestrator()
    try:
        asyncio.run(orchestrator.run_swarm_loop())
    except KeyboardInterrupt:
        print("\n🛑 Orchestrator shut down gracefully.")