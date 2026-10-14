 #TODO: after compleeting the agent loop , learn how to make it model/ llm agnostic
from google import genai
from google.genai import types
from dotenv import load_dotenv
from agent_core.tool_schema import (check_availability_function, book_slot_function,cancel_booking_function,
    reschedule_function)
from agent_core.tool_registry import tool_registry
from agent_core.system_prompt import SYSTEM_PROMPT
from core_agent.memory_layer import get_memories, save_turn
load_dotenv()

client=genai.Client()
booking_tool = types.Tool(function_declarations=[
    check_availability_function,
    book_slot_function,
    cancel_booking_function,
    reschedule_function,
])
tools = [booking_tool]
def get_agent_reply(input_msg:str,messages:list,user_id: str = "prabhat")-> str:
    messages.append(
        types.Content(role="user",parts=[types.Part.from_text(text=input_msg)])
    )
    memory_block=get_memories(user_id,input_msg)
    system_prompt= SYSTEM_PROMPT + "\n\n" + memory_block
    while True:
        response=client.models.generate_content(
            model="gemini-3.8-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                automatic_function_calling=types.AutomaticFunctionCallingConfig(
                    disable=True
                ),
                tools=tools,
                system_instruction=system_prompt,
                thinking_config=types.ThinkingConfig(thinking_level='low')
            )
        )
        parts=response.candidates[0].content.parts
        tool_call=None
        for part in parts:
            if part.function_call:
                tool_call=part.function_call
                #! This break statement takes out of the above for loop not the main while loop
                break
        if tool_call: # check if tool call present in the response
            #step1:# 1. Append Gemini's model response containing the function call
            messages.append(response.candidates[0].content)
            # step2:Execute the actual Python function
            tool_name=tool_registry[tool_call.name]
            result=tool_name(**tool_call.args)
            # Step3: Append the functions result
            tool_response = types.Content(
                role="user",
                parts=[types.Part.from_function_response( name=tool_call.name,response={"result": result})]
            )
            messages.append(tool_response)
            # Continue AGENT LOOP
            continue
        else:
            # Append final model response
            messages.append(response.candidates[0].content)
            # Agent is finished
            save_turn (user_id,input_msg,response.text)
            return response.text


#? Question : Why its  placed this way ??

'''

1.Memories are fetched once per user message, not on every pass of the while True. Tool-call rounds 
would otherwise repeat the slow retrieval.
2.Memories go in the system prompt, not in messages, so the chat history stays clean and memory 
facts don't pile up turn after turn.
3.save_turn is only called on the final reply, and it runs in a background thread, so it adds 
nothing to reply time.

'''




if __name__ == "__main__":
    messages=[]
    while True:
        input_msg=input("user prompt:")
        response=get_agent_reply(input_msg,messages)
        print(response)

        if input_msg=="exit":
            break