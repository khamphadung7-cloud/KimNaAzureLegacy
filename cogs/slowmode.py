import discord
from discord.ext import commands
from discord import app_commands

class Slowmode(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="slowmode", description="ตั้ง slowmode")
    @app_commands.checks.has_permissions(administrator=True)
    async def slowmode(self, interaction: discord.Interaction, seconds: int):
        try:
            await interaction.channel.edit(slowmode_delay=seconds)
            embed = discord.Embed(
                title="⏱️ Slowmode",
                description=f"ตั้ง slowmode เป็น {seconds} วินาที",
                color=0x2E64FE
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ เกิดข้อผิดพลาด", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Slowmode(bot))
    print("✅ Slowmode Cog loaded!")
