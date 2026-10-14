from memory.memory_layer import m, table

uid = "seed30"
ids_table = {i for e in table.data[uid]["entities"].values() for i in e["mem_ids"]}

# independent of get_all: ask Qdrant which of the table's IDs really exist
pts = m.vector_store.client.retrieve(
    collection_name=m.vector_store.collection_name, ids=list(ids_table)
)
print("IDs in table:", len(ids_table))
print("IDs that exist in Qdrant:", len(pts))

# does get_all have a cap?
try:
    r = m.get_all(filters={"user_id": uid}, top_k=100)
except TypeError:
    r = m.get_all(filters={"user_id": uid}, limit=100)
print("get_all with a bigger limit:", len(r["results"]))