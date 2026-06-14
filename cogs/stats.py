"""
📊 Stats - สถิติและข้อมูล
"""
import discord
from discord import app_commands
from discord.ext import commands
import logging

logger = logging.getLogger("Stats")

class Stats(commands.Cog):
    """📊 สถิติ"""
    
    def __init__(self, bot):
        self.bot = bot
        self.color = discord.Color.from_rgb(100, 100, 255)
    
    @app_commands.command(name="botstats", description="📊 สถิติบอท")
    async def botstats(self, interaction: discord.Interaction):
        """ดูสถิติบอท"""
        embed = discord.Embed(
            title="📊 สถิติบอท",
            color=self.color
        )
        embed.add_field(name="🤖 ชื่อบอท", value=self.bot.user.name, inline=True)
        embed.add_field(name="🟢 สถานะ", value="Online", inline=True)
        embed.add_field(name="📊 Ping", value=f"{round(self.bot.latency * 1000)}ms", inline=True)
        embed.add_field(name="🏢 เซิร์ฟเวอร์", value=len(self.bot.guilds), inline=True)
        embed.add_field(name="👥 ผู้ใช้", value=len(self.bot.users), inline=True)
        embed.add_field(name="📚 Cogs", value=len(self.bot.cogs), inline=True)
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="topservers", description="🏆 เซิร์ฟเวอร์ที่เยี่ยม")
    async def topservers(self, interaction: discord.Interaction):
        """ดูเซิร์ฟเวอร์ที่เยี่ยม"""
        guilds = sorted(self.bot.guilds, key=lambda g: g.member_count, reverse=True)[:10]
        embed = discord.Embed(
            title="🏆 เซิร์ฟเวอร์ Top 10",
            color=self.color
        )
        for i, guild in enumerate(guilds, 1):
            embed.add_field(
                name=f"{i}. {guild.name}",
                value=f"👥 {guild.member_count} คน",
                inline=False
            )
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Stats(bot))
    logger.info("✅ Stats Cog")
