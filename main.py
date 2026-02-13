import discord
import random
import os
import threading
from flask import Flask
from discord import app_commands
from discord.ui import View

# ================== WEB SERVER (KEEP ALIVE) ==================

app = Flask(__name__)

@app.route("/")
def home():
    return "im into the mainframe"

def run_web():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_web).start()

# ================== DISCORD SETUP ==================

intents = discord.Intents.default()
intents.message_content = True  # needed for on_message

GUILD_ID = 1143938392468504596  # 🔴 PUT YOUR SERVER ID HERE
GUILD = discord.Object(id=GUILD_ID)

class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync(guild=GUILD)
        print("Slash commands synced.")

client = MyClient()

# ================== EVENTS ==================

@client.event
async def on_ready():
    activity = discord.Streaming(
        name="sshala",
        url="https://twitch.tv/discord"
    )

    await client.change_presence(
        status=discord.Status.online,
        activity=activity
    )

    print(f"Logged in as {client.user}")
    print("im into the mainframe")

@client.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    if client.user in message.mentions:
        await message.channel.send("shut the fuck up")

# ================== COMMANDS ==================

@client.tree.command(name="die", description="kill him", guild=GUILD)
async def die(interaction: discord.Interaction):
    await interaction.response.send_message(
        "kill him. https://www.roblox.com/users/45152808/profile"
    )

@client.tree.command(name="sshala", description="me", guild=GUILD)
async def sshala(interaction: discord.Interaction):
    await interaction.response.send_message("me")

@client.tree.command(name="nog", description="le nog", guild=GUILD)
async def nog(interaction: discord.Interaction):
    options = [
        "no nogs today 😔",
        "collect my nogs",
        "nog moment",
        "rare nog drop"
    ]
    await interaction.response.send_message(random.choice(options))

# ================== BOG SOG LOG ==================

@client.tree.command(name="bsl", description="bog sog log", guild=GUILD)
@app_commands.describe(choice="Your choice")
@app_commands.choices(choice=[
    app_commands.Choice(name="bog", value="rock"),
    app_commands.Choice(name="sog", value="paper"),
    app_commands.Choice(name="log", value="scissors"),
])
async def bsl(interaction: discord.Interaction, choice: app_commands.Choice[str]):

    user_choice = choice.value
    bot_choice = random.choice(["rock", "paper", "scissors"])

    display = {
        "rock": "bog",
        "paper": "sog",
        "scissors": "log"
    }

    def decide(a, b):
        if a == b:
            return "no minds think alike"
        if (
            (a == "rock" and b == "scissors") or
            (a == "paper" and b == "rock") or
            (a == "scissors" and b == "paper")
        ):
            return "you won"
        return "you lost haha"

    result = decide(user_choice, bot_choice)

    await interaction.response.send_message(
        f"you chose **{display[user_choice]}**\n"
        f"i chose **{display[bot_choice]}**\n\n"
        f"{result}"
    )

# ================== RUN ==================

TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    print("DISCORD_TOKEN not found.")
else:
    client.run(TOKEN)
