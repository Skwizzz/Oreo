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
        async def join(ctx):
            if ctx.author.voice:
                channel = ctx.author.voice.channel
        await channel.connect(cls=wavelink.Player)

    @commands.command()
    async def leave(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()

    @commands.command()
    async def play(self,ctx, *, search: str):

        player: wavelink.Player = ctx.voice_client

        if not player:
            player = await ctx.author.voice.channel.connect(cls=wavelink.Player)

        tracks = await wavelink.YouTubeTrack.search(search)

        if not tracks:
            return await ctx.send("No song found")

        track = tracks[0]

        await player.play(track)

        await ctx.send(f"🎵 Now playing: **{track.title}**")

        queue = self.get_queue(ctx.guild.id)

        
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
    async def skip(self,ctx):
        player: wavelink.Player = ctx.voice_client
        await player.stop()

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
    
