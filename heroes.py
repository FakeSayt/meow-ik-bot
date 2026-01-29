# Skrócone imiona + pełna nazwa + tier
HERO_INFO = {
    "wukong": {"short": "wk", "tier": "🐳"},
    "louis ix": {"short": "lx", "tier": "❄️"},
    "tutankhamun": {"short": "tut", "tier": "💰"},
    "khubilai khan": {"short": "khan", "tier": "💰"},
    "himiko": {"short": "him", "tier": "💰"},
    "merlin": {"short": "mer", "tier": "💵"},
    # ... dodaj resztę
}

# TL;DR builds
HERO_BUILDS = {
    "wukong": "⭐ Best Artifact: Unknown\n⚔️ Best Main Stat: Unknown\n⚡ Best Passive Roll: Unknown\n🔁 Alternative Passive: Unknown",
    "louis ix": "⭐ Best Artifact: Unknown\n⚔️ Best Main Stat: Unknown\n⚡ Best Passive Roll: Unknown\n🔁 Alternative Passive: Unknown",
    "himiko": "⭐ Best Artifact: Unknown\n⚔️ Best Main Stat: Unknown\n⚡ Best Passive Roll: Unknown\n🔁 Alternative Passive: Unknown",
    "merlin": "⭐ Best Artifact: Unknown\n⚔️ Best Main Stat: Unknown\n⚡ Best Passive Roll: Unknown\n🔁 Alternative Passive: Unknown",
    # ... reszta
}

HERO_PRICE = {name: info["tier"] for name, info in HERO_INFO.items()}
