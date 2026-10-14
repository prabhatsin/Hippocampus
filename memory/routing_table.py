
import json
import os

PATH = "router_db.json"


class RoutingTable:
    def __init__(self):
        # {user_id: {"entities": {name: {"schema": s, "mem_ids": [..]}}}}
        self.data = {}
        self.load()

    def add(self, user_id, memory_id, entities):
        u = self.data.setdefault(user_id, {"entities": {}})
        for e in entities:
            name = e["entity"].strip().lower()
            e_rec = u["entities"].setdefault(
                name, {"schema": e["schema"], "mem_ids": []}
            )
            if memory_id not in e_rec["mem_ids"]:
                e_rec["mem_ids"].append(memory_id)
        self.save()

    def save(self):
        with open(PATH, "w") as f:
            json.dump(self.data, f, indent=2)

    def load(self):
        if os.path.exists(PATH):
            with open(PATH) as f:
                self.data = json.load(f)

    def lookup(self, user_id, query):
        ents = self.data.get(user_id, {}).get("entities", {})
        q = query.lower()
        matched = [name for name in ents if name in q]
        schemas = {ents[n]["schema"] for n in matched}

        pool_names = set(matched) | {
            n for n, rec in ents.items() if rec["schema"] in schemas
        }
        pool_ids = {i for n in pool_names for i in ents[n]["mem_ids"]}
        return matched, list(pool_ids)


'''
Design notes:
Names are lowercased and stripped, so “Badminton” and “badminton” become one entity.
Each entity keeps its schema, so we can later find all entities in the same schema.
It is stored per user_id, so users stay isolated like in Mem0.
lookup comes in Step 3.4, once we know the tags are being stored prop

'''