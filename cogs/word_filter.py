import discord
from discord.ext import commands
from discord import app_commands
import json
import os

class WordFilter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.filter_file = "word_filter.json"
        self.load_filters()

    def load_filters(self):
        if os.path.exists(self.filter_file):
            with open(self.filter_file, 'r') as f:
                self.filters = json.load(f)
        else:
            self.filters = {"words": [], "replacements": {}}

    def save_filters(self):
        with open(self.filter_file, 'w') as f:
            json.dump(self.filters, f, indent=4)

    @app_commands.command(name="addfilter", description="เพิ่มคำที่ต้องการกรอง")
    @app_commands.checks.has_permissions(administrator=True)
    async def addfilter(self, interaction: discord.Interaction, word: str, replacement: str = "*"):
        if word not in self.filters["words"]:
            self.filters["words"].append(word.lower())
            self.filters["replacements"][word.lower()] = replacement
            self.save_filters()
            await interaction.response.send_message(f"✅ เพิ่ม '{word}' เข้ากรอง", ephemeral=True)
        else:
            await interaction.response.send_message(f"❌ มีอยู่แล้ว", ephemeral=True)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return
        
        content = message.content.lower()
        filtered = content
        
        for word in self.filters["words"]:
            if word in content:
                replacement = self.filters["replacements"].get(word, "*")
                filtered = filtered.replace(word, replacement)
        
        if filtered != content:
            try:
                await message.delete()
                embed = discord.Embed(
                    title="⚠️ ข้อความถูกกรอง",
                    description=f"{message.author.mention} - {filtered}",
                    color=0xFFA500
                )
                await message.channel.send(embed=embed, delete_after=10)
            except:
                pass

async def setup(bot):
    await bot.add_cog(WordFilter(bot))
    print("✅ WordFilter Cog loaded!")
