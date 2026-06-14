import discord
from discord.ext import commands
from discord import app_commands

class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="ดูคำสั่งทั้งหมด")
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📚 คำสั่งทั้งหมด",
            description="🎮 **KIMNA AZURE LEGACY** Bot Commands",
            color=0x2E64FE
        )
        
        categories = {
            "⚙️ ระบบ": [
                "`/buildserver` - สร้างเซิร์ฟเวอร์",
                "`/serverinfo` - ข้อมูลเซิร์ฟเวอร์",
                "`/help` - ดูคำสั่ง"
            ],
            "👤 โปรไฟล์": [
                "`/balance` - ดูเหรียญ",
                "`/level` - ดูระดับ",
                "`/mystats` - ดูสถิติ"
            ],
            "🎮 เกม": [
                "`/dice` - ทอยลูกเต๋า",
                "`/coinflip` - พลิกเหรียญ",
                "`/8ball` - ถามลูกแม่มด",
                "`/rps` - Rock Paper Scissors"
            ],
            "👮 Mod": [
                "`/warn` - เตือน",
                "`/mute` - ปิดเสียง",
                "`/unmute` - เปิดเสียง",
                "`/kick` - Kick",
                "`/ban` - Ban"
            ],
            "💰 Economy": [
                "`/daily` - รับเหรียญรายวัน",
                "`/transfer` - ส่งเหรียญ",
                "`/richest` - คนรวยสุด"
            ]
        }
        
        for category, commands_list in categories.items():
            embed.add_field(name=category, value="\n".join(commands_list), inline=False)
        
        embed.set_footer(text="📖 พิมพ์ /help เพื่อดูคำสั่งเพิ่มเติม")
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(HelpCommand(bot))
    print("✅ HelpCommand Cog loaded!")
