import discord
from discord.ext import commands
from discord import app_commands
import json
import os

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.wallet_file = "wallets.json"
        self.load_wallets()

    def load_wallets(self):
        if os.path.exists(self.wallet_file):
            with open(self.wallet_file, 'r') as f:
                self.wallets = json.load(f)
        else:
            self.wallets = {}

    def save_wallets(self):
        with open(self.wallet_file, 'w') as f:
            json.dump(self.wallets, f, indent=4)

    def get_balance(self, user_id):
        return int(self.wallets.get(str(user_id), 0))

    def add_balance(self, user_id, amount):
        user_id = str(user_id)
        if user_id not in self.wallets:
            self.wallets[user_id] = 0
        self.wallets[user_id] += amount
        self.save_wallets()

    @app_commands.command(name="balance", description="ดูยอดเหรียญ")
    async def balance(self, interaction: discord.Interaction, member: discord.Member = None):
        if member is None:
            member = interaction.user
        bal = self.get_balance(member.id)
        embed = discord.Embed(
            title="💰 ยอดเหรียญ",
            description=f"{member.mention} มีเหรียญ **{bal:,}** เหรียญ",
            color=0xFFD700
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="daily", description="รับเหรียญรายวัน")
    async def daily(self, interaction: discord.Interaction):
        self.add_balance(interaction.user.id, 500)
        embed = discord.Embed(
            title="✅ รับเหรียญรายวัน",
            description=f"คุณได้รับ **500 เหรียญ**!\nทั้งหมด: **{self.get_balance(interaction.user.id):,}**",
            color=0x00FF00
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="transfer", description="ส่งเหรียญให้คน")
    async def transfer(self, interaction: discord.Interaction, member: discord.Member, amount: int):
        if self.get_balance(interaction.user.id) < amount:
            await interaction.response.send_message("❌ เหรียญไม่พอ!")
            return
        
        self.add_balance(interaction.user.id, -amount)
        self.add_balance(member.id, amount)
        embed = discord.Embed(
            title="💸 ส่งเหรียญ",
            description=f"ส่ง **{amount:,}** เหรียญให้ {member.mention}\nเหลือ: **{self.get_balance(interaction.user.id):,}**",
            color=0x00FF00
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Economy(bot))
    print("✅ Economy Cog loaded!")
