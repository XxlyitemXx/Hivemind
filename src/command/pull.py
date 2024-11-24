import nextcord
import subprocess
from nextcord.ext import commands
from assets.utils.config_loader import load_config
from assets.utils.logger import Logger

config = load_config()
owner_id = config.get("owner_id")
logger = Logger()
class Pull(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="pull")
    async def pull(self, ctx, path: str):
        logger.command(ctx.author.id, f"pull {path}", "attempting")
        await ctx.send("Pulling latest changes...")
        subprocess.run(["cd", path])
        subprocess.run(["git", "init"])
        subprocess.run(["git", "pull"])
        await ctx.send("Pulled latest changes. in " + path)

def setup(bot):
    bot.add_cog(Pull(bot))