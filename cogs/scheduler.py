import discord
from discord.ext import commands, tasks
from discord import app_commands
import json
import os
from datetime import datetime

class Scheduler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.scheduled_file = "scheduled.json"
        self.load_scheduled()
        self.scheduled_loop.start()

    def load_scheduled(self):
        if os.path.exists(self.scheduled_file):
            with open(self.scheduled_file, 'r') as f:
                self.scheduled = json.load(f)
        else:
            self.scheduled = {}

    def save_scheduled(self):
        with open(self.scheduled_file, 'w') as f:
            json.dump(self.scheduled, f, indent=4)

    @app_commands.command(name="schedule", description="ตั้งเวลาโพส")
    @app_commands.checks.has_permissions(administrator=True)
    async def schedule(self, interaction: discord.Interaction, message: str, hours: int):
        msg_id = str(interaction.channel.id)
        if msg_id not in self.scheduled:
            self.scheduled[msg_id] = []
        
        self.scheduled[msg_id].append({
            "message": message,
            "time": datetime.utcnow().timestamp() + (hours * 3600)
        })
        self.save_scheduled()
        
        await interaction.response.send_message(f"✅ ตั้งโพสในอีก {hours} ชั่วโมง", ephemeral=True)

    @tasks.loop(minutes=1)
    async def scheduled_loop(self):
        now = datetime.utcnow().timestamp()
        for ch_id, messages in self.scheduled.items():
            for msg in messages:
                if msg["time"] <= now:
                    try:
                        channel = self.bot.get_channel(int(ch_id))
                        await channel.send(msg["message"])
                        messages.remove(msg)
                        self.save_scheduled()
                    except:
                        pass

    @scheduled_loop.before_loop
    async def before_scheduled_loop(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(Scheduler(bot))
    print("✅ Scheduler Cog loaded!")
