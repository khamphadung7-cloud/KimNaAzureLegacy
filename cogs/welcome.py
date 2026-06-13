import discord, io
from discord import app_commands
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import pytz

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        # 1. ยศอัตโนมัติ
        role = discord.utils.get(guild.roles, name="Member")
        if role: await member.add_roles(role)

        # 2. สร้างรูป (ใช้พื้นหลัง welcome_bg.png)
        try:
            bg = Image.open("welcome_bg.png").convert("RGBA")
            draw = ImageDraw.Draw(bg)
            font = ImageFont.truetype("TH_font.ttf", 35)
            
            draw.text((960, 185), guild.name, fill=(255, 255, 255), font=font, anchor="ms")
            draw.text((900, 435), f"@{member.name}", fill=(255, 255, 255), font=font)
            
            buf = io.BytesIO()
            bg.save(buf, format="PNG")
            buf.seek(0)
            
            channel = discord.utils.get(guild.text_channels, name="welcome")
            if channel: await channel.send(f"ยินดีต้อนรับ {member.mention}!", file=discord.File(buf, "welcome.png"))
        except Exception as e:
            print(f"Error: {e}")

    @app_commands.command(name="testwelcome", description="ทดสอบระบบ")
    async def testwelcome(self, interaction: discord.Interaction):
        await interaction.response.send_message("ทดสอบการต้อนรับ...", ephemeral=True)
        await self.on_member_join(interaction.user)

async def setup(bot): await bot.add_cog(Welcome(bot))
