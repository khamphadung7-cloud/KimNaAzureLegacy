# cogs/admin.py
import discord
from discord import app_commands
from discord.ext import commands

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # เปลี่ยนมาใช้ Slash Command (/) เพื่อให้ใช้ง่ายเหมือนคำสั่งอื่น
    @app_commands.command(name="reload", description="สั่ง Reload ไฟล์ Cog ใหม่โดยไม่ต้อง Restart บอต")
    @app_commands.checks.has_permissions(administrator=True)
    async def reload(self, interaction: discord.Interaction, extension: str):
        try:
            # สั่ง Reload
            await self.bot.reload_extension(f'cogs.{extension}')
            await interaction.response.send_message(f"✅ โหลดไฟล์ `cogs.{extension}` ใหม่อีกรอบแล้วครับเสี่ย!", ephemeral=True)
        except Exception as e:
            # กรณีพิมพ์ชื่อไฟล์ผิด หรือไฟล์มีบัค บอตจะไม่ค้างแต่จะฟ้อง Error
            await interaction.response.send_message(f"❌ โหลดไม่ได้ครับ: `{e}`", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Admin(bot))
