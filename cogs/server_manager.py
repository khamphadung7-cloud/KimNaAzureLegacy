import discord
from discord import app_commands
from discord.ext import commands

class ServerManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="setup_server", description="สร้างระบบห้องและยศมืออาชีพ")
    @app_commands.checks.has_permissions(administrator=True)
    async def setup_server(self, interaction: discord.Interaction):
        guild = interaction.guild
        await interaction.response.send_message("⚙️ กำลังสร้างระบบเซิร์ฟเวอร์...")

        # 1. สร้างหมวดหมู่ (Categories)
        rules_cat = await guild.create_category("📌 ข้อมูลสำคัญ")
        voice_cat = await guild.create_category("🔊 ห้องเสียง")

        # 2. สร้างห้องและประกาศกฎ
        rules_channel = await guild.create_text_channel("กฎ-ระเบียบ", category=rules_cat)
        
        embed = discord.Embed(title="📜 กฎของเซิร์ฟเวอร์", description="ยินดีต้อนรับสู่เซิร์ฟเวอร์ระดับพรีเมียม", color=0xffd700)
        await rules_channel.send(embed=embed)
        
        # 3. จัดการยศ (ลำดับความสำคัญ)
        # ตัวอย่างการสร้างยศ 25 ยศ (เสี่ยต้องวนลูปสร้างเอาครับ)
        for i in range(1, 26):
            await guild.create_role(name=f"Level {i}", hoist=True)

        await interaction.edit_original_response(content="✅ ตั้งค่าระบบเสร็จสมบูรณ์! ห้องและยศพร้อมใช้งาน")

async def setup(bot):
    await bot.add_cog(ServerManager(bot))
