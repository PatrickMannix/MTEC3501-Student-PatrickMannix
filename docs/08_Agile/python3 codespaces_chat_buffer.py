import asyncio
import os
import time
from typing import Dict, List


class ChatBufferSystem:
    def __init__(self, priority_queue: asyncio.PriorityQueue, flush_interval: float = 5.0):
        self.priority_queue = priority_queue
        self.flush_interval = flush_interval
        self.buffer: List[Dict[str, str]] = []
        self._lock = asyncio.Lock()
        self._running = False

    async def ingest_chat(self, username: str, message: str) -> None:
        async with self._lock:
            self.buffer.append({
                "user": username,
                "text": message,
                "timestamp": time.time()
            })

    async def ingest_subscription(self, username: str, tier: str, custom_prompt: str = "") -> None:
        event_payload = {
            "type": "SUBSCRIPTION",
            "user": username,
            "tier": tier,
            "prompt": custom_prompt
        }
        await self.priority_queue.put((0, time.time(), event_payload))

    def _format_summary_block(self, messages: List[Dict[str, str]]) -> str:
        formatted_lines = [f"- {msg['user']}: {msg['text']}" for msg in messages]
        joined_chat = "\n".join(formatted_lines)
        return (
            f"[CHAT BATCH SUMMARY - {len(messages)} messages over {self.flush_interval}s]\n"
            f"Summarize the general vibe and reply to notable points below:\n"
            f"{joined_chat}"
        )

    async def _flush_loop(self) -> None:
        while self._running:
            await asyncio.sleep(self.flush_interval)

            async with self._lock:
                if not self.buffer:
                    continue
                batch_to_process = list(self.buffer)
                self.buffer.clear()

            summary_prompt = self._format_summary_block(batch_to_process)
            payload = {
                "type": "CHAT_BATCH",
                "message_count": len(batch_to_process),
                "prompt": summary_prompt
            }
            await self.priority_queue.put((10, time.time(), payload))

    async def start(self) -> None:
        self._running = True
        asyncio.create_task(self._flush_loop())

    def stop(self) -> None:
        self._running = False


async def mock_llm_worker(queue: asyncio.PriorityQueue) -> None:
    while True:
        priority, timestamp, payload = await queue.get()
        print(f"\n[LLM PROCESSING | Priority {priority} | Type: {payload['type']}]")
        print(payload["prompt"])
        await asyncio.sleep(0.8)
        queue.task_done()


async def main() -> None:
    codespace_name = os.getenv("CODESPACE_NAME", "local-dev")
    flush_seconds = float(os.getenv("CHAT_FLUSH_INTERVAL", "5.0"))
    print(f"Running in environment: {codespace_name} | Flush interval: {flush_seconds}s")

    main_queue = asyncio.PriorityQueue()
    buffer_system = ChatBufferSystem(priority_queue=main_queue, flush_interval=flush_seconds)

    await buffer_system.start()
    worker_task = asyncio.create_task(mock_llm_worker(main_queue))

    print("--- Starting 7-second high-frequency chat simulation ---")
    for i in range(1, 22):
        await buffer_system.ingest_chat(f"Viewer_{i}", f"Hype message #{i}!")

        if i == 12:
            print(">>> [WEBHOOK] SuperFan99 just subscribed! Bypassing buffer...")
            await buffer_system.ingest_subscription("SuperFan99", "Tier 1", "Say hi to the stream!")

        await asyncio.sleep(0.3)

    await asyncio.sleep(2)
    buffer_system.stop()
    worker_task.cancel()


if __name__ == "__main__":
    asyncio.run(main())