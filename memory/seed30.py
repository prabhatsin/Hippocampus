from memory.memory_layer import m, save_turn, flush, table

uid = "seed30"
facts = [
    "My manager Bob schedules too many meetings",
    "My sister Priya lives in Pune",
    "My friend Rohan works at Google in Bangalore",
    "My brother Karan is preparing for the UPSC exam",
    "I'm vegetarian",
    "I'm allergic to peanuts",
    "I play badminton on Saturdays",
    "I play cricket on Sundays",
    "I go running every morning at 6 am",
    "I work as a Python backend developer",
    "My team uses PostgreSQL and FastAPI",
    "I have an interview on Friday at 11 am with a startup called Zeta",
    "I'm preparing for agentic AI engineer roles",
    "I want to build a voice AI agent project",
    "I'm learning about memory systems for AI agents",
    "I drink black coffee with no sugar",
    "I live in Noida",
    "My dentist appointment is next Tuesday at 4 pm",
    "My laptop is a ThinkPad running Ubuntu",
    "I wake up at 5:30 am",
    "My mother Sunita calls me every evening",
    "I'm saving money to buy a motorcycle",
    "I love watching Formula 1 races",
    "I read science fiction novels before bed",
    "My colleague Neha is leading the migration project",
    "I dislike Monday standup meetings",
    "I do yoga on Wednesdays",
    "My favorite cuisine is South Indian food",
    "I want to switch to a remote job",
    "I'm planning a trip to Goa in December",
]

for f in facts:
    save_turn(uid, f, "Noted.")
flush()

stored = m.get_all(filters={"user_id": uid})["results"]
ids_in_table = {i for e in table.data[uid]["entities"].values() for i in e["mem_ids"]}
print("memories in Mem0:", len(stored))
print("memories tagged in router table:", len(ids_in_table))
print("entities:", len(table.data[uid]["entities"]))


