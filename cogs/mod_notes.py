import discord
from discord.ext import commands
from discord import app_commands
import json
import os

class ModNotes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.notes_file = "mod_notes.json"
        self.load_notes()

    def load_notes(self):
        if os.path.exists(self.notes_file):
            with open(self.notes_file, 'r') as f:
                self.notes = json.load(f)
        else:
            self.notes = {}

    def save_notes(self):
        with open(self.notes_file, 'w') as f:
            json.dump(self.notes, f, indent=4)

    @app_commands.command(name="addnote", description="เพิ่มบันทึก mod")
    @app_commands.checks.has_permissions(administrator=True)
    async def addnote(self, interaction: discord.Interaction, member: discord.Member, note: str):
        user_id = str(member.id)
        if user_id not in self.notes:
            self.notes[user_id] = []
        
        self.notes[user_id].append({
            "moderator": interaction.user.id,
            "note": note,
            "timestamp": str(discord.utils.utcnow())
        })
        self.save_notes()
        
        await interaction.response.send_message(f"✅ เพิ่มบันทึกสำหรับ {member.mention}", ephemeral=True)

    @app_commands.command(name="notes", description="ดูบันทึก")
    @app_commands.checks.has_permissions(administrator=True)
    async def notes(self, interaction: discord.Interaction, member: discord.Member):
        user_id = str(member.id)
        user_notes = self.notes.get(user_id, [])
        
        if not user_notes:
            await interaction.response.send_message(f"ไม่มีบันทึกสำหรับ {member.mention}", ephemeral=True)
            return
        
        embed = discord.Embed(
            title=f"📝 บันทึก {member.name}",
            color=0x2E64FE
        )
        
        for i, note in enumerate(user_notes, 1):
            embed.add_field(name=f"#{i}", value=note["note"], inline=False)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModNotes(bot))
    print("✅ ModNotes Cog loaded!")
