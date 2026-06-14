import discord
from discord.ext import commands, tasks
from discord import app_commands
import json
import os
from datetime import datetime, timedelta

class BumpReminder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config_file = "bump_config.json"
        self.load_config()
        self.bump_reminder_loop.start()

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {}

    def save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)

    @app_commands.command(name="setbump", description="เซตช่องสำหรับ bump")
    @app_commands.checks.has_permissions(administrator=True)
    async def setbump(self, interaction: discord.Interaction, channel: discord.TextChannel):
        guild_id = str(interaction.guild.id)
        if guild_id not in self.config:
            self.config[guild_id] = {}
        self.config[guild_id]['bump_channel'] = channel.id
        self.save_config()
        await interaction.response.send_message(f"✅ เซต bump channel เป็น {channel.mention}", ephemeral=True)

    @tasks.loop(minutes=30)
    async def bump_reminder_loop(self):
        for guild_id, config in self.config.items():
            ch_id = config.get('bump_channel')
            if ch_id:
                try:
                    channel = self.bot.get_channel(ch_id)
                    embed = discord.Embed(
                        title="📢 Bump Reminder",
                        description="ถึงเวลา Bump เซิร์ฟแล้ว! ใช้ `/bump`",
                        color=0xFFD700
                    )
                    await channel.send(embed=embed)
                except:
                    pass

    @bump_reminder_loop.before_loop
    async def before_bump_reminder_loop(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(BumpReminder(bot))
    print("✅ BumpReminder Cog loaded!")
