import discord
from discord.ext import commands
from discord import app_commands

class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_app_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.MissingPermissions):
            embed = discord.Embed(
                title="❌ ไม่มีสิทธิ์",
                description="คุณไม่มีสิทธิ์ใช้คำสั่งนี้",
                color=0xFF0000
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        
        elif isinstance(error, app_commands.BotMissingPermissions):
            embed = discord.Embed(
                title="❌ บอตไม่มีสิทธิ์",
                description="บอตไม่มีสิทธิ์ทำสิ่งนี้",
                color=0xFF0000
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        
        else:
            embed = discord.Embed(
                title="❌ เกิดข้อผิดพลาด",
                description=f"```{str(error)}```",
                color=0xFF0000
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(ErrorHandler(bot))
    print("✅ ErrorHandler Cog loaded!")
