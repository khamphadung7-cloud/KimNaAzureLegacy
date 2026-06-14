import discord
from discord.ext import commands
from discord import app_commands
import json
import os

class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config_file = "server_config.json"
        self.load_config()

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {}

    def save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)

    @app_commands.command(name="setprefix", description="เซตคำสั่งนำหน้า")
    @app_commands.checks.has_permissions(administrator=True)
    async def setprefix(self, interaction: discord.Interaction, prefix: str):
        guild_id = str(interaction.guild.id)
        if guild_id not in self.config:
            self.config[guild_id] = {}
        self.config[guild_id]['prefix'] = prefix
        self.save_config()
        await interaction.response.send_message(f"✅ เซต prefix เป็น `{prefix}`")

    @app_commands.command(name="setwelcomechannel", description="เซตช่องต้อนรับ")
    @app_commands.checks.has_permissions(administrator=True)
    async def setwelcomechannel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        guild_id = str(interaction.guild.id)
        if guild_id not in self.config:
            self.config[guild_id] = {}
        self.config[guild_id]['welcome_channel'] = channel.id
        self.save_config()
        await interaction.response.send_message(f"✅ เซตช่องต้อนรับเป็น {channel.mention}")

    @app_commands.command(name="viewconfig", description="ดูการตั้งค่า")
    async def viewconfig(self, interaction: discord.Interaction):
        guild_id = str(interaction.guild.id)
        config = self.config.get(guild_id, {})
        embed = discord.Embed(title="⚙️ การตั้งค่า", color=0x2E64FE)
        embed.add_field(name="Prefix", value=config.get('prefix', '!'), inline=False)
        embed.add_field(name="Welcome Channel", value=f"<#{config.get('welcome_channel', 'ยังไม่ได้ตั้ง')}>", inline=False)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Config(bot))
    print("✅ Config Cog loaded!")
