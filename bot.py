import discord 
from discord.ext import commands
from discord import app_commands
import json
import random
import sqlite3
from datetime import datetime, timedelta
import os
from pathlib import Path


COOLDOWN_MINUTE = 10
DATA_FOLDER = "data"
IMAGES_FOLDER = "images"
CONFIG_FILE = "characters.json"


os.makedirs(DATA_FOLDER, exist_ok=True)
os.makedirs(IMAGES_FOLDER, exist_ok=True)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


def init_db(): 
    conn = sqlite3.connect(f"{DATA_FOLDER}/mudae_bot.db")
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS claims
                (user_id INTEGER, character_name TEXT, claimed_at TIMESTAMP)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS cooldowns (user_id INTEGER PRIMARY KEY, last_roll TIMESTAMP)''')

    c.execute('''CREATE TABLE IF NOT EXISTS kakera (user_id INTEGER PRIMARY KEY, amount INTEGER DEFAULT 0)''')

    c.execute('''CREATE TABLE IF NOT EXISTS wishes (user_id INTEGER, character_name TEXT)''')

    conn.commit()
    conn.close()

#pour charger les perso depuis le json
def load_characters():
    if not os.path.exists(CONFIG_FILE):
        default_config = {
            "characters": [
            {"name" : "Cyril", "image": "apagnan.pgn", "rarity" : "rare"},
            ]
        }
        with open(CONFIG_FILE, 'r', encoding="utf-8") as f:
            json.dump(default_config, f, indent=4, ensure_ascii=False)
    
    with open(CONFIG_FILE, 'r', encoding="utf-8") as f:
        return json.load(f)['character']

# le random influencé par la rareté
def get_random_character():
    characters = load_characters()

    rarity_weights = {
        'commun': 50,
        'rare': 30,
        'epique': 15,
        'legendaire': 5
    }

    weighted_chars = []
    for char in characters: 
        rarity = char.get('rarity', 'commun').lower()
        weight = rarity_weights.get(rarity, 50)
        weighted_chars.extend([char] * weight)
    
    return random.choice(weighted_chars)

# verif le cooldown
def check_cooldown(user_id):
    conn = sqlite3.connect(f'{DATA_FOLDER}/mudae_bot.db')
    c = conn.cursor()
    c.execute('INSERT OR REPLACE INTO cooldowns (user_id, last_roll) VALUES (?, ?)', (user_id, datetime.now().isoformat()))
    conn.commit()
    conn.close()

