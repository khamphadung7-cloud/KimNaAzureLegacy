import discord
from discord.ext import commands
from discord import app_commands

class AutoMod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.spam_users = {}  # {user_id: message_count}
        self.bad_words = []  # เพิ่มคำหนักแน่นที่ต้องการ

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        
        # ตรวจสอบคำหนักแน่น
        content = message.content.lower()
        for word in self.bad_words:
            if word in content:
                try:
                    await message.delete()
                    await message.channel.send(f"⚠️ {message.author.mention} ข้อความถูกลบเพราะมีคำที่ไม่เหมาะสม")
                    return
                except:
                    pass
        
        # ตรวจสอบ Spam
        user_id = message.author.id
        if user_id not in self.spam_users:
            self.spam_users[user_id] = 0
        
        self.spam_users[user_id] += 1
        
        if self.spam_users[user_id] > 5:  # 5 ข้อความในเวลาสั้น
            try:
                await message.author.timeout(discord.utils.utcnow() + discord.timedelta(minutes=5))
                await message.channel.send(f"⏱️ {message.author.mention} ถูก Timeout 5 นาทีเพราะ Spam")
                self.spam_users[user_id] = 0
            except:
                pass

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        # ตรวจสอบการแก้ไขข้อความ
        if "@everyone" in after.content or "@here" in after.content:
            try:
                await after.delete()
                await after.channel.send(f"⚠️ {after.author.mention} ห้ามใช้ @everyone/@here")
            except:
                pass

async def setup(bot):
    await bot.add_cog(AutoMod(bot))
    print("✅ AutoMod Cog loaded!")
