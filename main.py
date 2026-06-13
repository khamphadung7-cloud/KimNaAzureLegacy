import discord
import os
from discord.ext import commands

# ตั้งค่า intents
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    # โหลด Cogs อัตโนมัติ
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and filename != "__init__.py":
            await bot.load_extension(f'cogs.{filename[:-3]}')
    
    # Sync Slash Commands
    try:
        await bot.tree.sync()
        print(f"✅ บอต {bot.user} ออนไลน์แล้วและ Sync คำสั่ง / เรียบร้อย!")
    except Exception as e:
        print(f"❌ Error syncing: {e}")

# รันบอตโดยใช้ Token จาก Environment Variable ใน Render
# ให้เสี่ยไปใส่ใน Render Settings > Environment > DISCORD_TOKEN
bot.run(os.environ.get("DISCORD_TOKEN"))
