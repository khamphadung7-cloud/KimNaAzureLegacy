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

@bot.event
async def on_ready():
    bot.session = aiohttp.ClientSession()
    await bot.tree.sync()
    print(f"✅ บอต {bot.user} เชื่อมต่อแล้ว!")

# 3. คำสั่งสุ่ม Mute
@bot.tree.command(name="randommute", description="สุ่ม Mute สมาชิกในห้อง")
@app_commands.checks.has_permissions(administrator=True)
async def randommute(interaction: discord.Interaction):
    await interaction.response.defer()
    members = [m for m in interaction.channel.members if not m.bot and m.id != interaction.user.id]
    if not members: return await interaction.followup.send("❌ ไม่มีคนให้สุ่ม!")
    
    target = random.choice(members)
    mute_minutes = random.randint(1, 10)
    msg = await interaction.followup.send(f"⚠️ {target.mention} โดนสุ่ม Mute **{mute_minutes} นาที**!")
    
    overwrite = interaction.channel.overwrites_for(target)
    overwrite.send_messages = False
    await interaction.channel.set_permissions(target, overwrite=overwrite)
    await asyncio.sleep(mute_minutes * 60)
    overwrite.send_messages = True
    await interaction.channel.set_permissions(target, overwrite=overwrite)
    await asyncio.sleep(30)
    try: await msg.delete()
    except: pass

# 4. ดึง Token จาก Environment เท่านั้น (ปลอดภัยที่สุด)
token = os.environ.get("DISCORD_TOKEN")
if token:
    bot.run(token)
else:
    print("❌ ERROR: ไม่พบ DISCORD_TOKEN ใน Environment Variables ของ Render!")
    
    target = random.choice(members)
    mute_minutes = random.randint(1, 10) # สุ่ม 1-10 นาที
    
    # แจ้งเตือนประกาศ
    msg = await interaction.followup.send(f"⚠️ **[SYSTEM ALERT]**\nโชคร้าย! {target.mention} ถูกสุ่ม Mute เป็นเวลา **{mute_minutes} นาที**!")
    
    # ปรับ Permission ไม่ให้พิมพ์
    overwrite = interaction.channel.overwrites_for(target)
    overwrite.send_messages = False
    await interaction.channel.set_permissions(target, overwrite=overwrite)
    
    # รอจนครบเวลา
    await asyncio.sleep(mute_minutes * 60)
    
    # คืนสิทธิ์การพิมพ์
    overwrite.send_messages = True
    await interaction.channel.set_permissions(target, overwrite=overwrite)
    await target.send(f"✅ คุณพ้นโทษ Mute ในห้อง {interaction.channel.name} แล้วครับ")
    
    # ลบข้อความประกาศหลังจากผ่านไป 30 วินาที
    await asyncio.sleep(30)
    await msg.delete()

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
