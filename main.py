import discord, os, aiohttp
from discord.ext import commands
from flask import Flask
from threading import Thread
import asyncio

# Web Server สำหรับ Render
app = Flask(__name__)
@app.route('/')
def home(): return "✅ KIMNA AZURE LEGACY - RUNNING"

Thread(target=lambda: app.run(host='0.0.0.0', port=8080)).start()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

async def load_extensions():
    """โหลด Cogs ทั้งหมด"""
    loaded = 0
    failed = 0
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f"✅ Loaded: {filename}")
                loaded += 1
            except Exception as e:
                print(f"❌ Error loading {filename}: {e}")
                failed += 1
    
    print(f"\n{'='*50}")
    print(f"📊 โหลด Cogs: ✅ {loaded} สำเร็จ | ❌ {failed} ล้มเหลว")
    print(f"{'='*50}\n")

@bot.event
async def on_ready():
    """เชื่อมต่อแล้วเริ่มต้น"""
    bot.session = aiohttp.ClientSession()
    await load_extensions()
    
    # Sync commands with retry
    try:
        await asyncio.sleep(1)
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} slash commands!")
    except discord.errors.HTTPException as e:
        print(f"⚠️ Rate limited, retrying...")
        await asyncio.sleep(60)
        try:
            await bot.tree.sync()
        except Exception as e:
            print(f"❌ Sync failed: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    
    # Status
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="🎮 KIMNA AZURE | /help"
        )
    )
    
    print(f"\n{'='*50}")
    print(f"✅ บอต {bot.user} เชื่อมต่อสำเร็จ!")
    print(f"{'='*50}\n")

@bot.event
async def on_error(event, *args, **kwargs):
    """จัดการ error"""
    print(f"❌ Error in {event}: {args}")

token = os.environ.get("DISCORD_TOKEN")
if token:
    bot.run(token)
else:
    print("❌ DISCORD_TOKEN not found!")
