"""
👑 Role System - ระบบบทบาท
"""
import discord
from discord import app_commands
from discord.ext import commands
import logging

logger = logging.getLogger("RoleSystem")

class RoleSystem(commands.Cog):
    """👑 บทบาท"""
    
    def __init__(self, bot):
        self.bot = bot
        self.color = discord.Color.from_rgb(200, 100, 200)
    
    @app_commands.command(name="addrole", description="👑 เพิ่มบทบาท")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def addrole(self, interaction: discord.Interaction, member: discord.Member, role: discord.Role):
        """เพิ่มบทบาท"""
        try:
            await member.add_roles(role)
            embed = discord.Embed(
                title="✅ เพิ่มบทบาทสำเร็จ",
                description=f"เพิ่มบทบาท {role.mention} ให้ {member.mention}",
                color=self.color
            )
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            embed = discord.Embed(title="❌ ข้อผิดพลาด", description=f"```{str(e)}```", color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="removerole", description="👑 ลบบทบาท")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def removerole(self, interaction: discord.Interaction, member: discord.Member, role: discord.Role):
        """ลบบทบาท"""
        try:
            await member.remove_roles(role)
            embed = discord.Embed(
                title="✅ ลบบทบาทสำเร็จ",
                description=f"ลบบทบาท {role.mention} จาก {member.mention}",
                color=self.color
            )
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            embed = discord.Embed(title="❌ ข้อผิดพลาด", description=f"```{str(e)}```", color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(RoleSystem(bot))
    logger.info("✅ Role System Cog")
