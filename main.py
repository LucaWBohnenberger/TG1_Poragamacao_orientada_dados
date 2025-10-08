from Streaming.usuario import Usuario
from Streaming.musica import Musica
from Streaming.playlist import Playlist
from Streaming.podcast import Podcast

# Imports necessários para a Inovação (Abrir no Navegador)
from youtubesearchpython import VideosSearch
import webbrowser # Biblioteca padrão do Python para abrir o navegador

# --- Variáveis Globais ---
usuarios = []
playlists = []
podcasts = []
musicas = []

# --- Função de Log ---
def log_error(log):
    # Usando 'a' para adicionar ao arquivo (append) e utf-8 para compatibilidade
    with open("log.txt", "a", encoding="utf-8") as file:
        file.write(str(log) + "\n")

# --- Carregamento de Dados ---
try:
    with open("config/dados.md", encoding="utf-8") as f:
        nome_variavel_leitura = "" # Renomeado para evitar conflito com o 'nome' do usuário logado
        lista1 = []
        tipo = ""

        for linha in f:
            arr = linha.strip().split()
            if not arr:
                continue

            if arr[0] == "#":
                tipo = arr[1]
                continue

            if tipo == "Usuários":
                if arr[0] == "-" and arr[1] == "nome:":
                    nome_variavel_leitura = arr[2]
                elif arr[0].startswith("playlists:"):
                    conteudo = " ".join(arr[1:])
                    conteudo = conteudo.strip("[]")
                    lista1 = [p.strip() for p in conteudo.split(",") if p.strip()]
                    usuarios.append(Usuario(nome=nome_variavel_leitura, playlists=lista1))
            
            if tipo == "Músicas":
                if arr[0] == "-" and arr[1] == "titulo:":
                    titulo = " ".join(arr[2:])
                elif arr[0] == "artista:":
                    artista = " ".join(arr[1:])
                elif arr[0] == "genero:":
                    genero = " ".join(arr[1:])
                elif arr[0] == "duracao:":
                    duracao = int(arr[1])
                    musicas.append(Musica(titulo=titulo, artista=artista, genero=genero, duracao=duracao))
            
            elif tipo == "Podcasts":
                if arr[0] == "-" and arr[1] == "titulo:":
                    titulo = " ".join(arr[2:])
                elif arr[0] == "temporada:":
                    temporada = " ".join(arr[1:])
                elif arr[0] == "episodio:":
                    episodio = int(arr[1])
                elif arr[0] == "host:":
                    host = " ".join(arr[1:])
                elif arr[0] == "duracao:":
                    duracao = int(arr[1])
                    podcasts.append(Podcast(titulo=titulo, temporada=temporada, episodio=episodio, host=host, duracao=duracao))

            elif tipo == "Playlists":
                if arr[0] == "-" and arr[1] == "nome:":
                    nome_playlist = " ".join(arr[2:]) # Renomeado para evitar conflito
                elif arr[0] == "usuario:":
                    usuario_playlist = " ".join(arr[1:])
                elif arr[0].startswith("itens:"):
                    conteudo = " ".join(arr[1:])
                    conteudo = conteudo.strip("[]")
                    itens = [p.strip() for p in conteudo.split(",") if p.strip()]

                    usuario_obj = None
                    for usuario in usuarios:
                        if usuario.nome == usuario_playlist:
                            usuario_obj = usuario
                            break

                    if usuario_obj is not None:
                        playlists.append(Playlist(nome=nome_playlist, usuario=usuario_obj, itens=itens))
                    else:
                        print(f"Aviso: usuário '{usuario_playlist}' não encontrado para a playlist '{nome_playlist}'")
                        log_error(ValueError(f"Usuário '{usuario_playlist}' não encontrado para a playlist '{nome_playlist}'."))

except Exception as e:
    log_error(e)


