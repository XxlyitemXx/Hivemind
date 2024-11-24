import nextcord
from nextcord.ext import commands
from nextcord import Interaction, ButtonStyle, TextInputStyle
from nextcord.ui import Button, View, Modal, TextInput
from assets.utils.config_loader import load_config
from assets.utils.logger import Logger

config = load_config()
logger = Logger()

class LogKeyModal(Modal):
    def __init__(self):
        super().__init__(title="Log Access")
        self.key = TextInput(
            label="Access Key",
            placeholder="Enter log access key",
            required=True,
            style=TextInputStyle.short
        )
        self.add_item(self.key)

class LogView(View):
    def __init__(self):
        super().__init__(timeout=60)

    @nextcord.ui.button(label="Enter Key", style=ButtonStyle.primary)
    async def key_button(self, button: Button, interaction: Interaction):
        modal = LogKeyModal()
        
        async def modal_callback(interaction: Interaction):
            if modal.key.value == config.get("log_key"):
                await interaction.response.defer(ephemeral=True)
                
                logs = logger.get_logs()
                chunks = [logs[i:i+1900] for i in range(0, len(logs), 1900)]
                
                for chunk in chunks:
                    embed = nextcord.Embed(
                        title="Bot Logs",
                        description=f"```{chunk}```",
                        color=nextcord.Color.blue()
                    )
                    await interaction.user.send(embed=embed)
                
                logger.info(f"User {interaction.user.id} accessed logs", "LOGS")
                await interaction.followup.send("Logs have been sent to your DMs!", ephemeral=True)
            else:
                logger.warning(f"User {interaction.user.id} failed to access logs - invalid key", "LOGS")
                await interaction.response.send_message("Invalid key!", ephemeral=True)
        
        modal.callback = modal_callback
        await interaction.response.send_modal(modal)

class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="logs")
    async def logs(self, ctx):
        if ctx.author.id != int(config.get("owner_id")):
            logger.warning(f"Unauthorized user {ctx.author.id} attempted to access logs", "LOGS")
            await ctx.send("You are not authorized to use this command.")
            return
        
        embed = nextcord.Embed(
            title="Log Access",
            description="Click the button below to enter the log access key.",
            color=nextcord.Color.blue()
        )
        
        view = LogView()
        await ctx.send(embed=embed, view=view)

def setup(bot):
    bot.add_cog(Logs(bot)) 