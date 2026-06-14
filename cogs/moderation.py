"""
⚖️ Moderation - จัดการห้อง
"""
import discord
from discord import app_commands
from discord.ext import commands
import logging

logger = logging.getLogger("Moderation")

class Moderation(commands.Cog):
    """⚖️ การจัดการ"""
    
    def __init__(self, bot):
        self.bot = bot
        self.color = discord.Color.from_rgb(255, 100, 100)
    
    @app_commands.command(name="purge", description="🧹 ลบข้อความ")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def purge(self, interaction: discord.Interaction, amount: int):
        """ลบข้อความ"""
        if amount <= 0 or amount > 100:
            embed = discord.Embed(
                title="❌ ข้อผิดพลาด",
                description="จำนวนต้อง 1-100",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        deleted = await interaction.channel.purge(limit=amount)
        embed = discord.Embed(
            title="✅ ลบข้อความสำเร็จ",
            description=f"ลบข้อความทั้งหมด: **{len(deleted)}** ข้อความ",
            color=self.color
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="kick", description="👢 ไล่ออก")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        """ไล่ออก"""
        reason = reason or "ไม่มีเหตุผล"
        try:
            await member.kick(reason=reason)
            embed = discord.Embed(
                title="👢 ไล่ออก",
                description=f"ไล่ออก {member.mention} ออกแล้ว",
                color=self.color
            )
            embed.add_field(name="📝 เหตุผล", value=reason, inline=False)
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            embed = discord.Embed(title="❌ ข้อผิดพลาด", description=f"```{str(e)}```", color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="ban", description="🚫 แบน")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        """แบน"""
        reason = reason or "ไม่มีเหตุผล"
        try:
            await member.ban(reason=reason)
            embed = discord.Embed(
                title="🚫 แบน",
                description=f"แบน {member.mention} แล้ว",
                color=self.color
            )
            embed.add_field(name="📝 เหตุผล", value=reason, inline=False)
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            embed = discord.Embed(title="❌ ข้อผิดพลาด", description=f"```{str(e)}```", color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Moderation(bot))
    logger.info("✅ Moderation Cog")
