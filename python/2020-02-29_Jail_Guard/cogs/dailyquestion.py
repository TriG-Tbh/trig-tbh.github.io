import discord
from discord.ext import commands
import asyncio
import time
import datetime
from dateutil import tz
import pdb

delay = 86400  # Delay between questions, in seconds


class DailyQuestionManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        tz_utc = tz.tzutc()
        tz_local = tz.tzlocal()
        while True:

            questionchannel = self.bot.get_channel("[REDACTED]")
            questionhistory = await questionchannel.history(limit=1).flatten()
            if len(questionhistory) > 0:
                previous = questionhistory[0]

                before = previous.created_at.replace(
                    tzinfo=tz_utc).astimezone(tz_local)
                now = datetime.datetime.fromtimestamp(
                    time.time()).replace(tzinfo=tz_local)

                difference = (now - before).total_seconds()

                if delay - difference > 0:
                    await asyncio.sleep(delay - difference)
            else:
                await asyncio.sleep(delay)
            channel = self.bot.get_channel("[REDACTED]")
            history = await channel.history(limit=None).flatten()
            """history = {
                message:
                message.created_at.replace(tzinfo=tz_utc).astimezone(tz_local)
                for message in history
            }
            now = datetime.datetime.fromtimestamp(
                time.time()).replace(tzinfo=tz_local)

            history = [
                message for message in history.keys()
                if abs((now - history[message]).total_seconds()) <= delay
            ]"""
            checkchannel = self.bot.get_channel("[REDACTED]")
            checkhistory = await checkchannel.history(limit=None).flatten()
            checkhistory = [message.content for message in checkhistory]
            questions = {}
            for message in history:
                if len(message.reactions) == 2 and len(
                    [m for m in checkhistory if message.content in m]) < 1:
                    questions[message] = 0


            
            votes = sorted([item for item in questions.keys() if len(item.reactions) == 2],
                            key=lambda item: self.get_votes(item),
                            reverse=True)
            

            question = votes[0]
            questionchannel = self.bot.get_channel("[REDACTED]")
            q_number = await questionchannel.history(limit=None).flatten()
            q_number = len(q_number) + 1
            q = question.content + ("?" if "?" not in question.content else "")
            message = f"<@&[REDACTED]> Daily Question #{q_number} (suggested by <@{question.author.id}>):\n\n{q}"
            await questionchannel.send(message)
            user = self.bot.get_user("[REDACTED]")
            await user.send(f"Question {q_number} has been asked at {str(datetime.datetime.now())}: {q}")
            #input()

    def get_votes(self, message):
        reactions = message.reactions
        yes = reactions[0].count - 1
        no = reactions[1].count - 1
        return yes - no

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id != "[REDACTED]" or message.author.bot:
            return

        await message.add_reaction("✅")
        await message.add_reaction("❌")


def setup(bot):
    bot.add_cog(DailyQuestionManager(bot))