import discord
from discord.ext import commands
from discord import app_commands
import json
import os

class SelfRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.selfroles_file = "self_roles.json"
        self.load_selfroles()

    def load_selfroles(self):
        if os.path.exists(self.selfroles_file):
            with open(self.selfroles_file, 'r') as f:
                self.selfroles = json.load(f)
        else:
            self.selfroles = {}

    def save_selfroles(self):
        with open(self.selfroles_file, 'w') as f:
            json.dump(self.selfroles, f, indent=4)

    @app_commands.command(name="addselfrole", description="เพิ่มยศให้เลือกเอง")
    @app_commands.checks.has_permissions(administrator=True)
    async def addselfrole(self, interaction: discord.Interaction, role: discord.Role):
        guild_id = str(interaction.guild.id)
        if guild_id not in self.selfroles:
            self.selfroles[guild_id] = []
        
        if role.id not in self.selfroles[guild_id]:
            self.selfroles[guild_id].append(role.id)
            self.save_selfroles()
            await interaction.response.send_message(f"✅ เพิ่ม {role.mention} เข้ารายการ Self Roles")
        else:
            await interaction.response.send_message(f"❌ {role.mention} มีอยู่แล้ว", ephemeral=True)

    @app_commands.command(name="role", description="เลือกหรือเลิกยศ")
    async def role(self, interaction: discord.Interaction, role: discord.Role):
        guild_id = str(interaction.guild.id)
        if guild_id not in self.selfroles or role.id not in self.selfroles[guild_id]:
            await interaction.response.send_message(f"❌ ยศนี้ไม่สามารถเลือกได้", ephemeral=True)
            return
        
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"✅ เลิก {role.mention} แล้ว", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"✅ ได้ {role.mention} แล้ว", ephemeral=True)

async def setup(bot):
    await bot.add_cog(SelfRoles(bot))
    print("✅ SelfRoles Cog loaded!")
