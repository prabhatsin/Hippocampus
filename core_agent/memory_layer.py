import os
import time
import threading
from dotenv import load_dotenv
from mem0 import Memory

load_dotenv()

config = {
    "llm": {
        "provider": "gemini",
        "config": {"model": "gemini-3.8-flash", "temperature": 0.1},
    },
    "embedder": {
        "provider": "gemini",
        "config": {"model": "gemini-embedding-001", "embedding_dims": 768},
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "collection_name": "voicemem",
            "path": "./qdrant_db",
            "embedding_model_dims": 768,
        },
    },
}

m = Memory.from_config(config)


def get_memories(user_id, query, k=5):
    start = time.time()
    res = m.search(query, filters={"user_id": user_id}, limit=k)
    ms = (time.time() - start) * 1000
    print(f"[memory] retrieval took {ms:.0f} ms")

    if not res["results"]:
        return ""
    lines = [f"- {r['memory']}" for r in res["results"]]
    return "Known about user:\n" + "\n".join(lines)


def _save(user_id, user_msg, assistant_msg):
    messages = [
        {"role": "user", "content": user_msg},
        {"role": "assistant", "content": assistant_msg},
    ]
    m.add(messages, user_id=user_id)


def save_turn(user_id, user_msg, assistant_msg):
    t = threading.Thread(target=_save, args=(user_id, user_msg, assistant_msg))
    t.start()