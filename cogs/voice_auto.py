import discord
from discord.ext import commands
from discord import app_commands
import json
import os

class VoiceAuto(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config_file = "voice_auto_config.json"
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

    @app_commands.command(name="setvAutoChannel", description="เซตห้องเสียงเพื่อสร้างห้องใหม่")
    @app_commands.checks.has_permissions(administrator=True)
    async def setautochannel(self, interaction: discord.Interaction, channel: discord.VoiceChannel):
        guild_id = str(interaction.guild.id)
        if guild_id not in self.config:
            self.config[guild_id] = {}
        self.config[guild_id]['auto_voice_channel'] = channel.id
        self.save_config()
        await interaction.response.send_message(f"✅ เซต {channel.name} เป็นห้องเสียง Auto", ephemeral=True)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if after.channel is None:
            return
        
        guild_id = str(member.guild.id)
        if guild_id not in self.config:
            return
        
        auto_ch_id = self.config[guild_id].get('auto_voice_channel')
        if not auto_ch_id or after.channel.id != auto_ch_id:
            return
        
        # สร้างห้องใหม่
        new_channel = await member.guild.create_voice_channel(
            name=f"🔊 {member.name}'s Channel",
            category=after.channel.category,
            user_limit=10
        )
        
        await member.move_to(new_channel)

async def setup(bot):
    await bot.add_cog(VoiceAuto(bot))
    print("✅ VoiceAuto Cog loaded!")
