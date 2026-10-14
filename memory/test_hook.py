# import time
# from memory.memory_layer import save_turn, table

# uid = "hook_test"
# save_turn(uid, "My manager Bob schedules too many meetings", "Noted.")
# save_turn(uid, "I'm vegetarian and I play badminton on weekends", "Nice!")
# time.sleep(30)
# print(table.data.get(uid))

from memory.memory_layer import m
print(m.get_all(filters={"user_id": "hook_test"}))



#? Issues in the step 3.3 :

'''
Step 3.3 issue

Problem: After saving two messages, the routing table was missing the badminton entry when the 
test printed it. Mem0 had stored the memory, and the entry appeared later, so the print simply 
ran before that background save finished. Each save runs in its own thread and makes several 
slow Gemini calls (extract, then tag), so a fixed sleep(30) is a guess. The same problem can
lose a save if the program exits too early.

Solution: Replace the thread-per-save with one background worker and a queue. save_turn only 
drops the turn into the queue, and the worker saves one at a time, in order. Add a flush() 
that waits until the queue is empty, and call it before printing or exiting, instead of sleep().
This is the parked TODO, and it is now a real problem rather than a theory.

Related safeguard: If tagging fails (for example a MALFORMED_RESPONSE), that memory is saved in
Mem0 but missing from the table. So in Step 3.4, if routing finds nothing, fall back to searching 
the full store.

'''