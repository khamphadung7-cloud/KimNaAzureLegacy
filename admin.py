name=cogs/admin.py
import discord
from discord import app_commands
from discord.ext import commands
import logging

logger = logging.getLogger("KimNaAzure.Admin")

class Admin(commands.Cog):
    """🔧 คำสั่ง Admin - ควบคุมบอท"""
    
    def __init__(self, bot):
        self.bot = bot
    
    # 🔄 Command: /reload
    @app_commands.command(
        name="reload",
        description="🔄 โหลด Cog ใหม่โดยไม่ต้อง Restart บอท"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def reload(self, interaction: discord.Interaction, extension: str):
        """โหลด Cog ใหม่"""
        try:
            await self.bot.reload_extension(f'cogs.{extension}')
            
            embed = discord.Embed(
                title="✅ โหลด Cog สำเร็จ",
                description=f"ไฟล์ `cogs.{extension}` โหลดใหม่แล้ว",
                color=discord.Color.green()
            )
            embed.set_footer(text="Admin Action ✓")
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
            logger.info(f"✅ Admin โหลด Cog: {extension}")
            
        except Exception as e:
            embed = discord.Embed(
                title="❌ โหลด Cog ล้มเหลว",
                description=f"ข้อผิดพลาด: ```{str(e)}```",
                color=discord.Color.red()
            )
            embed.set_footer(text="Error")
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
            logger.error(f"❌ โหลด Cog ล้มเหลว ({extension}): {e}")
    
    # 🧹 Command: /purge
    @app_commands.command(
        name="purge",
        description="🧹 ลบข้อความในแชทจำนวนที่กำหนด"
    )
    @app_commands.checks.has_permissions(manage_messages=True)
    async def purge(self, interaction: discord.Interaction, amount: int):
        """ลบข้อความ"""
        if amount <= 0:
            await interaction.response.send_message("❌ จำนวนต้องมากกว่า 0", ephemeral=True)
            return
        
        if amount > 100:
            await interaction.response.send_message("❌ จำนวนต้องน้อยกว่า 100", ephemeral=True)
            return
        
        try:
            deleted = await interaction.channel.purge(limit=amount)
            
            embed = discord.Embed(
                title="✅ ลบข้อความสำเร็จ",
                description=f"ลบข้อความทั้งหมด: **{len(deleted)}** ข้อความ",
                color=discord.Color.green()
            )
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
            logger.info(f"✅ ลบ {len(deleted)} ข้อความ")
            
        except Exception as e:
            embed = discord.Embed(
                title="❌ ข้อผิดพลาด",
                description=f"```{str(e)}```",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            logger.error(f"❌ Error purge: {e}")

async def setup(bot):
    """ตั้งค่า Cog"""
    await bot.add_cog(Admin(bot))
    logger.info("✅ Admin Cog โหลดสำเร็จ")
