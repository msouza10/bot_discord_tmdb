import discord
from discord.ext import commands
import requests
import asyncio  

class FilmeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    async def make_tmdb_request(self, url):
      try:
          response = requests.get(url)
          response.raise_for_status()
          return response.json()
      except requests.RequestException as e:
          print(f"Erro ao fazer requisição para o TMDb: {e}")
          return None
        
    async def is_valid_api_key(self, api_key):
        """Verifica se a chave da API do TMDb é válida."""
        test_url = f"https://api.themoviedb.org/3/movie/550?api_key={api_key}"
        try:
            response = requests.get(test_url)
            if response.status_code == 200:
                data = response.json()
                required_fields = ['id', 'title', 'overview', 'genres', 'release_date']
                return all(field in data for field in required_fields)
            else:
                return False
        except requests.RequestException:
            return False

    @commands.command(name='configurar_api')
    async def set_api_key(self, ctx):
        if ctx.guild is not None:
            await ctx.send("Vou te enviar uma mensagem privada para configurar sua chave da API.")

        def check(m):
            return m.author == ctx.author and isinstance(m.channel, discord.DMChannel)

        try:
            await ctx.author.send("Por favor, envie sua chave da API do TMDb aqui.")
            message = await self.bot.wait_for('message', check=check, timeout=300)
            api_key = message.content

            if await self.is_valid_api_key(api_key):
                self.bot.database.set_user_api_key(ctx.author.id, api_key)
                await ctx.author.send("Chave da API configurada com sucesso!")
            else:
                await ctx.author.send("A chave da API fornecida é inválida. Por favor, tente novamente com uma chave válida.")
        except asyncio.TimeoutError:
            await ctx.author.send("Você não enviou a chave da API a tempo. Por favor, tente o comando novamente.")

    def get_user_api_key(self, user_id):
        return self.bot.database.get_user_api_key(user_id)

    def get_streaming_services(self, movie_id, api_key):
        providers_url = f"https://api.themoviedb.org/3/movie/{movie_id}/watch/providers?api_key={api_key}"
        response = requests.get(providers_url)
        data = response.json()

        services = []
        if 'results' in data and 'BR' in data['results']:
            brazil_providers = data['results']['BR'].get('flatrate', [])
            services = [provider['provider_name'] for provider in brazil_providers]

        return services

    @commands.command(name='filme')
    async def fetch_movie(self, ctx, *, movie_title: str = ""):
        if movie_title.strip() == "":
            embed = discord.Embed(
                title="Comando Executado de Forma Incorreta",
                description="Você esqueceu de informar o título do filme.",
                color=discord.Color.red()
            )
            embed.add_field(
                name="Como usar o comando !filme",
                value="`!filme [título do filme]` - Busca informações sobre um filme específico.\n"
                      "Exemplo: `!filme Inception`.",
                inline=False
            )
            await ctx.send(embed=embed)
            return
          
        user_api_key = self.get_user_api_key(ctx.author.id)
        if not user_api_key:
            await ctx.send("Você precisa configurar sua chave da API do TMDb primeiro usando o comando !configurar_api")
            return

        search_url = f"https://api.themoviedb.org/3/search/movie?api_key={user_api_key}&query={movie_title}"
        search_response = requests.get(search_url).json()

        if not search_response['results']:
            await ctx.send("Filme não encontrado.")
            return

        movie_id = search_response['results'][0]['id']
        movie_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={user_api_key}"
        movie_response = requests.get(movie_url).json()

        title = movie_response.get('title', 'N/A')
        plot = movie_response.get('overview', 'Descrição não disponível.')
        release_date = movie_response.get('release_date', 'Data desconhecida')
        genres = ", ".join([genre['name'] for genre in movie_response.get('genres', [])])
        duration = f"{movie_response.get('runtime', 'N/A')} minutos"
        rating = movie_response.get('vote_average', 'N/A')
        votes = movie_response.get('vote_count', 'N/A')
        poster_path = movie_response.get('poster_path', '')
        poster_url = f"https://image.tmdb.org/t/p/original{poster_path}" if poster_path else ''
        tmdb_url = f"https://www.themoviedb.org/movie/{movie_id}"

        streaming_services = self.get_streaming_services(movie_id, user_api_key)

        trailer_url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={user_api_key}"
        trailer_response = requests.get(trailer_url).json()
        trailer_link = next((f"https://www.youtube.com/watch?v={video['key']}" 
                             for video in trailer_response.get('results', []) 
                             if video['site'] == 'YouTube' and video['type'] == 'Trailer'), None)

        description = f"""**Título:** {title}
**Data de Lançamento:** {release_date}
**Gêneros:** {genres}
**Duração:** {duration}
**Classificação:** {rating}/10 baseado em {votes} votos
**Enredo:** {plot}
**Link TMDb:** [Clique Aqui]({tmdb_url})"""

        if streaming_services:
            streaming_info = "**Disponível em:** " + ", ".join(streaming_services)
            description += f"\n{streaming_info}"

        if trailer_link:
            description += f"\n**Trailer:** [Assistir no YouTube]({trailer_link})"

        embed = discord.Embed(title="Informação do Filme", description=description, color=0x00ff00)
        if poster_url:
            embed.set_image(url=poster_url)
        await ctx.send(embed=embed)

    @commands.command(name='top_filmes')
    async def fetch_top_movies(self, ctx, *, args=None):
        user_api_key = self.get_user_api_key(ctx.author.id)
        if not user_api_key:
            await ctx.send("Você precisa configurar sua chave da API do TMDb primeiro usando o comando !configurar_api")
            return
  
        base_url = "https://api.themoviedb.org/3/movie/top_rated"
        filmes = []
        page = 1
  
        if args:
            if '-' in args:
                start, end = map(int, args.split('-'))
            else:
                start, end = 1, int(args)
        else:
            start, end = 1, 10
  
        if end > 250 or start > 250:
            await ctx.send("O limite máximo é 250 filmes. Por favor, ajuste o seu pedido.")
            return
  
        start, end = max(1, start), min(end, 250)
        if start > end:
            await ctx.send("Intervalo inválido. Por favor, forneça um intervalo válido.")
            return
  
        while len(filmes) < end:
            url = f"{base_url}?api_key={user_api_key}&page={page}"
            response = requests.get(url).json()
            filmes.extend(response['results'])
            page += 1
  
            if page > response['total_pages']:
                break
  
        filmes = filmes[start-1:end]
  
        message_lines = [
            f"{i+start}. [{filme['title']}](<https://www.themoviedb.org/movie/{filme['id']}>) - Avaliação: {filme['vote_average']}/10"
            for i, filme in enumerate(filmes)
        ]
        total_filmes = len(message_lines)
        filmes_por_mensagem = 25
  
        for i in range(0, total_filmes, filmes_por_mensagem):
            fim_intervalo = min(i + filmes_por_mensagem, total_filmes)
            mensagem_filmes = "\n".join(message_lines[i:fim_intervalo])
            await ctx.send(mensagem_filmes)
            await asyncio.sleep(1)

    @commands.command(name='pessoa')
    async def fetch_person(self, ctx, *, person_name):
        user_api_key = self.get_user_api_key(ctx.author.id)
        if not user_api_key:
            await ctx.send("Você precisa configurar sua chave da API do TMDb primeiro usando o comando !configurar_api")
            return
    
        
        search_url = f"https://api.themoviedb.org/3/search/person?api_key={user_api_key}&query={person_name}"
        search_response = requests.get(search_url)
        search_data = await self.make_tmdb_request(search_url)
        if not search_data or not search_data['results']:
            await ctx.send("Pessoa não encontrado.")
            return
    
        person = search_data['results'][0]
        person_id = person.get('id', 'N/A')
    
        
        person_url = f"https://api.themoviedb.org/3/person/{person_id}?api_key={user_api_key}&language=pt-BR"
        person_response = requests.get(person_url)
        person_data = person_response.json()
    
        
        profile_path = person_data.get('profile_path')
        profile_url = f"https://image.tmdb.org/t/p/w500{profile_path}" if profile_path else None
    
        name = person_data.get('name', 'N/A')
        known_for_department = person_data.get('known_for_department', 'Desconhecido')
        bio = person_data.get('biography', 'Biografia não disponível.')
        birth_date = person_data.get('birthday', 'Data de nascimento desconhecida')
        birth_place = person_data.get('place_of_birth', 'Local de nascimento desconhecido')
        death_date = person_data.get('deathday', 'Vivo')
        popularity = person_data.get('popularity', 'N/A')
        tmdb_url = f"https://www.themoviedb.org/person/{person_id}"
    
        description = (f"**Nome:** {name}\n"
                       f"**Conhecido(a) por:** {known_for_department}\n"
                       f"**Data de Nascimento:** {birth_date}\n"
                       f"**Local de Nascimento:** {birth_place}\n"
                       f"**Data de Falecimento:** {death_date if death_date else 'Vivo'}\n"
                       f"**Popularidade:** {popularity}\n"
                       f"**Biografia:** {bio}\n"
                       f"**Link TMDb:** [Clique Aqui]({tmdb_url})")
    
        embed = discord.Embed(title="Informação da Pessoa", description=description, color=0x00ff00)
        if profile_url:
            embed.set_thumbnail(url=profile_url)
        await ctx.send(embed=embed)

    @commands.command(name='elenco')
    async def fetch_cast_and_crew(self, ctx, *, movie_title):
        user_api_key = self.get_user_api_key(ctx.author.id)
        if not user_api_key:
            await ctx.send("Você precisa configurar sua chave da API do TMDb primeiro usando o comando !configurar_api")
            return

        search_url = f"https://api.themoviedb.org/3/search/movie?api_key={user_api_key}&query={movie_title}"
        search_response = requests.get(search_url).json()

        if not search_response['results']:
            await ctx.send("Filme não encontrado.")
            return

        movie_id = search_response['results'][0]['id']

        credits_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={user_api_key}"
        credits_response = requests.get(credits_url).json()

        cast = credits_response.get('cast', [])[:10]  # Limita aos 10 primeiros membros do elenco
        crew = credits_response.get('crew', [])[:10]  # Limita aos 10 primeiros membros da equipe técnica

        cast_names = ', '.join([member['name'] for member in cast])
        crew_names = ', '.join([member['name'] + ' (' + member['job'] + ')' for member in crew])

        description = f"**Elenco:** {cast_names}\n**Equipe:** {crew_names}"

        embed = discord.Embed(title=f"Elenco e Equipe de '{search_response['results'][0]['title']}'", description=description, color=0x00ff00)
        await ctx.send(embed=embed)

  
async def setup(bot):
    await bot.add_cog(FilmeCog(bot))
