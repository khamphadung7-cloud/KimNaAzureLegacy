import discord
from discord.ext import commands
from discord import app_commands
import json
import os

class InviteTracker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.invites_file = "invites.json"
        self.load_invites()

    def load_invites(self):
        if os.path.exists(self.invites_file):
            with open(self.invites_file, 'r') as f:
                self.invites = json.load(f)
        else:
            self.invites = {}

    def save_invites(self):
        with open(self.invites_file, 'w') as f:
            json.dump(self.invites, f, indent=4)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild_id = str(member.guild.id)
        if guild_id not in self.invites:
            self.invites[guild_id] = {}
        
        # หา invite ที่ใช้
        invites = await member.guild.invites()
        for invite in invites:
            invite_code = invite.code
            if invite_code not in self.invites[guild_id]:
                self.invites[guild_id][invite_code] = {"uses": 0, "inviter": str(invite.inviter.id) if invite.inviter else "Unknown"}
            
            self.invites[guild_id][invite_code]["uses"] = invite.uses
        
        self.save_invites()

    @app_commands.command(name="invites", description="ดูจำนวนคนที่คุณเชิญ")
    async def invites(self, interaction: discord.Interaction, member: discord.Member = None):
        if member is None:
            member = interaction.user
        
        guild_id = str(interaction.guild.id)
        invites = await interaction.guild.invites()
        
        total_invites = 0
        for invite in invites:
            if invite.inviter and invite.inviter.id == member.id:
                total_invites += invite.uses
        
        embed = discord.Embed(
            title="📨 คนที่เชิญ",
            description=f"{member.mention} เชิญมา **{total_invites}** คน",
            color=0x2E64FE
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(InviteTracker(bot))
    print("✅ InviteTracker Cog loaded!")
