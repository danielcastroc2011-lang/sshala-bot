import discord
import random
import os
import threading
import aiohttp

from flask import Flask
from bs4 import BeautifulSoup
from discord import app_commands
from discord.ui import View

# ================= FLASK KEEPALIVE =================

app = Flask(__name__)

@app.route("/")
def home():
    return "im into the mainframea"

def run_webserver():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_webserver, daemon=True).start()

# ================= DISCORD CLIENT =================

intents = discord.Intents.default()
intents.message_content = True  # REQUIRED for on_message

class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

client = MyClient()

# ================= READY =================

@client.event
async def on_ready():
    activity = discord.Streaming(
        name="sshala",
        url="https://cdn.discordapp.com/attachments/1074422699172053023/1460709020229697700/bird.mp4"
    )

    await client.change_presence(
        status=discord.Status.online,
        activity=activity
    )

    print("im into the mainframe")

# ================= SIMPLE COMMANDS =================

@client.tree.command(name="die", description="kill him")
async def die(interaction: discord.Interaction):
    await interaction.response.send_message(
        "kill him. https://www.roblox.com/users/45152808/profile"
    )

@client.tree.command(name="sshala", description="me")
async def sshala(interaction: discord.Interaction):
    await interaction.response.send_message(
        "me\nhttps://cdn.discordapp.com/attachments/1074422699172053023/1459562866033299668/Z7j3v6f.png"
    )

@client.tree.command(name="nog", description="le nog")
async def nog(interaction: discord.Interaction):
    options = [
        "https://cdn.discordapp.com/attachments/1074422699172053023/1460406828872499305/nogs.png",
        "https://cdn.discordapp.com/attachments/1074422699172053023/1460406829216694312/nogscomplain.png",
        "no nogs today 😔",
        "https://cdn.discordapp.com/attachments/1074422699172053023/1460406829577142323/collectmynogs.png",
        "https://cdn.discordapp.com/attachments/1074422699172053023/1460406939698729042/image.png",
        "https://cdn.discordapp.com/attachments/1074422699172053023/1460407110134137013/image.png",
    ]
    await interaction.response.send_message(random.choice(options))

# ================= ASYNC TOWER FETCH =================

async def fetch_towers():
    url = "https://jtoh.fandom.com/wiki/Towers"

    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=10) as resp:
            html = await resp.text()

    soup = BeautifulSoup(html, "html.parser")
    picks = []

    for a in soup.select("a[href]"):
        href = a.get("href")
        name = a.text.strip()

        if not name:
            continue

        if (
            (href.startswith("/wiki/Tower_of_") and name.startswith("Tower of")) or
            (href.startswith("/wiki/Citadel_of_") and name.startswith("Citadel of")) or
            (href.startswith("/wiki/Steeple_of_") and name.startswith("Steeple of"))
        ):
            picks.append(name)

    return picks

# ================= TOWER COMMANDS =================

@client.tree.command(name="towerroulette", description="gets a random tower and you GOTTA do it")
async def towerroulette(interaction: discord.Interaction):
    await interaction.response.defer()

    towers = await fetch_towers()
    if not towers:
        await interaction.followup.send("glitched out you poopoo")
        return

    await interaction.followup.send(f"go do **{random.choice(towers)}** you sucker")

@client.tree.command(name="towerace", description="race someone on a random tower")
@app_commands.describe(opponent="who")
async def towerace(interaction: discord.Interaction, opponent: discord.User):
    await interaction.response.defer()

    towers = await fetch_towers()
    if not towers:
        await interaction.followup.send("brok")
        return

    tower = random.choice(towers)

    await interaction.followup.send(
        f"{interaction.user.mention} vs {opponent.mention}\n"
        f"🏁 **race** 🏁\n\n"
        f"go do **{tower}**\n"
        f"first to finish the tower wins"
    )

# ================= ON MESSAGE =================

@client.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    if client.user in message.mentions:
        await message.channel.send("shut the fuck up")

# ================= RUN =================

client.run(os.getenv("DISCORD_TOKEN"))
