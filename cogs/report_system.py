import discord
from discord.ext import commands
from discord import app_commands
import json
import os

class ReportSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reports_file = "reports.json"
        self.load_reports()

    def load_reports(self):
        if os.path.exists(self.reports_file):
            with open(self.reports_file, 'r') as f:
                self.reports = json.load(f)
        else:
            self.reports = {}

    def save_reports(self):
        with open(self.reports_file, 'w') as f:
            json.dump(self.reports, f, indent=4)

    @app_commands.command(name="report", description="รายงานสมาชิก")
    async def report(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        guild_id = str(interaction.guild.id)
        if guild_id not in self.reports:
            self.reports[guild_id] = []
        
        report = {
            "reporter": interaction.user.id,
            "reported": member.id,
            "reason": reason,
            "timestamp": str(discord.utils.utcnow())
        }
        self.reports[guild_id].append(report)
        self.save_reports()
        
        # ส่งไปยัง mod channel
        mod_channel = discord.utils.get(interaction.guild.channels, name="📋-reports")
        if mod_channel:
            embed = discord.Embed(
                title="📢 รายงาน",
                color=0xFF0000
            )
            embed.add_field(name="ผู้รายงาน", value=interaction.user.mention, inline=False)
            embed.add_field(name="ผู้ถูกรายงาน", value=member.mention, inline=False)
            embed.add_field(name="เหตุผล", value=reason, inline=False)
            await mod_channel.send(embed=embed)
        
        await interaction.response.send_message("✅ รายงานสำเร็จ!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ReportSystem(bot))
    print("✅ ReportSystem Cog loaded!")
