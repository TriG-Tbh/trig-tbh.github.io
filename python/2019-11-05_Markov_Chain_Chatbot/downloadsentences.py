import discord
import re
import os

client = discord.Client()


@client.event
async def on_ready():
    channel = client.get_channel(293701153265287168)
    history = []
    print("Getting messages...")
    async for message in channel.history(limit=None):
        content = message.content
        if message.author.bot:
            continue
        for member in message.mentions:
            content = content.replace(member.mention, "")
        custom_emojis = re.findall(r'<:\w*:\d*>', content)
        for emoji in custom_emojis:
            content = content.replace(emoji, "")
        channels = re.findall(r'<#\d*>', content)
        for channel in channels:
            content = content.replace(channel, "")
        content = re.sub(r'^https?:\/\/.*[\r\n]*', '', content, flags=re.MULTILINE)
        if content is not None:
            if len(content) > 0:
                history.append(content)
    history = history[::-1]
    print("Saving...")
    dirpath = os.path.dirname(os.path.realpath(__file__))
    with open(dirpath + "/messages.txt", "w") as f:
        messages = "\n".join(history)
        f.write(messages)
    print("Done")
    import sys
    for _ in range(5):
        sys.exit()



token = "mfa.44HdtTSMB4kvaxc2XIMfykMEdwEQaasVA7Zj1xwHc-ZrcfYP96sIDx9KUprH3mu3qr6HJnIdL-72HYWSZbEk"

if __name__ == "__main__":
    client.run(token, bot=False)