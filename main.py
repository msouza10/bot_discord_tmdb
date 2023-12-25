import discord
from discord.ext import commands


TMDB_API_KEY = '8a37598beeaadf71a6ceb69d96f9714d'

DISCORD_BOT_TOKEN = 'MTE1NTk4NzYxOTk5MDIyNDk2Ng.G7yoKd.9dhgPl_gxgrVi27rgkj0IVrUAsBmn9hxULaugw'


intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
bot.tmdb_api_key = TMDB_API_KEY

@bot.event
async def on_ready():
    print(f'Logado como {bot.user}')
    await bot.load_extension('search')

bot.run(DISCORD_BOT_TOKEN)
