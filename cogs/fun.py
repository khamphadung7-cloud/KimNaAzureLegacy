import discord
from discord.ext import commands
from discord import app_commands
import random

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="dice", description="ทอยลูกเต๋า")
    async def dice(self, interaction: discord.Interaction):
        result = random.randint(1, 6)
        emoji_map = {1: "⚀", 2: "⚁", 3: "⚂", 4: "⚃", 5: "⚄", 6: "⚅"}
        embed = discord.Embed(
            title="🎲 ทอยลูกเต๋า",
            description=f"{emoji_map[result]} คุณได้ **{result}** {emoji_map[result]}",
            color=0xFF00FF
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="coinflip", description="พลิกเหรียญ")
    async def coinflip(self, interaction: discord.Interaction):
        result = random.choice(["หัว 🪙", "ก้อย 🪙"])
        embed = discord.Embed(
            title="🪙 พลิกเหรียญ",
            description=f"ออกมา **{result}**!",
            color=0xFFD700
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="8ball", description="ถามลูกแม่มด 8")
    async def eightball(self, interaction: discord.Interaction, question: str):
        responses = [
            "✅ ใช่แน่นอน", "✅ แน่นอน", "✅ สัญญาว่าใช่",
            "❓ ไม่แน่ใจ", "❓ ลองอีกครั้ง", "❓ ถามมาใหม่",
            "❌ ไม่เลย", "❌ ไม่คิด", "❌ อาจจะไม่"
        ]
        result = random.choice(responses)
        embed = discord.Embed(
            title="🔮 ลูกแม่มด 8",
            description=f"**คำถาม:** {question}\n\n**คำตอบ:** {result}",
            color=0x2E64FE
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="rps", description="เล่น Rock Paper Scissors")
    async def rps(self, interaction: discord.Interaction, choice: str):
        choices = ["rock", "paper", "scissors"]
        if choice.lower() not in choices:
            await interaction.response.send_message("❌ เลือก rock, paper หรือ scissors", ephemeral=True)
            return
        
        bot_choice = random.choice(choices)
        user_choice = choice.lower()
        
        emoji_map = {"rock": "🪨", "paper": "📄", "scissors": "✂️"}
        
        if user_choice == bot_choice:
            result = "🤝 มันเสมอ!"
            color = 0xFFFF00
        elif (user_choice == "rock" and bot_choice == "scissors") or \
             (user_choice == "paper" and bot_choice == "rock") or \
             (user_choice == "scissors" and bot_choice == "paper"):
            result = "🎉 คุณชนะ!"
            color = 0x00FF00
        else:
            result = "😢 บอตชนะ!"
            color = 0xFF0000
        
        embed = discord.Embed(
            title="✂️ Rock Paper Scissors",
            description=f"**คุณ:** {emoji_map[user_choice]} {user_choice.upper()}\n**บอต:** {emoji_map[bot_choice]} {bot_choice.upper()}\n\n{result}",
            color=color
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="random", description="สุ่มตัวเลข")
    async def random_number(self, interaction: discord.Interaction, min: int, max: int):
        result = random.randint(min, max)
        embed = discord.Embed(
            title="🎰 สุ่มตัวเลข",
            description=f"ระหว่าง {min} - {max}\n\n🎯 ได้ **{result}**",
            color=0xFF00FF
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Fun(bot))
    print("✅ Fun Cog loaded!")
