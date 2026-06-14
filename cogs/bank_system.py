import discord
from discord.ext import commands
from discord import app_commands
import json
import os

class BankSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bank_file = "bank.json"
        self.load_bank()

    def load_bank(self):
        if os.path.exists(self.bank_file):
            with open(self.bank_file, 'r') as f:
                self.bank = json.load(f)
        else:
            self.bank = {}

    def save_bank(self):
        with open(self.bank_file, 'w') as f:
            json.dump(self.bank, f, indent=4)

    @app_commands.command(name="deposit", description="ฝากเงิน")
    async def deposit(self, interaction: discord.Interaction, amount: int):
        user_id = str(interaction.user.id)
        if user_id not in self.bank:
            self.bank[user_id] = {"savings": 0, "interest_rate": 0.05}
        
        self.bank[user_id]["savings"] += amount
        self.save_bank()
        
        embed = discord.Embed(
            title="💳 ฝากเงิน",
            description=f"ฝากไป **{amount:,}** เหรียญ\nเงินในธนาคาร: **{self.bank[user_id]['savings']:,}**",
            color=0x00FF00
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="withdraw", description="ถอนเงิน")
    async def withdraw(self, interaction: discord.Interaction, amount: int):
        user_id = str(interaction.user.id)
        if user_id not in self.bank or self.bank[user_id]["savings"] < amount:
            await interaction.response.send_message("❌ เงินในธนาคารไม่พอ!", ephemeral=True)
            return
        
        self.bank[user_id]["savings"] -= amount
        self.save_bank()
        
        embed = discord.Embed(
            title="💳 ถอนเงิน",
            description=f"ถอนออก **{amount:,}** เหรียญ\nเงินในธนาคาร: **{self.bank[user_id]['savings']:,}**",
            color=0x00FF00
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="balance_bank", description="ดูเงินในธนาคาร")
    async def balance_bank(self, interaction: discord.Interaction, member: discord.Member = None):
        if member is None:
            member = interaction.user
        
        user_id = str(member.id)
        savings = 0
        if user_id in self.bank:
            savings = self.bank[user_id]["savings"]
        
        embed = discord.Embed(
            title="🏦 บัญชีธนาคาร",
            description=f"{member.mention}\n**เงินคงเหลือ:** {savings:,} เหรียญ",
            color=0x2E64FE
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(BankSystem(bot))
    print("✅ BankSystem Cog loaded!")
