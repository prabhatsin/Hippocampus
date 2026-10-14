# import time
# from memory.memory_layer import get_memories, get_memories_routed, table

# uid = "seed30"
# tests = [
#     ("Who is Bob?", ["bob"]),
#     ("Where does my sister live?", ["pune"]),
#     ("What do I play on weekends?", ["badminton", "cricket"]),
#     ("Am I allergic to anything?", ["peanut"]),
#     ("When is my interview?", ["zeta", "friday"]),
#     ("What does Rohan do?", ["google"]),
#     ("What should I eat tonight?", ["vegetarian"]),
#     ("What tech stack does my team use?", ["postgresql", "fastapi"]),
#     ("Who is leading the migration?", ["neha"]),
#     ("What time do I wake up?", ["5:30"]),
#     ("Do I have any appointments coming up?", ["dentist"]),
#     ("Tell me about my trip plans", ["goa"]),
# ]

# full_hits = routed_hits = 0
# for q, kws in tests:
#     matched, pool = table.lookup(uid, q)

#     t = time.time(); full = get_memories(uid, q); tf = (time.time() - t) * 1000
#     t = time.time(); routed = get_memories_routed(uid, q, fill=False); tr = (time.time() - t) * 1000

#     fh = any(k in full.lower() for k in kws)
#     rh = any(k in routed.lower() for k in kws)
#     full_hits += fh; routed_hits += rh
#     print(f"\n>> {q}\n   matched={matched} pool={len(pool)}")
#     print(f"   FULL   hit={fh} {tf:.0f} ms | ROUTED hit={rh} {tr:.0f} ms")

# print(f"\nFULL: {full_hits}/{len(tests)}   ROUTED: {routed_hits}/{len(tests)}")

from memory.memory_layer import table
print(sorted(table.data["seed30"]["entities"].keys()))

