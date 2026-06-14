"""
👋 Welcome - ระบบต้อนรับ
"""
import discord
from discord import app_commands
from discord.ext import commands
import logging

logger = logging.getLogger("Welcome")

class Welcome(commands.Cog):
    """👋 ต้อนรับ"""
    
    def __init__(self, bot):
        self.bot = bot
        self.color = discord.Color.from_rgb(100, 200, 100)
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        """เมื่อสมาชิกเข้าร่วม"""
        embed = discord.Embed(
            title=f"👋 ยินดีต้อนรับ {member.name}!",
            description=f"ยินดีต้อนรับเข้ากองทุน {member.guild.name}",
            color=self.color
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else "")
        embed.add_field(name="👥 สมาชิกคนที่", value=member.guild.member_count, inline=False)
        
        # ส่งไปแชตแรก
        for channel in member.guild.text_channels:
            if channel.permissions_for(member.guild.me).send_messages:
                await channel.send(embed=embed)
                break
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """เมื่อสมาชิกออก"""
        embed = discord.Embed(
            title=f"👋 さようなら {member.name}",
            description=f"{member.name} ออกจากเซิร์ฟเวอร์",
            color=discord.Color.red()
        )
        
        for channel in member.guild.text_channels:
            if channel.permissions_for(member.guild.me).send_messages:
                await channel.send(embed=embed)
                break

async def setup(bot):
    await bot.add_cog(Welcome(bot))
    logger.info("✅ Welcome Cog")
