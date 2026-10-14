import os
import time
import threading
from dotenv import load_dotenv
import numpy as np
import queue 


load_dotenv()

import atexit
from mem0 import Memory
from memory.router import extract_entities
from memory.routing_table import RoutingTable

table = RoutingTable()


config = {
    "llm": {
        "provider": "gemini",
        "config": {"model": "gemini-3.8-flash", "temperature": 0.1},
    },
    "embedder": {
        "provider": "fastembed",
        "config": {"model": "BAAI/bge-small-en-v1.5", "embedding_dims": 384},
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "collection_name": "voicemem",
            "path": "./qdrant_db",
            "embedding_model_dims": 384,
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
    t0 = time.time()
    messages = [
        {"role": "user", "content": user_msg},
        {"role": "assistant", "content": assistant_msg},
    ]
    result = m.add(messages, user_id=user_id)
    t1 = time.time()
    print(f"[save] mem0.add took {t1 - t0:.1f} s")

    for item in result.get("results", []):
        if item.get("event") in ("ADD", "UPDATE"):
            try:
                entities = extract_entities(item["memory"])
                table.add(user_id, item["id"], entities)
            except Exception as e:
                print(f"[router] tagging failed: {e}")
    print(f"[save] tagging took {time.time() - t1:.1f} s")




_q = queue.Queue()

def _worker():
    while True:
        item = _q.get()
        try:
            for attempt in range(2):          # one retry on failure
                try:
                    _save(*item)
                    break
                except Exception as e:
                    print(f"[save] attempt {attempt + 1} failed: {e}")
        finally:
            _q.task_done()

threading.Thread(target=_worker, daemon=True).start()

def save_turn(user_id, user_msg, assistant_msg):
    _q.put((user_id, user_msg, assistant_msg))   # returns instantly

def flush():
    _q.join()                                    # wait until all saves finish

# def save_turn(user_id, user_msg, assistant_msg):
#     t = threading.Thread(target=_save, args=(user_id, user_msg, assistant_msg))
#     t.start()
def warmup():
    '''
    The first m.search() call has a one-time load cost (about 5 s here), probably from loading 
    the keyword model, and warmup() pays it at startup so the users first question isnt hit 
    by it. Without it, the first reply in a voice call would have 5 seconds of dead air.
    '''
    start = time.time()
    m.search("warmup", filters={"user_id": "__warmup__"}, limit=1)
    m.embedding_model.embed("warmup", "search")
    print(f"[memory] warmup done in {(time.time() - start):.1f} s")

warmup()

def _close():
    try:
        m.vector_store.client.close()
    except Exception:
        pass

atexit.register(_close)



def get_memories_routed(user_id, query, k=5, fill=True):
    start = time.time()
    matched, pool_ids = table.lookup(user_id, query)

    if not pool_ids:
        print("[router] no match -> full search")
        return get_memories(user_id, query, k)

    qv = np.array(m.embedding_model.embed(query, "search"))
    pts = m.vector_store.client.retrieve(
        collection_name=m.vector_store.collection_name,
        ids=pool_ids, with_vectors=True,
    )
    scored = []
    for p in pts:
        v = np.array(p.vector[""])
        s = float(v @ qv / (np.linalg.norm(v) * np.linalg.norm(qv)))
        scored.append((s, p.payload.get("data")))
    scored.sort(reverse=True)
    texts = [t for _, t in scored[:k]]

    if fill and len(texts) < k:
        res = m.search(query, filters={"user_id": user_id}, limit=k)
        for r in res["results"]:
            if len(texts) >= k:
                break
            if r["memory"] not in texts:
                texts.append(r["memory"])

    ms = (time.time() - start) * 1000
    print(f"[router] matched={matched} pool={len(pool_ids)} took {ms:.0f} ms")
    return "Known about user:\n" + "\n".join(f"- {t}" for t in texts)


