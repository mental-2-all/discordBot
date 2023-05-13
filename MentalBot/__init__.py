import disnake
from disnake.ext import commands, tasks
import itertools
import aiohttp
import textwrap
import time

class MentalBot(commands.Bot):
    intents = disnake.Intents.all()
    def __init__(self):
        self.prefix = ["m.", "m ", "M.", "M "]

        self.my_guilds = [958488149724635146]

        super().__init__(command_prefix=self.prefix, intents=MentalBot.intents)
        self.statuss = itertools.cycle(
            [disnake.Game('MentalHealth Simulator'), disnake.Activity(type=disnake.ActivityType.watching, name="Mentally Ill People"), disnake.Game(f'{self.prefix[0]}help'), disnake.Game("MentalHealth.io")])
        self.remove_command('help')
    
    
    @commands.command(name="help")
    async def help(self, ctx):
        embed = disnake.Embed(title="Help Panel", description=self.description, color=disnake.Color.blurple())
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @tasks.loop(seconds=60)
    async def change_status(self):
        await self.change_presence(activity=next(self.statuss))

    @commands.Cog.listener()
    async def on_ready(self):
        self.change_status.start()
        print(f"{self.user.name} is ready")


    @commands.Cog.listener()
    async def on_message(self, message:disnake.Message):
        if message.author.bot:
            return
        
        data = {"content": message.content,
                "channel_name":message.channel.name,
                "time": time.time(),
                "nsfw": message.channel.nsfw,
            }
        print(message)
        print(message.content)