import nextcord
from nextcord.ext import commands
from assets.utils.config_loader import load_config
import os
from dotenv import load_dotenv
from assets.utils.logger import Logger
logger = Logger()
# Load environment variables
load_dotenv()

config = load_config()
intents = nextcord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    logger.info(f"Bot logged in as {bot.user}", "STARTUP")

bot.load_extension("command.ls")
bot.load_extension("command.pull")
bot.load_extension("command.system_info")
bot.load_extension("command.terminal")
bot.load_extension("command.register")
bot.load_extension("command.logs")




if __name__ == "__main__":
    bot.run(config.get("token"))