name=cogs/fortune_telling.py
"""
🔮 Fortune Telling - บอกดวงชะตากรรม
"""
import discord
from discord import app_commands
from discord.ext import commands
import random
import logging
from datetime import datetime

logger = logging.getLogger("FortuneTelling")

class FortuneTelling(commands.Cog):
    """🔮 ระบบบอกดวง"""
    
    def __init__(self, bot):
        self.bot = bot
        self.color = discord.Color.from_rgb(150, 75, 200)  # สีม่วง
        
        self.fortunes = {
            "love": [
                "💕 วันนี้เป็นวันดีสำหรับความรัก!",
                "💔 ความรักจะมีความท้าทายในสัปดาห์นี้",
                "💑 คู่กรรมของคุณจะปรากฏตัวในไม่ช้า",
                "😘 ความสัมพันธ์จะแข็งแกร่งขึ้น",
                "🚀 ความรักจะเลิกกว่าจินตนาการ",
            ],
            "money": [
                "💰 ภาคี่จะมาถึงในไม่ช้า!",
                "📉 ระวังการใช้จ่ายในสัปดาห์นี้",
                "💎 ลงทุนตอนนี้อาจให้ผลดี",
                "🎯 โอกาสทางการเงินมาถึง",
                "💸 ระวังค่าใช้จ่ายที่ไม่คาดคิด",
            ],
            "health": [
                "💪 สุขภาพดี! ดำเนินต่อไป",
                "😴 พักผ่อนให้มากขึ้นในสัปดาห์นี้",
                "🏃 ออกกำลังกายจะช่วยคุณ",
                "🍎 กินอาหารดีๆ เป็นสำคัญ",
                "⚠️ ระวังการเป่าลม อาจป่วย",
            ],
            "career": [
                "🚀 การเลื่อนตำแหน่งกำลังมาถึง!",
                "💼 เก็บตัวและรอโอกาส",
                "🎯 ทำความพยายามมากขึ้นจะมีผลดี",
                "📈 ธุรกิจจะเจริญรุ่งเรือง",
                "⚠️ ระวังการตัดสินใจรุนแรง",
            ],
        }
    
    @app_commands.command(name="fortune", description="🔮 บอกดวง")
    async def fortune(
        self,
        interaction: discord.Interaction,
        category: str = "love"
    ):
        """บอกดวงชะตากรรม"""
        categories = list(self.fortunes.keys())
        
        if category.lower() not in categories:
            embed = discord.Embed(
                title="❌ หมวดหมู่ไม่ถูกต้อง",
                description=f"เลือกจาก: {', '.join(categories)}",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        fortune = random.choice(self.fortunes[category.lower()])
        
        embed = discord.Embed(
            title=f"🔮 ดวงของ {interaction.user.name}",
            description=fortune,
            color=self.color,
            timestamp=datetime.now()
        )
        
        embed.add_field(name="📚 หมวดหมู่", value=category.upper(), inline=True)
        embed.add_field(name="✨ ความโชค", value="⭐" * random.randint(1, 5), inline=True)
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="zodiac", description="♈ ราศี/ดวงชะตา")
    async def zodiac(self, interaction: discord.Interaction, sign: str):
        """ดวงชะตาตามราศี"""
        zodiacs = {
            "aries": ("♈ ราศีแกะ", "21 มี.ค. - 19 เม.ย.", "กล้า เด็ดเดี่ยว มีพลังงาน"),
            "taurus": ("♉ ราศีวัว", "20 เม.ย. - 20 พ.ค.", "มั่นคง หนักแน่น ปฏิบัติตนดี"),
            "gemini": ("♊ ราศีมิถุนายน", "21 พ.ค. - 20 มิ.ย.", "ไหวพริบ พูดเพราะ ปราณีติ"),
            "cancer": ("♋ ราศีกรกฎ", "21 มิ.ย. - 22 ก.ค.", "อ่อนไหวอารมณ์ บ้านคนเก่า"),
            "leo": ("♌ ราศีสิงห์", "23 ก.ค. - 22 ส.ค.", "หน้า เจ้าเสนห์ ภาคภูมิใจ"),
            "virgo": ("♍ ราศีกันษ์", "23 ส.ค. - 22 ก.ย.", "วิเคราะห์ดี สะพานแล่น"),
            "libra": ("♎ ราศีตุลย์", "23 ก.ย. - 22 ต.ค.", "สง่างาม ชอบสิ่งสวย ยุติธรรม"),
            "scorpio": ("♏ ราศีพิจิก", "23 ต.ค. - 21 พ.ย.", "ลึกลับ มีอำนาจจิต"),
            "sagittarius": ("♐ ราศีธนู", "22 พ.ย. - 21 ธ.ค.", "รักษาตัวดี ชอบเที่ยว"),
            "capricorn": ("♑ ราศีมังกร", "22 ธ.ค. - 19 ม.ค.", "สำเร็จลัพธ์ ขยัน ต่อเนื่อง"),
            "aquarius": ("♒ ราศีกุมภ์", "20 ม.ค. - 18 ก.พ.", "อิสระ คิดแปลก ห่างไกล"),
            "pisces": ("♓ ราศีมีน", "19 ก.พ. - 20 มี.ค.", "ฝันไป อ่อนไหว จินตนาการดี"),
        }
        
        if sign.lower() not in zodiacs:
            embed = discord.Embed(
                title="❌ ราศีไม่ถูกต้อง",
                description=f"เลือกจาก: {', '.join(zodiacs.keys())}",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        name, date, traits = zodiacs[sign.lower()]
        
        embed = discord.Embed(
            title=name,
            color=self.color,
            timestamp=datetime.now()
        )
        
        embed.add_field(name="📅 วันเกิด", value=date, inline=False)
        embed.add_field(name="✨ ลักษณะ", value=traits, inline=False)
        embed.add_field(
            name="💫 ดวงชะตาวันนี้",
            value="⭐" * random.randint(2, 5),
            inline=False
        )
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(FortuneTelling(bot))
    logger.info("✅ FortuneTelling Cog")
