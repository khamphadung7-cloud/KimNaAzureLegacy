import discord
from discord.ext import commands
import datetime

class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_log_channel(self, guild):
        """ค้นหา log channel"""
        return discord.utils.get(guild.text_channels, name="📋-logs")

    async def log_action(self, guild, title, description, color=0x2E64FE, fields=None):
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
        
        if fields:
            for name, value in fields.items():
                embed.add_field(name=name, value=value, inline=False)
        
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await self.log_action(
            member.guild,
            "👋 สมาชิกใหม่เข้า",
            f"{member.mention}",
            0x00FF00,
            {
                "ชื่อ": member.name,
                "ID": member.id,
                "สร้างบัญชี": f"<t:{int(member.created_at.timestamp())}:R>",
                "ทั้งหมด": member.guild.member_count
            }
        )

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        await self.log_action(
            member.guild,
            "👋 สมาชิกออกไป",
            f"{member.mention}",
            0xFF0000,
            {
                "ชื่อ": member.name,
                "ID": member.id,
                "เหลือ": member.guild.member_count
            }
        )

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return
        await self.log_action(
            message.guild,
            "🗑️ ลบข้อความ",
            f"**ผู้ส่ง:** {message.author.mention}\n**ช่อง:** {message.channel.mention}",
            0xFFA500,
            {
                "เนื้อหา": message.content[:200] if message.content else "*(ไม่มีข้อความ)*",
                "Attachments": f"{len(message.attachments)}"
            }
        )

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot or before.content == after.content:
            return
        await self.log_action(
            before.guild,
            "✏️ แก้ไขข้อความ",
            f"**ผู้ส่ง:** {before.author.mention}\n**ช่อง:** {before.channel.mention}",
            0x9900FF,
            {
                "ก่อน": before.content[:100] if before.content else "*(ไม่มี)*",
                "หลัง": after.content[:100] if after.content else "*(ไม่มี)*"
            }
        )

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.roles != after.roles:
            added = set(after.roles) - set(before.roles)
            removed = set(before.roles) - set(after.roles)
            
            if added:
                await self.log_action(
                    after.guild,
                    "✅ เพิ่มยศ",
                    f"{after.mention} ได้ {', '.join([r.mention for r in added])}",
                    0x00FF00
                )
            
            if removed:
                await self.log_action(
                    after.guild,
                    "❌ ลบยศ",
                    f"{after.mention} เลิก {', '.join([r.mention for r in removed])}",
                    0xFF0000
                )

async def setup(bot):
    await bot.add_cog(Logging(bot))
    print("✅ Logging Cog loaded!")
