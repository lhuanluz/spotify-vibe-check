# Spotify Vibe Check 🎵

Um script Python que cria playlists personalizadas no Spotify baseadas no seu humor e artistas favoritos, usando IA para gerar recomendações musicais perfeitas para o momento.

## ✨ Funcionalidades

- Criação de playlists personalizadas baseadas no seu humor atual
- Recomendações de músicas usando IA (OpenAI)
- Nomes criativos e concisos para as playlists
- Reprodução automática da playlist criada
- Filtro de artistas que você não quer ouvir
- Integração direta com sua conta do Spotify

## 🚀 Como Usar

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/spotify-vibe-check.git
cd spotify-vibe-check
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente:

   a. Crie um arquivo `.env` na raiz do projeto com as credenciais do Spotify:
   ```
   SPOTIPY_CLIENT_ID=seu_client_id
   SPOTIPY_CLIENT_SECRET=seu_client_secret
   SPOTIPY_REDIRECT_URI=http://localhost:8888/callback
   ```

   b. Configure a variável de ambiente do Windows para a chave da OpenAI:
   - Nome: `OPENAI_API_KEY`
   - Valor: sua chave da API OpenAI

4. Execute o script:
```bash
python spotify_vibe_check.py
```

## 🎯 Como Funciona

1. O script pede seus artistas favoritos (separados por vírgula)
2. Você descreve seu humor/vibe atual
3. A IA gera recomendações de músicas baseadas nos seus artistas e humor
4. Uma nova playlist é criada no Spotify com as músicas recomendadas
5. A playlist começa a tocar automaticamente no seu dispositivo Spotify ativo

## 🔧 Configuração do Spotify

Para obter suas credenciais do Spotify:

1. Acesse o [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Crie uma nova aplicação
3. Copie o Client ID e Client Secret
4. Adicione `http://localhost:8888/callback` como URI de redirecionamento nas configurações da aplicação

## 📝 Exemplo de Uso

```
Enter your favorite artists (comma-separated):
daniel caesar, charlie wilson, giveon

Describe your current mood/vibe:
I want a chill rnb vibe mixing new and old stuff, nothing like harry styles

Created playlist: "Soulful Serenity"
Playlist URL: https://open.spotify.com/playlist/...
```

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes. 