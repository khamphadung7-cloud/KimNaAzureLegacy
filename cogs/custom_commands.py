import discord
from discord.ext import commands
from discord import app_commands
import json
import os

class CustomCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.commands_file = "custom_commands.json"
        self.load_commands()

    def load_commands(self):
        if os.path.exists(self.commands_file):
            with open(self.commands_file, 'r') as f:
                self.custom_cmds = json.load(f)
        else:
            self.custom_cmds = {}

    def save_commands(self):
        with open(self.commands_file, 'w') as f:
            json.dump(self.custom_cmds, f, indent=4)

    @app_commands.command(name="addcmd", description="เพิ่มคำสั่งเอง")
    @app_commands.checks.has_permissions(administrator=True)
    async def addcmd(self, interaction: discord.Interaction, name: str, response: str):
        self.custom_cmds[name.lower()] = response
        self.save_commands()
        await interaction.response.send_message(f"✅ เพิ่มคำสั่ง `{name}` แล้ว", ephemeral=True)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        
        if message.content.lower().startswith("!"):
            cmd_name = message.content[1:].split()[0].lower()
            if cmd_name in self.custom_cmds:
                await message.channel.send(self.custom_cmds[cmd_name])

async def setup(bot):
    await bot.add_cog(CustomCommands(bot))
    print("✅ CustomCommands Cog loaded!")
