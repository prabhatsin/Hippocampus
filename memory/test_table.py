
from memory.routing_table import RoutingTable
from memory.router import extract_entities

t = RoutingTable()
mem_id = "ac63dcbb-test"
text = "User plays badminton regularly on Saturdays"

t.add("router_test_2", mem_id, extract_entities(text))
print(t.data)