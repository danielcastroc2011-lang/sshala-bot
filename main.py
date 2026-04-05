import discord
import random
import requests
from bs4 import BeautifulSoup
from discord import app_commands
import os
import threading
from flask import Flask
from discord.ui import View

app = Flask(__name__)

@app.route("/")
def home():
    return "im into the mainframe"

def run_webserver():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_webserver, daemon=True).start()

intents = discord.Intents.default()
intents.message_content = True

class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

client = MyClient()

@client.event
async def on_ready():
    activity = discord.Streaming(
        name="sshala",
        url="https://www.twitch.tv/discord"
    )
    await client.change_presence(status=discord.Status.online, activity=activity)
    print("im into the mainframe")

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
        "https://cdn.discordapp.com/attachments/1074422699172053023/1460409414388547756/image.png",
    ]
    await interaction.response.send_message(random.choice(options))

@client.tree.command(name="towerroulette", description="gets a random tower and you GOTTA do it")
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

@client.tree.command(name="aitower", description="best tower names known to man")
async def aitower(interaction: discord.Interaction):
    prefixes = ["Tower of", "Citadel of", "Steeple of"]

    words = [
        "challenging","bog","master","og","fog","sog","nogs","intense","skibidi",
        "loser","fucking","sora","bugs","hc","dan","coins","feodoric","skill",
        "cursed","exploding","bullshit","tower","of","golden","obstacles",
        "downfall","bird","fall","nuclear","mystic","nommer","unknown","thanos",
        "city","heights","simple","complex","dynamic","vine","trials","imminent",
        "mind","misleading","mirage","lost","economy","candy","sandc3"
    ]

    prefix = random.choice(prefixes)
    chosen_words = random.sample(words, random.randint(1, 4))

    await interaction.response.send_message(f"{prefix} {' '.join(chosen_words)}")

@client.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    if client.user in message.mentions:
        await message.channel.send("shut the fuck up")

@client.tree.command(name="bsl", description="bog sog log")
@app_commands.describe(choice="Your choice", opponent="Optional opponent")
@app_commands.choices(choice=[
    app_commands.Choice(name="bog", value="rock"),
    app_commands.Choice(name="sog", value="paper"),
    app_commands.Choice(name="log", value="scissors"),
])
async def rps(interaction: discord.Interaction, choice: app_commands.Choice[str], opponent: discord.User | None = None):
    user_choice = choice.value

    display = {"rock": "bog", "paper": "sog", "scissors": "log"}

    def decide(a, b):
        if a == b:
            return "tie"
        if (a == "rock" and b == "scissors") or (a == "paper" and b == "rock") or (a == "scissors" and b == "paper"):
            return "win"
        return "lose"

    if opponent is None or opponent.bot:
        bot_choice = random.choice(["rock", "paper", "scissors"])
        result = decide(user_choice, bot_choice)

        msg = {"win": "you won", "lose": "you lost haha", "tie": "no minds think alike"}[result]

        await interaction.response.send_message(
            f"you chose **{display[user_choice]}**\n"
            f"i chose **{display[bot_choice]}**\n\n{msg}"
        )
        return

    class RPSView(View):
        def __init__(self):
            super().__init__(timeout=30)
            self.choice = None

        async def interaction_check(self, i: discord.Interaction):
            return i.user.id == opponent.id

        async def finish(self, i, pick):
            self.choice = pick
            await i.response.defer()
            self.stop()

        @discord.ui.button(label="bog", style=discord.ButtonStyle.secondary)
        async def rock(self, i, _):
            await self.finish(i, "rock")

        @discord.ui.button(label="sog", style=discord.ButtonStyle.secondary)
        async def paper(self, i, _):
            await self.finish(i, "paper")

        @discord.ui.button(label="log", style=discord.ButtonStyle.secondary)
        async def scissors(self, i, _):
            await self.finish(i, "scissors")

    view = RPSView()

    await interaction.response.send_message(
        f"{opponent.mention}, **{interaction.user.name}** wants to play\n"
        f"chose **{display[user_choice]}**\nchoose",
        view=view
    )

    await view.wait()

    if view.choice is None:
        await interaction.followup.send("took too long")
        return

    result = decide(user_choice, view.choice)

    if result == "win":
        outcome = f"**{interaction.user.name}** won"
    elif result == "lose":
        outcome = f"**{opponent.name}** won"
    else:
        outcome = "no minds think alike"

    await interaction.followup.send(
        f"**{interaction.user.name}** chose **{display[user_choice]}**\n"
        f"**{opponent.name}** chose **{display[view.choice]}**\n\n{outcome}"
    )

client.run(os.getenv("DISCORD_TOKEN"))
