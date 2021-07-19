import asyncio
import datetime
import discord
import humanize
import itertools
import re
import sys
import traceback
import wavelink
from discord.ext import commands
from typing import Union
import urllib.parse
import requests
import functions
from youtube_search import YoutubeSearch as ys
import collections
import random
import time

def generate_code():
    chars = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890"
    code = ""
    for _ in range(15):
        code = code + random.choice(chars)
    return code


RURL = re.compile('https?:\/\/(?:www\.)?.+')

def botembed(title):
    embed = functions.embed("Music - " + title, color=0x8f0000)
    return embed

def error(errormsg):
    embed = functions.error("Music", errormsg)
    return embed
    

class MusicController:

    def __init__(self, bot, guild_id):
        self.bot = bot
        self.guild_id = guild_id
        self.channel = None

        self.next = asyncio.Event()
        self.queue = asyncio.Queue()
        self.links = asyncio.Queue()

        self.volume = 100
        self.now_playing = None

        self.looping = False
        self.start = time.time()

        self.bot.loop.create_task(self.controller_loop())

    async def controller_loop(self):
        await self.bot.wait_until_ready()

        player = self.bot.wavelink.get_player(self.guild_id)
        await player.set_volume(self.volume)

        while True:
            #if self.now_playing:
            #    await self.now_playing.delete()

            self.next.clear()
            if not self.looping:
                self.song = await self.queue.get()
                self.link = await self.links.get()
            await player.play(self.song)
            self.start = time.time()
            embed = botembed("Now Playing")
            embed.description = f"🎵 " + self.bot.response(3) + f" [{self.song}]({self.link}) is now playing!"
            self.now_playing = await self.channel.send(embed=embed)

            await self.next.wait()


