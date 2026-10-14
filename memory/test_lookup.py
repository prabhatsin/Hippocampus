from memory.routing_table import RoutingTable

t = RoutingTable()
for q in [
    "Who is Bob?",
    "How are my meetings going?",
    "Do I play badminton?",
    "What should I eat tonight?",
    "Tell me about my boss",
]:
    print(q, "->", t.lookup("hook_test", q))


