import discord
import random
import requests
from bs4 import BeautifulSoup
from discord import app_commands
import os
import threading
from flask import Flask
import aiohttp
app = Flask(__name__)
from discord.ui import View, Button

@app.route("/")
def home():
    return "im into the mainframe"

def run_webserver():
    port = int(os.environ.get("PORT", 5000)) 
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_webserver).start()

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
    activity = discord.Streaming(
        name="sshala",
        url="https://cdn.discordapp.com/attachments/1074422699172053023/1460709020229697700/bird.mp4?ex=6967e6c9&is=69669549&hm=9fe76626d6c5348690a7356aa612888a547c46b5d1c6b700de0315cbd9c44e08&"
    )
    await client.change_presence(activity=activity)
    print("bird")


    await client.change_presence(
        status=discord.Status.online,
        activity=activity
    )

    print("im into the mainframe")


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
        "ToRRA getting cancelled being a SC Citadel, ALMOST SICKENING. Two years of work DESTROYED due to a rule change. Put yourself in this situation: your best friend that you have known for decades since kindergarten to college graduation and beyond, has been battling cancer for six months. You've cried with them, you've laughed with them, but in the end it overtakes them, and they pass away. You are devasted by this, you refuse to believe it, but it gets to you. They're gone forever. Through the grief you become determined, determined to do ANYTHING to find a cure for cancer, and to avenge your friend and the wonderful life they lived with you. You work tirelessly, day and night. You research, you test, you plot, you talk to doubting experts about how you could cure it! Work, sleep, work, sleep... as a med school graduate you know you can do it, for your friend. Your only motivation is to bring justice to cancer, and to the millions it killed. You bring in so much research and after two years of research and work, you're one link away, one link away from saving tens of millions of lives. But then... the World Health Organisation interferes, they email you and say that they've updated their testing and procedure guidelines, and that all of your work is essentially for nothing. But your work was perfectly acceptable beforehand! You stand your ground which was a terrible idea. The CDC sends people to your lab, they knock over beakers, they burn papers, they delete files and they OBLITERATE your lab until NOTHING, no work was left. You worked two years in the hopes of curing cancer and it's all destroyed because of a rule change. You are devastated by this, knowing that two whole years of work and tens of millions of people in the future are gone. You even- you even let down your friend... You go to your room and sob for 30 minutes straight. Give graceful a chance, the rule change happened in the development of the tower. Don't destroy two years of hard work to a rule change",
    ]

    prefix = random.choice(prefixes)
    word_count = random.randint(1, 4)
    chosen_words = random.sample(words, word_count)

    name = f"{prefix} " + " ".join(chosen_words)
    await interaction.response.send_message(name)


@client.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    
    if client.user in message.mentions:
        await message.channel.send("shut the fuck up")

@client.tree.command(name="bsl", description="bog sog log")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True)
@app_commands.describe(
    choice="Your choice",
    opponent="Optional: challenge another player"
)
@app_commands.choices(choice=[
    app_commands.Choice(name="bog", value="rock"),
    app_commands.Choice(name="sog", value="paper"),
    app_commands.Choice(name="log", value="scissors"),
])
async def rps(
    interaction: discord.Interaction,
    choice: app_commands.Choice[str],
    opponent: discord.User | None = None
):
    # internal logic stays rock/paper/scissors
    user_choice = choice.value

    display = {
        "rock": "bog",
        "paper": "sog",
        "scissors": "log"
    }

    def decide(a, b):
        if a == b:
            return "tie 😐"
        if (
            (a == "rock" and b == "scissors") or
            (a == "paper" and b == "rock") or
            (a == "scissors" and b == "paper")
        ):
            return "win"
        return "lose"

    # ===== BOT GAME =====
    if opponent is None or opponent.bot:
        bot_choice = random.choice(["rock", "paper", "scissors"])
        result = decide(user_choice, bot_choice)

        msg = {
            "win": "you won",
            "lose": "you lost haha",
            "tie": "no minds think alike"
        }[result]

        await interaction.response.send_message(
            f"you chose **{display[user_choice]}**\n"
            f"i chose **{display[bot_choice]}**\n\n"
            f"{msg}"
        )
        return

    # ===== PLAYER VS PLAYER =====
    class RPSView(View):
        def __init__(self):
            super().__init__(timeout=30)
            self.choice = None

        async def interaction_check(self, i: discord.Interaction):
            return i.user.id == opponent.id

        async def finish(self, i: discord.Interaction, pick):
            self.choice = pick
            self.stop()

        @discord.ui.button(label="bog", style=discord.ButtonStyle.secondary)
        async def rock(self, i: discord.Interaction, _):
            await self.finish(i, "rock")

        @discord.ui.button(label="sog", style=discord.ButtonStyle.secondary)
        async def paper(self, i: discord.Interaction, _):
            await self.finish(i, "paper")

        @discord.ui.button(label="log", style=discord.ButtonStyle.secondary)
        async def scissors(self, i: discord.Interaction, _):
            await self.finish(i, "scissors")

    view = RPSView()

    await interaction.response.send_message(
        f"{opponent.mention}, **{interaction.user.name}** wants to play bog sog log\n"
        f"le chose **{display[user_choice]}**\n"
        f"choose",
        view=view
    )

    await view.wait()

    if view.choice is None:
        await interaction.followup.send("took too long")
        return

    result = decide(user_choice, view.choice)

    if result == "win":
        outcome = f"**{interaction.user.name}** won {opponent.name} sucks"
    elif result == "lose":
        outcome = f"**{opponent.name}** won {interaction.user.name} sucks "
    else:
        outcome = "no minds think alike"

    await interaction.followup.send(
        f"**{interaction.user.name}** chose **{display[user_choice]}**\n"
        f"**{opponent.name}** chose **{display[view.choice]}**\n\n"
        f"{outcome}"
    )


client.run(os.getenv("DISCORD_TOKEN"))







