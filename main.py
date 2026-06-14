import discord, os, asyncio, random, aiohttp
from discord.ext import commands
from discord import app_commands
from flask import Flask
from threading import Thread

# 1. ระบบ Web Server
app = Flask(__name__)
@app.route('/')
def home(): return "✅ KIMNA AZURE ACTIVE"
Thread(target=lambda: app.run(host='0.0.0.0', port=8080)).start()

# 2. ตั้งค่าบอต
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# 3. คำสั่งสุ่ม Mute
@bot.tree.command(name="randommute", description="สุ่ม Mute สมาชิกในห้อง")
@app_commands.checks.has_permissions(administrator=True)
async def randommute(interaction: discord.Interaction):
    await interaction.response.defer()
    members = [m for m in interaction.channel.members if not m.bot and m.id != interaction.user.id]
    
    if not members:
        return await interaction.followup.send("❌ ไม่มีคนให้สุ่มในห้องนี้!")
    
    target = random.choice(members)
    mute_minutes = random.randint(1, 10)
    
    msg = await interaction.followup.send(f"⚠️ **[SYSTEM ALERT]**\nโชคร้าย! {target.mention} ถูกสุ่ม Mute เป็นเวลา **{mute_minutes} นาที**!")
    
    # ปิดการพิมพ์
    overwrite = interaction.channel.overwrites_for(target)
    overwrite.send_messages = False
    await interaction.channel.set_permissions(target, overwrite=overwrite)
    
    # รอเวลา
    await asyncio.sleep(mute_minutes * 60)
    
    # คืนสิทธิ์
    overwrite.send_messages = True
    await interaction.channel.set_permissions(target, overwrite=overwrite)
    
    # ลบประกาศ
    await asyncio.sleep(30)
    try: await msg.delete()
    except: pass

# 4. จุดเริ่มทำงาน
@bot.event
async def on_ready():
    bot.session = aiohttp.ClientSession()
    try:
        await bot.tree.sync()
        print(f"✅ บอต {bot.user} รันสมบูรณ์แบบ!")
    except Exception as e:
        print(f"❌ Error syncing: {e}")

# 5. รันบอต
token = os.environ.get("DISCORD_TOKEN")
if token:
    bot.run(token)
else:
    print("❌ ERROR: ไม่พบ DISCORD_TOKEN ใน Render!")
