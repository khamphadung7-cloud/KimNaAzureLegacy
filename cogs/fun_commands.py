name=cogs/01_fun_commands.py
"""
🎮 Fun Commands - คำสั่งฟั่นๆ
"""
import discord
from discord import app_commands
from discord.ext import commands
import random
import logging
from datetime import datetime

logger = logging.getLogger("FunCommands")

class FunCommands(commands.Cog):
    """🎮 คำสั่งฟั่นๆ"""
    
    def __init__(self, bot):
        self.bot = bot
        self.color = discord.Color.from_rgb(255, 100, 150)
    
    # ทายเลข
    @app_commands.command(name="guess_number", description="🎲 ทายเลข 1-100")
    async def guess_number(self, interaction: discord.Interaction):
        """ทายเลขตั้งแต่ 1-100"""
        secret = random.randint(1, 100)
        attempts = 0
        
        embed = discord.Embed(
            title="🎲 เกมทายเลข",
            description="ลองทายเลข 1-100 กัน!",
            color=self.color
        )
        embed.add_field(name="📝 ยาว", value="ตอบมา 5 ครั้ง", inline=False)
        
        await interaction.response.send_message(embed=embed)
    
    # คำหยาบ
    @app_commands.command(name="slap", description="🤐 ตบใคร")
    async def slap(self, interaction: discord.Interaction, target: discord.Member):
        """ตบสมาชิก"""
        if target == interaction.user:
            embed = discord.Embed(
                title="🤐 ตบตัวเอง",
                description=f"{interaction.user.mention} ตบตัวเองแล้ว 😂",
                color=discord.Color.red()
            )
        else:
            embed = discord.Embed(
                title="👋 ตบ!",
                description=f"{interaction.user.mention} ตบ {target.mention} 💥",
                color=self.color
            )
        
        await interaction.response.send_message(embed=embed)
    
    # ส่วนสูง
    @app_commands.command(name="hug", description="🤗 กอด")
    async def hug(self, interaction: discord.Interaction, target: discord.Member):
        """กอดสมาชิก"""
        embed = discord.Embed(
            title="🤗 กอด!",
            description=f"{interaction.user.mention} กอด {target.mention} ❤️",
            color=discord.Color.pink()
        )
        embed.set_image(url="https://media.giphy.com/media/G3va3W1d83rE4/giphy.gif")
        
        await interaction.response.send_message(embed=embed)
    
    # ทำไข่ไก่
    @app_commands.command(name="flip_coin", description="🪙 โยนเหรียญ")
    async def flip_coin(self, interaction: discord.Interaction):
        """โยนเหรียญหัวก้อย"""
        result = random.choice(["หัว 👑", "ก้อย 🪙"])
        
        embed = discord.Embed(
            title="🪙 โยนเหรียญ",
            description=f"ผลลัพธ์: **{result}**",
            color=self.color
        )
        
        await interaction.response.send_message(embed=embed)
    
    # หยิกเหรียญ
    @app_commands.command(name="dice", description="🎲 ทอยลูกเต๋า")
    async def dice(self, interaction: discord.Interaction):
        """ทอยลูกเต๋า 1-6"""
        result = random.randint(1, 6)
        
        embed = discord.Embed(
            title="🎲 ทอยลูกเต๋า",
            description=f"ผลลัพธ์: **{result}** 🎯",
            color=self.color
        )
        
        await interaction.response.send_message(embed=embed)
    
    # ความรู้สึก
    @app_commands.command(name="feeling", description="😊 ความรู้สึก")
    async def feeling(self, interaction: discord.Interaction):
        """บอกความรู้สึก"""
        feelings = [
            "😊 ดีใจ",
            "😢 เศร้า",
            "😡 โกรธ",
            "😂 ตลก",
            "🤩 ติดใจ",
            "😴 หนวดเมื่อย",
            "🤗 มีความสุข",
            "😎 เจ้า",
            "🥰 รักใครสักคน",
            "😲 ประหลาดใจ"
        ]
        
        feeling = random.choice(feelings)
        
        embed = discord.Embed(
            title="😊 ความรู้สึก",
            description=f"ความรู้สึกของ {interaction.user.mention}: **{feeling}**",
            color=self.color
        )
        
        await interaction.response.send_message(embed=embed)
    
    # ประวัติ
    @app_commands.command(name="8ball", description="🔮 ลูกแปด")
    async def magic_8ball(self, interaction: discord.Interaction, question: str):
        """ถามลูกแปดวิเศษ"""
        answers = [
            "✅ ใช่แน่นอน",
            "❌ ไม่ใช่",
            "🤷 บางทีใช่",
            "🤔 ต้องคิดอีก",
            "💯 เชื่อได้",
            "😕 ไม่แน่",
            "🚫 ห้ามเลย",
            "✨ มีโอกาส",
        ]
        
        answer = random.choice(answers)
        
        embed = discord.Embed(
            title="🔮 ลูกแปดวิเศษ",
            description=f"❓ คำถาม: {question}\n\n💬 คำตอบ: **{answer}**",
            color=self.color
        )
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(FunCommands(bot))
    logger.info("✅ Fun Commands Cog โหลด")
