import discord
from discord.ext import commands

class AutoMod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.spam_users = {}
        self.bad_words = ["badword"]  # เพิ่มคำหนักแน่นตามที่ต้องการ
        self.spam_threshold = 5

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return
        
        # ตรวจสอบคำหนักแน่น
        content = message.content.lower()
        for word in self.bad_words:
            if word in content:
                try:
                    await message.delete()
                    await message.channel.send(f"⚠️ {message.author.mention} ข้อความถูกลบเพราะมีคำที่ไม่เหมาะสม", delete_after=5)
                    return
                except:
                    pass
        
        # ตรวจสอบ Spam
        user_id = message.author.id
        if user_id not in self.spam_users:
            self.spam_users[user_id] = 0
        
        self.spam_users[user_id] += 1
        
        if self.spam_users[user_id] > self.spam_threshold:
            try:
                await message.author.timeout(discord.utils.utcnow() + discord.timedelta(minutes=5))
                await message.channel.send(f"⏱️ {message.author.mention} ถูก Timeout 5 นาทีเพราะ Spam")
                self.spam_users[user_id] = 0
            except:
                pass

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot:
            return
        
        # ตรวจสอบ @everyone/@here
        if "@everyone" in after.content or "@here" in after.content:
            try:
                await after.delete()
                await after.channel.send(f"⚠️ {after.author.mention} ห้ามใช้ @everyone/@here", delete_after=5)
            except:
                pass

async def setup(bot):
    await bot.add_cog(AutoMod(bot))
    print("✅ AutoMod Cog loaded!")
