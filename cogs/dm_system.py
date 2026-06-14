name=cogs/dm_system.py
"""
💬 DM System - ระบบส่งข้อความส่วนตัวไม่ตรวจหา
"""
import discord
from discord import app_commands
from discord.ext import commands
import logging
from datetime import datetime

logger = logging.getLogger("DMSystem")

class DMSystem(commands.Cog):
    """💬 ส่งข้อความส่วนตัว"""
    
    def __init__(self, bot):
        self.bot = bot
        self.color = discord.Color.from_rgb(100, 200, 255)
    
    @app_commands.command(name="dm", description="💬 ส่ง DM ไปยังผู้ใช้")
    @app_commands.checks.has_permissions(administrator=True)
    async def dm(self, interaction: discord.Interaction, user: discord.User, message: str):
        """ส่ง DM"""
        try:
            embed = discord.Embed(
                title="📨 ข้อความจากทีมงาน",
                description=message,
                color=self.color,
                timestamp=datetime.now()
            )
            
            embed.set_footer(text=f"เซิร์ฟเวอร์: {interaction.guild.name}")
            
            await user.send(embed=embed)
            
            result_embed = discord.Embed(
                title="✅ ส่งสำเร็จ",
                description=f"ส่งไปให้ {user.mention} เรียบร้อยแล้ว",
                color=discord.Color.green()
            )
            
            await interaction.response.send_message(embed=result_embed, ephemeral=True)
            logger.info(f"✅ DM sent to {user.name}: {message[:50]}")
        
        except Exception as e:
            error_embed = discord.Embed(
                title="❌ ข้อผิดพลาด",
                description=f"```{str(e)}```",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)
    
    @app_commands.command(name="announcement", description="📢 ประกาศลงไปทุกคน")
    @app_commands.checks.has_permissions(administrator=True)
    async def announcement(self, interaction: discord.Interaction, message: str):
        """ประกาศไปยังทุกคน"""
        await interaction.response.defer()
        
        embed = discord.Embed(
            title="📢 ประกาศจากเซิร์ฟเวอร์",
            description=message,
            color=self.color,
            timestamp=datetime.now()
        )
        embed.set_footer(text=f"จาก: {interaction.guild.name}")
        
        sent = 0
        failed = 0
        
        for member in interaction.guild.members:
            if member.bot:
                continue
            
            try:
                await member.send(embed=embed)
                sent += 1
            except:
                failed += 1
        
        result_embed = discord.Embed(
            title="✅ ประกาศแล้ว",
            description=f"ส่งไปให้: {sent} คน\nล้มเหลว: {failed} คน",
            color=discord.Color.green()
        )
        
        await interaction.followup.send(embed=result_embed)
        logger.info(f"📢 Announcement sent to {sent} users")

async def setup(bot):
    await bot.add_cog(DMSystem(bot))
    logger.info("✅ DMSystem Cog")
