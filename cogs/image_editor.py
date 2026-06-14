name=cogs/image_editor.py
"""
🎨 Image Editor - แต่งแปลงรูปภาพ
"""
import discord
from discord import app_commands
from discord.ext import commands
import aiohttp
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
from io import BytesIO
import logging

logger = logging.getLogger("ImageEditor")

class ImageEditor(commands.Cog):
    """🎨 แต่งแปลงรูป"""
    
    def __init__(self, bot):
        self.bot = bot
        self.color = discord.Color.from_rgb(255, 100, 200)
    
    async def download_image(self, url: str) -> Image.Image:
        """ดาวน์โหลดรูปภาพ"""
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                return Image.open(BytesIO(await resp.read()))
    
    @app_commands.command(name="grayscale", description="🎨 แปลงรูปเป็นขาวดำ")
    async def grayscale(self, interaction: discord.Interaction, user: discord.User = None):
        """แปลงรูปเป็นขาวดำ"""
        await interaction.response.defer()
        
        user = user or interaction.user
        avatar_url = user.avatar.url if user.avatar else None
        
        if not avatar_url:
            await interaction.followup.send("❌ ไม่พบภาพสำเร็จ", ephemeral=True)
            return
        
        try:
            img = await self.download_image(avatar_url)
            img = img.convert("L")  # แปลงเป็น Grayscale
            
            buf = BytesIO()
            img.save(buf, format='PNG')
            buf.seek(0)
            
            file = discord.File(buf, filename="grayscale.png")
            embed = discord.Embed(title="🎨 Grayscale", color=self.color)
            embed.set_image(url="attachment://grayscale.png")
            
            await interaction.followup.send(embed=embed, file=file)
        except Exception as e:
            logger.error(f"❌ Error: {e}")
            await interaction.followup.send(f"❌ {str(e)}", ephemeral=True)
    
    @app_commands.command(name="blur", description="🎨 เบลอรูป")
    async def blur(self, interaction: discord.Interaction, user: discord.User = None, radius: int = 5):
        """เบลอรูป"""
        await interaction.response.defer()
        
        user = user or interaction.user
        avatar_url = user.avatar.url if user.avatar else None
        
        if not avatar_url:
            await interaction.followup.send("❌ ไม่พบภาพ", ephemeral=True)
            return
        
        try:
            img = await self.download_image(avatar_url)
            img = img.filter(ImageFilter.GaussianBlur(radius=radius))
            
            buf = BytesIO()
            img.save(buf, format='PNG')
            buf.seek(0)
            
            file = discord.File(buf, filename="blur.png")
            embed = discord.Embed(title=f"🎨 Blur (Radius: {radius})", color=self.color)
            embed.set_image(url="attachment://blur.png")
            
            await interaction.followup.send(embed=embed, file=file)
        except Exception as e:
            await interaction.followup.send(f"❌ {str(e)}", ephemeral=True)
    
    @app_commands.command(name="invert", description="🎨 กลับสี")
    async def invert(self, interaction: discord.Interaction, user: discord.User = None):
        """กลับสี"""
        await interaction.response.defer()
        
        user = user or interaction.user
        avatar_url = user.avatar.url if user.avatar else None
        
        try:
            img = await self.download_image(avatar_url)
            img = ImageEnhance.Color(img).enhance(-1)  # Invert colors
            
            buf = BytesIO()
            img.save(buf, format='PNG')
            buf.seek(0)
            
            file = discord.File(buf, filename="invert.png")
            embed = discord.Embed(title="🎨 Inverted", color=self.color)
            embed.set_image(url="attachment://invert.png")
            
            await interaction.followup.send(embed=embed, file=file)
        except Exception as e:
            await interaction.followup.send(f"❌ {str(e)}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ImageEditor(bot))
    logger.info("✅ ImageEditor Cog")
