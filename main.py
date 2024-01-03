import asyncio
import discord
from discord.ext import commands
from database import Database
import aiohttp

DISCORD_BOT_TOKEN = 'MTE4OTM2NjAxNDY4OTk0NzY0OA.Ga6akp.UbaQ1BO5cZ27HvyipT_9YVRVr-3ECkyVf2P8rA'

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

async def main():
    bot = commands.Bot(command_prefix='!', intents=intents)
    database_path = 'sqlt_apis.db'
    bot.database = Database(database_path)
    bot.session = aiohttp.ClientSession()

    # Carregar as extensões (cogs)
    await bot.load_extension('search')
    await bot.load_extension('help_function')
    await bot.load_extension('movie_notifications')
    await bot.load_extension('recommend_movie')

    @bot.event
    async def on_ready():
        print(f'Logado como {bot.user}')
        movie_notifications_cog = bot.get_cog('MovieNotificationsCog')
        if movie_notifications_cog:
            await movie_notifications_cog.initialize()

    try:
        await bot.start(DISCORD_BOT_TOKEN)
    finally:
        await bot.session.close()

asyncio.run(main())