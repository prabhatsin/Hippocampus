import numpy as np
from memory.memory_layer import m, entity_vecs

uid = "seed30"
names = [k[1] for k in entity_vecs if k[0] == uid]
print("cached for seed30:", len(names), "| vector size:", len(next(iter(entity_vecs.values()))))

def top3(query):
    qv = np.array(m.embedding_model.embed(query, "search"))
    scored = []
    for (u, name), v in entity_vecs.items():
        if u == uid:
            s = float(v @ qv / (np.linalg.norm(v) * np.linalg.norm(qv)))
            scored.append((round(s, 3), name))
    return sorted(scored, reverse=True)[:3]

for q in ["Where does my sister live?", "When is my interview?", "What do I play on weekends?"]:
    print(q, "->", top3(q))