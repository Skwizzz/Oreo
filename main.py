
# OREO V1.0
# MADE BY SKWIZZ

# IMPORTING LIBRARIES AND SETTING UP VARIABLES FROM ENV ( setting up everything )
import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import yt_dlp
import asyncio
from discord import FFmpegPCMAudio
import time
import json
from prefix import load_prefixes, set_prefix, get_prefix
from music import Music
from debug import Debug
from prefix import prefixes
PREFIX_FILE = "prefixes.json"
load_dotenv()
load_prefixes()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log',encoding='utf8',mode='w')



class MyBot(commands.Bot):
    async def setup_hook(self):
        await self.add_cog(Music(self))
        await self.load_extension("debug")
       
bot = MyBot(command_prefix=get_prefix, intents=discord.Intents.all())
@bot.command()
@commands.has_permissions(administrator=True)
async def setprefix(ctx, new_prefix):
    set_prefix(ctx.guild.id, new_prefix)

    await ctx.send(f"My new prefix is now: `{new_prefix}`")
#GETTING QUEUES FOR THE MUSIC 



#COMMANDS AND EVENTS
@bot.event
async def on_ready():

    print(f"Bot successfully logged in as {bot.user.name}")
    print(f"Bot ping : {round(bot.latency * 1000)} ms ")
    activity = discord.Game(name=f"Oreo V1 💜, https://skwizzz.github.io/OreoHelpPanel/, I am in {len(bot.guilds)} servers")
    await bot.change_presence(status=discord.Status.online, activity=activity)

@bot.command()
async def clear(ctx, amount: str):
    if amount.lower() == "all":
        deleted = await ctx.channel.purge(limit=None)
        nb = len(deleted)

        embed = discord.Embed(
            title="Cleared",
            description=f"Successfully cleared **{nb} messages** (ALL)",
            color=discord.Color.purple()
        )

        msg = await ctx.send(embed=embed)
        await asyncio.sleep(3)
        await msg.delete()

    else:
        amount = int(amount)

        deleted = await ctx.channel.purge(limit=amount + 1)
        nb = len(deleted) - 1  # enlève la commande

        embed = discord.Embed(
            title="Cleared",
            description=f"Successfully cleared **{nb} messages**",
            color=discord.Color.purple()
        )

        msg = await ctx.send(embed=embed)
        await asyncio.sleep(3)
        await msg.delete()


@bot.command()
async def roast(ctx,member : discord.Member):
    await ctx.send(f"{member.mention} restarted ? 🐒 ")
    await ctx.send("https://tenor.com/view/shut-up-stfu-shut-your-mouth-slap-slapping-gif-8050553153066707611")
@bot.command()
async def remind(ctx,time :int,*,message):
    await ctx.send(f"I'll remind you in {time} seconds ⏳ ")
    await asyncio.sleep(time)
    await ctx.send(f"🔔Reminder : {message} {ctx.author.mention} ")
@bot.command()
async def stats(ctx):
    guild = ctx.guild
    statEmbed = discord.Embed(
        title="Stats",
        description=f"Stats of {guild.name}",
        
        
        color=discord.Color.purple()
        
    )
    statEmbed.add_field(name="Members",value=f"👥 Members: {guild.member_count}")
    statEmbed.add_field(name="Channels",value=f"💬 Channels: {len(guild.channels)}")
    statEmbed.set_thumbnail(url=guild.icon.url)
    await ctx.send(embed=statEmbed)




















# ALL MUSICS COMMAND AS HELP
@bot.command()
async def music(ctx):
    musicEmbed = discord.Embed(
        title="Music Commands",
        description="List of all usefull commands for playing music in vc with Oreo",
        color=discord.Color.purple()

    )
    musicEmbed.add_field(
        name="Join",
        value="Makes Oreo join your channel 🎧 (?join) ",
        inline=True
    )
    musicEmbed.add_field(
        name="Play",
        value="Play a youtube song from a link ▶️ (?play 'link')",
        inline=True
    )
    musicEmbed.add_field(
        name="Stop",
        value="Stops the current song ⏹️ (?stop)",
        inline=True
    )
    musicEmbed.add_field(
        name="Leave",
        value="Makes Oreo leave your channel 👋 (?leave)",
        inline=True
    )
    musicEmbed.add_field(
        name="Skip",
        value="Skips the current song to the next in the queue ⏩ (?skip)",
        inline=True
    )
    musicEmbed.add_field(
        name="Queue",
        value="Shows the currents songs in queue ⏳ (?queue)",
        inline=True
    )
    
    await ctx.send(embed=musicEmbed)



# LISTING ALL COMMANDS IN AN EMBED 
@bot.command()
async def helpMe(ctx):
    helpEmbed = discord.Embed(
        title="Help",
        description="Listing all Oreo's commands",
        
        color=discord.Color.purple()
        )
    helpEmbed.set_footer(text="All commands starts with lowercase letters ")
    helpEmbed.add_field(
        name="Prefix",
        value="Use ? before any command to call the bot ❓",
        inline= True
        )
    helpEmbed.add_field(
        name="Music",
        value="Displays an embed with all the commands used to play music in a voice channel",
        inline= True
        )
    helpEmbed.add_field(
        name="Clear",
        value="Clears a specified number of messages (syntax : ?clear numberOfMessages or ?clear all)",
        inline= True
        )    
    helpEmbed.add_field(
        name="Userinfo",
        value="Gets user info (name,ID,profile picture), (syntax ?userinfo @user)",
        inline= True
        )   
    helpEmbed.add_field(
        name="Ping",
        value="Checks the bot latency",
        inline= True
        ) 
    helpEmbed.add_field(
        name="Roast",
        value="Roasts an user (syntax ?roast @user)",
        inline= True
        )    
    helpEmbed.add_field(
        name="Remind",
        value="Reminds you (syntax : ?remind time(in seconds) message)",
        inline= True
        )   
    helpEmbed.add_field(
        name="Stats",
        value="Shows the stats of the server",
        inline= True
        ) 
    helpEmbed.add_field(
        name="AutoClear start",
        value="Starts an autoclear that will clear the current channel every 2 mins (syntax : ?autoclear start)",
        inline= True
        ) 
    helpEmbed.add_field(
        name="AutoClear stop",
        value="Stops the autoclear (syntax : ?autoclear stop)",
        inline= True
        )   
    helpEmbed.add_field(
        name="Setprefix",
        value="Sets a new prefix for the bot (Saved for this server)(syntax : ?setprefix PREFIX)",
        inline= True
        )
        
        
        
        
        
        
        
    await ctx.send(embed=helpEmbed)
    

# RUNS THE BOT WHEN STARTING SCRIPT
bot.run(token, log_handler=handler, log_level=logging.DEBUG)
