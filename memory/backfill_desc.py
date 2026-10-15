from memory.memory_layer import m, table

coll = m.vector_store.collection_name
client = m.vector_store.client

for uid, u in table.data.items():
    for name, rec in u["entities"].items():
        if rec.get("desc"):
            continue
        pts = client.retrieve(collection_name=coll, ids=rec["mem_ids"][:1])
        if pts:
            rec["desc"] = f"{name}: {pts[0].payload.get('data')}"
table.save()

for name in ["priya", "job interview", "peanut allergy", "saturdays"]:
    print(table.data["seed30"]["entities"][name]["desc"])