from memory.memory_layer import m, table

ids = table.lookup("hook_test", "Who is Bob?")[1]
client = m.vector_store.client
coll = m.vector_store.collection_name

pts = client.retrieve(collection_name=coll, ids=ids, with_vectors=True)
# for p in pts:
#     print(p.id, p.payload.get("data"), len(p.vector))

for p in pts:
    v = p.vector
    print(type(v))
    if isinstance(v, dict):
        for k, val in v.items():
            print("key:", repr(k), type(val), getattr(val, "__len__", lambda: "n/a")())

q = m.embedding_model.embed("Who is Bob?", "search")
print("query vector length:", len(q))