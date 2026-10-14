
# from memory.router import extract_entities

# for m in [
#     "User has a manager named Bob who schedules too many meetings",
#     "User follows a vegetarian diet",
#     "User has an interview scheduled for Friday, October 16, 2026",
#     "User loves playing badminton",
#     "User is preparing for agentic AI roles",
# ]:
#     print(m, "->", extract_entities(m))


from memory.memory_layer import m
# r = m.add("I play chess on Sundays", user_id="router_test")
# print(r)

r = m.add("I play badminton on Saturdays", user_id="router_test_2")
print(r)



#! Note : remember that spacy warning  in the terminal output :

'''

Solution:
pip install "mem0ai[nlp]"
python -m spacy download en_core_web_sm

This installs spaCy and its English model. Mem0 uses it for lemmatization and entity handling 
in hybrid search. It adds some install size and a little import time. If you dont care, 
ignoring the message is also fine.

'''


'''
3. The Qdrant ImportError ... shutting down

This one is a cosmetic error at exit. Qdrant’s local mode tries to close while Python is already tearing down. It does not affect your data. Two options:

Ignore it. It's only noise.
Close it cleanly: at the end of a script, call m.vector_store.client.close() before exiting. Note that this attribute path depends on your Mem0 version, so if it errors, skip it.

The best long-term fix is moving from local-file Qdrant to a Qdrant server (Docker), but that is not needed now.

'''
