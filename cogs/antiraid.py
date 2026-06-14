import discord
from discord.ext import commands
import json
import os
from datetime import datetime, timedelta

class AntiRaid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.join_times = {}
        self.config_file = "antiraid_config.json"
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

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild_id = str(member.guild.id)
        
        # ตรวจสอบอายุบัญชี
        account_age = datetime.utcnow() - member.created_at
        if account_age < timedelta(hours=1):
            try:
                await member.ban(reason="⚠️ AntiRaid - บัญชีใหม่")
                mod_channel = discord.utils.get(member.guild.channels, name="📋-logs")
                if mod_channel:
                    embed = discord.Embed(
                        title="🚫 AntiRaid",
                        description=f"Ban {member.mention} - บัญชีใหม่",
                        color=0xFF0000
                    )
                    await mod_channel.send(embed=embed)
            except:
                pass
            return
        
        # ตรวจสอบจำนวนคนเข้า
        now = datetime.utcnow()
        if guild_id not in self.join_times:
            self.join_times[guild_id] = []
        
        self.join_times[guild_id] = [t for t in self.join_times[guild_id] if now - t < timedelta(minutes=1)]
        self.join_times[guild_id].append(now)
        
        if len(self.join_times[guild_id]) > 5:  # มากกว่า 5 คนใน 1 นาที
            try:
                await member.kick(reason="⚠️ AntiRaid - ตรวจพบ raid")
                mod_channel = discord.utils.get(member.guild.channels, name="📋-logs")
                if mod_channel:
                    embed = discord.Embed(
                        title="🚫 AntiRaid Alert",
                        description=f"ตรวจพบ raid! {len(self.join_times[guild_id])} คนเข้าใน 1 นาที",
                        color=0xFF0000
                    )
                    await mod_channel.send(embed=embed)
            except:
                pass

async def setup(bot):
    await bot.add_cog(AntiRaid(bot))
    print("✅ AntiRaid Cog loaded!")
