import discord
from discord.ext import commands
from discord import app_commands

class NicknameSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="setnick", description="เปลี่ยนชื่อของคุณ")
    async def setnick(self, interaction: discord.Interaction, nickname: str):
        try:
            await interaction.user.edit(nick=nickname)
            embed = discord.Embed(
                title="✅ เปลี่ยนชื่อสำเร็จ",
                description=f"ชื่อใหม่: **{nickname}**",
                color=0x00FF00
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ เกิดข้อผิดพลาด: {str(e)}", ephemeral=True)

    @app_commands.command(name="resetnick", description="รีเซ็ตชื่อกลับเป็นชื่อเดิม")
    async def resetnick(self, interaction: discord.Interaction):
        try:
            await interaction.user.edit(nick=None)
            await interaction.response.send_message("✅ รีเซ็ตชื่อแล้ว!", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ เกิดข้อผิดพลาด", ephemeral=True)

async def setup(bot):
    await bot.add_cog(NicknameSystem(bot))
    print("✅ NicknameSystem Cog loaded!")