# --- Menu Inicial ---
def menu_inicial():
    while(True):
        try:
            print("\n----------Menu----------")
            print("1) Entrar como usuário")
            print("2) Criar novo usuário")
            print("3) Listar usuários")
            print("4) Sair")
            escolha = input(">> ")

            match escolha:
                case "1":
                    while(True):
                        print("\nQual o nome do seu usuário?")
                        print("Digite 'Retorno' para retornar")
                        nome_login = input(">> ")

                        if nome_login.lower() == "retorno":
                            break
                        
                        usuario_encontrado = None
                        for u in usuarios:
                            if u.nome.lower() == nome_login.lower():
                                usuario_encontrado = u
                                break

                        if(usuario_encontrado):
                            print(f"\nUsuário válido, bem vindo {usuario_encontrado.nome}")
                            logado(usuario_encontrado)
                            break
                        else:
                            print("\nUsuário inválido!")
                            raise ValueError("Nome não existente na base de dados")

                case "2":
                    print("\nQual o nome do usuario novo?")
                    print("Nota: por favor não use o nome de um usuário já existente")
                    tentativa_nome = input(">> ")
                    
                    usuario_ja_existe = False
                    for u in usuarios:
                        if u.nome.lower() == tentativa_nome.lower():
                            usuario_ja_existe = True
                            break

                    if(not usuario_ja_existe):
                        print("Usuário válido")
                        usuarios.append(Usuario(nome=tentativa_nome))
                        print("Usuário criado")
                    else:
                        print("Usuário inválido!")
                        raise ValueError("Usuário já existente na base de dados!")
                
                case "3":
                    print("\n--- Usuários Cadastrados ---")
                    for u in usuarios:
                        print(f"- {u.nome}")

                case "4":
                    print("\nObrigado por utilizar nosso serviço!")
                    return
                
                case _:
                    print(f"\nEscolha desconhecida: {escolha}")

        except Exception as e:
            log_error(e)
            continue

