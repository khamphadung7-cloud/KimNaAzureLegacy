import discord, os, aiohttp, asyncio
from discord.ext import commands
from flask import Flask
from threading import Thread

# 1. ระบบ Web Server (สำหรับให้ Render รันบอตได้ 24 ชม.)
app = Flask(__name__)
@app.route('/')
def home():
    return "✅ บอตออนไลน์ 24 ชม. ทำงานปกติ"

def run_server():
    app.run(host='0.0.0.0', port=8080)

Thread(target=run_server).start()

# 2. ตั้งค่าบอต
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# 3. ฟังก์ชันโหลดไฟล์ Cogs (รวมไฟล์ทุกไฟล์ในโฟลเดอร์ cogs อัตโนมัติ)
async def load_extensions():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

# 4. ส่วนการเริ่มทำงาน
@bot.event
async def on_ready():
    bot.session = aiohttp.ClientSession()
    
    # โหลดไฟล์คำสั่งทั้งหมด
    await load_extensions()
    
    # Sync Slash Commands (ทำให้คำสั่ง / ใช้งานได้)
    try:
        await bot.tree.sync()
        print(f"✅ บอตออนไลน์แล้ว! {bot.user} เชื่อมต่อแล้วและ Sync คำสั่ง / เรียบร้อย")
    except Exception as e:
        print(f"❌ Error syncing Slash Commands: {e}")

# 5. รันบอต (ดึง Token จาก Environment Variables)
# เสี่ยใช้จุดนี้เป็นจุดรันหลักครับ
token = os.environ.get("DISCORD_TOKEN")

if __name__ == "__main__":
    if token:
        bot.run(token)
    else:
        print("❌ Error: ไม่พบ DISCORD_TOKEN ใน Environment Variable ของ Render")
