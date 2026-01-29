import asyncio
from heroes import HERO_BUILDS
from ai_helper import ai_fill_unknowns

def get_hero_build(name: str):
    name_lower = name.lower()
    build = HERO_BUILDS.get(name_lower)
    if not build:
        return f"""✨ TL;DR – Best Artifact for {name.title()}
⭐ Best Artifact: Unknown
⚔️ Best Main Stat: Unknown
⚡ Best Passive Roll: Unknown
🔁 Alternative Passive: Unknown"""
    
    build_filled = asyncio.run(asyncio.to_thread(ai_fill_unknowns, name, build))
    return build_filled
