import discord
from discord.ext import commands
from discord import app_commands

class ColorRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.colors = {
            "red": discord.Color.red(),
            "blue": discord.Color.blue(),
            "green": discord.Color.green(),
            "yellow": discord.Color.gold(),
            "purple": discord.Color.purple(),
            "pink": discord.Color.magenta()
        }

    @app_commands.command(name="color", description="เลือกสียศของคุณ")
    async def color(self, interaction: discord.Interaction, color: str):
        if color.lower() not in self.colors:
            await interaction.response.send_message(f"❌ สีไม่มี", ephemeral=True)
            return
        
        # สร้างยศสี
        color_role = discord.utils.get(
            interaction.guild.roles,
            name=f"Color-{color.upper()}"
        )
        
        if not color_role:
            color_role = await interaction.guild.create_role(
                name=f"Color-{color.upper()}",
                color=self.colors[color.lower()]
            )
        
        # ลบยศสีเก่า
        for role in interaction.user.roles:
            if role.name.startswith("Color-"):
                await interaction.user.remove_roles(role)
        
        await interaction.user.add_roles(color_role)
        await interaction.response.send_message(f"✅ เปลี่ยนสีเป็น {color.upper()}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ColorRoles(bot))
    print("✅ ColorRoles Cog loaded!")
