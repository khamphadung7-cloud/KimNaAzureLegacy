import discord, asyncio, random
from discord import app_commands
from discord.ext import commands

class RandomMute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="randommute", description="สุ่ม Mute สมาชิกในห้องนี้ชั่วคราว")
    @app_commands.checks.has_permissions(administrator=True)
    async def randommute(self, interaction: discord.Interaction):
        await interaction.response.defer()
        
        # กรองเอาแค่คน ไม่เอาบอต และไม่เอาตัวคนสั่ง
        members = [m for m in interaction.channel.members if not m.bot and m.id != interaction.user.id]
        
        if not members:
            return await interaction.followup.send("❌ ไม่มีใครในห้องให้สุ่ม!")
        
        target = random.choice(members)
        mute_minutes = random.randint(1, 10) 
        
        # ประกาศเตือน
        msg = await interaction.followup.send(f"⚠️ **[SYSTEM MUTE]**\n{target.mention} โดนสุ่ม Mute เป็นเวลา **{mute_minutes} นาที**!")
        
        # Mute โดยแก้ Permission ห้องนั้น
        overwrite = interaction.channel.overwrites_for(target)
        overwrite.send_messages = False
        await interaction.channel.set_permissions(target, overwrite=overwrite)
        
        # รอเวลาครบ
        await asyncio.sleep(mute_minutes * 60)
        
        # ปลด Mute
        overwrite.send_messages = True
        await interaction.channel.set_permissions(target, overwrite=overwrite)
        
        # ลบข้อความหลังผ่านไป 30 วินาที
        await asyncio.sleep(30)
        try: await msg.delete()
        except: pass

async def setup(bot):
    await bot.add_cog(RandomMute(bot))
  
