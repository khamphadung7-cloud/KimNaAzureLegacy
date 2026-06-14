"""
🎵 Music - ระบบเพลง
"""
import discord
from discord import app_commands
from discord.ext import commands
import logging

logger = logging.getLogger("Music")

class Music(commands.Cog):
    """🎵 เพลง"""
    
    def __init__(self, bot):
        self.bot = bot
        self.color = discord.Color.from_rgb(255, 100, 200)
        self.playlist = []
    
    @app_commands.command(name="play", description="▶️ เล่นเพลง")
    async def play(self, interaction: discord.Interaction, song: str):
        """เล่นเพลง"""
        if not interaction.user.voice:
            embed = discord.Embed(
                title="❌ ข้อผิดพลาด",
                description="คุณต้องเข้า Voice Channel ก่อน",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        embed = discord.Embed(
            title="▶️ เล่นเพลง",
            description=f"กำลังเล่น: **{song}**",
            color=self.color
        )
        embed.set_image(url="https://media.giphy.com/media/xT9IgEx8SbQ0teblME/giphy.gif")
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="stop", description="⏹️ หยุดเพลง")
    async def stop(self, interaction: discord.Interaction):
        """หยุดเพลง"""
        embed = discord.Embed(
            title="⏹️ หยุดเพลง",
            description="หยุดการเล่นเพลง",
            color=self.color
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Music(bot))
    logger.info("✅ Music Cog")
