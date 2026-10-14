
#! Why  a different memory needed only ??

'''
The key difference from text agents is latency. A voice turn has roughly 500-800 ms for STT, LLM and TTS combined, so there’s no room for slow memory lookups mid-turn. So real systems:

#? prefetch profile and history at call start
#? write memory asynchronously after the call
#? keep mid-call retrieval rare and fast
'''


# Ranked by how much they matter in production voice systems:

'''

1.Call state (slots/dialogue state). Structured fields like name, order items, appointment time, 
current step. This is the most important one, because voice has no screen, so the agent must 
never lose or re-ask these. Its usually a JSON object, not free text.

2.Rolling transcript buffer. The last N turns, plus a running summary once the call gets long. 
This is your STM.

3.Caller profile. Facts keyed by phone number or user ID: name, language, preferences, account 
info. Its loaded before the greeting so the agent can say “Hi Prabhat” immediately.

4.Past call summaries. A short summary and outcome of each earlier call, plus open issues.
This is episodic LTM, and its written after hangup, not during the call.

5.Knowledge base (RAG). Company FAQs and policies, retrieved only when the question needs them.

'''






'''
#? Layer 1: Basic memory (get this working first)
Use Mem0 as the backend.
After each turn, save facts in the background (never block the reply).
Before each reply, fetch top-5 memories and inject them into the LLM prompt.

#?Layer 2: Prefetch inside silence
Run retrieval on the partial transcript while the user is still talking or pausing.
Don' wait for the final transcript. Cache the result and use it when the reply starts.
This alone gives you the main latency win.

#?Layer 3: Schema/entity routing
Keep a small table: schema → entities → Mem0 memory IDs.
Use the LLM (or cheap NER) to tag each new memory with its schema and entity.
At query time, find matching entities and schemas, collect their memory IDs, and search only those.
Start with 5-6 fixed schemas (work, health, people, daily_life, goals, knowledge). Skip emergence until later.

#?Layer 4: Right brain (emotion)
Tag each user utterance with an emotion label. Start from the transcript, and add a speech-emotion model later if you want tone.
Store two kinds of notes: general traits, and emotion linked to an entity (“stressed about the interview”).
At session end, run one LLM pass to consolidate repeated patterns into stable traits.
At retrieval, add the matching persona notes to the prompt.

#?Layer 5: Later extras
Cluster emergence, voiceprint speaker ID, audio memory.


#?. Practical advice
Do Layer 1 + 2 first. That alone gives you a working, fast voice memory.
Measure latency at every layer. Retrieval must stay under about 150-200 ms.
Keep the memory layer decoupled, as the paper does, so you can swap the backend later.
Keep injected memory short (about 5 items) so the LLM stays fast.

'''

#! Doubt / Question ?? 
#! Is Mem0 the base in the paper VoiceMem ??
'''
Yes. VoiceMem sits on top of Mem0.

=>Section 4.2: the paper says Mem0 is the lower-layer backend because of its generality and 
strong performance.
=>Design: VoiceMem only manages routing, the dual brain and streaming on top. The MemSearch 
call in their equations is whatever backend you plug in.
=>Table 4: they also tried LangMem and Zep as backends. The index helped all three.
=>Mem0 on LoCoMo: 61.68 alone, 91.20 with VoiceMems index on top.

'''