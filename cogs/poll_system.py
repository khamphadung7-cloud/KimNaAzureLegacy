import discord
from discord.ext import commands
from discord import app_commands
import asyncio

class PollSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="poll", description="สร้างสำรวจความคิดเห็น")
    async def poll(self, interaction: discord.Interaction, question: str, option1: str, option2: str, option3: str = None):
        embed = discord.Embed(
            title="📊 สำรวจความคิดเห็น",
            description=f"**{question}**",
            color=0x2E64FE
        )
        
        options = [f"1️⃣ {option1}", f"2️⃣ {option2}"]
        if option3:
            options.append(f"3️⃣ {option3}")
        
        embed.add_field(name="ตัวเลือก", value="\n".join(options), inline=False)
        
        msg = await interaction.response.send_message(embed=embed)
        
        await msg.add_reaction("1️⃣")
        await msg.add_reaction("2️⃣")
        if option3:
            await msg.add_reaction("3️⃣")

async def setup(bot):
    await bot.add_cog(PollSystem(bot))
    print("✅ PollSystem Cog loaded!")
