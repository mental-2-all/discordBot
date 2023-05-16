# This example requires the 'message_content' intent.

import aiohttp
import disnake
import os
import dotenv
import textwrap
from disnake import Option

dotenv.load_dotenv()


from MentalBot import MentalBot

bot = MentalBot()

description = textwrap.dedent(
    (
        f"""
        **General**
        `m.help` - help command 
        `/help` - also a help command
        
        illness [mention] - ig illness for fun
        """
    )
)


@bot.command(name="help")
async def help(ctx):
    embed = disnake.Embed(
        title="Help Panel", description=description, color=disnake.Color.blurple()
    )
    embed.set_thumbnail(url=bot.user.avatar.url)
    embed.set_footer(
        text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar.url
    )
    await ctx.send(embed=embed)


@bot.slash_command(name="help", description="A help command!")
async def slash_help(inter):
    embed = disnake.Embed(
        title="Help Panel", description=description, color=disnake.Color.blurple()
    )
    embed.set_thumbnail(url=bot.user.avatar.url)
    embed.set_footer(
        text=f"Requested by {inter.author.name}", icon_url=inter.author.avatar.url
    )
    await inter.response.send_message(embed=embed)


@bot.command(name="scrape_all")
async def scrapeAllMessages(ctx):
    msgs = await ctx.channel.history(limit=1000).flatten()
    for msg in msgs:
        data = {
            "user": msg.author.name,
            "id": str(msg.author.id),
            "content": msg.content,
        }
        print(data)
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "http://127.0.0.1:6969/data_and_pred", json=data
            ) as response:
                pass


@bot.slash_command(name="illness", guild_ids=[697155840221905014, 958488149724635146])
async def getIllness(inter: disnake.CommandInteraction, user: disnake.User):
    """
    Get's illness of someone

    Parameters
    ----------
    user: the user you want to see
    inter: discord interaction
    """
    pred = 0
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "http://127.0.0.1:6969/pred", json={"id": str(user.id)}
        ) as response:
            if response.status == 200:
                # jsonify({"status": 200, "msg": "success", "pred": index / count})
                j = await response.json()
                try:
                    pred = float(j["pred"])
                except:
                    pred = 69
            else:
                pred = 69
    try:
        desc = ""
        if pred != 69:
            desc = f"**idk all jokes no serious** \nOur models prediction of {user.name}'s chances of mental illness: between -1 and 1, -1 is very ill, 0 is perfectly ok, 1 is extremely ok\n Pred:{pred}"
        else:
            desc = f"{user.name} is not in our db/processed sryy!! you first have to wait for them to start talking ;)\n or ask eddie ;)"

        embed = disnake.Embed(
            title=f"Illness of {user.name}",
            description=desc,
            color=disnake.Color.blurple(),
        )
        embed.set_thumbnail(url=bot.user.avatar.url)
        embed.set_footer(
            text=f"Requested by {inter.author.name}", icon_url=inter.author.avatar.url
        )
        await inter.response.send_message(embed=embed)
    except:
        return


if __name__ == "__main__":
    bot.run(os.getenv("TOKEN"))
