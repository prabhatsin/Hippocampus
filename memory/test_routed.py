from memory.memory_layer import get_memories_routed

uid = "hook_test"
for q in ["Who is Bob?", "What should I eat tonight?", "What should I eat tonight?"]:
    print("Q:", q)
    print(get_memories_routed(uid, q, fill=False), "\n")