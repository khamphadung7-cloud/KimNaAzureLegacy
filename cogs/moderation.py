import discord
from discord.ext import commands
from discord import app_commands
import datetime

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.warnings = {}  # {user_id: count}

    @app_commands.command(name="warn", description="เตือนสมาชิก")
    @app_commands.checks.has_permissions(administrator=True)
    async def warn(self, interaction: discord.Interaction, member: discord.Member, reason: str = "ไม่ได้ระบุ"):
        if member.id not in self.warnings:
            self.warnings[member.id] = 0
        self.warnings[member.id] += 1
        
        embed = discord.Embed(
            title="⚠️ เตือน",
            description=f"{member.mention} ได้รับเตือน\n**เหตุผล:** {reason}\n**ครั้งที่:** {self.warnings[member.id]}",
            color=0xFFA500
        )
        await interaction.response.send_message(embed=embed)
        
        if self.warnings[member.id] >= 3:
            await member.kick(reason=f"ถูกเตือน 3 ครั้ง: {reason}")
            await interaction.followup.send(f"❌ {member.mention} ถูก Kick เพราะเตือน 3 ครั้ง!")

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
            await interaction.response.send_message(f"❌ ไม่พบผู้ใช้ {user_id}")

async def setup(bot):
    await bot.add_cog(Moderation(bot))
    print("✅ Moderation Cog loaded!")
