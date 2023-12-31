# 🎬 Bot do Discord: Buscador de Filmes TMDb

Este bot do Discord permite que os usuários busquem informações sobre filmes usando a API do TMDb (The Movie Database). Cada usuário pode configurar sua própria chave da API do TMDb para realizar pesquisas personalizadas.

## ⚙️ Configuração Inicial

Antes de começar a usar o bot, cada usuário precisa configurar sua chave da API do TMDb. Siga os passos abaixo para obter e configurar sua chave da API:

1. **Obtenha sua chave da API do TMDb**:
   - 🌐 Crie uma conta ou faça login no [TMDb](https://www.themoviedb.org/).
   - 🔑 Navegue até as configurações da sua conta e procure a seção para gerar uma chave da API.

2. **Configure sua chave da API no bot**:
   - 🤖 No Discord, use o comando `!configurar_api [sua_chave_api]` para configurar sua chave da API.
   - Substitua `[sua_chave_api]` pela chave da API que você obteve do TMDb.

## 📜 Comandos Disponíveis

- `!configurar_api [chave]`: Configura sua chave da API do TMDb para uso com o bot.
- `!filme [título do filme]`: Busca informações sobre um filme específico. Exemplo: `!filme Inception`.
- `!top_filmes`: Mostra os 10 filmes mais bem avaliados no TMDb.
- `!top_filmes [N]`: Mostra os top N filmes mais bem avaliados. Exemplo: `!top_filmes 20`.
- `!top_filmes [X-Y]`: Mostra os filmes mais bem avaliados em um intervalo específico. Exemplo: `!top_filmes 10-20`.
- `!ajuda`: Mostra como utilizar os comandos do bot.
- `!elenco [título do filme]`: Busca informações sobre o elenco do filme. Exemplo: `!elenco Oppenheimer`.
- `!pessoa [nome]`: Busca informações sobre uma pessoa específica na indústria cinematográfica. Exemplo: `!pessoa Brad Pitt`.
- `!recomendacao [título do filme]`: Recomenda filmes com base em um título fornecido. Exemplo: `!recomendacao 300`.

## 🗃️ Limites e Funcionamento do Banco de Dados

- **Limite de Filmes**: Para comandos que listam filmes, como `!top_filmes`, o limite máximo é de 250 filmes por solicitação.
- **Banco de Dados**: As chaves da API são armazenadas de forma segura e associadas aos IDs dos usuários do Discord.
- **Privacidade e Segurança**: As chaves da API são tratadas com total privacidade e segurança.

## 📝 Notas

- O bot respeita os limites de chamadas de API impostos pelo TMDb.
- Este bot foi criado para fins educacionais e de entretenimento.

## 💡 Possíveis Melhorias

- Cache de Resultados
- Recomendações Personalizadas - Implementado em 30/12/2023
- Funcionalidades Avançadas de Pesquisa
- Notificações de Lançamentos e Eventos - A ser melhorado
- API_KEY em DM - Implementado em 27/12/2023
- Rota inicial de configuração - Implementado em 26/12/2023
- Comando de `!ajuda` - Implementado em 27/12/2023
- Informações sobre plataformas de streaming disponíveis - Implementado em 28/12/2023
- Busca por atores - Implementado em 28/12/2023
- Alterar da biblioteca requests para aiohttp
- Informações de Elenco e Equipe - Implementado em 28/12/2023
- Integração com Redes Sociais
- Integração com Plataformas de Streaming
- Ajuste no output do `!top_filmes [X]`
- Monitoramento da API
- **Crítico**: Comandos vazios não retornam erros ou auxílios para o usuário.
- Suporte Multilíngue
- Sistema de Favoritos
- Funcionalidade de Lembrete/Alarme para Lançamentos
- Feedback e Sugestões dos Usuários do bot
