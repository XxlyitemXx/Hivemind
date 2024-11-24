import nextcord
from nextcord.ext import commands
from assets.utils.config_loader import load_config
from assets.utils.logger import Logger
import requests

logger = Logger()

config = load_config()
intents = nextcord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        public_ip = requests.get("https://api.ipify.org").text
        await bot.change_presence(
            activity=nextcord.Activity(
                type=nextcord.ActivityType.watching, name=public_ip
            )
        )
    except:
        logger.error("Could not fetch public IP address", "STARTUP")
        await bot.change_presence(
            activity=nextcord.Activity(
                type=nextcord.ActivityType.watching, name="IP Unavailable"
            )
        )
    logger.info(f"Bot logged in as {bot.user}", "STARTUP")


bot.load_extension("command.ls")
bot.load_extension("command.pull")
bot.load_extension("command.system_info")
bot.load_extension("command.terminal")
bot.load_extension("command.register")
bot.load_extension("command.logs")


if __name__ == "__main__":
    bot.run(config.get("token"))
