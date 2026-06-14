name=cogs/ai_chat.py
"""
🤖 AI Chat - ระบบสนทนากับ AI
"""
import discord
from discord import app_commands
from discord.ext import commands
import random
import logging
from datetime import datetime

logger = logging.getLogger("AIChat")

class AIChat(commands.Cog):
    """🤖 สนทนากับ AI"""
    
    def __init__(self, bot):
        self.bot = bot
        self.color = discord.Color.from_rgb(100, 255, 100)
        self.responses = {
            "hello": ["สวัสดีครับ! 👋", "ว่าไงครับ! 😊", "หัวใจ AI ส่งมา ♻️"],
            "how": ["ผมสบายดี ขอบคุณที่ถาม! 😌", "ฟิตพอ ขอบคุณ! 💪", "ดี มีแนวโน้มตื่นตัว! ⚡"],
            "thanks": ["ยินดีครับ! 🙏", "ไม่เป็นไร ครับ!", "ด้วยความสุขใจ! 😄"],
            "bye": ["ลาก่อนครับ! 👋", "เจอกันใหม่! 😊", "ปล่อยไปก่อน! ✌️"],
        }
    
    @app_commands.command(name="ask", description="🤖 ถามคำถาม AI")
    async def ask(self, interaction: discord.Interaction, question: str):
        """ถามคำถาม AI"""
        
        responses = {
            "will": ["ใช่ที่สุด! ✅", "ไม่มั่นใจเท่าไหร่ 🤔", "อาจจะ ได้ 50/50", "ไม่เลยครับ ❌"],
            "can": ["ได้ตามทักษะ 💪", "ไม่ได้หรอก ❌", "บางทีก็ได้ ✓", "แน่นอนครับ! 🚀"],
            "should": ["ควรทำเลยครับ! ✅", "ไม่ต้องหรอก ❌", "ขึ้นอยู่กับคุณ 🤷", "ลองดูก่อน 🔍"],
        }
        
        # ตัวอักษรแรก
        for key, answers in responses.items():
            if key in question.lower():
                answer = random.choice(answers)
                
                embed = discord.Embed(
                    title=f"🤖 {question}",
                    description=f"```\n{answer}\n```",
                    color=self.color,
                    timestamp=datetime.now()
                )
                
                await interaction.response.send_message(embed=embed)
                return
        
        # Default
        default_answers = [
            "ผมยังไม่คิดออก 🤔",
            "เป็นคำถามที่ยากเลยครับ 😅",
            "ต้องคิดหน่อย ⏳",
            "ลองคิดดูเองสิ! 💭",
        ]
        
        embed = discord.Embed(
            title=f"🤖 {question}",
            description=random.choice(default_answers),
            color=self.color
        )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="joke", description="😂 บอกตลก")
    async def joke(self, interaction: discord.Interaction):
        """บอกตลก"""
        jokes = [
            "🤔 ถามว่าเหนือบ้านบอทที่ไหน? => บนเมฆ! ☁️",
            "😂 ทำไมหนูจึงก้าวไปข้างหน้า? => เพราะมันชั้นแรก! 😄",
            "🎮 ทำไมเกมเมอร์ถึงชื่น? => เพราะพวกมันชอบ 'เพลย์' ด้วย! 🎯",
            "🍕 ทำไม AI ถึงชอบพิซซ่า? => เพราะมันมี 'โปรแกรม' ในการทำ! 🔥",
            "💻 บอทบอกผีว่า: ผมไม่กลัวเธอ => เพราะผมเป็น 'ผี'ดาวน์ด้วย! 👻",
        ]
        
        embed = discord.Embed(
            title="😂 ตลกดี",
            description=random.choice(jokes),
            color=self.color
        )
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(AIChat(bot))
    logger.info("✅ AIChat Cog")
