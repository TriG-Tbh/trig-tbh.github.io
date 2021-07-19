from discord.ext import commands

import settings
import functions

def botembed():
    embed = functions.embed("General", color=0xC0C0C0)
    return embed

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def echo(self, ctx, *message):
        if len(message) == 0:
            embed = botembed()
            embed.add_field(name="Error", value="Invalid parameter - message cannot be empty.", inline=False)
            return await ctx.send(embed=embed)
        message = " ".join(message)
        if not functions.is_sanitized(ctx.message):
            embed = botembed()
            embed.add_field(name="Error", value="Invalid parameter - message cannot contain mentions.", inline=False)
            return await ctx.send(embed=embed)
        await ctx.send(message)

    @commands.command()
    async def cascade(self, ctx, parameter=None, *message):
        if len(message) == 0 and parameter is None:
            embed = botembed()
            embed.add_field(name="Error", value="Invalid parameter - message cannot be empty.", inline=False)
            return await ctx.send(embed=embed)
        message = " ".join(message)
        if parameter != "-reverse":
            message = parameter + " " + message
        elif len(message) == 0 and parameter == "-reverse":
            message = parameter
        send = ""
        for i in range(len(message)):
            if message[i] != " ":
                send += message[:i+1] + "\n"
        send = send.strip()
        if parameter == "-reverse":
            lines = send.split("\n")
            lines = lines[::-1]
            send = "\n".join(lines)
        return await ctx.send(send)


def setup(bot):
    bot.add_cog(General(bot))