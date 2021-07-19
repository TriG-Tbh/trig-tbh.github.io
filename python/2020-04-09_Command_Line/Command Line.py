__version__ = 1.0

import os
import platform
import traceback
import subprocess
import sys

import discord
prefix = ""

global clear




def clear():
    system = platform.system()
    if system == "Windows":
        os.system("cls")
    elif system == "Linux":
        os.system("clear")
    else:
        print("Unknown system, cannot clear")

if __name__ == "__main__":
    clear()
    token = input("User token: ")
    bot = input("Bot (T/F)? ").lstrip().strip().lower()
    bot = (True if bot == "t" else False)
    if bot:
        from discord.ext import commands
        client = commands.Bot(command_prefix=prefix)
    else:
        client = discord.Client()

global execute


def execute(cmdstring):
    cmd = subprocess.Popen(cmdstring, shell=True, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    output_bytes = cmd.stdout.read() + cmd.stderr.read()
    output_str = str(output_bytes, "utf-8")
    output_str = output_str.strip()
    print(output_str)

async def aexec(code):
    # Make an async function with the code and `exec` it
    exec(
        f'async def __ex(): ' +
        ''.join(f'\n {l}' for l in code.split('\n'))
    )

    # Get `__ex` from local variables, call it and return the result
    return await locals()['__ex']()

global quit

def quit():
    sys.exit(0)


global exit

def exit():
    print("Use quit() to exit")

clear()


async def main():
    while True:
        directory = os.getcwd()
        command = input("(" + directory + ") >>> ")
        command = command.strip()
        if command[-1] == ":":
            line = "example"
            while line != "":
                line = input("... ")
                command += "\n" + line
        if command == "clear()":
            clear()
            continue
        if "async " in command or "await " in command:
            try:
                await aexec("print({})".format(command))
            except:
                try:
                    await aexec(command)
                except:
                    tb = traceback.format_exc().strip()
                    print(tb)
        else:
            try:
                exec("print({})".format(command))
            except:
                try:
                    exec(command)
                except:
                    tb = traceback.format_exc().strip()
                    print(tb)
                    
@client.event
async def on_ready():
    clear()
    print("Discord Command Line v{}".format(__version__))
    print("Logged in as: {}#{}".format(client.user.name, client.user.discriminator))
    await main()

if __name__ == "__main__":
    clear()
    print("Logging in...")
    try:
        client.run(token, bot=bot)
    except:
        tb = traceback.format_exc().strip()
        print(tb)