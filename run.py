import discord
import random
import requests
from bs4 import BeautifulSoup
from discord import app_commands
import os
from flask import Flask
import threading

# ---------------- WEB SERVER (FOR RENDER FREE TIER) ----------------

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_web, daemon=True).start()

# ---------------- DISCORD BOT ----------------

# Intents
intents = discord.Intents.default()

# Client
class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

client = MyClient()

@client.event
async def on_ready():
    print("im into the mainframe")

# ---------------- COMMANDS ----------------

@client.tree.command(name="die", description="kill him")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True)
async def die(interaction: discord.Interaction):
    await interaction.response.send_message(
        "kill him. https://www.roblox.com/users/45152808/profile"
    )

@client.tree.command(name="sshala", description="me")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True)
async def sshala(interaction: discord.Interaction):
    await interaction.response.send_message(
        "me\nhttps://cdn.discordapp.com/attachments/1074422699172053023/1459562866033299668/Z7j3v6f.png"
    )

@client.tree.command(name="nog", description="le nog")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True)
async def nog(interaction: discord.Interaction):
    options = [
        "https://cdn.discordapp.com/attachments/1074422699172053023/1460406828872499305/nogs.png",
        "https://cdn.discordapp.com/attachments/1074422699172053023/1460406829216694312/nogscomplain.png",
        "no nogs today 😔",
        "https://cdn.discordapp.com/attachments/1074422699172053023/1460406829577142323/collectmynogs.png",
        "https://cdn.discordapp.com/attachments/1074422699172053023/1460406939698729042/image.png",
        "https://cdn.discordapp.com/attachments/1074422699172053023/1460407110134137013/image.png",
        "https://cdn.discordapp.com/attachments/1074422699172053023/1460409414388547756/image.png",
    ]
    await interaction.response.send_message(random.choice(options))

# ---------------- TOWER ROULETTE ----------------

@client.tree.command(name="towerroulette", description="gets a random tower and you GOTTA do it")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True)
async def towerroulette(interaction: discord.Interaction):
    await interaction.response.defer()

    url = "https://jtoh.fandom.com/wiki/Towers"
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

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

    if not picks:
        await interaction.followup.send("glitched out you poopoo")
        return

    await interaction.followup.send(f"go do {random.choice(picks)} you sucker")

# ---------------- AI TOWER NAME ----------------

@client.tree.command(name="aitower", description="best tower names known to man")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_context
