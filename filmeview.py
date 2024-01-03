import discord
import logging
from discord.ui import View, Button

class FilmeView(View):
  def __init__(self, movie_id, api_key, bot, session_id):
      super().__init__()
      self.movie_id = movie_id
      self.api_key = api_key
      self.bot = bot
      self.session_id = session_id

      # Certifique-se de que cada botão tenha um custom_id único
      self.add_item(Button(label="Favoritos", style=discord.ButtonStyle.green, custom_id=f"add_to_favorites_{movie_id}"))
      self.add_item(Button(label="Curtir", style=discord.ButtonStyle.blurple, custom_id=f"like_movie_{movie_id}"))
      self.add_item(Button(label="Watchlist", style=discord.ButtonStyle.grey, custom_id=f"add_to_watchlist_{movie_id}"))

      async def make_tmdb_post(self, method, endpoint, data):
          url = f"https://api.themoviedb.org/3/{endpoint}"
          headers = {'Authorization': f'Bearer {self.api_key}', 'Content-Type': 'application/json;charset=utf-8'}
          logging.info(f"Fazendo solicitação {method} para {url} com dados: {data}")
  
          if method.upper() == 'POST':
              response = await self.bot.session.post(url, headers=headers, json=data)
          else:
              response = await self.bot.session.get(url, headers=headers)
  
          return response
  
      async def handle_response(self, response, action, interaction):
          logging.info(f"Manipulando resposta da ação {action}")
          if response.status == 200 or response.status == 201:
              await interaction.response.send_message(f'Filme {action} com sucesso!', ephemeral=True)
          else:
              error_message = "Houve um problema ao processar sua solicitação."
              try:
                  json_response = await response.json()
                  if 'status_message' in json_response:
                      error_message += f" Erro: {json_response['status_message']}"
              except Exception as e:
                  logging.error(f"Erro ao processar resposta JSON: {e}")
                  pass
              await interaction.response.send_message(error_message, ephemeral=True)
  
      async def button_callback(self, button, interaction, action, data):
          logging.info(f"Botão {button.custom_id} pressionado, iniciando ação {action}")
          response = await self.make_tmdb_post('POST', f'account/{{account_id}}/{action}?api_key={self.api_key}&session_id={self.session_id}', data)
          await self.handle_response(response, action, interaction)
  
      @discord.ui.button(label='Favoritos', style=discord.ButtonStyle.green, custom_id='add_to_favorites')
      async def favoritos_button_callback(self, button, interaction):
          logging.info("Botão Favoritos pressionado")
          data = {'media_type': 'movie', 'media_id': self.movie_id, 'favorite': True}
          await self.button_callback(button, interaction, 'favorite', data)
  
      @discord.ui.button(label='Curtir', style=discord.ButtonStyle.blurple, custom_id='like_movie')
      async def curtir_button_callback(self, button, interaction):
          logging.info("Botão Curtir pressionado")
          data = {'media_type': 'movie', 'media_id': self.movie_id, 'watchlist': True}
          await self.button_callback(button, interaction, 'watchlist', data)
  
      @discord.ui.button(label='Watchlist', style=discord.ButtonStyle.grey, custom_id='add_to_watchlist')
      async def watchlist_button_callback(self, button, interaction):
          logging.info("Botão Watchlist pressionado")
          data = {'media_type': 'movie', 'media_id': self.movie_id, 'watchlist': True}
          await self.button_callback(button, interaction, 'watchlist', data)
  