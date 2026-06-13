import discord, io, datetime
from discord import app_commands
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        # 1. ยศอัตโนมัติ
        role = discord.utils.get(guild.roles, name="Member")
        if role: await member.add_roles(role)

        # 2. วาดรูปต้อนรับ
        try:
            bg = Image.open("welcome_bg.png").convert("RGBA")
            draw = ImageDraw.Draw(bg)
            
            # ใช้ฟอนต์ Sriracha ที่ชื่อไฟล์ TH_font.ttf
            font_size = 32
            font = ImageFont.truetype("TH_font.ttf", font_size)
            
            # พิกัดตำแหน่งข้อความ (ปรับให้เข้ากับช่องในรูปของเสี่ย)
            # x = ขวา/ซ้าย, y = บน/ล่าง
            draw.text((700, 275), f"Member #{guild.member_count}", fill=(255, 255, 255), font=font) # เข้าคนที่
            draw.text((700, 350), f"{member.name}", fill=(255, 255, 255), font=font)              # ชื่อสมาชิก
            draw.text((700, 425), f"Invite by Link", fill=(255, 255, 255), font=font)              # ใครเชิญ
            draw.text((700, 500), f"Member", fill=(255, 255, 255), font=font)                      # ยศหลัก
            
            # เวลาปัจจุบัน
            now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
            draw.text((700, 580), f"{now}", fill=(255, 255, 255), font=font)                      # ข้อมูลเวลา
            
            buf = io.BytesIO()
            bg.save(buf, format="PNG")
            buf.seek(0)
            
            channel = discord.utils.get(guild.text_channels, name="welcome")
            if channel: 
                await channel.send(f"ยินดีต้อนรับ {member.mention} สู่ {guild.name}!", file=discord.File(buf, "welcome.png"))
        except Exception as e:
            print(f"❌ ระบบต้อนรับ Error: {e}")

    @app_commands.command(name="testwelcome", description="ทดสอบระบบต้อนรับ")
    async def testwelcome(self, interaction: discord.Interaction):
        await interaction.response.send_message("กำลังสร้างรูป...", ephemeral=True)
        await self.on_member_join(interaction.user)

async def setup(bot): await bot.add_cog(Welcome(bot))
