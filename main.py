import discord, os, aiohttp
from discord.ext import commands
from flask import Flask
from threading import Thread

# 1. ระบบ Web Server (สำหรับกันดับบน Render)
app = Flask(__name__)
@app.route('/')
def home():
    return "✅ บอตออนไลน์ 24 ชม."

def run_server():
    app.run(host='0.0.0.0', port=8080)

# รัน Web Server แยก Thread
Thread(target=run_server).start()

# 2. ตั้งค่าบอต
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    # สร้าง Session สำหรับโหลดรูปโปรไฟล์
    bot.session = aiohttp.ClientSession()
    
    # โหลด Cog ต้อนรับ (ต้องมีไฟล์ cogs/welcome.py อยู่)
    await bot.load_extension('cogs.welcome')
    
    # Sync Slash Commands
    try:
        await bot.tree.sync()
        print(f"✅ บอตออนไลน์แล้ว! {bot.user} เชื่อมต่อแล้วและ Sync คำสั่ง / เรียบร้อย")
    except Exception as e:
        print(f"❌ Error syncing: {e}")

# 3. รันบอต (ดึง Token จาก Environment Variables)
token = os.environ.get("DISCORD_TOKEN")
if token:
    bot.run(token)
else:
    print("❌ Error: ไม่พบ DISCORD_TOKEN ใน Environment Variable ของ Render")
