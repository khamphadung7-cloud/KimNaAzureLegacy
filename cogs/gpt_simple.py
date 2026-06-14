name=cogs/gpt_simple.py
"""
🧠 Simple GPT - ตอบคำถามง่ายๆ
"""
import discord
from discord import app_commands
from discord.ext import commands
import logging
from datetime import datetime

logger = logging.getLogger("SimpleGPT")

class SimpleGPT(commands.Cog):
    """🧠 ตอบคำถามง่ายๆ"""
    
    def __init__(self, bot):
        self.bot = bot
        self.color = discord.Color.from_rgb(0, 200, 100)
        self.knowledge = {
            "ระดับ": ["1. Junior", "2. Senior", "3. Lead", "4. Manager"],
            "เงิน": ["ขอติดต่อ HR", "ขึ้นอยู่กับประสบการณ์", "ตามมาตรฐาน"],
            "งาน": ["มีความสุข", "ดีขึ้น", "ทำอย่างเต็มที่"],
        }
    
    @app_commands.command(name="gpt", description="🧠 ถามคำถาม AI แบบง่ายๆ")
    async def gpt(self, interaction: discord.Interaction, question: str):
        """ตอบคำถาม"""
        answer = "ผมไม่รู้เลยครับ 🤔"
        
        for keyword, answers in self.knowledge.items():
            if keyword.lower() in question.lower():
                import random
                answer = random.choice(answers)
                break
        
        embed = discord.Embed(
            title="🧠 คำตอบ",
            description=f"```\n{answer}\n```",
            color=self.color,
            timestamp=datetime.now()
        )
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(SimpleGPT(bot))
    logger.info("✅ SimpleGPT Cog")
