import discord
from discord.ext import commands
from discord import app_commands
import json
import os

class AutoRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config_file = "auto_role_config.json"
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

    @app_commands.command(name="setautorole", description="เซตยศให้อัตโนมัติ")
    @app_commands.checks.has_permissions(administrator=True)
    async def setautorole(self, interaction: discord.Interaction, role: discord.Role):
        guild_id = str(interaction.guild.id)
        if guild_id not in self.config:
            self.config[guild_id] = {}
        
        self.config[guild_id]['auto_role'] = role.id
        self.save_config()
        
        embed = discord.Embed(
            title="✅ ตั้ง Auto Role",
            description=f"สมาชิกใหม่จะได้ {role.mention}",
            color=0x00FF00
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild_id = str(member.guild.id)
        if guild_id not in self.config:
            return
        
        role_id = self.config[guild_id].get('auto_role')
        if not role_id:
            return
        
        role = member.guild.get_role(role_id)
        if role:
            await member.add_roles(role)
            print(f"✅ ให้ยศ {role.name} กับ {member.name}")

async def setup(bot):
    await bot.add_cog(AutoRole(bot))
    print("✅ AutoRole Cog loaded!")
