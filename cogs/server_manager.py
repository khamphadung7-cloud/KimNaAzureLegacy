import discord
from discord.ext import commands

class ServerManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ระบบสร้างห้องหมวดหมู่
    @commands.has_permissions(administrator=True)
    @commands.command()
    async def setup_server(self, ctx):
        guild = ctx.guild
        # สร้างหมวดหมู่
        category = await guild.create_category("📌 ข้อมูลสำคัญ")
        # สร้างห้องในหมวดหมู่
        await guild.create_text_channel("กฎ-ระเบียบ", category=category)
        await guild.create_text_channel("ประกาศ", category=category)
        await ctx.send("✅ ตั้งค่าห้องพื้นฐานเรียบร้อย!")

    # ระบบประกาศกฎแบบ Embed สวยๆ
    @commands.command()
    async def post_rules(self, ctx):
        embed = discord.Embed(
            title="📜 กฎของเซิร์ฟเวอร์",
            description="กรุณาอ่านเพื่อความเป็นระเบียบ",
            color=discord.Color.gold()
        )
        embed.add_field(name="1. ห้ามใช้คำหยาบ", value="เด็ดขาด", inline=False)
        embed.add_field(name="2. ห้ามโปรโมท", value="ทุกกรณี", inline=False)
        embed.set_footer(text="เซิร์ฟเวอร์นี้ดูแลด้วยระบบอัตโนมัติ")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(ServerManager(bot))
  
