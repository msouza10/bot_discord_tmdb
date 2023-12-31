
import discord
from discord.ext import commands
import requests
import asyncio

class RecomendacaoFilmeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("RecomendacaoFilmeCog iniciado")

    async def buscar_api_key_usuario(self, user_id):
        api_key = self.bot.database.get_user_api_key(user_id)
        return api_key

    async def obter_id_filme(self, api_key, nome_filme):
        url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={nome_filme}"
        response = await self.bot.loop.run_in_executor(None, requests.get, url)
        if response.status_code == 200:
            data = response.json()
            if data['results']:
                return data['results'][0]['id']
        return None

    async def obter_detalhes_filme(self, api_key, movie_id):
        movie_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
        response = requests.get(movie_url)
        if response.status_code == 200:
            movie_response = response.json()
            return {
                "title": movie_response.get('title', 'N/A'),
                "plot": movie_response.get('overview', 'Descrição não disponível.'),
                "release_date": movie_response.get('release_date', 'Data desconhecida'),
                "genres": ", ".join([genre['name'] for genre in movie_response.get('genres', [])]),
                "duration": f"{movie_response.get('runtime', 'N/A')} minutos",
                "rating": movie_response.get('vote_average', 'N/A'),
                "votes": movie_response.get('vote_count', 'N/A'),
                "poster_url": f"https://image.tmdb.org/t/p/original{movie_response.get('poster_path', '')}",
                "tmdb_url": f"https://www.themoviedb.org/movie/{movie_id}"
            }
        else:
            return None

    async def recomendar_filme(self, api_key, movie_id, max_recomendacoes=5):
        url = f"https://api.themoviedb.org/3/movie/{movie_id}/recommendations?api_key={api_key}&language=pt-BR"
        response = await self.bot.loop.run_in_executor(None, requests.get, url)
        if response.status_code == 200:
            data = response.json()
            recomendacoes = []
            for filme in data['results'][:max_recomendacoes]:
                detalhes_filme = await self.obter_detalhes_filme(api_key, filme['id'])
                recomendacoes.append(detalhes_filme)
            return recomendacoes
        return None

    @commands.command(name='recomendacao')
    async def recomendacao_command(self, ctx, nome_filme, max_recomendacoes: int = 3):
        user_id = ctx.author.id
        api_key = await self.buscar_api_key_usuario(user_id)
        if api_key:
            movie_id = await self.obter_id_filme(api_key, nome_filme)
            if movie_id:
                recomendacoes = await self.recomendar_filme(api_key, movie_id, max_recomendacoes)
                if recomendacoes:
                    for filme in recomendacoes:
                        if filme:
                            embed = discord.Embed(title=filme['title'], color=0x00ff00)
                            embed.add_field(name="Data de Lançamento", value=filme['release_date'], inline=True)
                            embed.add_field(name="Gêneros", value=filme['genres'], inline=True)
                            embed.add_field(name="Duração", value=filme['duration'], inline=True)
                            embed.add_field(name="Classificação", value=f"{filme['rating']}/10", inline=True)
                            embed.add_field(name="Votos", value=filme['votes'], inline=True)
                            embed.add_field(name="Enredo", value=filme['plot'], inline=False)
                            embed.add_field(name="Link TMDb", value=f"[Clique Aqui]({filme['tmdb_url']})", inline=False)
                            if filme['poster_url']:
                                embed.set_image(url=filme['poster_url'])
                            await ctx.send(embed=embed)
                else:
                    await ctx.send('Não foram encontradas recomendações para este filme.')
            else:
                await ctx.send('Não foi possível encontrar um filme com esse nome.')
        else:
            await ctx.send('Por favor, configure sua chave da API do TMDb com o comando `!configurar_api`.')

async def setup(bot):
  await bot.add_cog(RecomendacaoFilmeCog(bot))
