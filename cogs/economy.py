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
        if message.author.bot or not message.guild:
            return
        
        user_id = str(message.author.id)
        if user_id not in self.stats:
            self.stats[user_id] = {"messages": 0, "servers": {}}
        
        guild_id = str(message.guild.id)
        if guild_id not in self.stats[user_id]["servers"]:
            self.stats[user_id]["servers"][guild_id] = 0
        
        self.stats[user_id]["messages"] += 1
        self.stats[user_id]["servers"][guild_id] += 1
        self.save_stats()

    @app_commands.command(name="mystats", description="ดูสถิติของคุณ")
    async def mystats(self, interaction: discord.Interaction, member: discord.Member = None):
        if member is None:
            member = interaction.user
        
        user_id = str(member.id)
        user_stats = self.stats.get(user_id, {"messages": 0, "servers": {}})
        
        embed = discord.Embed(
            title="📊 สถิติผู้ใช้",
            color=0x2E64FE
        )
        embed.set_author(name=member.name, icon_url=member.avatar.url)
        embed.add_field(name="ข้อความทั้งหมด", value=f"**{user_stats['messages']:,}**", inline=True)
        embed.add_field(name="เซิร์ฟเวอร์", value=f"**{len(user_stats['servers'])}**", inline=True)
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="serverstats", description="ดูสถิติเซิร์ฟเวอร์")
    async def serverstats(self, interaction: discord.Interaction):
        guild = interaction.guild
        embed = discord.Embed(
            title="📊 สถิติเซิร์ฟเวอร์",
            color=0x2E64FE
        )
        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
        embed.add_field(name="ชื่อ", value=guild.name, inline=False)
        embed.add_field(name="สมาชิก", value=f"**{guild.member_count}**", inline=True)
        embed.add_field(name="บ๊อต", value=f"**{sum(1 for m in guild.members if m.bot)}**", inline=True)
        embed.add_field(name="ช่อน", value=f"**{len(guild.channels)}**", inline=True)
        embed.add_field(name="ยศ", value=f"**{len(guild.roles)}**", inline=True)
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Stats(bot))
    print("✅ Stats Cog loaded!")
