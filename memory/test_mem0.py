import os
from dotenv import load_dotenv
from mem0 import Memory

load_dotenv()
os.environ.setdefault("GOOGLE_API_KEY", os.getenv("GEMINI_API_KEY", ""))

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
uid = "prabhat"

m.add("I have an interview on Friday", user_id=uid)
m.add("I'm vegetarian", user_id=uid)
m.add("My manager Bob schedules too many meetings", user_id=uid)
m.add("I'm preparing for agentic AI roles", user_id=uid)

# query="Who is Bob?"
# query="What am I preparing for?"
query="Tell me about my work"

res = m.search(query, filters={"user_id": uid}, limit=5)
for r in res["results"]:
    print(r["memory"], "|", r["score"])