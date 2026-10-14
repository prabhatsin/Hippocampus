# import time
# from memory_layer import get_memories, save_turn
from agent_core.main_loop import get_agent_reply
# uid = "prabhat"

# print(get_memories(uid, "What should I eat?"))

# save_turn(uid, "I love playing chess on weekends", "Nice, chess is a great hobby!")
# time.sleep(15)   # wait so the background thread finishes before the script exits

# print(get_memories(uid, "What are my hobbies?"))


if __name__ == "__main__":
    messages=[]
    while True:
        input_msg=input("user prompt:")
        response=get_agent_reply(input_msg,messages,user_id="Akku")
        print(response)

        if input_msg=="exit":
            break

