# import time
# from memory_layer import get_memories, save_turn
# from agent_core.main_loop import get_agent_reply
# uid = "prabhat"

# print(get_memories(uid, "What should I eat?"))

# save_turn(uid, "I love playing chess on weekends", "Nice, chess is a great hobby!")
# time.sleep(15)   # wait so the background thread finishes before the script exits

# print(get_memories(uid, "What are my hobbies?"))


# if __name__ == "__main__":
#     messages=[]
#     while True:
#         input_msg=input("user prompt:")
#         response=get_agent_reply(input_msg,messages,user_id="Akku")
#         print(response)

#         if input_msg=="exit":
#             break


import time
from memory.memory_layer import get_memories, save_turn

uid = "l2_test"

# seed (uses Gemini for fact extraction, so it takes a few seconds)
for msg in ["I have an interview on Friday", "I'm vegetarian",
            "My manager Bob schedules too many meetings",
            "I'm preparing for agentic AI roles"]:
    save_turn(uid, msg, "Noted.")
time.sleep(40)

queries = [
    "Who is Bob?",                          # 1
    "What should I eat before my big day?", # 2
    "What am I preparing for?",             # 3
    "Tell me about my work",                # 4
]
for q in queries:
    print("Q:", q)
    print(get_memories(uid, q), "\n")

# 5: search while a save is running
save_turn(uid, "I love playing badminton", "Nice!")
print("Q: What do I love? (during a background save)")
print(get_memories(uid, "What do I love?"))
time.sleep(20)

