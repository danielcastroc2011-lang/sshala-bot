import discord
import random
import requests
from bs4 import BeautifulSoup
from discord import app_commands

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
        "https://cdn.discordapp.com/attachments/1074422699172053023/1460409414388547756/image.png?ex=6966cfc1&is=69657e41&hm=07ef2643ff95f80ccf262d930d4afe5b069d25184334bb3a5f8085235cba1c88&",
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

# ---------------- REAL GPT AI ----------------

@client.tree.command(name="aitower", description="best tower names known to man")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True)
async def aitower(interaction: discord.Interaction):
    prefixes = [
        "Tower of",
        "Citadel of",
        "Steeple of",
    ]

    words = [
"challenging",
"bog",
"master",
"og"
"fog",
"sog",
"nogs",
"intense",
"skibidi",
"loser",
"fucking",
"sora",
"bugs",
"hc",
"dan",
"coins",
"feodoric",
"skill",
"cursed",
"exploding",
"bullshit",
"tower",
"of",
"in days of yore we had danced, among gods and kings and fools but when mankind moves on, what is there to dance about? growth is brilliance, brilliance is respect, respect is power when i don the cape i too will dance, but not among gods, not among kings, not among fools i will dance, for it shall mean the end of worlds and beyond i will watch the sun go supernova and i will laugh about it till the cosmos is no longer illuminated",
"golden",
"obstacles",
"downfall",
"bird",
"fall",
"nuclear",
"mystic",
"nommer",
"plungophonically",
"unknown",
"thanos",
"city",
"heights",
"simple",
"complex",
"dynamic",
"vine",
"trials",
"imminent",
"mind",
"misleading",
"mirage",
"lost",
"economy",
]
    prefix = random.choice(prefixes)
    word_count = random.randint(1, 4)
    chosen_words = random.sample(words, word_count)

    name = f"{prefix} " + " ".join(chosen_words)
    await interaction.response.send_message(name)



# ---------------- RUN ----------------
client.run("MTQ2MDM5MzE1NDUzNTYyNDczNA.Gt39-E.zFqcPRtdAOH0pxJ7_rH7KY12-rLz0EDPj-zzwY")
