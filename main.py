import discord
import random
import requests
from bs4 import BeautifulSoup
from discord import app_commands
import os
import threading
from flask import Flask
import aiohttp
# ------------------- Minimal Web Server -------------------
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

def run_webserver():
    port = int(os.environ.get("PORT", 5000))  # Render sets this automatically
    app.run(host="0.0.0.0", port=port)

# Run web server in a separate thread so it doesn't block the bot
threading.Thread(target=run_webserver).start()

# ------------------- Discord Bot -------------------

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
    activity = discord.Activity(
        type=discord.ActivityType.playing,
        name="sshala"
    )

    await client.change_presence(
        status=discord.Status.online,
        activity=activity
    )

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
        "challenging", "bog", "master", "og", "fog", "sog", "nogs", "intense", "skibidi",
        "loser", "fucking", "sora", "bugs", "hc", "dan", "coins", "feodoric", "skill",
        "cursed", "exploding", "bullshit", "tower", "of",
        "in days of yore we had danced, among gods and kings and fools but when mankind moves on, what is there to dance about? growth is brilliance, brilliance is respect, respect is power when i don the cape i too will dance, but not among gods, not among kings, not among fools i will dance, for it shall mean the end of worlds and beyond i will watch the sun go supernova and i will laugh about it till the cosmos is no longer illuminated",
        "golden", "obstacles", "downfall", "bird", "fall", "nuclear", "mystic", "nommer",
        "plungophonically", "unknown", "thanos", "city", "heights", "simple", "complex",
        "dynamic", "vine", "trials", "imminent", "mind", "misleading", "mirage", "lost",
        "economy",
        "candy",
        "sandc3",
    ]

    prefix = random.choice(prefixes)
    word_count = random.randint(1, 4)
    chosen_words = random.sample(words, word_count)

    name = f"{prefix} " + " ".join(chosen_words)
    await interaction.response.send_message(name)

@client.tree.command(
    name="towersongroulette",
    description="Gets a random tower song from any floor"
)
async def towersongroulette(interaction: discord.Interaction):
    await interaction.response.defer()

    CATEGORY_URL = "https://jtoh.fandom.com/wiki/Category:Towers"

    async with aiohttp.ClientSession() as session:
        # Step 1 ➤ Get tower list
        async with session.get(CATEGORY_URL) as resp:
            soup = BeautifulSoup(await resp.text(), "html.parser")

        tower_links = [
            "https://jtoh.fandom.com" + a["href"]
            for a in soup.select("a.category-page__member-link")
            if a.get("href", "").startswith("/wiki/")
        ]

        if not tower_links:
            await interaction.followup.send("no tower 😔")
            return

        random.shuffle(tower_links)

        # Step 2 ➤ Try towers until one has music
        for tower_url in tower_links[:10]:
            async with session.get(tower_url) as resp:
                tower_soup = BeautifulSoup(await resp.text(), "html.parser")

            song_files = []

            # Find soundtrack table
            for table in tower_soup.select("table.wikitable"):
                caption = table.find("caption")
                if not caption or "Soundtrack" not in caption.text:
                    continue

                for row in table.find_all("tr")[1:]:
                    for a in row.select("a[href]"):
                        href = a["href"]

                        if any(ext in href.lower() for ext in (".mp3", ".ogg", ".wav")):
                            if href.startswith("//"):
                                href = "https:" + href
                            elif href.startswith("/"):
                                href = "https://jtoh.fandom.com" + href

                            song_files.append(href)

            if song_files:
                song = random.choice(song_files)
                tower_name = tower_url.split("/")[-1].replace("_", " ")
                await interaction.followup.send(
                    f" song **{tower_name}** soundtrack:\n{song}"
                )
                return

        await interaction.followup.send("no sng 💀")

@client.event
async def on_message(message: discord.Message):
    # ignore yourself
    if message.author.bot:
        return

    # check if bot is mentioned
    if client.user in message.mentions:
        await message.channel.send("shut the fuck up")
@client.tree.command(
    name="gameroulette",
    description="im murdering you you fucker"
)
async def gameroulette(interaction: discord.Interaction):
    await interaction.response.defer()

    # Roblox Discover API (popular games)
    url = "https://games.roblox.com/v1/games/list?model.sortToken=&model.gameSetTypeId=100000003&model.sortOrder=Desc&model.universeId=0"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                await interaction.followup.send("roblox")
                return

            data = await resp.json()

    games = data.get("games", [])
    if not games:
        await interaction.followup.send("no game no bacon no games")
        return

    game = random.choice(games)

    name = game["name"]
    place_id = game["placeId"]
    link = f"https://www.roblox.com/games/{place_id}"

    await interaction.followup.send(
        f" **Game Roulette**\n"
        f"go play **{name}**\n{link}"
    )




# ---------------- RUN ----------------
client.run(os.getenv("DISCORD_TOKEN"))








