import discord
from discord.ext import commands
import os
import asyncio

# ตรงนี้คือการนำค่า TOKEN มาจาก Environment Variable ของ Render (ดีกว่าเก็บไว้ในไฟล์ config)
# เสี่ยไปที่ Render Dashboard > Settings > Environment > Add Secret
# ตั้งชื่อว่า DISCORD_TOKEN แล้วใส่ค่า Token ของบอตครับ
import os
TOKEN = os.environ.get("DISCORD_TOKEN")

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.all())

    async def setup_hook(self):
        # โหลดไฟล์คำสั่งทั้งหมดจากโฟลเดอร์ cogs
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py') and filename != "__init__.py":
                await self.load_extension(f'cogs.{filename[:-3]}')
                print(f"✅ โหลดไฟล์ {filename} เรียบร้อย")
        
        # Sync คำสั่ง Slash กับ Discord
        await self.tree.sync()
        print("✅ บอตเริ่มทำงานและ Sync คำสั่งทั้งหมดแล้ว!")

bot = MyBot()
bot.run(TOKEN)