# --- Menu do Usuário Logado ----
def logado(usuario_logado):
    while(True):
        print("\n----------Menu----------")
        print("1) Reproduzir uma música")
        print("2) Listar músicas")
        print("3) Listar podcasts")
        print("4) Listar playlists")
        print("5) Reproduzir uma playlist")
        print("6) Criar nova playlist")
        print("7) Concatenar playlists")
        print("8) Gerar relatório")
        print("9) Sair")
        escolha = input(">> ")

        match escolha:
            case "1":
                try:
                    print("\nQual música você gostaria de ouvir?")
                    for m in musicas:
                        print(f"- {m.titulo}")
                    nome_musica = input(">> ")

                    musica_encontrada = None
                    for m in musicas:
                        if m.titulo.lower() == nome_musica.lower():
                            musica_encontrada = m
                            break

                    if not musica_encontrada:
                        print(f"\nA música '{nome_musica}' não foi encontrada.")
                        raise ValueError(f"Música não encontrada: {nome_musica}")

                    print(f"\nBuscando '{musica_encontrada.titulo}' de '{musica_encontrada.artista}' no YouTube...")
                    
                    query = f"{musica_encontrada.titulo} {musica_encontrada.artista}"
                    search = VideosSearch(query, limit=1)
                    video_url = search.result()['result'][0]['link']
                    
                    print("Abrindo a música no seu navegador...")
                    webbrowser.open(video_url)
                    
                    usuario_logado.ouvir_midia(musica_encontrada)
                    musica_encontrada.reproduzir()
                    
                    print(f"\nA reprodução de '{musica_encontrada.titulo}' foi registrada no sistema.")

                except Exception as e:
                    print(f"\nOcorreu um erro ao tentar reproduzir a música: {e}")
                    log_error(e)

            case "2":
                print("\n--- Músicas Disponíveis ---")
                for m in musicas:
                    print(f"- {m.titulo} por {m.artista}")

            case "3":
                print("\n--- Podcasts Disponíveis ---")
                for p in podcasts:
                         print(f"- {p.titulo} (T{p.temporada} E{p.episodio})")

            case "4":
                print(f"\n--- Playlists de {usuario_logado.nome} ---")
                for p in playlists:
                    if p.usuario.nome == usuario_logado.nome:
                        print(f"- {p.nome}")
                            
            case "5":
                try:
                    print("\nQual playlist deseja ouvir?")
                    print(f"--- Playlists de {usuario_logado.nome} ---")
                    
                    playlist_encontrada = False
                    for p in playlists:
                        if p.usuario.nome == usuario_logado.nome:
                            print(f"- {p.nome}")
                            playlist_encontrada = True
                    
                    if not playlist_encontrada:
                        print("Você ainda não criou nenhuma playlist.")
                        continue

                    nome_play = input("Playlist: ")
                    
                    playlist_tocada = False
                    for p in playlists:
                        if p.usuario.nome == usuario_logado.nome and p.nome.lower() == nome_play.lower():
                            print(f"\nReproduzindo a playlist '{p.nome}'...")
                            p.ouvir_playlist()
                            print(f"\nPlaylist '{p.nome}' finalizada. Reproduções totais da playlist: {p.reproducoes}")
                            playlist_tocada = True
                            break
                    
                    if not playlist_tocada:
                        print("Playlist não encontrada.")

                except Exception as e:
                    print(f"\nOcorreu um erro ao reproduzir a playlist: {e}")
                    log_error(e)

            case "6":
                try:
                    temp_list = []
                    temp_list_mostrar = []
                    
                    # Adicionar Músicas
                    while True:
                        print("\nEscolha quais musicas adicionar (Digite 'proximo' para continuar):")
                        for m in musicas: print(f"- {m.titulo}")
                        
                        temp_input = input("Musica: ")
                        if temp_input.lower() == 'proximo': break

                        if temp_input in temp_list_mostrar:
                            print("Essa musica já foi adicionada.")
                            continue
                        
                        musica_adicionada = False
                        for m in musicas:
                            if temp_input.lower() == m.titulo.lower():
                                temp_list.append(m)
                                temp_list_mostrar.append(m.titulo)
                                musica_adicionada = True
                                print(f"'{m.titulo}' adicionada.")
                                break
                        if not musica_adicionada: print("Musica não encontrada.")
                        print("Playlist atual:", temp_list_mostrar)
                    
                    # Adicionar Podcasts
                    while True:
                        print("\nEscolha quais podcasts adicionar (Digite 'proximo' para finalizar):")
                        for p in podcasts: print(f"- {p.titulo}")
                        
                        temp_input = input("Podcast: ")
                        if temp_input.lower() == 'proximo': break

                        if temp_input in temp_list_mostrar:
                            print("Esse podcast já foi adicionado.")
                            continue

                        podcast_adicionado = False
                        for p in podcasts:
                            if temp_input.lower() == p.titulo.lower():
                                temp_list.append(p)
                                temp_list_mostrar.append(p.titulo)
                                podcast_adicionado = True
                                print(f"'{p.titulo}' adicionado.")
                                break
                        if not podcast_adicionado: print("Podcast não encontrado.")
                        print("Playlist atual:", temp_list_mostrar)

                    print("\nComo gostaria de chamar sua playlist?")
                    nome_playlist = input("Nome: ")
                    
                    new_playlist = Playlist(nome_playlist, usuario_logado, temp_list)
                    if hasattr(usuario_logado, 'adicionar_playlist'):
                        usuario_logado.adicionar_playlist(new_playlist)
                    else:
                        if not hasattr(usuario_logado, 'playlists'): usuario_logado.playlists = []
                        usuario_logado.playlists.append(new_playlist)

                    playlists.append(new_playlist)
                    print("\nPlaylist nova adicionada com sucesso!")

                except Exception as e:
                    print(f"\nOcorreu um erro ao criar a playlist: {e}")
                    log_error(e)
                    
            
            
            case "9":
                return
            
            case _:
                print(f"\nEscolha desconhecida: {escolha}")

# --- Ponto de Entrada Principal ---
if __name__ == "__main__":
    # Esta linha executa o menu inicial quando o script é iniciado.
    menu_inicial()