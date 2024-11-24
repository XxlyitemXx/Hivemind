import nextcord
import subprocess
from nextcord.ext import commands
from assets.utils.config_loader import load_config
from assets.utils.logger import Logger

config = load_config()
owner_id = config.get("owner_id")
logger = Logger()
class Ls(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ls")
    async def ls(self, ctx, path: str):
        logger.command(ctx.author.id, f"ls {path}", "attempting")
        if ctx.author.id != owner_id:
            await ctx.send("You are not allowed to use this bot")
        if path == "":
            path = "/"
        await ctx.send("Listing files in " + path)
        process = subprocess.Popen("ls -la " + path, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        await ctx.send(stdout.decode("utf-8"))

def setup(bot):
    bot.add_cog(Ls(bot))