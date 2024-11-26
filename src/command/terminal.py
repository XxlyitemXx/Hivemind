import nextcord
from nextcord.ext import commands
from nextcord import Interaction, ButtonStyle, TextInputStyle
from nextcord.ui import Button, View, Modal, TextInput
import subprocess
import os
from assets.utils.config_loader import load_config
from assets.utils.session_manager import SessionManager
from assets.utils.credential_manager import CredentialManager
from assets.utils.logger import Logger
import platform

config = load_config()
session_manager = SessionManager()
cred_manager = CredentialManager(config.get("registration_key"))
logger = Logger()

class LoginModal(Modal):
    def __init__(self):
        super().__init__(title="Login")
        self.username = TextInput(
            label="Username",
            placeholder="Enter username",
            required=True,
        )
        self.password = TextInput(
            label="Password",
            placeholder="Enter password",
            required=True,
            style=TextInputStyle.paragraph
        )
        self.add_item(self.username)
        self.add_item(self.password)

class CommandModal(Modal):
    def __init__(self):
        super().__init__(title="Enter Command")
        self.command = TextInput(
            label="Command",
            placeholder="Enter your command",
            required=True,
        )
        self.add_item(self.command)

class TerminalView(View):
    def __init__(self, user_id):
        super().__init__(timeout=None)
        self.user_id = user_id

    @nextcord.ui.button(label="Enter Command", style=ButtonStyle.primary)
    async def command_button(self, button: Button, interaction: Interaction):
        if not session_manager.has_active_session(self.user_id):
            await interaction.response.send_message("No active session. Please login first.", ephemeral=True)
            return

        modal = CommandModal()
        
        async def modal_callback(interaction: Interaction):
            current_dir = session_manager.get_current_dir(self.user_id)
            command = modal.command.value
            
            logger.command(self.user_id, command, "attempting")
            
            try:
                if command.startswith('venv '):
                    venv_args = command[5:].strip()
                    if venv_args == "deactivate":
                        session_manager.deactivate_venv(self.user_id)
                        await interaction.response.send_message("Virtual environment deactivated", ephemeral=True)
                        return
                    elif venv_args.startswith("activate "):
                        venv_path = os.path.join(current_dir, venv_args[9:].strip())
                        if os.path.exists(os.path.join(venv_path, "bin", "activate")):
                            session_manager.activate_venv(self.user_id, venv_path)
                            await interaction.response.send_message(f"Activated virtual environment at {venv_path}", ephemeral=True)
                            return
                        else:
                            await interaction.response.send_message("Invalid virtual environment path", ephemeral=True)
                            return
                if not os.path.isabs(current_dir):
                    current_dir = os.path.abspath(current_dir)
                
                env = os.environ.copy()
                if session_manager.is_venv_active(self.user_id):
                    venv_path = session_manager.is_venv_active(self.user_id)
                    if platform.system() == "Windows":
                        python_path = os.path.join(venv_path, "Scripts", "python.exe")
                        env["PATH"] = os.path.join(venv_path, "Scripts") + os.pathsep + env["PATH"]
                    else:
                        python_path = os.path.join(venv_path, "bin", "python")
                        env["PATH"] = os.path.join(venv_path, "bin") + os.pathsep + env["PATH"]
                    env["VIRTUAL_ENV"] = venv_path
                    if command.startswith('python '):
                        command = f"{python_path} {command[7:]}"

                system = platform.system()
                if system == "Windows":
                    process = subprocess.Popen(
                        command,
                        shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        cwd=current_dir,
                        env=env,
                        universal_newlines=True
                    )
                else:
                    process = subprocess.Popen(
                        command,
                        shell=True,
                        executable='/bin/bash',
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        cwd=current_dir,
                        env=env,
                        universal_newlines=True
                    )
                
                stdout, stderr = process.communicate()
                
                if command.startswith('cd '):
                    new_dir = command[3:].strip()
                    if new_dir == "~" or new_dir.startswith("~/"):
                        new_dir = os.path.expanduser(new_dir)
                    
                    try:
                        if os.path.isabs(new_dir):
                            if os.path.exists(new_dir):
                                session_manager.set_current_dir(self.user_id, new_dir)
                        else:
                            new_abs_path = os.path.abspath(os.path.join(current_dir, new_dir))
                            if os.path.exists(new_abs_path):
                                session_manager.set_current_dir(self.user_id, new_abs_path)
                    except Exception as e:
                        await interaction.response.send_message(f"Error changing directory: {str(e)}", ephemeral=True)
                        return

                result = stdout if stdout else stderr
                if len(result) > 2000:
                    result = result[:1997] + "..."

                embed = nextcord.Embed(
                    title="Command Output",
                    description=f"```\n{result}\n```",
                    color=nextcord.Color.green()
                )
                embed.add_field(name="Working Directory", value=current_dir)
                logger.command(self.user_id, command, "completed")
                await interaction.response.send_message(embed=embed, ephemeral=True)

            except Exception as e:
                await interaction.response.send_message(f"Error executing command: {str(e)}", ephemeral=True)
                logger.error(f"Command execution failed: {str(e)}", "TERMINAL")

        modal.callback = modal_callback
        await interaction.response.send_modal(modal)

    @nextcord.ui.button(label="Close Connection", style=ButtonStyle.danger)
    async def close_button(self, button: Button, interaction: Interaction):
        session_manager.end_session(self.user_id)
        await interaction.message.delete()

class Terminal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="terminal")
    async def terminal(self, ctx):
        if ctx.author.id != int(config.get("owner_id")):
            await ctx.send("You are not authorized to use this command.")
            return

        view = View()
        button = Button(label="Login", style=ButtonStyle.primary)

        async def button_callback(interaction: Interaction):
            modal = LoginModal()
            
            async def modal_callback(interaction: Interaction):
                success = cred_manager.verify_credentials(modal.username.value, modal.password.value)
                
                if success:
                    session_manager.create_session(ctx.author.id)
                    embed = nextcord.Embed(
                        title="Terminal Session",
                        description="Connected to terminal. Use the buttons below to interact.",
                        color=nextcord.Color.green()
                    )
                    view = TerminalView(ctx.author.id)
                    logger.auth(ctx.author.id, "terminal login", "success")
                    await interaction.response.send_message(embed=embed, view=view)
                else:
                    await interaction.response.send_message("Invalid credentials!", ephemeral=True)
                    logger.auth(ctx.author.id, "terminal login", "failed")
            modal.callback = modal_callback
            await interaction.response.send_modal(modal)

        button.callback = button_callback
        view.add_item(button)
        await ctx.send("Please click the button below to login:", view=view)

def setup(bot):
    bot.add_cog(Terminal(bot)) 