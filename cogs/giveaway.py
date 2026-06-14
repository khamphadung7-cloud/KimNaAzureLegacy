import discord
from discord.ext import commands
from discord import app_commands
import random
import asyncio

class Giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.giveaways = {}

    @app_commands.command(name="giveaway", description="สร้างการจับรางวัล")
    @app_commands.checks.has_permissions(administrator=True)
    async def giveaway(self, interaction: discord.Interaction, prize: str, duration: int, winners: int = 1):
        await interaction.response.defer()
        
        embed = discord.Embed(
            title="🎁 การจับรางวัล",
            description=f"**รางวัล:** {prize}\n**ผู้ชนะ:** {winners}\n\nกดปุ่มด้านล่างเพื่อเข้าร่วม!",
            color=0xFF00FF
        )
        
        msg = await interaction.channel.send(embed=embed)
        
        # ใช้ reaction
        await msg.add_reaction("🎉")
        
        self.giveaways[msg.id] = {
            "prize": prize,
            "winners": winners,
            "duration": duration,
            "channel": interaction.channel.id
        }
        
        await asyncio.sleep(duration)
        
        # เลือกผู้ชนะ
        try:
            reaction = discord.utils.get(msg.reactions, emoji="🎉")
            if reaction:
                participants = [u async for u in reaction.users() if not u.bot]
                
                if participants:
                    giveaway_winners = random.sample(participants, min(winners, len(participants)))
                    winner_text = " ".join([u.mention for u in giveaway_winners])
                    
                    embed = discord.Embed(
                        title="🎊 ผู้ชนะ!",
                        description=f"{winner_text}\n**รางวัล:** {prize}",
                        color=0x00FF00
                    )
                    await interaction.channel.send(embed=embed)
                else:
                    await interaction.channel.send("❌ ไม่มีผู้เข้าร่วม")
        except:
            pass
        
        if msg.id in self.giveaways:
            del self.giveaways[msg.id]

async def setup(bot):
    await bot.add_cog(Giveaway(bot))
    print("✅ Giveaway Cog loaded!")
