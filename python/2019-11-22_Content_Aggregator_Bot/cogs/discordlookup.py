import discord
from discord.ext import commands

def dlembed():
    return discord.Embed(title="Discord", color=0xffffff)

def helpmessage(prefix):
    embed = dlembed()
    embed.add_field(name="**Prefix**", value="{}d-".format(prefix))
    embed.add_field(name="**{}d-userinfo/user [user name/ID]**".format(prefix), value="Returns information about a specified user")
    embed.add_field(name="**{}d-serverinfo/server [server ID]**".format(prefix), value="Returns information about a specified server")
    
    return embed

def getuser(obj):
    embed = dlembed()
    if not isinstance(obj, discord.Member):
        name = obj.display_name
        discriminator = obj.discriminator
        userid = obj.id
        creation = str(obj.created_at)
        avatarurl = str(obj.avatar_url)
        embed.add_field(name="**Name**", value=name)
        embed.add_field(name="**Tag**", value="@{}#{}".format(name, discriminator))
        embed.add_field(name="**Profile**", value="<@{}>".format(userid))
        embed.add_field(name="**User ID**", value=userid)
        embed.add_field(name="**Date Created**", value=creation)
        embed.add_field(name="**Avatar URL**", value="[Avatar URL]({} \"Avatar URL\")".format(avatarurl))     
        embed.set_image(url=avatarurl)
    else:
        name = obj.name
        nickname = None
        if obj.display_name != obj.name:
            nickname = obj.display_name
        discriminator = obj.discriminator
        userid = obj.id
        datejoined = str(obj.joined_at)
        creation = str(obj.created_at)
        avatarurl = str(obj.avatar_url)
        embed.add_field(name="**Name**", value=name)
        embed.add_field(name="**Nickname**", value=str(nickname))
        embed.add_field(name="**Tag**", value="@{}#{}".format(name, discriminator))
        embed.add_field(name="**User ID**", value=userid)
        embed.add_field(name="**Date Created**", value=creation)
        embed.add_field(name="**Date Joined**", value=datejoined)
        embed.add_field(name="**Roles**", value=", ".join(["<@&{}>".format(r.id) for r in obj.roles]))
        embed.add_field(name="**Avatar URL**", value="[Avatar URL]({} \"Avatar URL\")".format(avatarurl))   
        embed.set_image(url=avatarurl)
    return embed

def getserver(server):
    embed = dlembed()
    return embed
    

class DiscordLookup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=["d-userinfo", "d-user"])
    async def userinfo(self, ctx, identification=None):
        if identification is None:
            identification = ctx.message.author.id
        isprivate = isinstance(ctx.channel, discord.abc.PrivateChannel)
        user = None
        if not isprivate:
            server = ctx.channel.guild
        try:
            identification = int(identification)
        except:
            if isprivate:
                embed = dlembed()
                embed.add_field(name="**Error Message**", value="Cannot find user - name searching is not available in DMs")
                return await ctx.send(embed=embed)
            users = [m for m in server.members if identification.lower() in m.name.lower()]
            if len(users) == 0:
                embed = dlembed()
                embed.add_field(name="**Error Message**", value="Cannot find user with name `{}`".format(identification))
                return await ctx.send(embed=embed)
            user = users[0]
        else:
            if not isprivate:
                users = [m for m in server.members if identification == m.id]
                user = (users[0] if len(users) > 0 else None)
            else:
                user = self.bot.get_user(identification)
                if user is None:
                    embed = dlembed()
                    embed.add_field(name="**Error Message**", value="Cannot find user with ID `{}` (have you tried using this command in a server?)".format(identification))
                    return await ctx.send(embed=embed)
            if user is None:
                user = self.bot.get_user(identification)
                if user is None:
                    embed = dlembed()
                    embed.add_field(name="**Error Message**", value="Cannot find user with ID `{}`".format(identification))
                    return await ctx.send(embed=embed)
        embed = getuser(user)
        await ctx.send(embed=embed)

    @commands.command(aliases=["d-serverinfo", "d-server"])
    async def serverinfo(self, ctx, identification=None):
        isprivate = isinstance(ctx.channel, discord.abc.PrivateChannel)
        if identification is None:
            if isprivate:
                embed = dlembed()
                embed.add_field(name="**Error Message**", value="This command cannot be used in DMs")
                return await ctx.send(embed=embed)
            else:
                identification = ctx.guild.id
        try:
            identification = int(identification)
        except:
            embed = dlembed()
            embed.add_field(name="**Error Message**", value="Cannot find server - invalid server ID specified")
            return await ctx.send(embed=embed)
        server = self.bot.get_guild(identification)
        if server is None:
            embed = dlembed()
            embed.add_field(name="**Error Message**", value="Cannot find server with ID `{}`".format(identification))
            return await ctx.send(embed=embed)
        if server.unavailable:
            embed = dlembed()
            embed.add_field(name="**Error Message**", value="Server is currently unavailable")
            return await ctx.send(embed=embed)
        servername = server.name
        id = server.id
        members = len(server.members)
        owner = server.owner
        ownername = owner.name
        ownertag = "<@{}>".format(owner.id)
        picture = str(server.icon_url)
        embed = dlembed()
        embed.add_field(name="**Server Name**", value=servername)
        embed.add_field(name="**Server ID**", value=id)
        embed.add_field(name="**Member Count**", value="{} members".format(members))
        embed.add_field(name="**Owner**", value=ownertag)
        embed.set_image(url=picture)
        return await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(DiscordLookup(bot))