import os
import json

PREFIX_FILE = "prefixes.json"
prefixes = {}

def load_prefixes():
    global prefixes

    if not os.path.exists(PREFIX_FILE):
        with open(PREFIX_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)

    with open(PREFIX_FILE, "r", encoding="utf-8") as f:
        prefixes = json.load(f)

def save_prefixes():
    with open(PREFIX_FILE, "w", encoding="utf-8") as f:
        json.dump(prefixes, f, indent=4)

def set_prefix(guild_id, value):
    prefixes[str(guild_id)] = value
    save_prefixes()

def get_prefix(bot, message):
    if not message.guild:
        return "?"
    return prefixes.get(str(message.guild.id), "?")