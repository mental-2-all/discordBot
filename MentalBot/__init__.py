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

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        if message.author.bot and message.guild is None:
            return
        elif not message.author.bot and message.guild is None:
            msgs = [
                {
                    "role": "system",
                    "content": "You are a intelligent and passionate mental doctor/therapist.",
                },
            ]
            messages = await message.channel.history(limit=200).flatten()
            messages = messages[3:len(messages)]
            for messagee in messages:
                if messagee.author.id == 1106761415919935609:
                    # bot
                    msgs.append(
                        {"role": "assistant", "content": messagee.content},
                    )
                else:
                    msgs.append(
                        {"role": "user", "content": messagee.content},
                    )

            msgs.append({"role": "user", "content": message.content})
            chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=msgs)
            reply = chat.choices[0].message.content
            await message.channel.send(reply)

            await self.process_commands(message)
            return
        elif message.author.bot:
            return
        self.message_count += 1
        print(self.message_count)

        if self.message_count % 2 == 0:
            self.message_count = 0
            users = message.guild.members

            async with aiohttp.ClientSession() as session:
                for user in users:
                    async with session.post(
                        "http://127.0.0.1:6969/pred", json={"user": user.name}
                    ) as response:
                        print(await response.text())
                        jso = await response.json()
                        if  jso["status"] == 200:
                            predScore = float(jso["pred"])
                            if predScore < -0.5:
                                await session.post(
                                    "http://127.0.0.1:6969/flag",
                                    json={"user": user.name, "bool": True, "score":predScore},
                                )
                                print("pred score <-0.5")
                        pass

        data = {
            "user": message.author.name,
            "content": message.content,
            "time": time.time(),
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "http://127.0.0.1:6969/data", json=data
            ) as response:
                # print(await response.text())
                pass
        await self.process_commands(message)
        # print(message)
        # print(message.content)
