name=cogs/auto_respond.py
"""
🔄 Auto Respond - ตอบข้อความอัตโนมัติ
"""
import discord
from discord.ext import commands
import logging
import json
import os

logger = logging.getLogger("AutoRespond")

class AutoRespond(commands.Cog):
    """🔄 ตอบอัตโนมัติ"""
    
    def __init__(self, bot):
        self.bot = bot
        self.response_file = "auto_responses.json"
        self.load_responses()
    
    def load_responses(self):
        if os.path.exists(self.response_file):
            with open(self.response_file, 'r', encoding='utf-8') as f:
                self.responses = json.load(f)
        else:
            self.responses = {
                "hello": "สวัสดีครับ! 👋",
                "thanks": "ยินดีครับ! 🙏",
                "bye": "ลาก่อนครับ! 👋",
            }
            self.save_responses()
    
    def save_responses(self):
        with open(self.response_file, 'w', encoding='utf-8') as f:
            json.dump(self.responses, f, ensure_ascii=False, indent=4)
    
    @commands.Cog.listener()
    async def on_message(self, message):
        """ฟังข้อความและตอบ"""
        if message.author.bot:
            return
        
        for keyword, response in self.responses.items():
            if keyword.lower() in message.content.lower():
                embed = discord.Embed(
                    description=response,
                    color=discord.Color.from_rgb(100, 200, 255)
                )
                await message.reply(embed=embed, mention_author=False)
                break

async def setup(bot):
    await bot.add_cog(AutoRespond(bot))
    logger.info("✅ AutoRespond Cog")
