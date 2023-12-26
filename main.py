import discord
from discord.ext import commands
from database import Database
import asyncio

DISCORD_BOT_TOKEN = 'MTE4OTI0NDk5MjYzNjU5MjEyOA.GavR4u.QSAj02QBW9j56UsxUuJV7Vg5GwJJEqaKTQizgs'

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

async def main():
    bot = commands.Bot(command_prefix='!', intents=intents)

    database_path = 'sqlt_apis.db'
    bot.database = Database(database_path)

    @bot.event
    async def on_ready():
        print(f'Logado como {bot.user}')

    await bot.load_extension('search')

    await bot.start(DISCORD_BOT_TOKEN)

asyncio.run(main())