class Music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.controllers = {}
        self.identifiers = ["PLACEHOLDER"] # placeholder is never used, this is just a placeholder node

        if not hasattr(bot, 'wavelink'):
            self.bot.wavelink = wavelink.Client(bot=self.bot)

        self.bot.loop.create_task(self.start_nodes())

    async def start_nodes(self):
        await self.bot.wait_until_ready()

        # Initiate our nodes. For this example we will use one server.
        # Region should be a discord.py guild.region e.g sydney or us_central (Though this is not technically required)

        identifier = self.identifiers[0]
        while identifier in self.identifiers:
            identifier = generate_code()
        self.identifiers.append(identifier)
        
        self.node = await self.bot.wavelink.initiate_node(host='[REDACTED]',
                                                     port=80,
                                                     rest_uri='[REDACTED]:80',
                                                     password='[REDACTED]',
                                                     identifier=identifier,
                                                     region='us_west')

        


        # Set our node hook callback
        self.node.set_hook(self.on_event_hook)

    async def on_event_hook(self, event):
        """Node hook callback."""
        if isinstance(event, (wavelink.TrackEnd, wavelink.TrackException)):
            controller = self.get_controller(event.player)
            controller.next.set()

    def get_controller(self, value: Union[commands.Context, wavelink.Player]):
        if isinstance(value, commands.Context):
            gid = value.guild.id
        else:
            gid = value.guild_id

        try:
            controller = self.controllers[gid]
        except KeyError:
            controller = MusicController(self.bot, gid)
            self.controllers[gid] = controller

        return controller

    async def cog_check(self, ctx):
        """A local check which applies to all commands in this cog."""
        if not ctx.guild:
            raise commands.NoPrivateMessage
        return True

    async def cog_command_error(self, ctx, error):
        """A local error handler for all errors arising from commands in this cog."""
        if isinstance(error, commands.NoPrivateMessage):
            try:
                embed = error("🚫 " + self.bot.response(2) + " this command can't be used in DMs.")
                return await ctx.send(embed=embed)
            except discord.HTTPException:
                pass

        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    @commands.command(name='connect', aliases=["join"])
    async def connect_(self, ctx, *, channel: discord.VoiceChannel=None, silent=False):
        """Connect to a valid voice channel."""
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                raise discord.DiscordException('No channel to join. Please either specify a valid channel or join one.')

        player = self.bot.wavelink.get_player(ctx.guild.id)
        
        await player.connect(channel.id)

        if not silent:
            embed = botembed("Connected")
            embed.description = "🔊 " + self.bot.response(3) + f" I've connected to `{channel.name}`."
            await ctx.send(embed=embed)


        controller = self.get_controller(ctx)
        controller.channel = ctx.channel

    @commands.command(aliases=["p"])
    async def play(self, ctx, *, query: str=None):
        """Search for and add a song to the Queue."""
        
        if not query:
            embed = error("🚫 " + self.bot.response(2) + " you need to pass a search term or link to play a song.")
            return await ctx.send(embed=embed)

        #await self.start_nodes()
        qcopy = query
        controller = self.get_controller(ctx)
        
        if not RURL.match(query):
            #query = f'ytsearch:{query}'
            
            search_results = ys(query, max_results=1).to_dict()
            href = search_results[0]["url_suffix"]

            base = ("https://www.youtube.com" + href)
            
            query = base
                
            await controller.links.put(base)
        else:
            await controller.links.put(query)

        tracks = await self.bot.wavelink.get_tracks(f'{query}')
        

        if not tracks:
            embed = error("🚫 " + self.bot.response(2) + " it looks like I couldn't find anything with that query.")
            return await ctx.send(embed=embed)

        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.is_connected:
            await ctx.invoke(self.connect_, silent=True)

        track = tracks[0]

        controller = self.get_controller(ctx)
        if len(controller.queue._queue) > 0 or player.is_playing:
            embed = botembed("Song Added")
            
            embed.description = ("📥 " + self.bot.response(1) +  f" `{str(track)}` has been added to the queue.")
            await ctx.send(embed=embed)
        await controller.queue.put(track)
        

    @commands.command()
    async def pause(self, ctx):
        """Pause the player."""
        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.is_playing:
            embed = error("🚫 " + self.bot.response(2) +  " it looks like I'm not playing anything right now...")
            return await ctx.send(embed=embed)

        embed = botembed("Paused")
        await player.set_pause(True)
        embed.description = "⏸️ " + self.bot.response(1) + " I've paused the current song."
        await ctx.send(embed=embed)
        

    @commands.command(aliases=["res"])
    async def resume(self, ctx):
        """Resume the player from a paused state."""
        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.paused:
            embed = error("🚫 " + self.bot.response(2) +  " it looks like I'm not paused right now...")
            return await ctx.send(embed=embed)

        await player.set_pause(False)
        embed = botembed("Resumed")
        embed.description = "▶️ " + self.bot.response(1) + " I've resumed the current song."
        await ctx.send(embed=embed)
        

    @commands.command(aliases=["s"])
    async def skip(self, ctx):
        """Skip the currently playing song."""
        player = self.bot.wavelink.get_player(ctx.guild.id)

        if not player.is_playing:
            embed = error("🚫 " + self.bot.response(2) +  " it looks like I'm not playing anything right now...")
            return await ctx.send(embed=embed)

        #await ctx.send('Skipping the song!', delete_after=15)
        await player.stop()

    @commands.command(aliases=["vol"])
    async def volume(self, ctx, *, vol=None):
        """Set the player volume."""
        if not vol:
            embed = error("🚫 " + self.bot.response(2) + " you need to pass a volume setting between 0 and 100.")
            return await ctx.send(embed=embed)
        elif not(vol.isdigit()):
            embed = error("🚫 " + self.bot.response(2) + " you need to pass a volume setting between 0 and 100.")
            return await ctx.send(embed=embed)
        
        player = self.bot.wavelink.get_player(ctx.guild.id)
        controller = self.get_controller(ctx)

        vol = max(min(vol, 100), 0)
        controller.volume = vol

        
        embed = botembed("🔊 " + self.bot.response(1) + f" I set the volume to `{vol}`.")
        await player.set_volume(vol)

    @commands.command(aliases=['np', 'current', 'nowplaying'])
    async def now_playing(self, ctx):
        """Retrieve the currently playing song."""
        player = self.bot.wavelink.get_player(ctx.guild.id)

        if not player.current:
            embed = error("🚫 " + self.bot.response(2) +  " it looks like I'm not playing anything right now...")
            return await ctx.send(embed=embed)


        controller = self.get_controller(ctx)
        #await controller.now_playing.delete()

        current = time.time()
        
        length = time.gmtime(controller.song.length / 1000)
        if controller.song.length / 1000 >= 3600:
            fstring = "%H:%M:%S"
        else:
            fstring = "%M:%S"
        length_r = time.strftime(fstring, length)

        dt = time.gmtime(current - controller.start)
        dt_r = time.strftime(fstring, dt)

        
        embed = botembed("Now Playing")

        embed.description = ("🔊 " + self.bot.response(1) + f" Currently, I'm playing [{controller.song}]({controller.link})\n(`{dt_r}` / `{length_r}`).")

        controller.now_playing = await ctx.send(embed=embed)

    @commands.command(aliases=['q'])
    async def queue(self, ctx, page=1):
        """Retrieve information on the next 5 songs from the queue."""
        
        controller = self.get_controller(ctx)
        
        if not(str(page).isdigit()):
            embed = error("🚫 " + self.bot.response(2) +  " you need to pass a page number to view.")
            return await ctx.send(embed=embed)
        page = int(page)

        viewable = 5

        pages = int(len(controller.queue._queue) // viewable) + (1 if len(controller.queue._queue) % viewable > 0 else 0)

        page = min(max(page, 1), pages)
        start = (page-1) * viewable
        end = min(max(start + viewable, 1), len(controller.queue._queue))


        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.current or not controller.queue._queue:
            embed = error("🚫 " + self.bot.response(2) +  " there's nothing in the queue right now...")
            return await ctx.send(embed=embed)

        upcoming = list(controller.queue._queue)[start:end]
        upcominglinks = list(controller.links._queue)[start:end]

        desc = ""
        for i in range(len(upcoming)):
            desc = desc + f"\n**{start + i + 1}**: [{upcoming[i]}]({upcominglinks[i]})" 

        embed = botembed(f"Queue (#{start + 1} - #{end})")

        embed.description = "🔢 " + self.bot.response(1) + f" Here's what's next...\n(Showing page {page} of {pages})\n" + desc

        await ctx.send(embed=embed)

    @commands.command(aliases=['disconnect', 'dc', "dis"])
    async def stop(self, ctx):
        """Stop and disconnect the player and controller."""
        player = self.bot.wavelink.get_player(ctx.guild.id)
        channel = ctx.author.voice.channel
        try:
            del self.controllers[ctx.guild.id]
        except KeyError:
            await player.disconnect()
            embed = botembed("Disconnected")
            embed.description = "👋 " + self.bot.response(4) + f" I've disconnected from `{channel.name}`."
            return await ctx.send(embed=embed)

        await player.disconnect()
        embed = botembed("Disconnected")
        embed.description = "👋 " + self.bot.response(4) + f" I've disconnected from `{channel.name}`."
        await ctx.send(embed=embed)
        
    @commands.command()
    async def move(self, ctx, frompos=None, topos=None):
        if not topos:
            embed = error("🚫 " + self.bot.response(2) +  " you need to specify where you want your song to go.")
            return await ctx.send(embed=embed)
        if not(frompos.isdigit()) or not(topos.isdigit()):
            embed = error("🚫 " + self.bot.response(2) +  " you need to specify where in the queue you want your song to go.")
            return await ctx.send(embed=embed)

        
        
        controller = self.get_controller(ctx)
        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.current or not controller.queue._queue:
            embed = error("🚫 " + self.bot.response(2) +  " there's nothing in the queue right now...")
            return await ctx.send(embed=embed)


        frompos = min(max(int(frompos), 1), len(controller.queue._queue))
        topos = min(max(int(topos), 1), len(controller.queue._queue))
        frompos -= 1
        topos -= 1
        
        song = controller.queue._queue[frompos]
        link = controller.links._queue[frompos]


        del controller.queue._queue[frompos]
        del controller.links._queue[frompos]


        controller.queue._queue.insert(topos, song)
        controller.links._queue.insert(topos, link)

        

        embed = botembed("Song Moved")
        embed.description = "🔄 " + self.bot.response(1) +  " [{}]({}) has been moved from `#{}` to `#{}` in the queue.".format(song, link, frompos + 1, topos + 1)
        return await ctx.send(embed=embed)

    @commands.command(aliases=["r"])
    async def remove(self, ctx, pos=None):
        if not pos:
            embed = error("🚫 " + self.bot.response(2) +  " you need to specify what song you want to remove.")
            return await ctx.send(embed=embed)
        if not(pos.isdigit()):
            embed = error("🚫 " + self.bot.response(2) +  " you need to specify what song in the queue you want to remove.")
            return await ctx.send(embed=embed)

        
        
        controller = self.get_controller(ctx)
        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.current or not controller.queue._queue:
            embed = error("🚫 " + self.bot.response(2) +  " there's nothing in the queue right now...")
            return await ctx.send(embed=embed)

        pos = min(max(int(pos), 1), len(controller.queue._queue))

        pos -= 1

        song = controller.queue._queue[pos]
        link = controller.links._queue[pos]

        del controller.queue._queue[pos] 
        del controller.links._queue[pos]

        embed = botembed("Song Removed")
        embed.description = "📤 " + self.bot.response(1) +  " [{}]({}) has been removed from the queue.".format(song, link)
        return await ctx.send(embed=embed)


    @commands.command()
    async def loop(self, ctx):
        controller = self.get_controller(ctx)
        player = self.bot.wavelink.get_player(ctx.guild.id)
        
        controller.looping = not(controller.looping)

        embed = botembed("Loop Toggled")
        embed.description = "🔁 " + self.bot.response(1) +  " Looping has been set to `{}`.".format(controller.looping)
        return await ctx.send(embed=embed)
        
    

def setup(bot):
    bot.add_cog(Music(bot))

