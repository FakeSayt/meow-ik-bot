from openai import OpenAI
import traceback
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def ai_fill_unknowns(hero_name: str, build_text: str):
    if "Unknown" not in build_text:
        return build_text

    prompt = f"""
You are an expert in Infinity Kingdom. Hero: "{hero_name}".
Here is the current TL;DR build:

{build_text}

Fill in the Unknown fields accurately using in-game data.
Respond only with the updated TL;DR build in the same format.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=200
        )
        content = response.choices[0].message.content.strip()
        return content if content else build_text
    except Exception as e:
        print("[ERROR] AI failed:", repr(e))
        traceback.print_exc()
        return build_text
