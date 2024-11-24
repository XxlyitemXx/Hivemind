import nextcord
from nextcord.ext import commands
import psutil
import platform
from nextcord import Interaction, ButtonStyle
from nextcord.ui import Button, View
from assets.utils.config_loader import load_config
from assets.utils.logger import Logger
config = load_config()
logger = Logger()
class SystemInfoView(View):
    def __init__(self):
        super().__init__(timeout=60)

    @nextcord.ui.button(label="Refresh", style=ButtonStyle.green)
    async def refresh_button(self, button: Button, interaction: Interaction):
        await interaction.response.edit_message(embed=create_system_info_embed())

class SystemInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="sysinfo")
    async def system_info(self, ctx):
        logger.command(ctx.author.id, "sysinfo", "attempting")
        if ctx.author.id != int(config.get("owner_id")):
            await ctx.send("You are not authorized to use this command.")
            logger.command(ctx.author.id, "sysinfo", "failed")
            return
            
        embed = create_system_info_embed()
        view = SystemInfoView()
        await ctx.send(embed=embed, view=view)
        logger.command(ctx.author.id, "sysinfo", "completed")
def create_system_info_embed():
    embed = nextcord.Embed(
        title="System Information",
        color=nextcord.Color.blue()
    )
    
    cpu_usage = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    embed.add_field(name="CPU Usage", value=f"{cpu_usage}%", inline=True)
    embed.add_field(name="Memory Usage", value=f"{memory.percent}%", inline=True)
    embed.add_field(name="Disk Usage", value=f"{disk.percent}%", inline=True)
    
    return embed

def setup(bot):
    bot.add_cog(SystemInfo(bot))
