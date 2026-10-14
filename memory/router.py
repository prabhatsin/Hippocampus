import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client()

SCHEMAS = ["work", "health", "people", "daily_life", "goals", "knowledge"]


PROMPT = """Extract the key entities from this memory about a user.
For each entity, pick ONE schema from: {schemas}.
Return JSON only: [{{"entity": "...", "schema": "..."}}]
Use short, canonical names (e.g. "Bob", not "my manager Bob").

Memory: {memory}"""


def extract_entities(memory_text):
    resp = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=PROMPT.format(schemas=SCHEMAS, memory=memory_text),
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            thinking_config=types.ThinkingConfig(thinking_level="low"),
            temperature=0
            ),
    )
    return json.loads(resp.text)
