# This example requires the 'message_content' intent.

import disnake
from disnake.ext import commands
import os
import dotenv 
import textwrap 

dotenv.load_dotenv()


from MentalBot import MentalBot

bot = MentalBot()

description = textwrap.dedent((f"""
        **General**
        `m.help` - help command 
        `/help` - also a help command
        """))

@bot.command(name="help")
async def help(ctx):
    embed = disnake.Embed(title="Help Panel", description=description, color=disnake.Color.blurple())
    embed.set_thumbnail(url=bot.user.avatar.url)
    embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar.url)
    await ctx.send(embed=embed)

@bot.slash_command(name="help", description="A help command!")
async def slash_help(inter):
    embed = disnake.Embed(title="Help Panel", description=description, color=disnake.Color.blurple())
    embed.set_thumbnail(url=bot.user.avatar.url)
    embed.set_footer(text=f"Requested by {inter.author.name}", icon_url=inter.author.avatar.url)
    await inter.response.send_message(embed=embed)



if __name__ == '__main__':
    bot.run(os.getenv("TOKEN"))
