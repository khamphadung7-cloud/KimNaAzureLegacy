import discord
from discord import app_commands
from discord.ext import commands, tasks
from PIL import Image, ImageDraw, ImageFont, ImageOps
import io
import imageio
from datetime import datetime
import pytz

class WelcomeSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.invites = {}
        self.keep_alive_task.start()

    def cog_unload(self):
        self.keep_alive_task.cancel()

    # --- 1. ระบบกันดับ (Keep-Alive) ---
    @tasks.loop(minutes=3)
    async def keep_alive_task(self):
        print(f"🔄 [Keep-Alive] บอตยังรันอยู่: {datetime.now(pytz.timezone('Asia/Bangkok')).strftime('%H:%M:%S')}")

    # --- 2. ระบบต้อนรับสมาชิกใหม่ (Welcome) ---
    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        # เพิ่มยศอัตโนมัติ
        role = discord.utils.get(guild.roles, name="Member")
        if role: await member.add_roles(role)

        # สร้างรูป (พิกัดตามดีไซน์ที่คุยกัน)
        try:
            background = Image.open("welcome_bg.png").convert("RGBA")
            draw = ImageDraw.Draw(background)
            font_main = ImageFont.truetype("TH_font.ttf", 35)
            font_id = ImageFont.truetype("TH_font.ttf", 30)

            # แปะชื่อและข้อมูล
            draw.text((960, 185), f"{guild.name}", fill=(255, 255, 255), font=font_main, anchor="ms")
            draw.text((900, 335), f"#{len(guild.members):,}", fill=(255, 255, 255), font=font_id)
            draw.text((900, 435), f"@{member.name}", fill=(255, 255, 255), font=font_id)
            
            # ส่งรูป
            final_buffer = io.BytesIO()
            background.save(final_buffer, format="PNG")
            final_buffer.seek(0)
            channel = discord.utils.get(guild.text_channels, name="welcome")
            if channel:
                await channel.send(f"ยินดีต้อนรับ {member.mention}!", file=discord.File(final_buffer, "welcome.png"))
        except Exception as e:
            print(f"❌ Error ต้อนรับ: {e}")

    # --- 3. คำสั่ง Slash Command (/testwelcome) ---
    @app_commands.command(name="testwelcome", description="ทดสอบระบบต้อนรับ")
    @app_commands.checks.has_permissions(administrator=True)
    async def testwelcome(self, interaction: discord.Interaction):
        await interaction.response.send_message("กำลังทดสอบสร้างรูป...", ephemeral=True)
        await self.on_member_join(interaction.user)

async def setup(bot):
    await bot.add_cog(WelcomeSystem(bot))
  
