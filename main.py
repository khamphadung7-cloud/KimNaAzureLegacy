import discord, os, asyncio, random
from discord.ext import commands
from discord import app_commands  # <--- เสี่ยต้องใส่บรรทัดนี้เพิ่มเข้าไปครับ!
from flask import Flask
from threading import Thread

# 1. ระบบ Web Server (สำหรับให้ Render รันบอตได้ 24 ชม.)
app = Flask(__name__)
@app.route('/')
def home():
    return "✅ บอตออนไลน์ 24 ชม. ทำงานปกติ"

def run_server():
    app.run(host='0.0.0.0', port=8080)

Thread(target=run_server).start()

# 2. ตั้งค่าบอต
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ บอต {bot.user} พร้อมสุ่ม Mute คนแล้ว!")

# --- คำสั่งสุ่ม Mute (/randommute) ---
@bot.tree.command(name="randommute", description="สุ่ม Mute สมาชิกในห้องนี้ชั่วคราว")
@app_commands.checks.has_permissions(administrator=True)
async def randommute(interaction: discord.Interaction):
    await interaction.response.defer()
    
    # ดึงรายชื่อสมาชิกที่ไม่ใช่บอตและไม่ใช่อินเตอร์แอคเตอร์
    members = [m for m in interaction.channel.members if not m.bot and m.id != interaction.user.id]
    
    if not members:
        return await interaction.followup.send("❌ ไม่มีใครในห้องให้สุ่ม!")
    
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
