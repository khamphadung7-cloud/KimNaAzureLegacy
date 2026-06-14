import discord
from discord.ext import commands
from discord import app_commands
import json
import os

class AFKSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.afk_file = "afk.json"
        self.load_afk()

    def load_afk(self):
        if os.path.exists(self.afk_file):
            with open(self.afk_file, 'r') as f:
                self.afk_users = json.load(f)
        else:
            self.afk_users = {}

    def save_afk(self):
        with open(self.afk_file, 'w') as f:
            json.dump(self.afk_users, f, indent=4)

    @app_commands.command(name="afk", description="ตั้ง AFK")
    async def afk(self, interaction: discord.Interaction, reason: str = "ไม่ได้ระบุ"):
        user_id = str(interaction.user.id)
        self.afk_users[user_id] = reason
        self.save_afk()
        
        embed = discord.Embed(
            title="💤 ตั้ง AFK",
            description=f"เหตุผล: {reason}",
            color=0xFFD700
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        
        user_id = str(message.author.id)
        
        # ลบ AFK
        if user_id in self.afk_users:
            del self.afk_users[user_id]
            self.save_afk()
            await message.channel.send(f"👋 {message.author.mention} กลับมาแล้ว!", delete_after=5)
        
        # แจ้งว่ามีคนเขียนถึงคนที่ AFK
        if message.mentions:
            for member in message.mentions:
                mention_id = str(member.id)
                if mention_id in self.afk_users:
                    embed = discord.Embed(
                        title="💤 ผู้ใช้ AFK",
                        description=f"{member.name} ตั้ง AFK\n**เหตุผล:** {self.afk_users[mention_id]}",
                        color=0xFFD700
                    )
                    await message.channel.send(embed=embed, delete_after=10)

async def setup(bot):
    await bot.add_cog(AFKSystem(bot))
    print("✅ AFKSystem Cog loaded!")
