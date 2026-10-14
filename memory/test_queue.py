import time
from memory.memory_layer import save_turn, flush, table

uid = "queue_test_3"
t = time.time()
save_turn(uid, "My sister Priya lives in Pune", "Noted.")
save_turn(uid, "I work as a backend developer", "Noted.")
save_turn(uid, "I play cricket on Sundays", "Noted.")
print(f"3 saves queued in {(time.time() - t) * 1000:.0f} ms")

flush()
print(f"all saved after {time.time() - t:.0f} s")
print(table.data.get(uid))