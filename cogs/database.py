import sqlite3
import discord
from discord.ext import commands

class Database:
    def __init__(self, db_name="server_data.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # สร้างตารางสำหรับเก็บข้อมูลห้องและยศ
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS rooms 
                             (id INTEGER PRIMARY KEY, category_name TEXT, channel_id INTEGER)''')
        self.conn.commit()

class DatabaseCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()

async def setup(bot):
    """Discord.py ต้องการ setup function เมื่อ load extension"""
    await bot.add_cog(DatabaseCog(bot))
