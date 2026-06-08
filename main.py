
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

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log',encoding='utf8',mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='?',intents=intents,status="?help for list of commands")
#GETTING QUEUES FOR THE MUSIC 
queues = {}

def get_queue(guild_id):
    if guild_id not in queues:
        queues[guild_id] = []
    return queues[guild_id]
#COMMANDS AND EVENTS
@bot.event
async def on_ready():

    print(f"Bot successfully logged in as {bot.user.name}")
# COMMANDS FOR THE MUSIC PLAYER
@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
def play_next(ctx):
    queue = get_queue(ctx.guild.id)

    if len(queue) > 0:
        song = queue.pop(0)

        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(song["url"], download=False)
            audio_url = info["url"]

        source = FFmpegPCMAudio(
            audio_url,
            before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
        )

        ctx.voice_client.play(
            source,
            after=lambda e: play_next(ctx)
        )

@bot.command()
async def play(ctx, *, query: str):

    if not ctx.voice_client:
        await ctx.invoke(join)

    queue = get_queue(ctx.guild.id)

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'default_search': 'ytsearch1',  
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=False)

        # ytsearch renvoie une liste
        if 'entries' in info:
            info = info['entries'][0]

        url = info['url']
        title = info.get('title')

    queue.append({
    "url": info["webpage_url"],
    "title": title
})

    await ctx.send(f"🎵 Added : **{title}** to queue")

    if not ctx.voice_client.is_playing():
        play_next(ctx)
@bot.command()
async def skip(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("Skipping ⏭️")
@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        ctx.voice_client.stop()
        get_queue(ctx.guild.id).clear()
        await ctx.send("Successfully stopped 🛑")

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


@bot.command()
async def queue(ctx):
    q = get_queue(ctx.guild.id)

    embed = discord.Embed(
        title="🎧 Music Queue",
        color=discord.Color.purple()
    )

    if len(q) == 0:
        embed.description = "Empty ❌"
        await ctx.send(embed=embed)
        return

    description = ""

    for i, song in enumerate(q[:10], start=1):  
        description += f"**{i}.** {song['title']}\n"

    embed.description = description


    embed.set_footer(text=f"{len(q)} song(s) in queue")

    await ctx.send(embed=embed)
bot.run(token, log_handler=handler, log_level=logging.DEBUG)