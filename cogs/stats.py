import discord
from discord.ext import commands
from discord import app_commands
import json
import os

class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.stats_file = "stats.json"
        self.load_stats()

    def load_stats(self):
        if os.path.exists(self.stats_file):
            with open(self.stats_file, 'r') as f:
                self.stats = json.load(f)
        else:
            self.stats = {}

    def save_stats(self):
        with open(self.stats_file, 'w') as f:
            json.dump(self.stats, f, indent=4)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        
        user_id = str(message.author.id)
        if user_id not in self.stats:
            self.stats[user_id] = {"messages": 0, "reactions": 0}
        
        self.stats[user_id]["messages"] += 1
        self.save_stats()

    @app_commands.command(name="mystats", description="ดูสถิติของคุณ")
    async def mystats(self, interaction: discord.Interaction, member: discord.Member = None):
        if member is None:
            member = interaction.user
        
        user_id = str(member.id)
        user_stats = self.stats.get(user_id, {"messages": 0, "reactions": 0})
        
        embed = discord.Embed(
            title="📊 สถิติ",
            color=0x2E64FE
        )
        embed.add_field(name="สมาชิก", value=member.mention, inline=False)
        embed.add_field(name="ข้อความ", value=user_stats.get("messages", 0), inline=False)
        embed.add_field(name="ปฏิกิริยา", value=user_stats.get("reactions", 0), inline=False)
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="serverstats", description="ดูสถิติเซิร์ฟเวอร์")
    async def serverstats(self, interaction: discord.Interaction):
        guild = interaction.guild
        embed = discord.Embed(
            title="📊 สถิติเซิร์ฟเวอร์",
            color=0x2E64FE
        )
        embed.add_field(name="ชื่อ", value=guild.name, inline=False)
        embed.add_field(name="สมาชิก", value=guild.member_count, inline=False)
        embed.add_field(name="ช่อง", value=len(guild.channels), inline=False)
        embed.add_field(name="ยศ", value=len(guild.roles), inline=False)
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Stats(bot))
    print("✅ Stats Cog loaded!")
