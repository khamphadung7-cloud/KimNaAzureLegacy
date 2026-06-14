import discord
from discord.ext import commands
from discord import app_commands
import json
import os

class Starboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.stars_file = "starboard.json"
        self.star_threshold = 5
        self.load_stars()

    def load_stars(self):
        if os.path.exists(self.stars_file):
            with open(self.stars_file, 'r') as f:
                self.stars = json.load(f)
        else:
            self.stars = {}

    def save_stars(self):
        with open(self.stars_file, 'w') as f:
            json.dump(self.stars, f, indent=4)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if str(payload.emoji) != "⭐":
            return
        
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        
        # หาจำนวน ⭐
        star_count = 0
        for reaction in message.reactions:
            if str(reaction.emoji) == "⭐":
                star_count = reaction.count
        
        msg_id = str(payload.message_id)
        if msg_id not in self.stars and star_count >= self.star_threshold:
            # หา starboard channel
            starboard = discord.utils.get(message.guild.channels, name="⭐-starboard")
            if not starboard:
                return
            
            embed = discord.Embed(
                title=f"⭐ {star_count} Stars",
                description=message.content[:200] if message.content else "*(No text)*",
                color=0xFFD700
            )
            embed.set_author(name=message.author.name, icon_url=message.author.avatar.url)
            embed.add_field(name="Channel", value=message.channel.mention, inline=False)
            
            if message.attachments:
                embed.set_image(url=message.attachments[0].url)
            
            starred_msg = await starboard.send(embed=embed)
            self.stars[msg_id] = starred_msg.id
            self.save_stars()

async def setup(bot):
    await bot.add_cog(Starboard(bot))
    print("✅ Starboard Cog loaded!")
