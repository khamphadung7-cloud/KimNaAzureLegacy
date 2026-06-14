import discord, os, aiohttp
from discord.ext import commands
from flask import Flask
from threading import Thread
import asyncio

# Web Server สำหรับ Render
app = Flask(__name__)
@app.route('/')
def home(): return "✅ KIMNA AZURE ACTIVE"
Thread(target=lambda: app.run(host='0.0.0.0', port=8080)).start()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

async def load_extensions():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f"✅ Loaded: {filename}")
            except Exception as e:
                print(f"❌ Error loading {filename}: {e}")

@bot.event
async def on_ready():
    bot.session = aiohttp.ClientSession()
    await load_extensions()
    
    # Sync with retry
    try:
        await asyncio.sleep(2)  # รอสักครู่
        await bot.tree.sync()
        print(f"✅ Synced commands!")
    except discord.errors.HTTPException as e:
        print(f"⚠️ Rate limited, retrying in 60 seconds...")
        await asyncio.sleep(60)
        await bot.tree.sync()
    
    print(f"✅ บอต {bot.user} เชื่อมต่อแล้วและดึง Cogs ครบ!")

token = os.environ.get("DISCORD_TOKEN")
if token: bot.run(token)
