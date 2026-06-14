name=main.py
import discord
import os
import aiohttp
import asyncio
import logging
from discord.ext import commands, tasks
from flask import Flask
from threading import Thread
from datetime import datetime

# ⚙️ ตั้งค่า Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("KimNaAzure")

# 🌐 Web Server สำหรับ Keep-Alive (Render.com)
app = Flask(__name__)

@app.route('/')
def home():
    return {
        "status": "✅ RUNNING",
        "bot_name": "KIMNA AZURE LEGACY",
        "timestamp": datetime.now().isoformat()
    }, 200

@app.route('/ping')
def ping():
    """Endpoint สำหรับการ Ping URL ทุก 1 นาที"""
    return {"message": "🏓 Pong! บอทยังมีชีวิตอยู่", "time": datetime.now().isoformat()}, 200

def run_flask():
    """รัน Flask Server ในเธรด"""
    try:
        logger.info("🚀 Flask Server เริ่มต้นบน http://0.0.0.0:8080")
        app.run(host='0.0.0.0', port=8080, debug=False)
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
    "color": discord.Color.from_rgb(0, 150, 255)  # สีฟ้าสวย
}

# 💰 ข้อมูลราคา (ปรับได้)
PRICING = {
    "basic": {"name": "แพ็คเกจพื้นฐาน", "price": 0, "features": ["คำสั่งพื้นฐาน", "ตอบสนองแบบ Real-time"]},
    "premium": {"name": "แพ็คเกจพรีเมียม", "price": 99, "features": ["ทุกอย่างใน Basic", "ระบบ Database", "Support 24/7"]},
    "enterprise": {"name": "แพ็คเกจองค์กร", "price": 999, "features": ["ทุกอย่างใน Premium", "API Custom", "ตัวแทนสนับสนุนส่วนตัว"]}
}

async def load_extensions():
    """โหลด Cogs ทั้งหมดจากโฟลเดอร์ cogs"""
    loaded = 0
    failed = 0
    cogs_dir = './cogs'
    
    if not os.path.exists(cogs_dir):
        os.makedirs(cogs_dir)
        logger.warning(f"⚠️ สร้างโฟลเดอร์ {cogs_dir} ใหม่")
    
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
    logger.info(f"📊 ผลการโหลด Cogs: ✅ {loaded} สำเร็จ | ❌ {failed} ล้มเหลว")
    logger.info(f"{'='*60}\n")

@bot.event
async def on_ready():
    """เมื่อบอทเชื่อมต่อสำเร็จ"""
    try:
        bot.session = aiohttp.ClientSession()
        await load_extensions()
        
        # Sync Slash Commands
        try:
            await asyncio.sleep(1)
            synced = await bot.tree.sync()
            logger.info(f"✅ Sync {len(synced)} Slash Commands!")
        except discord.errors.HTTPException:
            logger.warning("⚠️ Rate Limited - จะลองใหม่ใน 60 วินาที...")
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
        logger.info(f"📌 เจ้าของ: {BOT_CONFIG['owner']}")
        logger.info(f"{'='*60}\n")
        
        # เริ่ม Keep-Alive Task
        if not keep_alive_task.is_running():
            keep_alive_task.start()
            logger.info("✅ Keep-Alive Task เริ่มต้นแล้ว")
    
    except Exception as e:
        logger.error(f"❌ ข้อผิดพลาด on_ready: {e}")

@bot.event
async def on_error(event, *args, **kwargs):
    """จัดการ Error ที่เกิดขึ้น"""
    logger.error(f"❌ ข้อผิดพลาด [{event}]: {args}")

# 🔄 Task สำหรับ Keep-Alive (Ping URL ทุก 1 นาที)
@tasks.loop(minutes=1)
async def keep_alive_task():
    """Ping URL ทุก 1 นาที เพื่อให้บอทไม่หลับ"""
    try:
        if bot.session:
            async with bot.session.get('http://localhost:8080/ping') as resp:
                data = await resp.json()
                logger.info(f"🏓 Keep-Alive Ping สำเร็จ: {data.get('message')}")
    except Exception as e:
        logger.warning(f"⚠️ Keep-Alive Ping ล้มเหลว: {e}")

