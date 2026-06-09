import discord
from discord.ext import commands
import yt_dlp
from discord import FFmpegPCMAudio
queues = {}
class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_queue(self, guild_id):
        if not hasattr(self.bot, "queues"):
            self.bot.queues = {}
        return self.bot.queues.setdefault(guild_id, [])

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
        else:
            await ctx.send("You're not in a voice channel")

    @commands.command()
    async def leave(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()

    @commands.command()
    async def play(self, ctx, *, query: str):

        if not ctx.voice_client:
            await ctx.invoke(self.join)

        queue = self.get_queue(ctx.guild.id)

        ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'default_search': 'ytsearch1',
        'cookiefile': 'cookies.txt',
        'noplaylist': True,
        'nocheckcertificate': True,
        'http_headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }
}

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=False)

            if 'entries' in info:
                info = info['entries'][0]

        queue.append({
            "url": info["webpage_url"],
            "title": info["title"]
        })

        await ctx.send(f"🎵 Added: **{info['title']}**")

        if not ctx.voice_client.is_playing():
            self.play_next(ctx)

    def play_next(self, ctx):
        queue = self.get_queue(ctx.guild.id)

        if queue:
            song = queue.pop(0)

            ydl_opts = {'format': 'bestaudio/best', 'quiet': True}

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(song["url"], download=False)

            source = FFmpegPCMAudio(info["url"])

            ctx.voice_client.play(source, after=lambda e: self.play_next(ctx))

    @commands.command()
    async def skip(self, ctx):
        if ctx.voice_client:
            ctx.voice_client.stop()

    @commands.command()
    async def stop(self, ctx):
        if ctx.voice_client:
            ctx.voice_client.stop()
            self.get_queue(ctx.guild.id).clear()

    @commands.command()
    async def queue(self, ctx):
        q = self.get_queue(ctx.guild.id)

        embed = discord.Embed(title="Queue")

        if not q:
            embed.description = "Empty"
        else:
            embed.description = "\n".join(
                f"{i+1}. {s['title']}" for i, s in enumerate(q[:10])
            )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Music(bot))
    
