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
                await owner.send(f"Olá {owner.name}! Obrigado por adicionar o The Cinephile ao seu servidor! "
                                 "Use o comando `!ajuda` para ver a lista de comandos disponíveis.")
            except discord.errors.Forbidden:
                print(f"Não foi possível enviar DM para o dono do servidor {guild.name}.")

    @commands.command(name='ajuda')
    async def help_command(self, ctx):
      embed = discord.Embed(
          title="Ajuda do The Cinephile",
          description="Veja abaixo como usar os comandos do bot:",
          color=discord.Color.blue()
      )
      embed.add_field(name="!configurar_api",
                      value="Configura sua chave da API do TMDb.", inline=False)
      embed.add_field(name="!filme <titulo>",
                      value="Busca informações sobre um filme. Exemplo: `!filme Oppenheimer `.", inline=False)
      embed.add_field(name="!top_filmes [N]",
                      value="Mostra os top N filmes mais bem avaliados. Exemplo: `!top_filmes 20`", inline=False)
      embed.add_field(name="!top_filmes [X-Y]",
                      value="Mostra os filmes mais bem avaliados em um intervalo específico. Exemplo: `!top_filmes 10-20`.", inline=False)
      embed.add_field(name="!pessoa <nome>",
        value="Busca informações sobre uma pessoa específica na indústria cinematográfica, como atores, diretores, etc. Fornece detalhes como nome, biografia, data de nascimento, local de nascimento, papéis notáveis e mais. Exemplo: `!pessoa Brad Pitt`.", inline=False)
      embed.add_field(name="!elenco <titulo>",
        value="Busca informações sobre o elenco do filme. Exemplo: `!elenco Oppenheimer `.", inline=False)
      embed.add_field(name="!canal_notificacoes <nome>",
        value="Escolhe um canal para receber notificacoes sobre novos filmes, esse comando funciona para administradores do server discord. Exemplo: `!canal_notificacoes Cine-News`.", inline=False)
      embed.add_field(name="!verificar_notificacoes",
        value="Reenvia todas as notificações para o canal escolhido", inline=False)
      embed.add_field(name="!recomendacao <titulo>",
        value= "Recomenda um filme com base no nome de outro filme. Exemplo: `!recomendacao 300`.", inline=False)
      embed.add_field(name="!favoritos", value="Exibe a lista de seus filmes favoritos.", inline=False)
      embed.add_field(name="!watchlist", value="Exibe a lista de filmes na sua watchlist.", inline=False)
  
      await ctx.send(embed = embed)
        

async def setup(bot):
  await bot.add_cog(BotEvents(bot))