@keep_alive_task.before_loop
async def before_keep_alive():
    """รอให้บอทพร้อมก่อน"""
    await bot.wait_until_ready()

# 🎨 Slash Command - /help (แสดงคำสั่ง)
@bot.tree.command(name="help", description="📖 แสดงคำสั่งทั้งหมดของบอท")
async def help_command(interaction: discord.Interaction):
    """แสดงคำสั่งพื้นฐาน"""
    embed = discord.Embed(
        title=f"📖 {BOT_CONFIG['name']} - ศูนย์ช่วยเหลือ",
        description="คำสั่งทั้งหมดของบอทนี้",
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
    
    embed.set_footer(text=f"v{BOT_CONFIG['version']} | เจ้าของ: {BOT_CONFIG['owner']}")
    
    await interaction.response.send_message(embed=embed)

# 💰 Slash Command - /pricing (แสดงราคา)
@bot.tree.command(name="pricing", description="💰 ดูแพ็คเกจราคาและฟีเจอร์")
async def pricing_command(interaction: discord.Interaction):
    """แสดงแพ็คเกจราคา"""
    embed = discord.Embed(
        title="💰 แพ็คเกจราคาและฟีเจอร์",
        description="เลือกแพ็คเกจที่เหมาะกับคุณ",
        color=BOT_CONFIG["color"]
    )
    
    for key, package in PRICING.items():
        features_text = "\n".join([f"✅ {feature}" for feature in package['features']])
        embed.add_field(
            name=f"📦 {package['name']}",
            value=f"💵 ราคา: {package['price']} บาท\n\n{features_text}",
            inline=False
        )
    
    embed.set_footer(text="📞 ติดต่อสอบถามเพิ่มเติมได้ที่: Support Server")
    
    await interaction.response.send_message(embed=embed)

# ℹ️ Slash Command - /info (ข้อมูลบอท)
@bot.tree.command(name="info", description="ℹ️ ข้อมูลเกี่ยวกับบอท")
async def info_command(interaction: discord.Interaction):
    """แสดงข้อมูลบอท"""
    embed = discord.Embed(
        title=f"ℹ️ {BOT_CONFIG['name']}",
        description=f"บอท Discord ชั้นเยี่ยมของคุณ",
        color=BOT_CONFIG["color"],
        timestamp=datetime.now()
    )
    
    embed.add_field(name="📌 ชื่อบอท", value=BOT_CONFIG['name'], inline=True)
    embed.add_field(name="📌 เวอร์ชัน", value=BOT_CONFIG['version'], inline=True)
    embed.add_field(name="👤 เจ้าของ", value=BOT_CONFIG['owner'], inline=True)
    embed.add_field(name="📚 Library", value="discord.py", inline=True)
    embed.add_field(name="⏰ สถานะ", value="🟢 Online", inline=True)
    embed.add_field(name="📊 Ping", value=f"{round(bot.latency * 1000)}ms", inline=True)
    
    embed.set_thumbnail(url=bot.user.avatar.url if bot.user else "")
    embed.set_footer(text=f"เวลา: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    await interaction.response.send_message(embed=embed)

# 🚀 เริ่มต้นบอท
if __name__ == "__main__":
    # เริ่มต้น Flask Server ในเธรด
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()
    logger.info("🚀 Flask Server Thread เริ่มต้นแล้ว")
    
    # รับ Token และเริ่มบอท
    token = os.environ.get("DISCORD_TOKEN")
    if token:
        logger.info("✅ พบ DISCORD_TOKEN - กำลังเริ่มบอท...")
        bot.run(token)
    else:
        logger.error("❌ ไม่พบ DISCORD_TOKEN ในตัวแปร Environment!")
