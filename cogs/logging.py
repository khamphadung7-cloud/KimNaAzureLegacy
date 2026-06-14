import discord
from discord.ext import commands
import datetime

class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log_channel_id = None

    def get_log_channel(self, guild):
        """ค้นหา log channel"""
        return discord.utils.get(guild.text_channels, name="📋-logs")

    async def log_action(self, guild, title, description, color=0x2E64FE):
        """บันทึกการกระทำ"""
        channel = self.get_log_channel(guild)
        if not channel:
            return
        
        embed = discord.Embed(
            title=title,
            description=description,
            color=color,
            timestamp=datetime.datetime.now()
        )
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await self.log_action(
            member.guild,
            "👋 สมาชิกใหม่เข้า",
            f"{member.mention} ({member.id}) เข้ามาแล้ว\nทั้งหมด: {member.guild.member_count}",
            0x00FF00
        )

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        await self.log_action(
            member.guild,
            "👋 สมาชิกออกไป",
            f"{member.mention} ({member.id}) ออกไป\nเหลือ: {member.guild.member_count}",
            0xFF0000
        )

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return
        await self.log_action(
            message.guild,
            "🗑️ ลบข้อความ",
            f"**ผู้ส่ง:** {message.author.mention}\n**เนื้อหา:** {message.content[:100]}",
            0xFFA500
        )

async def setup(bot):
    await bot.add_cog(Logging(bot))
    print("✅ Logging Cog loaded!")
