# cogs/admin.py
from discord.ext import commands
import discord

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="reload")
    @commands.has_permissions(administrator=True)
    async def reload(self, ctx, extension: str):
        await self.bot.reload_extension(f'cogs.{extension}')
        await ctx.send(f"✅ โหลดไฟล์ `{extension}` ใหม่อีกรอบแล้วครับเสี่ย!")

async def setup(bot):
    await bot.add_cog(Admin(bot))
  
