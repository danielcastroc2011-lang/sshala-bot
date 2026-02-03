import discord
from discord import app_commands
import random
import os
import asyncio
import aiohttp
import time
import threading
from flask import Flask
from bs4 import BeautifulSoup
import traceback
import sys

# ================== FLASK ==================

app = Flask(__name__)

@app.route("/")
def home():
    return "bot alive"

# ================== DISCORD ==================

# enable message content intent so on_message and mentions work
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True

class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

client = MyClient()

@client.event
async def on_ready():
    print(f"DISCORD ONLINE AS {client.user}", flush=True)
    activity = discord.Streaming(
        name="sshala",
        url="https://cdn.discordapp.com/attachments/1074422699172053023/1460709020229697700/bird.mp4"
    )
    await client.change_presence(status=discord.Status.online, activity=activity)

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

# ================== COMMAND ==================

@client.tree.command(name="towerroulette")
async def towerroulette(interaction: discord.Interaction):
    await interaction.response.defer()
    towers = await fetch_towers()
    await interaction.followup.send(f"go do **{random.choice(towers)}**")

@client.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    # The message_content intent must be enabled in code and in the bot settings
    if client.user in message.mentions:
        await message.channel.send("shut the fuck up")

# ================== DISCORD THREAD (IMPORT-SAFE) ==================

def start_discord():
    async def runner():
        # Do not print the token itself to logs; only indicate presence
        token = os.getenv("DISCORD_TOKEN")
        if not token:
            print("ERROR: DISCORD_TOKEN missing (environment variable not set). Bot will not start.", flush=True)
            return
        print("DISCORD_TOKEN present — attempting to start client", flush=True)

        while True:
            try:
                await client.start(token)
            except discord.HTTPException as e:
                # Rate-limited or other HTTP exception
                status = getattr(e, "status", None)
                print(f"discord.HTTPException caught: status={status} error={e}", flush=True)
                traceback.print_exc(file=sys.stdout)
                if status == 429:
                    print("Rate limited — waiting 10 minutes", flush=True)
                    await asyncio.sleep(600)
                else:
                    # Sleep to avoid tight crash loop, log and retry
                    await asyncio.sleep(30)
            except Exception as e:
                # Log any other exception and back off before retrying
                print("Exception in Discord runner:", e, flush=True)
                traceback.print_exc(file=sys.stdout)
                await asyncio.sleep(30)

    # run the async runner in a new event loop
    try:
        asyncio.run(runner())
    except Exception:
        print("Fatal exception running asyncio.run in start_discord():", file=sys.stdout)
        traceback.print_exc(file=sys.stdout)

if __name__ == "__main__":
    # start discord in a background thread so we can run Flask in the main thread
    threading.Thread(target=start_discord, daemon=True).start()

    # Run Flask for keepalive in hosting environments (Heroku / Replit, etc.)
    port = int(os.environ.get("PORT", 8080))
    # disable the reloader to avoid double-starting threads
    app.run(host="0.0.0.0", port=port, use_reloader=False)
