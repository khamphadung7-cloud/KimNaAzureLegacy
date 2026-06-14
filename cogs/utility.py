"""
🔧 Utility - เครื่องมือต่างๆ
"""
import discord
from discord import app_commands
from discord.ext import commands
import logging
from datetime import datetime

logger = logging.getLogger("Utility")

class Utility(commands.Cog):
    """🔧 เครื่องมือ"""
    
    def __init__(self, bot):
        self.bot = bot
        self.color = discord.Color.from_rgb(150, 150, 150)
    
    @app_commands.command(name="ping", description="📡 Ping บอท")
    async def ping(self, interaction: discord.Interaction):
        """ตรวจสอบ Ping"""
        latency = round(self.bot.latency * 1000)
        embed = discord.Embed(
            title="📡 Ping",
            description=f"**{latency}ms** 🏓",
            color=self.color
        )
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="userinfo", description="👤 ข้อมูลผู้ใช้")
    async def userinfo(self, interaction: discord.Interaction, user: discord.User = None):
        """ดูข้อมูลผู้ใช้"""
        user = user or interaction.user
        embed = discord.Embed(
            title="👤 ข้อมูลผู้ใช้",
            color=self.color
        )
        embed.add_field(name="👤 ชื่อ", value=user.name, inline=True)
        embed.add_field(name="🆔 ID", value=user.id, inline=True)
        embed.add_field(name="📅 สร้างเมื่อ", value=user.created_at.strftime("%d/%m/%Y"), inline=True)
        embed.set_thumbnail(url=user.avatar.url if user.avatar else "")
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="serverinfo", description="🏠 ข้อมูลเซิร์ฟเวอร์")
    async def serverinfo(self, interaction: discord.Interaction):
        """ดูข้อมูลเซิร์ฟเวอร์"""
        guild = interaction.guild
        embed = discord.Embed(
            title="🏠 ข้อมูลเซิร์ฟเวอร์",
            color=self.color
        )
        embed.add_field(name="🏛️ ชื่อ", value=guild.name, inline=True)
        embed.add_field(name="🆔 ID", value=guild.id, inline=True)
        embed.add_field(name="👥 สมาชิก", value=guild.member_count, inline=True)
        embed.add_field(name="📅 สร้างเมื่อ", value=guild.created_at.strftime("%d/%m/%Y"), inline=True)
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="calc", description="🧮 คำนวณ")
    async def calc(self, interaction: discord.Interaction, expr: str):
        """คำนวณ"""
        try:
            result = eval(expr)
            embed = discord.Embed(
                title="🧮 ผลการคำนวณ",
                description=f"{expr} = **{result}**",
                color=self.color
            )
        except Exception as e:
            embed = discord.Embed(
                title="❌ ข้อผิดพลาด",
                description=f"```{str(e)}```",
                color=discord.Color.red()
            )
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Utility(bot))
    logger.info("✅ Utility Cog")
