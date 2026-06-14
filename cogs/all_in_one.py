name=cogs/all_in_one.py
"""
🏗️ All-In-One Server Setup System
ระบบสร้างและตั้งค่าเซิร์ฟเวอร์แบบมืออาชีพ พร้อมภาษาไทย UI สวยงาม
"""
import discord
from discord.ext import commands
from discord import app_commands
import json
import os
import logging
from datetime import datetime
from typing import Optional, List

logger = logging.getLogger("AllInOne")

class AllInOne(commands.Cog):
    """🏗️ ระบบสร้างเซิร์ฟเวอร์อัตโนมัติ"""
    
    def __init__(self, bot):
        self.bot = bot
        self.config_file = "server_setup.json"
        self.color_primary = discord.Color.from_rgb(0, 150, 255)
        self.color_success = discord.Color.green()
        self.color_error = discord.Color.red()
        self.load_config()
    
    def load_config(self):
        """โหลดค่าตั้งค่าจากไฟล์"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
                logger.info(f"✅ โหลด Config จาก {self.config_file}")
            else:
                self.config = {}
                logger.warning(f"⚠️ ไฟล์ {self.config_file} ไม่พบ สร้างใหม่")
        except Exception as e:
            logger.error(f"❌ ข้อผิดพลาดในการโหลด Config: {e}")
            self.config = {}
    
    def save_config(self):
        """บันทึกค่าตั้งค่าลงไฟล์"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            logger.info(f"✅ บันทึก Config เรียบร้อย")
        except Exception as e:
            logger.error(f"❌ ข้อผิดพลาดในการบันทึก Config: {e}")
    
    def get_embed_header(self, title: str, emoji: str = "🏗️") -> discord.Embed:
        """สร้าง Embed Header มาตรฐาน"""
        embed = discord.Embed(
            title=f"{emoji} {title}",
            color=self.color_primary,
            timestamp=datetime.now()
        )
        embed.set_footer(text="KIMNA AZURE LEGACY", icon_url=self.bot.user.avatar.url if self.bot.user else "")
        return embed
    
    @app_commands.command(
        name="buildserver",
        description="🏗️ สร้างเซิร์ฟเวอร์พร้อมระบบตั้งค่าครบถ้วน"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def buildserver(self, interaction: discord.Interaction):
        """สร้างเซิร์ฟเวอร์แบบมืออาชีพ"""
        await interaction.response.defer()
        guild = interaction.guild
        
        if not guild:
            embed = self.get_embed_header("❌ ข้อผิดพลาด")
            embed.description = "ไม่สามารถใช้คำสั่งนี้ได้นอก Server"
            await interaction.followup.send(embed=embed)
            return
        
        # Embed สถานะ
        status_embed = self.get_embed_header("⚙️ กำลังสร้างเซิร์ฟเวอร์", "⏳")
        status_embed.description = "กรุณารอซักครู่... **0%**"
        status_msg = await interaction.followup.send(embed=status_embed)
        
        progress = 0
        total_steps = 8
        
        try:
            # 📁 Step 1: สร้าง Categories
            logger.info(f"📁 Step 1: สร้าง Categories สำหรับ {guild.name}")
            categories = {
                "info": await guild.create_category("📢┃ข้อมูล-ประกาศ", position=0),
                "general": await guild.create_category("💬┃ห้องทั่วไป", position=1),
                "gaming": await guild.create_category("🎮┃เกมมิ่ง", position=2),
                "media": await guild.create_category("🎨┃สื่อ-ศิลปะ", position=3),
                "voice": await guild.create_category("🔊┃ห้องเสียง", position=4),
                "staff": await guild.create_category("👑┃ทีมงาน (ไม่เปิด)", position=5),
                "archive": await guild.create_category("📦┃คลังเก่า", position=6),
            }
            progress += 1
            await self._update_status(status_msg, progress, total_steps)
            
            # 📄 Step 2: สร้าง Text Channels - Info
            logger.info("📄 Step 2: สร้าง Info Channels")
            info_channels = {
                "rules": await guild.create_text_channel("📜┃กฎระเบียบ", category=categories["info"]),
                "announce": await guild.create_text_channel("📢┃ประกาศสำคัญ", category=categories["info"]),
                "welcome": await guild.create_text_channel("👋┃ยินดีต้อนรับ", category=categories["info"]),
                "verify": await guild.create_text_channel("✅┃ยืนยันตัวตน", category=categories["info"]),
            }
            
            # ตั้งสิทธิ์ (อ่านอย่างเดียว)
            for ch in info_channels.values():
                await ch.set_permissions(guild.default_role, send_messages=False)
            
            progress += 1
            await self._update_status(status_msg, progress, total_steps)
            
            # 💬 Step 3: สร้าง General Channels
            logger.info("💬 Step 3: สร้าง General Channels")
            general_channels = {
                "general": await guild.create_text_channel("💬┃ทั่วไป", category=categories["general"]),
                "random": await guild.create_text_channel("🎲┃สุ่มเรื่อง", category=categories["general"]),
                "memes": await guild.create_text_channel("😂┃มีมส์", category=categories["general"]),
                "suggestions": await guild.create_text_channel("💡┃เสนอแนะ", category=categories["general"]),
            }
            progress += 1
            await self._update_status(status_msg, progress, total_steps)
            
            # 🎮 Step 4: สร้าง Gaming Channels
            logger.info("🎮 Step 4: สร้าง Gaming Channels")
            gaming_channels = {
                "gaming": await guild.create_text_channel("🎮┃เกม", category=categories["gaming"]),
                "tournament": await guild.create_text_channel("🏆┃แข่งขัน", category=categories["gaming"]),
                "liveplay": await guild.create_text_channel("🎬┃Live Play", category=categories["gaming"]),
            }
            progress += 1
            await self._update_status(status_msg, progress, total_steps)
            
            # 🎨 Step 5: สร้าง Media Channels
            logger.info("🎨 Step 5: สร้าง Media Channels")
            media_channels = {
                "art": await guild.create_text_channel("🎨┃ศิลปะ", category=categories["media"]),
                "music": await guild.create_text_channel("🎵┃เพลง", category=categories["media"]),
                "videos": await guild.create_text_channel("🎥┃วิดีโอ", category=categories["media"]),
            }
            progress += 1
            await self._update_status(status_msg, progress, total_steps)
            
            # 🔊 Step 6: สร้าง Voice Channels
            logger.info("🔊 Step 6: สร้าง Voice Channels")
            voice_channels = {
                "lobby": await guild.create_voice_channel("🔊┃Lobby", category=categories["voice"], user_limit=0),
                "gaming": await guild.create_voice_channel("🎮┃Gaming", category=categories["voice"], user_limit=20),
                "music": await guild.create_voice_channel("🎵┃Music", category=categories["voice"], user_limit=10),
                "karaoke": await guild.create_voice_channel("🎤┃Karaoke", category=categories["voice"], user_limit=15),
            }
            progress += 1
            await self._update_status(status_msg, progress, total_steps)
            
            # 👑 Step 7: สร้าง Staff Channels + Roles
            logger.info("👑 Step 7: สร้าง Staff & Roles")
            
            # Staff Channels
            staff_channels = {
                "logs": await guild.create_text_channel("📋┃บันทึก", category=categories["staff"]),
                "reports": await guild.create_text_channel("⚠️┃รายงาน", category=categories["staff"]),
                "announcement": await guild.create_text_channel("📢┃ประกาศภายใน", category=categories["staff"]),
            }
            
            # ตั้งสิทธิ์ Staff Channels (เฉพาะ Staff)
            for ch in staff_channels.values():
                await ch.set_permissions(guild.default_role, view_channel=False)
            
            # สร้าง Roles
            roles_config = [
                {"name": "👑 Owner", "color": (255, 0, 0), "hoist": True},
                {"name": "🔱 Admin", "color": (255, 100, 0), "hoist": True},
                {"name": "⚔️ Moderator", "color": (0, 150, 255), "hoist": True},
                {"name": "📱 Support", "color": (100, 200, 50), "hoist": True},
                {"name": "⭐ VIP", "color": (255, 215, 0), "hoist": True},
                {"name": "👤 Member", "color": (150, 150, 150), "hoist": False},
                {"name": "🤖 Bot", "color": (88, 165, 245), "hoist": True},
            ]
            
            roles_created = []
            for role_cfg in roles_config:
                role = await guild.create_role(
                    name=role_cfg["name"],
                    color=discord.Color.from_rgb(*role_cfg["color"]),
                    hoist=role_cfg["hoist"]
                )
                roles_created.append(role)
                logger.info(f"✅ สร้าง Role: {role_cfg['name']}")
            
            progress += 1
            await self._update_status(status_msg, progress, total_steps)
            
            # 🎉 Step 8: ส่งข้อความต้อนรับและสรุป
            logger.info("🎉 Step 8: ส่งข้อความต้อนรับ")
            
            welcome_embed = discord.Embed(
                title=f"🎉 ยินดีต้อนรับสู่ {guild.name}!",
                description="""
**เซิร์ฟเวอร์ของคุณเตรียมพร้อมแล้ว! ✨**

📁 **ระบบที่สร้างสำเร็จ:**
• 📢 7 Categories (หมวดหมู่)
• 💬 14 Text Channels (ห้องแชท)
• 🔊 4 Voice Channels (ห้องเสียง)
• 👑 7 Roles (ยศ/บทบาท)

**🚀 ขั้นตอนถัดไป:**
1️⃣ ไปที่ #กฎระเบียบ เพื่ออ่านกฎ
2️⃣ ไปที่ #ยืนยันตัวตน เพื่อได้รับยศ Member
3️⃣ เพลิดเพลินกับเซิร์ฟเวอร์!

💡 **Tips:** ใช้ `/help` เพื่อดูคำสั่งทั้งหมด
                """,
                color=self.color_success,
                timestamp=datetime.now()
            )
            
            welcome_embed.set_thumbnail(url=guild.icon.url if guild.icon else "")
            welcome_embed.set_footer(text="KIMNA AZURE LEGACY | Server Setup Complete")
            
            await info_channels["welcome"].send(embed=welcome_embed)
            
            # ส่ง Rules Embed
            rules_embed = discord.Embed(
                title="📜 กฎระเบียบเซิร์ฟเวอร์",
                description="""
**1️⃣ ความเคารพ**
• ให้ความเคารพกับสมาชิกทุกคน

**2️⃣ พฤติกรรม**
• ห้ามแสดงพฤติกรรมที่รุนแรง
• ห้ามสแปม หรือพิมพ์ซ้ำๆ

**3️⃣ คณุภาพ**
• ส่งเนื้อหาที่มีความหมาย
• ใช้ภาษาสุภาพ

**4️⃣ ความปลอดภัย**
• ห้ามแชร์ข้อมูลส่วนตัว
• ห้ามโพสต์เนื้อหาที่ผิดกฎหมาย
                """,
                color=self.color_primary
            )
            
            await info_channels["rules"].send(embed=rules_embed)
            
            progress = total_steps
            
            # Final Status
            final_embed = self.get_embed_header("✅ สร้างเซิร์ฟเวอร์สำเร็จ!", "🎉")
            final_embed.description = f"""
**เสร็จแล้ว! 100%**

📊 **สรุปผลลัพธ์:**
✅ Categories: {len(categories)} อัน
✅ Text Channels: {len(info_channels) + len(general_channels) + len(gaming_channels) + len(media_channels) + len(staff_channels)}
✅ Voice Channels: {len(voice_channels)} อัน
✅ Roles: {len(roles_created)} อัน

🎯 **ดูรายละเอียดได้ใน:**
• {info_channels['welcome'].mention}
• {info_channels['rules'].mention}
            """
            
            await status_msg.edit(embed=final_embed)
            
            # บันทึก Config
            self.config[str(guild.id)] = {
                "name": guild.name,
                "created_at": datetime.now().isoformat(),
                "channels": {
                    "info": {ch: ch.id for ch in info_channels},
                    "general": {ch: ch.id for ch in general_channels},
                    "gaming": {ch: ch.id for ch in gaming_channels},
                    "media": {ch: ch.id for ch in media_channels},
                    "voice": {ch: ch.id for ch in voice_channels},
                    "staff": {ch: ch.id for ch in staff_channels},
                },
                "roles": {role.name: role.id for role in roles_created}
            }
            self.save_config()
            
            logger.info(f"✅ เสร็จสิ้นการสร้างเซิร์ฟเวอร์: {guild.name}")
        
        except Exception as e:
            logger.error(f"❌ ข้อผิดพลาดในการสร้างเซิร์ฟเวอร์: {e}")
            error_embed = self.get_embed_header("❌ เกิดข้อผิดพลาด", "⚠️")
            error_embed.description = f"```{str(e)}```"
            error_embed.color = self.color_error
            await status_msg.edit(embed=error_embed)
    
    async def _update_status(self, msg: discord.Message, current: int, total: int):
        """อัปเดตสถานะความก้าวหน้า"""
        percent = int((current / total) * 100)
        embed = self.get_embed_header("⚙️ กำลังสร้างเซิร์ฟเวอร์", "⏳")
        
        # Progress Bar
        filled = int(percent / 10)
        progress_bar = "█" * filled + "░" * (10 - filled)
        
        embed.description = f"""
กรุณารอซักครู่...

`{progress_bar}` **{percent}%**

📊 ความก้าวหน้า: {current}/{total} ขั้นตอน
        """
        
        try:
            await msg.edit(embed=embed)
        except Exception as e:
            logger.warning(f"⚠️ ไม่สามารถอัปเดต Status: {e}")
    
    @app_commands.command(
        name="serverconfig",
        description="⚙️ ดูการตั้งค่าเซิร์ฟเวอร์"
    )
    async def serverconfig(self, interaction: discord.Interaction):
        """ดูการตั้งค่าเซิร์ฟเวอร์"""
        guild = interaction.guild
        guild_id = str(guild.id)
        
        if guild_id not in self.config:
            embed = self.get_embed_header("⚙️ การตั้งค่าเซิร์ฟเวอร์", "⚙️")
            embed.description = "❌ ยังไม่มีการตั้งค่า\n\nใช้ `/buildserver` เพื่อสร้างเซิร์ฟเวอร์"
            await interaction.response.send_message(embed=embed)
            return
        
        config = self.config[guild_id]
        embed = self.get_embed_header(f"⚙️ {config['name']}", "⚙️")
        
        embed.add_field(
            name="📅 สร้างเมื่อ",
            value=config['created_at'].split('T')[0],
            inline=False
        )
        
        embed.add_field(
            name="👑 Roles",
            value=f"```{', '.join(config['roles'].keys())}```",
            inline=False
        )
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    """ตั้งค่า Cog"""
    await bot.add_cog(AllInOne(bot))
    logger.info("✅ AllInOne Cog โหลดสำเร็จ")
