import os
import aiohttp
import asyncio
import logging
import discord
from discord.ext import commands, tasks
from flask import Flask, jsonify
from threading import Thread
from datetime import datetime
import requests

# ⚙️ ตั้งค่า Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("KimNaAzure")

# 🌐 Web Server สำหรับ Render.com Keep-Alive
app = Flask(__name__)

# 📊 สถิติ
STATS = {
    "start_time": datetime.now(),
    "ping_count": 0,
    "bot_status": "offline"
}

@app.route('/')
def home():
    """หน้าแรก"""
    uptime = (datetime.now() - STATS["start_time"]).total_seconds()
    hours = int(uptime // 3600)
    minutes = int((uptime % 3600) // 60)
    seconds = int(uptime % 60)
    
    return jsonify({
        "status": "✅ RUNNING",
        "bot_name": "KIMNA AZURE LEGACY",
        "timestamp": datetime.now().isoformat(),
        "bot_status": STATS["bot_status"],
        "uptime": f"{hours}h {minutes}m {seconds}s",
        "ping_count": STATS["ping_count"]
    }), 200

@app.route('/ping')
def ping():
    """Endpoint สำหรับการ Keep-Alive Ping"""
    STATS["ping_count"] += 1
    return jsonify({
        "message": "🏓 Pong! บอทยังมีชีวิตอยู่",
        "time": datetime.now().isoformat(),
        "ping_number": STATS["ping_count"]
    }), 200

@app.route('/status')
def status():
    """ดูสถานะบอท"""
    return jsonify({
        "bot_status": STATS["bot_status"],
        "last_ping": datetime.now().isoformat(),
        "uptime": str(datetime.now() - STATS["start_time"])
    }), 200

@app.route('/health')
def health():
    """Health Check สำหรับ Render"""
    return jsonify({"healthy": True}), 200

def run_flask():
    """รัน Flask Server ในเธรด"""
    try:
        port = int(os.environ.get("PORT", 8080))
        logger.info(f"🚀 Flask Server เริ่มต้นบน http://0.0.0.0:{port}")
        app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
    except Exception as e:
        logger.error(f"❌ Flask Error: {e}")

# 🤖 ตั้งค่า Discord Bot
intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# 📊 ตั้งค่าเริ่มต้นบอท
BOT_CONFIG = {
    "name": "KIMNA AZURE LEGACY",
    "version": "1.0.0",
    "owner": "ToneyToyau",
    "prefix": "!",
    "color": discord.Color.from_rgb(0, 150, 255)  # สีฟ้า
}

# 💰 ข้อมูลราคา
PRICING = {
    "basic": {
        "name": "แพ็คเกจพื้นฐาน",
        "price": 0,
        "features": ["คำสั่งพื้นฐาน", "ตอบสนองแบบ Real-time"]
    },
    "premium": {
        "name": "แพ็คเกจพรีเมียม",
        "price": 99,
        "features": ["ทุกอย่างใน Basic", "ระบบ Database", "Support 24/7"]
    },
    "enterprise": {
        "name": "แพ็คเกจองค์กร",
        "price": 999,
        "features": ["ทุกอย่างใน Premium", "API Custom", "ตัวแทนสนับสนุนส่วนตัว"]
    }
}

async def load_extensions():
    """โหลด Cogs ทั้งหมด"""
    loaded = 0
    failed = 0
    cogs_dir = './cogs'
    
    if not os.path.exists(cogs_dir):
        os.makedirs(cogs_dir)
        logger.warning(f"⚠️ สร้างโฟลเดอร์ {cogs_dir}")
    
    for filename in os.listdir(cogs_dir):
        if filename.endswith('.py') and not filename.startswith('_'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                logger.info(f"✅ โหลด Cog: {filename}")
                loaded += 1
            except Exception as e:
                logger.error(f"❌ โหลด Cog ล้มเหลว ({filename}): {e}")
                failed += 1
    
    logger.info(f"\n{'='*60}")
    logger.info(f"📊 ผลการโหลด Cogs: ✅ {loaded} | ❌ {failed}")
    logger.info(f"{'='*60}\n")

@bot.event
async def on_ready():
    """เมื่อบอทเชื่อมต่อสำเร็จ"""
    try:
        STATS["bot_status"] = "online"
        bot.session = aiohttp.ClientSession()
        await load_extensions()
        
        # Sync Slash Commands
        try:
            await asyncio.sleep(1)
            synced = await bot.tree.sync()
            logger.info(f"✅ Sync {len(synced)} Slash Commands!")
        except discord.errors.HTTPException:
            logger.warning("⚠️ Rate Limited - ลองใหม่ใน 60 วินาที...")
            await asyncio.sleep(60)
            try:
                await bot.tree.sync()
            except Exception as e:
                logger.error(f"❌ Sync Command ล้มเหลว: {e}")
        except Exception as e:
            logger.error(f"❌ ข้อผิดพลาด Sync: {e}")
        
        # ตั้งสถานะบอท
        await bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f"🎮 {BOT_CONFIG['name']} | /help"
            )
        )
        
        logger.info(f"\n{'='*60}")
        logger.info(f"✅ บอท {bot.user} เชื่อมต่อสำเร็จ!")
        logger.info(f"📌 ชื่อ: {BOT_CONFIG['name']}")
        logger.info(f"📌 เวอร์ชัน: {BOT_CONFIG['version']}")
        logger.info(f"{'='*60}\n")
        
        # เริ่ม Keep-Alive Task
        if not keep_alive_task.is_running():
            keep_alive_task.start()
            logger.info("✅ Keep-Alive Task เริ่มต้นแล้ว (ทุก 5 นาที)")
    
    except Exception as e:
        logger.error(f"❌ ข้อผิดพลาด on_ready: {e}")
        STATS["bot_status"] = "error"

@bot.event
async def on_error(event, *args, **kwargs):
    """จัดการ Error"""
    logger.error(f"❌ ข้อผิดพลาด [{event}]: {args}")

# 🔄 Keep-Alive Task (Ping ทุก 5 นาที)
@tasks.loop(minutes=5)
async def keep_alive_task():
    """Ping URL ตัวเองทุก 5 นาที"""
    try:
        # ดึง URL ของ Render
        render_url = os.environ.get("RENDER_EXTERNAL_URL", "http://localhost:8080")
        
        async with bot.session.get(f"{render_url}/ping") as resp:
            if resp.status == 200:
                data = await resp.json()
                logger.info(f"🏓 Keep-Alive Ping #{data.get('ping_number')}: สำเร็จ")
            else:
                logger.warning(f"⚠️ Keep-Alive ได้ Status: {resp.status}")
    except Exception as e:
        logger.warning(f"⚠️ Keep-Alive ล้มเหลว: {e}")

@keep_alive_task.before_loop
async def before_keep_alive():
    """รอให้บอทพร้อม"""
    await bot.wait_until_ready()

# 📖 Slash Command: /help
@bot.tree.command(name="help", description="📖 แสดงคำสั่งทั้งหมด")
async def help_command(interaction: discord.Interaction):
    """แสดงคำสั่ง"""
    embed = discord.Embed(
        title=f"📖 {BOT_CONFIG['name']} - ศูนย์ช่วยเหลือ",
        description="คำสั่งทั้งหมดของบอท",
        color=BOT_CONFIG["color"],
        timestamp=datetime.now()
    )
    
    embed.add_field(
        name="🎯 คำสั่งพื้นฐาน",
        value="`/help` - แสดงความช่วยเหลือ\n`/pricing` - ดูแพ็คเกจราคา\n`/info` - ข้อมูลบอท",
        inline=False
    )
    
    embed.add_field(
        name="⚙️ คำสั่ง Admin",
        value="`/reload [extension]` - โหลด Cog ใหม่",
        inline=False
    )
    
    embed.set_footer(text=f"v{BOT_CONFIG['version']}")
    
    await interaction.response.send_message(embed=embed)

# 💰 Slash Command: /pricing
@bot.tree.command(name="pricing", description="💰 ดูแพ็คเกจราคา")
async def pricing_command(interaction: discord.Interaction):
    """แสดงราคา"""
    embed = discord.Embed(
        title="💰 แพ็คเกจราคา",
        description="เลือกแพ็คเกจที่เหมาะกับคุณ",
        color=BOT_CONFIG["color"]
    )
    
    for key, package in PRICING.items():
        features = "\n".join([f"✅ {f}" for f in package['features']])
        embed.add_field(
            name=f"📦 {package['name']}",
            value=f"💵 {package['price']} บาท\n\n{features}",
            inline=False
        )
    
    await interaction.response.send_message(embed=embed)

# ℹ️ Slash Command: /info
@bot.tree.command(name="info", description="ℹ️ ข้อมูลบอท")
async def info_command(interaction: discord.Interaction):
    """แสดงข้อมูล"""
    uptime = (datetime.now() - STATS["start_time"]).total_seconds()
    hours = int(uptime // 3600)
    minutes = int((uptime % 3600) // 60)
    
    embed = discord.Embed(
        title=f"ℹ️ {BOT_CONFIG['name']}",
        color=BOT_CONFIG["color"],
        timestamp=datetime.now()
    )
    
    embed.add_field(name="📌 ชื่อ", value=BOT_CONFIG['name'], inline=True)
    embed.add_field(name="📌 เวอร์ชัน", value=BOT_CONFIG['version'], inline=True)
    embed.add_field(name="👤 เจ้าของ", value=BOT_CONFIG['owner'], inline=True)
    embed.add_field(name="⏰ Uptime", value=f"{hours}h {minutes}m", inline=True)
    embed.add_field(name="📊 Ping", value=f"{round(bot.latency * 1000)}ms", inline=True)
    embed.add_field(name="🟢 สถานะ", value=STATS["bot_status"].upper(), inline=True)
    
    await interaction.response.send_message(embed=embed)

# 🚀 เริ่มต้น
if __name__ == "__main__":
    logger.info("🚀 เริ่มต้น KIMNA AZURE LEGACY...")
    
    # เริ่ม Flask Server
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # รับ Token
    token = os.environ.get("DISCORD_TOKEN")
    if token:
        logger.info("✅ พบ DISCORD_TOKEN - กำลังเริ่มบอท...")
        bot.run(token)
    else:
        logger.error("❌ ไม่พบ DISCORD_TOKEN!")
