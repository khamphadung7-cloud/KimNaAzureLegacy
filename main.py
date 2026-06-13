import discord
import os
import aiohttp
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

server = Thread(target=run_server)
server.start()

# 2. ตั้งค่า Intent (ต้องใช้สำหรับการตรวจจับสมาชิกใหม่)
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    # สร้าง Session สำหรับดึงรูป
    bot.session = aiohttp.ClientSession()
    
    # โหลด Cogs จากโฟลเดอร์ cogs
    if not os.path.exists('./cogs'):
        os.makedirs('./cogs')
        
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and filename != "__init__.py":
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f"📦 โหลด Cog: {filename} สำเร็จ")
            except Exception as e:
                print(f"❌ โหลด Cog {filename} ไม่ได้: {e}")
    
    # Sync คำสั่ง Slash Command
    try:
        await bot.tree.sync()
        print(f"✅ บอตออนไลน์แล้ว! พร้อมใช้งาน Slash Commands")
    except Exception as e:
        print(f"❌ Error syncing commands: {e}")

# 3. รันบอต (ดึง Token จาก Environment Variables ของ Render)
token = os.environ.get("DISCORD_TOKEN")
if token:
    bot.run(token)
else:
    print("❌ Error: ไม่พบ DISCORD_TOKEN ใน Environment Variable ของ Render")
