import discord
from discord.ext import commands
import config

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.all())

    async def setup_hook(self):
        # ตรงนี้เอาไว้โหลด cogs หรือ sync คำสั่ง
        await self.tree.sync()
        print("✅ บอตเริ่มทำงานแบบสะอาดแล้ว!")

bot = MyBot()
bot.run(config.TOKEN)
