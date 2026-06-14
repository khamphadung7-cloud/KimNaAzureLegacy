import discord
from discord.ext import commands
from discord import app_commands
import json
import os

class Verification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config_file = "verification_config.json"
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

    @app_commands.command(name="setverify", description="เซตช่องยืนยัน")
    @app_commands.checks.has_permissions(administrator=True)
    async def setverify(self, interaction: discord.Interaction, channel: discord.TextChannel, role: discord.Role):
        guild_id = str(interaction.guild.id)
        if guild_id not in self.config:
            self.config[guild_id] = {}
        
        self.config[guild_id]['verify_channel'] = channel.id
        self.config[guild_id]['verify_role'] = role.id
        self.save_config()
        
        embed = discord.Embed(
            title="✅ ยืนยันตัวตน",
            description=f"กดปุ่มด้านล่างเพื่อยืนยัน",
            color=0x00FF00
        )
        
        msg = await channel.send(embed=embed)
        await msg.add_reaction("✅")
        
        await interaction.response.send_message("✅ เซตช่องยืนยันแล้ว", ephemeral=True)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if str(payload.emoji) != "✅":
            return
        
        guild = self.bot.get_guild(payload.guild_id)
        guild_id = str(payload.guild_id)
        
        if guild_id not in self.config:
            return
        
        role_id = self.config[guild_id].get('verify_role')
        if not role_id:
            return
        
        member = guild.get_member(payload.user_id)
        role = guild.get_role(role_id)
        
        if member and role:
            await member.add_roles(role)

async def setup(bot):
    await bot.add_cog(Verification(bot))
    print("✅ Verification Cog loaded!")
