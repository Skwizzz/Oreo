import discord
from discord.ext import commands, tasks


class Debug(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"My ping is {round(self.bot.latency * 1000)} ms")

    @commands.command()
    async def userinfo(self, ctx, member: discord.Member = None):
        member = member or ctx.author

        embed = discord.Embed(title="User Info")
        embed.add_field(name="Name", value=member.name)
        embed.add_field(name="ID", value=member.id)
        embed.set_thumbnail(url=member.avatar.url)

        await ctx.send(embed=embed)


class AutoClear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.target_channel = None

    @tasks.loop(minutes=2)
    async def clear_loop(self):
        if self.target_channel:
            await self.target_channel.purge(limit=100)

    @clear_loop.before_loop
    async def before_loop(self):
        await self.bot.wait_until_ready()

    @commands.command()
    async def autoclear(self, ctx, mode: str):

        if mode.lower() == "start":
            self.target_channel = ctx.channel

            if not self.clear_loop.is_running():
                self.clear_loop.start()

            await ctx.send("🧹 AutoClear started")

        elif mode.lower() == "stop":
            self.target_channel = None

            if self.clear_loop.is_running():
                self.clear_loop.stop()

            await ctx.send("🛑 AutoClear stopped")


async def setup(bot):
    await bot.add_cog(Debug(bot))
    await bot.add_cog(AutoClear(bot))
    print("Debug Loaded")