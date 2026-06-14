import discord
from discord.ext import commands
from discord import app_commands

class MemberInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="userinfo", description="ดูข้อมูลสมาชิก")
    async def userinfo(self, interaction: discord.Interaction, member: discord.Member = None):
        if member is None:
            member = interaction.user
        
        embed = discord.Embed(
            title="👤 ข้อมูลสมาชิก",
            color=0x2E64FE
        )
        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(name="ชื่อ", value=member.name, inline=True)
        embed.add_field(name="ID", value=member.id, inline=True)
        embed.add_field(name="สถานะ", value=str(member.status).upper(), inline=True)
        embed.add_field(name="สร้างบัญชี", value=f"<t:{int(member.created_at.timestamp())}:R>", inline=True)
        embed.add_field(name="เข้าเซิร์ฟ", value=f"<t:{int(member.joined_at.timestamp())}:R>", inline=True)
        embed.add_field(name="ยศ", value=f"{len(member.roles)-1}", inline=True)
        
        if member.roles[1:]:
            roles_text = " ".join([r.mention for r in member.roles[1:][:5]])
            if len(member.roles) > 6:
                roles_text += f" +{len(member.roles)-6} more"
            embed.add_field(name="ยศที่ได้", value=roles_text, inline=False)
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(MemberInfo(bot))
    print("✅ MemberInfo Cog loaded!")
