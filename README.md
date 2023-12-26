# Bot do Discord: Buscador de Filmes TMDb

Este bot do Discord permite que os usuários busquem informações sobre filmes usando a API do TMDb (The Movie Database). Cada usuário pode configurar sua própria chave da API do TMDb para realizar pesquisas personalizadas.

## Configuração Inicial

Antes de começar a usar o bot, cada usuário precisa configurar sua chave da API do TMDb. Siga os passos abaixo para obter e configurar sua chave da API:

1. **Obtenha sua chave da API do TMDb**:
   - Crie uma conta ou faça login no [TMDb](https://www.themoviedb.org/).
   - Navegue até as configurações da sua conta e procure a seção para gerar uma chave da API.

2. **Configure sua chave da API no bot**:
   - No Discord, use o comando `!configurar_api [sua_chave_api]` para configurar sua chave da API.
   - Substitua `[sua_chave_api]` pela chave da API que você obteve do TMDb.

## Comandos Disponíveis

- `!configurar_api [chave]`: Configura sua chave da API do TMDb para uso com o bot.
- `!filme [título do filme]`: Busca informações sobre um filme específico. Exemplo: `!filme Inception`.
- `!top_filmes`: Mostra os 10 filmes mais bem avaliados no TMDb.
- `!top_filmes [N]`: Mostra os top N filmes mais bem avaliados. Exemplo: `!top_filmes 20`.
- `!top_filmes [X-Y]`: Mostra os filmes mais bem avaliados em um intervalo específico. Exemplo: `!top_filmes 10-20`.

## Limites e Funcionamento do Banco de Dados

- **Limite de Filmes**: Para comandos que listam filmes, como `!top_filmes`, o limite máximo é de 250 filmes por solicitação.
- **Banco de Dados**: Cada chave da API do TMDb é armazenada de forma segura em um banco de dados SQLite. O bot associa cada chave da API ao ID do usuário do Discord, permitindo configurações personalizadas e uso individualizado.
- **Privacidade e Segurança**: As chaves da API são armazenadas de forma segura e privada. Recomenda-se que os usuários configurem suas chaves da API em mensagens diretas com o bot.

## Notas

- Cada usuário deve usar sua própria chave da API do TMDb para fazer consultas.
- O bot respeita os limites de chamadas de API impostos pelo TMDb. Por favor, use o bot de maneira responsável.
- Este bot foi criado para fins educacionais e de entretenimento.

## Possiveis Melhorias

- Cache de Resultados
- Recomendações Personalizadas
- Funcionalidades Avançadas de Pesquisa
- Notificações de Lançamentos e Eventos

