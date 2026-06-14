import discord
from discord.ext import commands
from discord import app_commands
import json
import os
import random

class LevelUp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.levels_file = "levels.json"
        self.load_levels()

    def load_levels(self):
        if os.path.exists(self.levels_file):
            with open(self.levels_file, 'r') as f:
                self.levels = json.load(f)
        else:
            self.levels = {}

    def save_levels(self):
        with open(self.levels_file, 'w') as f:
            json.dump(self.levels, f, indent=4)

    def get_user_data(self, user_id):
        user_id = str(user_id)
        if user_id not in self.levels:
            self.levels[user_id] = {"level": 1, "exp": 0}
        return self.levels[user_id]

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        
        user_data = self.get_user_data(message.author.id)
        exp_gain = random.randint(5, 15)
        user_data["exp"] += exp_gain
        
        exp_needed = user_data["level"] * 100
        
        if user_data["exp"] >= exp_needed:
            user_data["level"] += 1
            user_data["exp"] = 0
            
            embed = discord.Embed(
                title="🎉 ระดับขึ้น!",
                description=f"{message.author.mention} ขึ้นระดับเป็น **{user_data['level']}**",
                color=0x00FF00
            )
            await message.channel.send(embed=embed)
        
        self.save_levels()

    @app_commands.command(name="level", description="ดูระดับของคุณ")
    async def level(self, interaction: discord.Interaction, member: discord.Member = None):
        if member is None:
            member = interaction.user
        
        user_data = self.get_user_data(member.id)
        
        embed = discord.Embed(
            title="📊 ระดับ",
            color=0x2E64FE
        )
        embed.add_field(name="สมาชิก", value=member.mention, inline=False)
        embed.add_field(name="ระดับ", value=user_data["level"], inline=False)
        embed.add_field(name="ประสบการณ์", value=f"{user_data['exp']}/{user_data['level'] * 100}", inline=False)
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="leaderboard", description="ดูตารางอันดับ")
    async def leaderboard(self, interaction: discord.Interaction):
        sorted_users = sorted(
            self.levels.items(),
            key=lambda x: (x[1]["level"], x[1]["exp"]),
            reverse=True
        )[:10]
        
        leaderboard_text = ""
        for i, (user_id, data) in enumerate(sorted_users, 1):
            leaderboard_text += f"{i}. <@{user_id}> - Level {data['level']}\n"
        
        embed = discord.Embed(
            title="🏆 ตารางอันดับ",
            description=leaderboard_text,
            color=0xFFD700
        )
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(LevelUp(bot))
    print("✅ LevelUp Cog loaded!")
