import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import json
import os

class Reminder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reminders_file = "reminders.json"
        self.load_reminders()

    def load_reminders(self):
        if os.path.exists(self.reminders_file):
            with open(self.reminders_file, 'r') as f:
                self.reminders = json.load(f)
        else:
            self.reminders = {}

    def save_reminders(self):
        with open(self.reminders_file, 'w') as f:
            json.dump(self.reminders, f, indent=4)

    @app_commands.command(name="remind", description="ตั้งการเตือน")
    async def remind(self, interaction: discord.Interaction, seconds: int, message: str):
        await interaction.response.send_message(f"✅ เตือนคุณในอีก {seconds} วินาที")
        
        await asyncio.sleep(seconds)
        
        embed = discord.Embed(
            title="⏰ การเตือน",
            description=message,
            color=0xFFD700
        )
        
        try:
            await interaction.user.send(embed=embed)
        except:
            await interaction.channel.send(f"{interaction.user.mention} {message}", embed=embed)

    @app_commands.command(name="reminders", description="ดูการเตือนทั้งหมด")
    async def reminders(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        user_reminders = self.reminders.get(user_id, [])
        
        if not user_reminders:
            await interaction.response.send_message("❌ ไม่มีการเตือน")
            return
        
        reminders_text = "\n".join([f"{i+1}. {r}" for i, r in enumerate(user_reminders)])
        embed = discord.Embed(
            title="⏰ การเตือน",
            description=reminders_text,
            color=0xFFD700
        )
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Reminder(bot))
    print("✅ Reminder Cog loaded!")
