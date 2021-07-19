# DNI

import discord
import random
import datetime
import os
import json
import asyncio
import concurrent.futures
import nest_asyncio

nest_asyncio.apply()

def response(resp_type):
    options = {
        0: "footer"
        } # i only need footer for this
    with open(os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)), "responses.json")) as f:
        responses = json.loads(f.read())
    
    response = random.choice(responses[options[resp_type]])
    return response

def embed(title, color=None):
    if color is None:
        color = random.randint(0, 0xffffff)
    botembed = discord.Embed(title=title, color=color)
    timestamp = datetime.datetime.utcnow()
    botembed.timestamp = timestamp
    #botembed.set_footer(text=response(0))
    return botembed


def error(source, errormsg):
    botembed = embed("Error - {}".format(source), color=0xff0000)
    botembed.description = errormsg
    return botembed


def isowner(user):
    return user.id == 424991711564136448

def run_async(bot, function):
    loop = asyncio.get_event_loop()
    
    task = loop.create_task(function)
    #return bot.loop.run_until_complete(task)

class Fragile(object):
    class Break(Exception):
      """Break out of the with statement"""

    def __init__(self, value):
        self.value = value

    def __enter__(self):
        return self.value.__enter__()

    def __exit__(self, etype, value, traceback):
        error = self.value.__exit__(etype, value, traceback)
        if etype == self.Break:
            return True
        return error
