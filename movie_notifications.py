import discord
from discord.ext import commands, tasks
import aiohttp  
import asyncio
import datetime

class MovieNotificationsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = '8a37598beeaadf71a6ceb69d96f9714d'
        self.notification_channel_id = None
        print("Iniciando o MovieNotificationsCog...")
        self.session = aiohttp.ClientSession()
        self.upcoming_movies_check.start()

    async def load_notification_channel_id(self):
      print("Carregando ID do canal de notificações...")
      result = await self.bot.database.get_notification_channel()
      if result:
        self.notification_channel_id = result
        print(f"ID do canal de notificações carregado: {self.notification_channel_id}")
      else:
        print("Nenhum ID de canal de notificações encontrado no banco de dados.")

    async def initialize(self):
      print("Inicializando o cog...")
      await self.load_notification_channel_id()
      print("ID do canal de notificações salvo com sucesso.")
      
    async def save_notification_channel_id(self):
      print(f"Salvando o ID do canal de notificações: {self.notification_channel_id}")
      await self.bot.database.save_notification_channel(self.notification_channel_id)
      

    async def cog_unload(self):
      print("Descarregando o cog...")
      await self.session.close()

    async def get_upcoming_movies(self):
      print("Obtendo filmes em breve...")
      upcoming_url = f"https://api.themoviedb.org/3/movie/upcoming?api_key={self.api_key}&language=pt-BR"
      async with self.session.get(upcoming_url) as response:
          if response.status == 200:
              data = await response.json()
              movies = data.get('results', [])
              print(f"Filmes obtidos: {movies}")
              return movies
          else:
              print(f"Erro ao buscar filmes: {response.status}")
              return []

    def get_notified_movies(self):
        print("Obtendo filmes já notificados...")
        notified_movies = self.bot.database.get_notified_movies()
        print(f"Filmes já notificados: {notified_movies}")
        return notified_movies

    def add_notified_movie(self, movie_id):
        print(f"Adicionando filme notificado: {movie_id}")
        self.bot.database.add_notified_movie(movie_id)
        print("Filme notificado adicionado com sucesso.")

    def clean_notified_movies(self):
        print("Limpando filmes notificados...")
        self.bot.database.clean_notified_movies()
        print("Filmes notificados limpos com sucesso.")

    def create_movie_embed(self, movie):
        print(f"Criando embed para o filme: {movie.get('title', 'N/A')}")
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
        print("Embed criado com sucesso.")
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

    async def check_upcoming_movies(self, force_resend=False, ignore_limit=False):
      print("Iniciando a verificação de filmes em breve...")
      if not self.notification_channel_id:
          print("Nenhum canal de notificações definido.")
          return
    
      notified_movies = self.get_notified_movies()
      try:
          upcoming_movies = await self.get_upcoming_movies()
      except Exception as e:
          print(f"Erro ao obter filmes vindouros: {e}")
          return
      print(f"Filmes vindouros: {upcoming_movies}")
    
      if upcoming_movies:
          channel = self.bot.get_channel(self.notification_channel_id)
          if channel:
              count = 0
              for movie in upcoming_movies:
                  movie_id = movie.get('id')
                  release_date = movie.get('release_date')
                  print(f"Processando filme: ID {movie_id}, Data de Lançamento: {release_date}")
    
                  if release_date:
                      release_date_obj = datetime.datetime.strptime(release_date, "%Y-%m-%d")
                      current_date = datetime.datetime.now()
                      if current_date - datetime.timedelta(days=30) < release_date_obj <= current_date:
                          print(f"Filme {movie_id} foi lançado nos últimos 30 dias.")
    
                          if force_resend or movie_id not in notified_movies:
                              embed = self.create_movie_embed(movie)
                              print(f"Preparando para notificar o filme {movie_id}")
                              try:
                                  await channel.send(embed=embed)
                                  print(f"Notificação enviada para o filme {movie_id}")
                                  self.add_notified_movie(movie_id)
                                  count += 1
                                  print(f"Filme adicionado em notificado {movie_id}")
                                  if not ignore_limit and count >= 5:
                                      print("Limite de notificações alcançado.")
                                      break
                              except Exception as e:
                                  print(f"Erro ao enviar notificação para o filme {movie_id}: {e}")
                          else:
                              print(f"Filme {movie_id} já notificado anteriormente.")
                      else:
                          print(f"Filme {movie_id} fora do intervalo dos últimos 30 dias.")
                  else:
                      print(f"Filme {movie_id} sem data de lançamento definida ou já lançado.")
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
        confirmation_message = await ctx.send("Tem certeza que deseja executar a verificação e reenviar todas as notificações? ✅ para confirmar.")
        await confirmation_message.add_reaction("✅")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == '✅' and reaction.message.id == confirmation_message.id

        try:
            await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send("Tempo esgotado. Verificação cancelada.")
            return

        await ctx.send("Executando verificação de filmes em breve e reenviando notificações...")
        await self.check_upcoming_movies(force_resend=True, ignore_limit=True)

async def setup(bot):
    print("Configurando o bot...")
    cog = MovieNotificationsCog(bot)
    await bot.add_cog(cog)
    print("Bot configurado com sucesso.")
