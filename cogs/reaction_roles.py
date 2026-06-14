import discord
from discord.ext import commands
from discord import app_commands
import json
import os

class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.roles_file = "reaction_roles.json"
        self.load_roles()

    def load_roles(self):
        if os.path.exists(self.roles_file):
            with open(self.roles_file, 'r') as f:
                self.reaction_roles = json.load(f)
        else:
            self.reaction_roles = {}

    def save_roles(self):
        with open(self.roles_file, 'w') as f:
            json.dump(self.reaction_roles, f, indent=4)

    @app_commands.command(name="reactionrole", description="ตั้งระบบกดปุ่มได้ยศ")
    @app_commands.checks.has_permissions(administrator=True)
    async def reactionrole(self, interaction: discord.Interaction, message_id: int, emoji: str, role: discord.Role):
        msg_id = str(message_id)
        if msg_id not in self.reaction_roles:
            self.reaction_roles[msg_id] = {}
        
        self.reaction_roles[msg_id][emoji] = role.id
        self.save_roles()
        
        embed = discord.Embed(
            title="✅ ตั้ง Reaction Role",
            description=f"{emoji} → {role.mention}",
            color=0x00FF00
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        msg_id = str(payload.message_id)
        if msg_id not in self.reaction_roles:
            return
        
        emoji = str(payload.emoji)
        if emoji not in self.reaction_roles[msg_id]:
            return
        
        guild = self.bot.get_guild(payload.guild_id)
        role = guild.get_role(self.reaction_roles[msg_id][emoji])
        member = guild.get_member(payload.user_id)
        
        if member and role:
            await member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        msg_id = str(payload.message_id)
        if msg_id not in self.reaction_roles:
            return
        
        emoji = str(payload.emoji)
        if emoji not in self.reaction_roles[msg_id]:
            return
        
        guild = self.bot.get_guild(payload.guild_id)
        role = guild.get_role(self.reaction_roles[msg_id][emoji])
        member = guild.get_member(payload.user_id)
        
        if member and role:
            await member.remove_roles(role)

async def setup(bot):
    await bot.add_cog(ReactionRoles(bot))
    print("✅ ReactionRoles Cog loaded!")
