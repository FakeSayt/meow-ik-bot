import traceback
from openai import OpenAI
import config

client = OpenAI(api_key=config.OPENAI_API_KEY)

def ai_fill_unknowns(hero_name: str, build_text: str):
    if "Unknown" not in build_text:
        return build_text

    prompt = f"""
Infinity Kingdom. Only use actual in-game data.
Hero: "{hero_name}"
Current TL;DR build:

{build_text}

Fill all Unknown fields accurately (Best Artifact, Main Stat, Passive, Alternative Passive). 
Do NOT invent artifacts. If unknown, leave as 'Unknown'.
Respond ONLY with the updated TL;DR build in the same format.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=300
        )
        content = response.choices[0].message.content.strip()
        return content if content else build_text
    except Exception as e:
        print("[ERROR] AI failed to fill unknowns:", repr(e))
        traceback.print_exc()
        return build_text
