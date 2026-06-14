import discord
from discord.ext import commands
from discord import app_commands

class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tickets = {}

    @app_commands.command(name="ticket", description="สร้างตั๋ว Support")
    async def ticket(self, interaction: discord.Interaction, reason: str):
        guild = interaction.guild
        category = discord.utils.get(guild.categories, name="🎫 Support Tickets")
        
        if not category:
            category = await guild.create_category("🎫 Support Tickets")
        
        # สร้างช่อง
        channel = await guild.create_text_channel(
            name=f"ticket-{interaction.user.name}",
            category=category
        )
        
        # เซต permission
        await channel.set_permissions(guild.default_role, view_channel=False)
        await channel.set_permissions(interaction.user, view_channel=True)
        
        self.tickets[channel.id] = interaction.user.id
        
        embed = discord.Embed(
            title="🎫 ตั๋ว Support",
            description=f"**เรื่อง:** {reason}\n\nทีม Support จะมาช่วยในไม่ช้า!",
            color=0x2E64FE
        )
        
        await channel.send(embed=embed)
        await interaction.response.send_message(f"✅ สร้างตั๋วแล้ว: {channel.mention}", ephemeral=True)

    @app_commands.command(name="closeticket", description="ปิดตั๋ว")
    @app_commands.checks.has_permissions(administrator=True)
    async def closeticket(self, interaction: discord.Interaction):
        if interaction.channel.id not in self.tickets:
            await interaction.response.send_message("❌ นี่ไม่ใช่ช่องตั๋ว", ephemeral=True)
            return
        
        await interaction.response.send_message("⏳ กำลังปิดตั๋ว...")
        await interaction.channel.delete()
        del self.tickets[interaction.channel.id]

async def setup(bot):
    await bot.add_cog(Ticket(bot))
    print("✅ Ticket Cog loaded!")
