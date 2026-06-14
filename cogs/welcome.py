import discord, io, datetime
from discord import app_commands
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import json, os

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config_file = "welcome_config.json"
        self.load_config()

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {}

    def save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)

    @app_commands.command(name="setwelcomemessage", description="เซตข้อความต้อนรับ")
    @app_commands.checks.has_permissions(administrator=True)
    async def setwelcomemessage(self, interaction: discord.Interaction, message: str):
        guild_id = str(interaction.guild.id)
        if guild_id not in self.config:
            self.config[guild_id] = {}
        self.config[guild_id]['welcome_message'] = message
        self.save_config()
        await interaction.response.send_message(f"✅ เซตข้อความต้อนรับแล้ว", ephemeral=True)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        guild_id = str(guild.id)
        
        # ข้อความต้อนรับ
        config = self.config.get(guild_id, {})
        welcome_msg = config.get('welcome_message', f'ยินดีต้อนรับ {member.mention}')
        
        channel = discord.utils.get(guild.text_channels, name="welcome") or discord.utils.get(guild.text_channels, name="📢-ประกาศ")
        if channel:
            embed = discord.Embed(
                title="👋 ยินดีต้อนรับ",
                description=f"{member.mention}\n{welcome_msg}",
                color=0x2E64FE
            )
            embed.set_thumbnail(url=member.avatar.url)
            embed.add_field(name="สมาชิกคนที่", value=f"#{guild.member_count}", inline=True)
            embed.add_field(name="สร้างบัญชี", value=f"<t:{int(member.created_at.timestamp())}:R>", inline=True)
            await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Welcome(bot))
    print("✅ Welcome Cog loaded!")
