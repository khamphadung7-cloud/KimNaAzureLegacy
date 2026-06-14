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
        embed = discord.Embed(
            title="🎲 ทอยลูกเต๋า",
            description=f"คุณได้ **{result}** 🎯",
            color=0xFF00FF
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="coinflip", description="พลิกเหรียญ")
    async def coinflip(self, interaction: discord.Interaction):
        result = random.choice(["หัว", "ก้อย"])
        embed = discord.Embed(
            title="🪙 พลิกเหรียญ",
            description=f"ออกมา **{result}**!",
            color=0xFFD700
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="8ball", description="ถามลูกแม่มด 8")
    async def eightball(self, interaction: discord.Interaction, question: str):
        responses = ["ใช่แน่นอน", "ไม่แน่ใจ", "ไม่เลย", "อาจจะ", "แน่นอน", "ไม่คิด", "สัญญาว่าใช่", "ลองอีกครั้ง"]
        result = random.choice(responses)
        embed = discord.Embed(
            title="🔮 ลูกแม่มด 8",
            description=f"**คำถาม:** {question}\n**คำตอบ:** {result}",
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
        
        if user_choice == bot_choice:
            result = "มันเสมอ!"
        elif (user_choice == "rock" and bot_choice == "scissors") or \
             (user_choice == "paper" and bot_choice == "rock") or \
             (user_choice == "scissors" and bot_choice == "paper"):
            result = "คุณชนะ! 🎉"
        else:
            result = "บอตชนะ! 🤖"
        
        embed = discord.Embed(
            title="✂️ Rock Paper Scissors",
            description=f"**คุณ:** {user_choice}\n**บอต:** {bot_choice}\n\n{result}",
            color=0xFF00FF
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Fun(bot))
    print("✅ Fun Cog loaded!")
