import disnake
from disnake.ext import commands, tasks
import itertools
import aiohttp
import openai
import dotenv
import os

dotenv.load_dotenv()


openai.api_key = os.getenv("OPENAI_API_KEY")


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

    @tasks.loop(seconds=60)
    async def change_status(self):
        await self.change_presence(activity=next(self.statuss))

    @commands.Cog.listener()
    async def on_ready(self):
        self.change_status.start()
        print(f"{self.user.name} is ready")

    @commands.Cog.listener()
    async def on_message(self, msg: disnake.Message):
        if msg.author.bot or msg.author.id == 1106761415919935609:
            return
        if "gpt" in msg.content:
            msgs = [
                {
                    "role": "system",
                    "content": "You are a intelligent and passionate mental doctor/therapist.",
                },
            ]
            msgs.append({"role": "user", "content": msg.content})
            chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=msgs)
            reply = chat.choices[0].message.content
            if len(reply) >= 2000:
                await msg.reply("sry my msg is too long >2000, discord is pissy wissy")
                await self.process_commands(msg)
                return
            await msg.reply(reply)
            await self.process_commands(msg)
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
