import discord
from discord.ext import commands, tasks

class KeepAlive(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.self_ping.start()  # เริ่มระบบยิงตัวเอง

    def cog_unload(self):
        self.self_ping.cancel() # ปิดเมื่อบอตหยุดทำงาน

    @tasks.loop(minutes=3) # ยิงตัวเองทุกๆ 3 นาที
    async def self_ping(self):
        # บอตจะอัปเดตสถานะตัวเอง เพื่อให้ระบบรู้ว่า "ยังตื่นอยู่"
        await self.bot.change_presence(activity=discord.Game(name="ระบบบริหารจัดการ 24 ชม."))
        print(f"🔄 บอตยิงตัวเอง (Self-Ping) สำเร็จแล้ว เมื่อเวลา {discord.utils.utcnow()}")

async def setup(bot):
    await bot.add_cog(KeepAlive(bot))
  
