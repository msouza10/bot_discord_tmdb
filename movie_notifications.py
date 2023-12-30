import discord
from discord.ext import commands, tasks
import requests
import asyncio

class MovieNotificationsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = '8a37598beeaadf71a6ceb69d96f9714d'
        self.notification_channel_id = None
        self.upcoming_movies_check.start()
    
    async def load_notification_channel_id(self):
      result = await self.bot.database.get_notification_channel()
      if result:
          self.notification_channel_id = result

    async def initialize(self):
      await self.load_notification_channel_id()

    async def save_notification_channel_id(self):
      await self.bot.database.save_notification_channel(self.notification_channel_id)
  
    def cog_unload(self):
        self.upcoming_movies_check.cancel()

    def get_upcoming_movies(self):
        print("Obtendo filmes em breve...")
        upcoming_url = f"https://api.themoviedb.org/3/movie/upcoming?api_key={self.api_key}&language=pt-BR"
        response = requests.get(upcoming_url)
        if response.status_code == 200:
            return response.json().get('results', [])
        else:
            print(f"Erro ao buscar filmes: {response.status_code}")
            return []

    def get_notified_movies(self):
        notified_movies = self.bot.database.get_notified_movies()
        print(f"Filmes já notificados: {notified_movies}")
        return notified_movies

    def add_notified_movie(self, movie_id):
        self.bot.database.add_notified_movie(movie_id)

    def clean_notified_movies(self):
        self.bot.database.clean_notified_movies()

    def create_movie_embed(self, movie):
        title = movie.get('title', 'N/A')
        overview = movie.get('overview', 'Sinopse não disponível.')
        release_date = movie.get('release_date', 'Data desconhecida')
        vote_average = movie.get('vote_average', 'N/A')
        poster_path = movie.get('poster_path', '')
        poster_url = f"https://image.tmdb.org/t/p/original{poster_path}" if poster_path else ''
        genres = ', '.join([genre['name'] for genre in movie.get('genres', [])])
        tmdb_url = f"https://www.themoviedb.org/movie/{movie['id']}"

        embed = discord.Embed(title=f"Próximo lançamento: {title}", description=overview, color=0x00ff00)
        embed.add_field(name="Data de Lançamento", value=release_date)
        embed.add_field(name="Avaliação", value=str(vote_average))
        embed.add_field(name="Gêneros", value=genres if genres else 'Gêneros desconhecidos', inline=False)
        embed.add_field(name="Mais informações", value=f"[Clique aqui]({tmdb_url})", inline=False)
        if poster_url:
            embed.set_image(url=poster_url)
        return embed

    @commands.command(name='canal_notificacoes')
    @commands.has_permissions(administrator=True)
    async def set_notification_channel(self, ctx, channel_name: str = None):
        if channel_name:
            channel = discord.utils.get(ctx.guild.channels, name=channel_name)
            if channel is None:
                await ctx.send("Canal não encontrado.")
                return
        else:
            channel = ctx.channel
  
        if channel_name and len([ch for ch in ctx.guild.channels if ch.name == channel_name]) > 1:
            await ctx.send("Aviso: Há mais de um canal com esse nome. Usando o primeiro encontrado.")
  

        confirmation_message = await ctx.send(f"Confirmar '{channel.name}' como o canal de notificações? ✅ para confirmar.")
        await confirmation_message.add_reaction("✅")
  
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == '✅' and reaction.message.id == confirmation_message.id
  
        try:
            await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send("Tempo esgotado. Canal de notificações não alterado.")
        else:
            self.notification_channel_id = channel.id
            print(f"Canal de notificações definido para: {self.notification_channel_id}")
            await ctx.send(f"Canal de notificações de filmes definido para: {channel.mention}")
            await self.save_notification_channel_id()

    async def check_upcoming_movies(self):
      print("Iniciando a verificação de filmes em breve...")
      if not self.notification_channel_id:
          print("Nenhum canal de notificações definido.")
          return

      notified_movies = self.get_notified_movies()
      upcoming_movies = self.get_upcoming_movies()
      print(f"Filmes vindouros: {upcoming_movies}")
      if upcoming_movies:
          channel = self.bot.get_channel(self.notification_channel_id)
          if channel:
              count = 0
              for movie in upcoming_movies:
                  if count >= 5:
                      break
                  movie_id = movie.get('id')
                  print(f"Verificando filme {movie_id}")
                  if movie_id in notified_movies:
                      print(f"Filme {movie_id} já notificado.")
                      continue
  
                  embed = self.create_movie_embed(movie)
                  print(f"Notificando filme {movie_id}")
                  await channel.send(embed=embed)
  
                  self.add_notified_movie(movie_id)
                  count += 1
          else:
              print(f"Não foi possível encontrar o canal com ID {self.notification_channel_id}")
      else:
          print("Nenhum filme novo para notificar.")
  
      self.clean_notified_movies()

    @tasks.loop(hours=1)
    async def upcoming_movies_check(self):
        await self.check_upcoming_movies()

    @upcoming_movies_check.before_loop
    async def before_upcoming_movies_check(self):
        await self.bot.wait_until_ready()

    @commands.command(name='verificar_filmes')
    @commands.has_permissions(administrator=True)
    async def run_upcoming_movies_check(self, ctx):
        await ctx.send("Executando verificação de filmes em breve...")
        await self.check_upcoming_movies()

async def setup(bot):
    cog = MovieNotificationsCog(bot)
    await bot.add_cog(cog)
