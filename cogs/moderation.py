import discord
from discord.ext import commands
from discord import app_commands
import datetime
import json
import os

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.warnings = {}
        self.mutes = {}

    @app_commands.command(name="warn", description="เตือนสมาชิก")
    @app_commands.checks.has_permissions(administrator=True)
    async def warn(self, interaction: discord.Interaction, member: discord.Member, reason: str = "ไม่ได้ระบุ"):
        if member.id not in self.warnings:
            self.warnings[member.id] = 0
        self.warnings[member.id] += 1
        
        embed = discord.Embed(
            title="⚠️ เตือน",
            description=f"{member.mention} ได้รับเตือน\n**เหตุผล:** {reason}\n**ครั้งที่:** {self.warnings[member.id]}/3",
            color=0xFFA500
        )
        await interaction.response.send_message(embed=embed)
        
        if self.warnings[member.id] >= 3:
            try:
                await member.kick(reason=f"ถูกเตือน 3 ครั้ง: {reason}")
                await interaction.followup.send(f"❌ {member.mention} ถูก Kick เพราะเตือน 3 ครั้ง!")
            except:
                await interaction.followup.send(f"❌ ไม่สามารถ Kick ได้")

    @app_commands.command(name="mute", description="ปิดเสียง")
    @app_commands.checks.has_permissions(administrator=True)
    async def mute(self, interaction: discord.Interaction, member: discord.Member, duration: int, reason: str = "ไม่ได้ระบุ"):
        mute_role = discord.utils.get(interaction.guild.roles, name="🔇-Muted")
        if not mute_role:
            mute_role = await interaction.guild.create_role(name="🔇-Muted", color=discord.Color.dark_gray())
        
        await member.add_roles(mute_role)
        self.mutes[member.id] = discord.utils.utcnow() + datetime.timedelta(minutes=duration)
        
        embed = discord.Embed(
            title="🔇 Mute",
            description=f"{member.mention} ถูก Mute {duration} นาที\n**เหตุผล:** {reason}",
            color=0xFF0000
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="unmute", description="เปิดเสียง")
    @app_commands.checks.has_permissions(administrator=True)
    async def unmute(self, interaction: discord.Interaction, member: discord.Member):
        mute_role = discord.utils.get(interaction.guild.roles, name="🔇-Muted")
        if mute_role and mute_role in member.roles:
            await member.remove_roles(mute_role)
            await interaction.response.send_message(f"✅ เปิดเสียง {member.mention} แล้ว!")
        else:
            await interaction.response.send_message(f"❌ {member.mention} ไม่ได้ถูก Mute", ephemeral=True)

    @app_commands.command(name="kick", description="Kick สมาชิกออก")
    @app_commands.checks.has_permissions(administrator=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = "ไม่ได้ระบุ"):
        await member.kick(reason=reason)
        embed = discord.Embed(
            title="👢 Kick",
            description=f"{member.mention} ถูก Kick\n**เหตุผล:** {reason}",
            color=0xFF0000
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="ban", description="Ban สมาชิก")
    @app_commands.checks.has_permissions(administrator=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = "ไม่ได้ระบุ"):
        await member.ban(reason=reason)
        embed = discord.Embed(
            title="🔨 Ban",
            description=f"{member.mention} ถูก Ban\n**เหตุผล:** {reason}",
            color=0xFF0000
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="unban", description="ยกเลิก Ban")
    @app_commands.checks.has_permissions(administrator=True)
    async def unban(self, interaction: discord.Interaction, user_id: int):
        try:
            user = await self.bot.fetch_user(user_id)
            await interaction.guild.unban(user)
            await interaction.response.send_message(f"✅ ยกเลิก Ban {user.mention} แล้ว!")
        except:
            await interaction.response.send_message(f"❌ ไม่พบผู้ใช้", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Moderation(bot))
    print("✅ Moderation Cog loaded!")
