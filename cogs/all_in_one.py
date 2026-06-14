import discord
from discord.ext import commands
from discord import app_commands

class AllInOne(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="buildserver", description="สร้าง 50+ ห้อง และตั้งค่าระบบรายห้องแบบมืออาชีพ")
    @app_commands.checks.has_permissions(administrator=True)
    async def buildserver(self, interaction: discord.Interaction):
        await interaction.response.send_message("⚙️ กำลังสร้างและเซตระบบรายห้อง...", ephemeral=True)
        guild = interaction.guild

        # 1. สร้างโครงสร้างหลัก
        cat_info = await guild.create_category("📢┃WELCOME & INFO")
        
        # 2. สร้างห้องและ "เซตระบบ" ทันที
        # เซตห้องกฎ: ห้ามทุกคนพิมพ์
        rule_ch = await guild.create_text_channel("📜┃กฎระเบียบ", category=cat_info)
        await rule_ch.set_permissions(guild.default_role, send_messages=False)
        
        # เซตห้องต้อนรับ
        await guild.create_text_channel("📢┃ประกาศ", category=cat_info)
        await guild.create_text_channel("👤┃ยืนยันตัวตน", category=cat_info)
        
        # เซตห้องเสียง
        cat_voice = await guild.create_category("🔊┃VOICE CHANNELS")
        voice_ch = await guild.create_voice_channel("🔊┃ห้องพักผ่อนหลัก", category=cat_voice, user_limit=10)
        
        # 3. สร้างยศ 25+ ระดับ (วนลูปสร้าง)
        for i in range(1, 26):
            await guild.create_role(name=f"Member Lvl {i}", hoist=True)

        await interaction.followup.send("✅ ตั้งค่าโครงสร้างและระบบ Permission รายห้องเสร็จสิ้น!")

    # ระบบต้อนรับอัตโนมัติ
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = discord.utils.get(member.guild.text_channels, name="📢┃ประกาศ")
        if channel:
            # ใช้ Embed สวยๆ ต้อนรับ
            embed = discord.Embed(title=f"ยินดีต้อนรับคุณ {member.name}", description="สู่ KIMNA AZURE", color=0x2E64FE)
            await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(AllInOne(bot))
