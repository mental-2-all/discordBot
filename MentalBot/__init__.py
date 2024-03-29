import disnake
from disnake.ext import commands, tasks
import itertools
import time
import aiohttp
import openai
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI")
openai.my_api_key = api_key


class MentalBot(commands.Bot):
    intents = disnake.Intents.all()

    def __init__(self):
        self.prefix = ["m.", "m ", "M.", "M "]

        self.my_guilds = [958488149724635146]

        super().__init__(command_prefix=self.prefix, intents=MentalBot.intents)
        self.statuss = itertools.cycle(
            [
                disnake.Game("MentalHealth Simulator"),
                disnake.Activity(
                    type=disnake.ActivityType.watching, name="Mentally Ill People"
                ),
                disnake.Game(f"{self.prefix[0]}help"),
                disnake.Game("MentalHealth.io"),
            ]
        )
        self.remove_command("help")
        self.message_count = 0

    @commands.command(name="help")
    async def help(self, ctx):
        embed = disnake.Embed(
            title="Help Panel",
            description=self.description,
            color=disnake.Color.blurple(),
        )
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.set_footer(
            text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar.url
        )
        await ctx.send(embed=embed)

    @tasks.loop(seconds=60)
    async def change_status(self):
        await self.change_presence(activity=next(self.statuss))

    @commands.Cog.listener()
    async def on_ready(self):
        self.change_status.start()
        print(f"{self.user.name} is ready")

    @commands.command(name="scrape_all")
    async def scrapeAllMessages(self, ctx):
        msgs = await ctx.channel.history(limit=1000).flatten()

    # @tasks.loop(seconds=10)
    # async def updateData(self):
    #     async with aiohttp.ClientSession() as session:
    #          async with session.post("http://127.0.0.1:6969/getData", json={"user": "ed.xyz"}) as response:
    #             print("update sucessful for user ed.xyz")

    @commands.Cog.listener()
    async def on_message(self, msg: disnake.Message):
        if msg.author.bot or msg.author.id == 1106761415919935609:
            return
        data = {
            "user": msg.author.name,
            "id": str(msg.author.id),
            "content": msg.content,
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "http://127.0.0.1:6969/data_and_pred", json=data
            ) as response:
                pass
        await self.process_commands(msg)
