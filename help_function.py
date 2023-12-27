import discord
from discord.ext import commands

class BotEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        owner = guild.owner
        if owner:
            try:
                await owner.send(f"Olá {owner.name}! Obrigado por adicionar o FilmeBot ao seu servidor! "
                                 "Use o comando `!ajuda` para ver a lista de comandos disponíveis.")
            except discord.errors.Forbidden:
                print(f"Não foi possível enviar DM para o dono do servidor {guild.name}.")

    @commands.command(name='ajuda')
    async def help_command(self, ctx):
        help_text = ("Aqui estão os comandos que você pode usar:\n"
                     "`!configurar_api`: Configura sua chave da API do TMDb.\n"
                     "`!filme <titulo>`: Busca informações sobre um filme.\n"
                     "`!top_filmes [N]`: Mostra os top N filmes mais bem avaliados. Exemplo: `!top_filmes 20`"
                     "`!top_filmes [X-Y]`: Mostra os filmes mais bem avaliados em um intervalo específico. Exemplo: `!top_filmes 10-20`.\n")
        await ctx.send(help_text)

async def setup(bot):
  await bot.add_cog(BotEvents(bot))

