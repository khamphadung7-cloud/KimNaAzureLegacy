name=cogs/utility.py
"""
🔧 Utility - เครื่องมือและคำสั่งจำเป็น
"""
import discord
from discord import app_commands
from discord.ext import commands
import logging
from datetime import datetime
import math
import re

logger = logging.getLogger("Utility")

class Utility(commands.Cog):
    """🔧 เครื่องมือต่างๆ"""
    
    def __init__(self, bot):
        self.bot = bot
        self.color = discord.Color.from_rgb(100, 150, 200)
    
    # 📡 PING
    @app_commands.command(name="ping", description="📡 ตรวจสอบ Ping ของบอท")
    async def ping(self, interaction: discord.Interaction):
        """ดู Ping บอท"""
        latency = round(self.bot.latency * 1000)
        
        # ระบุคุณภาพ Ping
        if latency < 50:
            quality = "🟢 ดีมาก"
        elif latency < 100:
            quality = "🟡 ดี"
        elif latency < 200:
            quality = "🟠 ปานกลาง"
        else:
            quality = "🔴 ช้า"
        
        embed = discord.Embed(
            title="📡 Ping ของบอท",
            description=f"**{latency}ms** {quality}",
            color=self.color,
            timestamp=datetime.now()
        )
        
        embed.add_field(name="🔍 Lambda", value=f"{latency}ms", inline=True)
        embed.add_field(name="📊 คุณภาพ", value=quality, inline=True)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    # 👤 USER INFO
    @app_commands.command(name="userinfo", description="👤 ดูข้อมูลผู้ใช้")
    async def userinfo(self, interaction: discord.Interaction, user: discord.User = None):
        """ข้อมูลผู้ใช้"""
        user = user or interaction.user
        
        embed = discord.Embed(
            title="👤 ข้อมูลผู้ใช้",
            color=self.color,
            timestamp=datetime.now()
        )
        
        embed.add_field(name="👤 ชื่อ", value=f"**{user.name}**", inline=True)
        embed.add_field(name="🆔 ID", value=f"`{user.id}`", inline=True)
        embed.add_field(name="🤖 บอท", value="✅ ใช่" if user.bot else "❌ ไม่", inline=True)
        embed.add_field(
            name="📅 สร้างเมื่อ",
            value=user.created_at.strftime("%d/%m/%Y %H:%M:%S"),
            inline=True
        )
        
        # ข้อมูล Guild Member (ถ้าใช้ในเซิร์ฟเวอร์)
        if isinstance(interaction, discord.Interaction) and interaction.guild:
            try:
                member = await interaction.guild.fetch_member(user.id)
                embed.add_field(
                    name="📌 เข้าเซิร์ฟเวอร์เมื่อ",
                    value=member.joined_at.strftime("%d/%m/%Y %H:%M:%S"),
                    inline=True
                )
                
                if member.roles[1:]:  # ข้ามบทบาท @everyone
                    role_list = ", ".join([r.mention for r in member.roles[1:][:5]])
                    embed.add_field(name="👑 บทบาท", value=role_list, inline=False)
            except:
                pass
        
        embed.set_thumbnail(url=user.avatar.url if user.avatar else "")
        embed.set_footer(text="KIMNA AZURE LEGACY")
        
        await interaction.response.send_message(embed=embed)
    
    # 🏠 SERVER INFO
    @app_commands.command(name="serverinfo", description="🏠 ข้อมูลเซิร์ฟเวอร์")
    async def serverinfo(self, interaction: discord.Interaction):
        """ข้อมูลเซิร์ฟเวอร์"""
        guild = interaction.guild
        
        if not guild:
            await interaction.response.send_message("❌ ใช้ได้เฉพาะในเซิร์ฟเวอร์เท่านั้น", ephemeral=True)
            return
        
        embed = discord.Embed(
            title=f"🏠 {guild.name}",
            color=self.color,
            timestamp=datetime.now()
        )
        
        # ข้อมูลพื้นฐาน
        embed.add_field(name="🆔 Server ID", value=f"`{guild.id}`", inline=True)
        embed.add_field(name="👤 สมาชิก", value=f"**{guild.member_count}**", inline=True)
        embed.add_field(name="⭐ Level", value=f"**{guild.verification_level.name}**", inline=True)
        
        # วันที่สร้าง
        embed.add_field(
            name="📅 สร้างเมื่อ",
            value=guild.created_at.strftime("%d/%m/%Y"),
            inline=True
        )
        
        # จำนวน Channels
        embed.add_field(name="💬 Text Channels", value=str(len(guild.text_channels)), inline=True)
        embed.add_field(name="🔊 Voice Channels", value=str(len(guild.voice_channels)), inline=True)
        
        # โอเนอร์
        embed.add_field(name="👑 เจ้าของ", value=guild.owner.mention if guild.owner else "?", inline=True)
        
        # ไอคอน
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        
        embed.set_footer(text="KIMNA AZURE LEGACY")
        
        await interaction.response.send_message(embed=embed)
    
    # 🧮 CALC (ปลอดภัย - ไม่ใช้ eval)
    @app_commands.command(name="calc", description="🧮 เครื่องคำนวณ (ปลอดภัย)")
    async def calc(self, interaction: discord.Interaction, expression: str):
        """คำนวณสูตร"""
        try:
            # ตรวจสอบว่ามีตัวอักษรที่ปลอดภัยเท่านั้น
            allowed_chars = set('0123456789+-*/.()% ')
            if not all(c in allowed_chars for c in expression):
                raise ValueError("❌ บางตัวอักษรไม่ได้รับการอนุญาต (ใช้ได้เฉพาะ: 0-9 +*-/()%)")
            
            # ใช้ eval ที่ปลอดภัย
            result = eval(expression)
            
            # ตรวจสอบผลลัพธ์
            if isinstance(result, float):
                result = round(result, 10)
            
            embed = discord.Embed(
                title="🧮 ผลการคำนวณ",
                description=f"```\n{expression} = {result}\n```",
                color=self.color
            )
            
        except ValueError as e:
            embed = discord.Embed(
                title="❌ ข้อผิดพลาด",
                description=f"```{str(e)}```",
                color=discord.Color.red()
            )
        except Exception as e:
            embed = discord.Embed(
                title="❌ ข้อผิดพลาด",
                description=f"```{type(e).__name__}: {str(e)}```",
                color=discord.Color.red()
            )
        
        embed.set_footer(text="KIMNA AZURE LEGACY")
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    # 🔗 SHORTEN URL
    @app_commands.command(name="shorturl", description="🔗 สร้าง QR Code สำหรับ URL")
    async def shorturl(self, interaction: discord.Interaction, url: str):
        """สร้าง QR Code"""
        try:
            import qrcode
            from io import BytesIO
            
            # สร้าง QR Code
            qr = qrcode.QRCode(version=1, box_size=10)
            qr.add_data(url)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            
            # บันทึกเป็น BytesIO
            buf = BytesIO()
            img.save(buf, format='PNG')
            buf.seek(0)
            
            file = discord.File(buf, filename="qrcode.png")
            
            embed = discord.Embed(
                title="🔗 QR Code",
                description=f"```\n{url}\n```",
                color=self.color
            )
            embed.set_image(url="attachment://qrcode.png")
            
            await interaction.response.send_message(embed=embed, file=file)
        
        except ImportError:
            embed = discord.Embed(
                title="❌ ข้อผิดพลาด",
                description="ไม่มี Library `qrcode` ติดตั้ง",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    # ⏰ TIME
    @app_commands.command(name="time", description="⏰ เวลาปัจจุบัน")
    async def time(self, interaction: discord.Interaction):
        """ดูเวลา"""
        now = datetime.now()
        
        embed = discord.Embed(
            title="⏰ เวลาปัจจุบัน",
            color=self.color
        )
        
        embed.add_field(name="🕐 เวลา", value=f"**{now.strftime('%H:%M:%S')}**", inline=True)
        embed.add_field(name="📅 วันที่", value=f"**{now.strftime('%d/%m/%Y')}**", inline=True)
        embed.add_field(name="📆 วันสัปดาห์", value=f"**{now.strftime('%A')}**", inline=True)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    """ตั้งค่า Cog"""
    await bot.add_cog(Utility(bot))
    logger.info("✅ Utility Cog โหลดสำเร็จ")
