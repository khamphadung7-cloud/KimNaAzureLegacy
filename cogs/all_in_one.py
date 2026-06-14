import discord
from discord.ext import commands
from discord import app_commands
import json
import os

class AllInOne(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config_file = "server_setup.json"
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

    @app_commands.command(name="buildserver", description="สร้าง 50+ ห้อง และตั้งค่าระบบรายห้องแบบมืออาชีพ")
    @app_commands.checks.has_permissions(administrator=True)
    async def buildserver(self, interaction: discord.Interaction):
        await interaction.response.defer()
        guild = interaction.guild
        
        embed = discord.Embed(
            title="⚙️ กำลังสร้างเซิร์ฟเวอร์...",
            description="รอซักครู่นะ...",
            color=0x2E64FE
        )
        msg = await interaction.followup.send(embed=embed)

        try:
            # 1. สร้าง Categories
            cat_info = await guild.create_category("📢┃WELCOME & INFO")
            cat_general = await guild.create_category("💬┃GENERAL")
            cat_voice = await guild.create_category("🔊┃VOICE CHANNELS")
            cat_gaming = await guild.create_category("🎮┃GAMING")
            cat_media = await guild.create_category("🎨┃MEDIA")
            cat_staff = await guild.create_category("👑┃STAFF ONLY")
            cat_archive = await guild.create_category("📦┃ARCHIVE")

            # 2. สร้างช่องข้อมูล
            rule_ch = await guild.create_text_channel("📜┃กฎระเบียบ", category=cat_info)
            await rule_ch.set_permissions(guild.default_role, send_messages=False)
            
            announce_ch = await guild.create_text_channel("📢┃ประกาศ", category=cat_info)
            verify_ch = await guild.create_text_channel("✅┃ยืนยันตัวตน", category=cat_info)
            
            # 3. สร้างช่องทั่วไป
            await guild.create_text_channel("💬┃general", category=cat_general)
            await guild.create_text_channel("📸┃memes", category=cat_general)
            await guild.create_text_channel("🎵┃music-requests", category=cat_general)
            await guild.create_text_channel("🎮┃gaming", category=cat_gaming)
            
            # 4. สร้างห้องเสียง
            await guild.create_voice_channel("🔊┃ห้องพักผ่อน", category=cat_voice, user_limit=10)
            await guild.create_voice_channel("🎮┃Gaming", category=cat_voice, user_limit=20)
            await guild.create_voice_channel("🎤┃Karaoke", category=cat_voice, user_limit=15)
            
            # 5. สร้าง Staff channels
            staff_log = await guild.create_text_channel("📋┃logs", category=cat_staff)
            await staff_log.set_permissions(guild.default_role, view_channel=False)
            
            # 6. สร้างยศ
            roles_list = []
            for i, name in enumerate(["👑 Owner", "🔱 Admin", "⚔️ Moderator", "📱 Support", "⭐ VIP", "👤 Member"], 1):
                color = discord.Color.random()
                role = await guild.create_role(name=name, color=color, hoist=True)
                roles_list.append(role)

            # 7. ส่งข้อความต้อนรับ
            embed_welcome = discord.Embed(
                title=f"🎉 ยินดีต้อนรับสู่ {guild.name}",
                description=f"""
