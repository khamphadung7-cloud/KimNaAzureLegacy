import discord
from discord.ext import commands
from discord import app_commands
import random

class Trivia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.trivia_data = [
            {
                "question": "กรุงเทพหลวงประเทศอะไร?",
                "options": ["ไทย", "เวียดนาม", "กัมพูชา", "ลาว"],
                "answer": 0
            },
            {
                "question": "พระอาทิตย์ขึ้นทางไหน?",
                "options": ["ตะวันตก", "ตะวันออก", "เหนือ", "ใต้"],
                "answer": 1
            },
            {
                "question": "2+2 เท่ากับเท่าไร?",
                "options": ["3", "4", "5", "6"],
                "answer": 1
            }
        ]

    @app_commands.command(name="trivia", description="เล่นเกมตอบคำถาม")
    async def trivia(self, interaction: discord.Interaction):
        q = random.choice(self.trivia_data)
        
        embed = discord.Embed(
            title="🧠 Trivia",
            description=q["question"],
            color=0x2E64FE
        )
        
        for i, option in enumerate(q["options"], 1):
            embed.add_field(name=f"{i}️⃣", value=option, inline=False)
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Trivia(bot))
    print("✅ Trivia Cog loaded!")
