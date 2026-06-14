import discord
import asyncio
import random
from discord import app_commands
from discord.ext import commands

class RandomMute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="randommute", description="สุ่ม Mute สมาชิกในห้องนี้ชั่วคราว")
    @app_commands.checks.has_permissions(administrator=True)
    async def randommute(self, interaction: discord.Interaction):
        # 1. แจ้ง Discord ว่ากำลังทำงาน (Defer)
        await interaction.response.defer()
        
        # 2. กรองสมาชิก (เอาเฉพาะคน, ไม่เอาบอต, ไม่เอาคนสั่ง)
        members = [m for m in interaction.channel.members if not m.bot and m.id != interaction.user.id]
        
        if not members:
            return await interaction.followup.send("❌ ไม่มีใครในห้องให้สุ่ม!")
        
        target = random.choice(members)
        mute_minutes = random.randint(1, 10) 
        
        # 3. ประกาศเตือน
        msg = await interaction.followup.send(f"⚠️ **[SYSTEM MUTE]**\nโชคร้าย! {target.mention} โดนสุ่ม Mute เป็นเวลา **{mute_minutes} นาที**!")
        
        # 4. ทำการ Mute
        overwrite = interaction.channel.overwrites_for(target)
        overwrite.send_messages = False
        await interaction.channel.set_permissions(target, overwrite=overwrite)
        
        # 5. รอจนครบเวลา (ทำงานแบบ Background เพื่อไม่ให้บอตค้าง)
        await asyncio.sleep(mute_minutes * 60)
        
        # 6. ปลด Mute
        overwrite.send_messages = True
        await interaction.channel.set_permissions(target, overwrite=overwrite)
        
        # 7. เก็บงาน (ลบข้อความ)
        await asyncio.sleep(30)
        try: 
            await msg.delete()
        except: 
            pass

# ฟังก์ชันสำหรับโหลด Cog
async def setup(bot):
    await bot.add_cog(RandomMute(bot))
    print("✅ RandomMute Cog loaded successfully!")
