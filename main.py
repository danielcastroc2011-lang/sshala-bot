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

# ================== FLASK (KEEPALIVE) ==================

app = Flask(__name__)

@app.route("/")
def home():
    return "alive"

def run_webserver():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_webserver, daemon=True).start()

# ================== DISCORD CLIENT ==================

intents = discord.Intents.default()

class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

client = MyClient()

# ================== STARTUP ==================

@client.event
async def on_ready():
    activity = discord.Streaming(
        name="sshala",
        url="https://cdn.discordapp.com/attachments/1074422699172053023/1460709020229697700/bird.mp4"
    )
    await client.change_presence(status=discord.Status.online, activity=activity)
    print("BOT ONLINE")

# ================== TOWER CACHE ==================

TOWER_CACHE = []
TOWER_CACHE_TIME = 0

async def fetch_towers():
    global TOWER_CACHE, TOWER_CACHE_TIME

    if TOWER_CACHE and time.time() - TOWER_CACHE_TIME < 3600:
        return TOWER_CACHE

    url = "https://jtoh.fandom.com/wiki/Towers"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=15) as r:
            html = await r.text()

    soup = BeautifulSoup(html, "html.parser")
    towers = []

    for a in soup.select("a[href]"):
        href = a.get("href")
        name = a.text.strip()

        if not href or not name:
            continue

        if (
            (href.startswith("/wiki/Tower_of_") and name.startswith("Tower of")) or
            (href.startswith("/wiki/Citadel_of_") and name.startswith("Citadel of")) or
            (href.startswith("/wiki/Steeple_of_") and name.startswith("Steeple of"))
        ):
            towers.append(name)

    TOWER_CACHE = towers
    TOWER_CACHE_TIME = time.time()
    return towers

# ================== COMMANDS ==================

@client.tree.command(name="die")
async def die(interaction: discord.Interaction):
    await interaction.response.send_message(
        "kill him. https://www.roblox.com/users/45152808/profile"
    )

@client.tree.command(name="sshala")
async def sshala(interaction: discord.Interaction):
    await interaction.response.send_message(
        "me\nhttps://cdn.discordapp.com/attachments/1074422699172053023/1459562866033299668/Z7j3v6f.png"
    )

@client.tree.command(name="nog")
async def nog(interaction: discord.Interaction):
    options = [
        "no nogs today 😔",
        "https://cdn.discordapp.com/attachments/1074422699172053023/1460406828872499305/nogs.png",
        "https://cdn.discordapp.com/attachments/1074422699172053023/1460406829216694312/nogscomplain.png",
        "https://cdn.discordapp.com/attachments/1074422699172053023/1460406829577142323/collectmynogs.png",
    ]
    await interaction.response.send_message(random.choice(options))

@client.tree.command(name="towerroulette")
async def towerroulette(interaction: discord.Interaction):
    await interaction.response.defer()
    towers = await fetch_towers()

    if not towers:
        await interaction.followup.send("broke 💀")
        return

    await interaction.followup.send(f"go do **{random.choice(towers)}**")

@client.tree.command(name="towerace")
async def towerace(interaction: discord.Interaction, opponent: discord.User):
    await interaction.response.defer()
    towers = await fetch_towers()

    if not towers:
        await interaction.followup.send("broke 💀")
        return

    tower = random.choice(towers)

    await interaction.followup.send(
        f"{interaction.user.mention} vs {opponent.mention}\n"
        f"🏁 **RACE** 🏁\n\n"
        f"go do **{tower}**\n"
        f"first to finish wins"
    )

@client.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    if client.user in message.mentions:
        await message.channel.send("shut the fuck up")

# ================== SAFE START ==================

async def main():
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise RuntimeError("DISCORD_TOKEN missing")

    while True:
        try:
            await client.start(token)
        except discord.HTTPException as e:
            if e.status == 429:
                print("Rate limited. Waiting 10 minutes...")
                await asyncio.sleep(600)
            else:
                raise e

asyncio.run(main())
