import discord
from discord import app_commands
from discord.ui import View
import random
import os
import asyncio
import aiohttp
import time
import threading
from flask import Flask
from bs4 import BeautifulSoup

# ================== FLASK ==================

app = Flask(__name__)

@app.route("/")
def home():
    return "bot alive"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)

# ================== DISCORD ==================

intents = discord.Intents.default()

class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

client = MyClient()

@client.event
async def on_ready():
    print(f"DISCORD ONLINE AS {client.user}")
    activity = discord.Streaming(
        name="sshala",
        url="https://cdn.discordapp.com/attachments/1074422699172053023/1460709020229697700/bird.mp4"
    )
    await client.change_presence(
        status=discord.Status.online,
        activity=activity
    )

# ================== TOWER CACHE ==================

TOWER_CACHE = []
TOWER_CACHE_TIME = 0

async def fetch_towers():
    global TOWER_CACHE, TOWER_CACHE_TIME

    if TOWER_CACHE and time.time() - TOWER_CACHE_TIME < 3600:
        return TOWER_CACHE

    async with aiohttp.ClientSession() as session:
        async with session.get("https://jtoh.fandom.com/wiki/Towers", timeout=15) as r:
            html = await r.text()

    soup = BeautifulSoup(html, "html.parser")
    towers = []

    for a in soup.select("a[href]"):
        href = a.get("href")
        name = a.text.strip()
        if href and name and name.startswith(("Tower of", "Citadel of", "Steeple of")):
            towers.append(name)

    TOWER_CACHE = towers
    TOWER_CACHE_TIME = time.time()
    return towers

# ================== COMMANDS ==================

@client.tree.command(name="towerroulette")
async def towerroulette(interaction: discord.Interaction):
    await interaction.response.defer()
    towers = await fetch_towers()
    await interaction.followup.send(f"go do **{random.choice(towers)}**")

@client.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    if client.user in message.mentions:
        await message.channel.send("shut the fuck up")

# ================== DISCORD THREAD ==================

def run_discord():
    async def runner():
        token = os.getenv("DISCORD_TOKEN")
        if not token:
            raise RuntimeError("DISCORD_TOKEN missing")

        while True:
            try:
                await client.start(token)
            except discord.HTTPException as e:
                if e.status == 429:
                    print("Rate limited — waiting 10 minutes")
                    await asyncio.sleep(600)
                else:
                    raise

    asyncio.run(runner())

# ================== START BOTH ==================

if __name__ == "__main__":
    threading.Thread(target=run_discord, daemon=True).start()
    run_flask()
