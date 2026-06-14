name=cogs/crypto_tracker.py
"""
🪙 Crypto Tracker - ติดตามราคาเหรียญดิจิทัล
"""
import discord
from discord import app_commands
from discord.ext import commands, tasks
import aiohttp
import logging
from datetime import datetime
from typing import Optional

logger = logging.getLogger("CryptoTracker")

class CryptoTracker(commands.Cog):
    """🪙 ระบบติดตามราคา Crypto"""
    
    def __init__(self, bot):
        self.bot = bot
        self.color = discord.Color.from_rgb(243, 102, 25)  # สีส้ม
        self.api_url = "https://api.coingecko.com/api/v3"
        self.crypto_list = ["bitcoin", "ethereum", "cardano", "solana", "ripple"]
    
    @app_commands.command(name="crypto", description="🪙 ตรวจสอบราคา Crypto")
    async def crypto(self, interaction: discord.Interaction, coin: str = "bitcoin"):
        """ดูราคา Crypto"""
        await interaction.response.defer()
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.api_url}/simple/price",
                    params={
                        "ids": coin.lower(),
                        "vs_currencies": "usd,eur,thb",
                        "include_market_cap": "true",
                        "include_24hr_vol": "true",
                        "include_24hr_change": "true"
                    }
                ) as resp:
                    data = await resp.json()
            
            if coin.lower() not in data:
                embed = discord.Embed(
                    title="❌ ไม่พบ Crypto",
                    description=f"ไม่พบ `{coin}`\n\n💡 ลองใช้: bitcoin, ethereum, cardano...",
                    color=discord.Color.red()
                )
                await interaction.followup.send(embed=embed)
                return
            
            prices = data[coin.lower()]
            
            embed = discord.Embed(
                title=f"🪙 {coin.upper()}",
                color=self.color,
                timestamp=datetime.now()
            )
            
            embed.add_field(
                name="💵 ราคา USD",
                value=f"**${prices.get('usd', 'N/A'):,.2f}**",
                inline=True
            )
            embed.add_field(
                name="🇪🇺 ราคา EUR",
                value=f"**€{prices.get('eur', 'N/A'):,.2f}**",
                inline=True
            )
            embed.add_field(
                name="🇹🇭 ราคา THB",
                value=f"**฿{prices.get('thb', 'N/A'):,.2f}**",
                inline=True
            )
            
            # Change 24h
            change_24h = prices.get('usd_24h_change', 0)
            emoji = "📈" if change_24h > 0 else "📉"
            embed.add_field(
                name=f"{emoji} เปลี่ยนแปลง 24h",
                value=f"**{change_24h:+.2f}%**",
                inline=True
            )
            
            embed.set_footer(text="KIMNA AZURE | CoinGecko API")
            
            await interaction.followup.send(embed=embed)
        
        except Exception as e:
            logger.error(f"❌ Crypto Error: {e}")
            embed = discord.Embed(
                title="❌ ข้อผิดพลาด",
                description=f"```{str(e)}```",
                color=discord.Color.red()
            )
            await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(CryptoTracker(bot))
    logger.info("✅ CryptoTracker Cog")
