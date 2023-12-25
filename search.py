import discord
from discord.ext import commands
import requests

class FilmeCog(commands.Cog):
    def __init__(self, bot, tmdb_api_key):
        self.bot = bot
        self.tmdb_api_key = tmdb_api_key

    @commands.command(name='filme')
    async def fetch_movie(self, ctx, *, movie_title):
        search_url = f"https://api.themoviedb.org/3/search/movie?api_key={self.tmdb_api_key}&query={movie_title}"
        search_response = requests.get(search_url).json()

        if search_response['results']:
            movie_id = search_response['results'][0]['id']
            movie_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={self.tmdb_api_key}"
            movie_response = requests.get(movie_url).json()

            title = movie_response['title']
            plot = movie_response['overview']
            release_date = movie_response['release_date']
            poster_path = movie_response['poster_path']
            poster_url = f"https://image.tmdb.org/t/p/original{poster_path}"
            tmdb_url = f"https://www.themoviedb.org/movie/{movie_id}"

            description = f"**Título:** {title}\n**Data de Lançamento:** {release_date}\n**Enredo:** {plot}\n**Link TMDb:** [Clique Aqui]({tmdb_url})"
            embed = discord.Embed(title="Informação do Filme", description=description, color=0x00ff00)
            embed.set_image(url=poster_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Filme não encontrado.")

    @commands.command(name='top_filmes')
    async def fetch_top_movies(self, ctx, *, args=None):
        base_url = "https://api.themoviedb.org/3/movie/top_rated"
  
        
        if args:
            if '-' in args:
                start, end = map(int, args.split('-'))
            else:
                start, end = 1, int(args)
        else:
            start, end = 1, 10 
  
        
        if end > 250 or start > 250:
            await ctx.send("Não é possível buscar mais de 250 filmes. Por favor, tente novamente com um valor válido até 250.")
            return
  
        if start > end:
            await ctx.send("Intervalo inválido. Por favor, forneça um intervalo válido.")
            return
  
        filmes = []
        page = 1
  
        while len(filmes) < end:
            url = f"{base_url}?api_key={self.tmdb_api_key}&page={page}"
            response = requests.get(url).json()
            filmes.extend(response['results'])
            page += 1
  
            if page > response['total_pages']:
                break
  
        filmes = filmes[start-1:end]
        message_lines = [f"{i+start}. {filme['title']} - Avaliação: {filme['vote_average']}/10" for i, filme in enumerate(filmes)]
        message = "\n".join(message_lines)
  
        for i in range(0, len(message), 2000):
            await ctx.send(message[i:i+2000])

async def setup(bot):
    await bot.add_cog(FilmeCog(bot, bot.tmdb_api_key))
