"""
🎮 Games - เกมต่างๆ
"""
import discord
from discord import app_commands
from discord.ext import commands
import random
import logging

logger = logging.getLogger("Games")

class Games(commands.Cog):
    """🎮 เกมต่างๆ"""
    
    def __init__(self, bot):
        self.bot = bot
        self.color = discord.Color.from_rgb(100, 200, 255)
    
    @app_commands.command(name="rps", description="✂️ หนังสือ กระดาษ กรรไกร")
    @app_commands.choices(choice=[
        app_commands.Choice(name="📄 กระดาษ", value="paper"),
        app_commands.Choice(name="✂️ กรรไกร", value="scissors"),
        app_commands.Choice(name="🪨 หนังสือ", value="rock"),
    ])
    async def rock_paper_scissors(self, interaction: discord.Interaction, choice: app_commands.Choice[str]):
        """เล่นหนังสือ กระดาษ กรรไกร"""
        user_choice = choice.value
        bot_choices = ["rock", "paper", "scissors"]
        bot_choice = random.choice(bot_choices)
        choice_emoji = {"rock": "🪨", "paper": "📄", "scissors": "✂️"}
        
        if user_choice == bot_choice:
            result = "🤝 เสมอ!"
        elif (user_choice == "rock" and bot_choice == "scissors") or \
             (user_choice == "paper" and bot_choice == "rock") or \
             (user_choice == "scissors" and bot_choice == "paper"):
            result = "🎉 คุณชนะ!"
        else:
            result = "😢 บอทชนะ"
        
        embed = discord.Embed(title="✂️ หนังสือ กระดาษ กรรไกร", color=self.color)
        embed.add_field(name="👤 คุณเลือก", value=choice_emoji.get(user_choice), inline=True)
        embed.add_field(name="🤖 บอทเลือก", value=choice_emoji.get(bot_choice), inline=True)
        embed.add_field(name="📊 ผลลัพธ์", value=result, inline=False)
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="guess", description="🎲 ทายเลข 1-100")
    async def guess_number(self, interaction: discord.Interaction):
        """ทายเลข"""
        secret = random.randint(1, 100)
        embed = discord.Embed(
            title="🎲 เกมทายเลข",
            description="คิดเลข 1-100 ลองทายดู! (ใช้ Reaction ด้านล่าง)",
            color=self.color
        )
        embed.add_field(name="📝 กฎ", value="ลองทายให้ถูก 5 ครั้ง", inline=False)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Games(bot))
    logger.info("✅ Games Cog")
