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

