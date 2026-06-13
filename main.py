import discord
import os
from discord.ext import commands
from flask import Flask
from threading import Thread

# 1. ระบบ Web Server จิ๋ว (เพื่อให้ Render มองว่าเป็นเว็บไซต์)
app = Flask(__name__)
@app.route('/')
def home():
    return "✅ บอตออนไลน์ 24 ชม."

def run_server():
    app.run(host='0.0.0.0', port=8080)

# 2. เริ่มต้นรัน Web Server
server = Thread(target=run_server)
server.start()

# 3. ส่วนของบอต Discord
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    # โหลด Cogs
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and filename != "__init__.py":
            await bot.load_extension(f'cogs.{filename[:-3]}')
    
    # Sync Slash Commands
    try:
        await bot.tree.sync()
        print(f"✅ บอตออนไลน์แล้วและ Sync คำสั่ง / เรียบร้อย!")
    except Exception as e:
        print(f"❌ Error syncing: {e}")

bot.run(os.environ.get("DISCORD_TOKEN"))
