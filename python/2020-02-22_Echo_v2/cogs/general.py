import discord
from discord.ext import commands

import os
import functions

#print(type(functions))

def botembed():
    return functions.embed("General", color=0xC0C0C0)

def help(prefix):
    pass

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def morse(self, ctx, method=None, *message, ):
        if method is None:
            embed = botembed()
            embed.add_field(name="Error", value="Missing parameter - please specify whether you want to encode or decode a message.")
            return await ctx.send(embed=embed)
        if len(message) < 1:
            embed = botembed()
            embed.add_field(name="Error", value="Invalid parameter - the message cannot be blank.")
            return await ctx.send(embed=embed)
        method = method.lower().strip()
        message = " ".join(message)
        morsecode = { 'A':'.-', 'B':'-...', 
                    'C':'-.-.', 'D':'-..', 'E':'.', 
                    'F':'..-.', 'G':'--.', 'H':'....', 
                    'I':'..', 'J':'.---', 'K':'-.-', 
                    'L':'.-..', 'M':'--', 'N':'-.', 
                    'O':'---', 'P':'.--.', 'Q':'--.-', 
                    'R':'.-.', 'S':'...', 'T':'-', 
                    'U':'..-', 'V':'...-', 'W':'.--', 
                    'X':'-..-', 'Y':'-.--', 'Z':'--..', 
                    '1':'.----', '2':'..---', '3':'...--', 
                    '4':'....-', '5':'.....', '6':'-....', 
                    '7':'--...', '8':'---..', '9':'----.', 
                    '0':'-----', ',':'--..--', '.':'.-.-.-', 
                    '?':'..--..', '/':'-..-.', '-':'-....-', 
                    '(':'-.--.', ')':'-.--.-', ":": "---...", "=":"-...-", "+":".-.-.", "_":"..--.-"} 
        if method == "encode":
            try:
                message = message.upper()
                cipher = '' 
                for letterpos in range(len(message)): 
                    if message[letterpos] != ' ' and message[letterpos] in morsecode.keys(): 
                        cipher += morsecode[message[letterpos]] + (' ' if message[letterpos+1] != " " else "")
                    else: 
                        cipher += '/'
                if cipher.endswith("/"):
                    cipher = cipher[:-1]
                cipher = cipher.strip()
                return await ctx.send(cipher)
            except:
                embed = botembed()
                embed.add_field(name="Error", value="Invalid parameter - an error has occuredan error has occured while translating this message")
                return await ctx.send(embed=embed)
        elif method == "decode":
            try:
                words = message.split("/")
                letters = []
                for word in words:
                    wletters = word.split(" ")
                    letters.append(wletters)
                cipher = []
                decodedmorse = dict([(value, key) for key, value in morsecode.items()]) 
                for word in letters:
                    newword = []
                    for letter in word:
                        newword.append(decodedmorse[letter])
                    cipher.append("".join(newword))
                cipher = " ".join(cipher)
                cipher = cipher.lower()
                return await ctx.send(cipher)
            except Exception as e:
                embed = botembed()
                embed.add_field(name="Error", value="Invalid parameter - an error has occured while translating this message")
                await ctx.send(embed=embed)
                raise e
        else:
            embed = botembed()
            embed.add_field(name="Error", value="Invalid parameter - ")
            return await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(General(bot))
