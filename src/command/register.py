import nextcord
from nextcord.ext import commands
from nextcord import Interaction, TextInputStyle, ButtonStyle
from nextcord.ui import Modal, TextInput, View, Button
from assets.utils.config_loader import load_config
from assets.utils.credential_manager import CredentialManager
from assets.utils.logger import Logger
config = load_config()
logger = Logger()
cred_manager = CredentialManager(config.get("registration_key"))

class RegisterModal(Modal):
    def __init__(self):
        super().__init__(title="Register Terminal User")
        
        self.username = TextInput(
            label="Username",
            placeholder="Enter desired username",
            required=True,
            min_length=3,
            max_length=32
        )
        
        self.password = TextInput(
            label="Password",
            placeholder="Enter secure password",
            required=True,
            min_length=8,
            style=TextInputStyle.short
        )

        self.reg_key = TextInput(
            label="Registration Key",
            placeholder="Enter registration key",
            required=True,
            style=TextInputStyle.paragraph
        )

        self.add_item(self.username)
        self.add_item(self.password)
        self.add_item(self.reg_key)

    async def callback(self, interaction: Interaction):
        # Check registration key
        if self.reg_key.value != config.get("registration_key"):
            await interaction.response.send_message("Invalid registration key.", ephemeral=True)
            return
        
        # Register the user
        success, message = cred_manager.register_user(
            self.username.value, 
            self.password.value,
            self.reg_key.value
        )
        
        if success:
            logger.auth(interaction.user.id, "registration", "success")
            await interaction.response.send_message("User registered successfully!", ephemeral=True)
        else:
            await interaction.response.send_message(f"Registration failed: {message}", ephemeral=True)
            logger.auth(interaction.user.id, "registration", "failed")
class Register(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="register")
    async def register(self, ctx):
        if ctx.author.id != int(config.get("owner_id")):
            await ctx.send("You are not authorized to register new users.")
            return

        # Create a view with a button
        view = View()
        button = Button(label="Register", style=ButtonStyle.primary)

        async def button_callback(interaction: Interaction):
            modal = RegisterModal()
            await interaction.response.send_modal(modal)

        button.callback = button_callback
        view.add_item(button)
        await ctx.send("Click to register a new user:", view=view)

def setup(bot):
    bot.add_cog(Register(bot)) 