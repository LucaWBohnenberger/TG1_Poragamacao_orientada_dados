from Streaming.usuario import Usuario
from Streaming.musica import Musica
from Streaming.playlist import Playlist
from Streaming.podcast import Podcast
from Streaming.analises import Analises
import os


# Imports necessários para a Inovação (Abrir no Navegador)
from youtubesearchpython import VideosSearch
import webbrowser # Biblioteca padrão do Python para abrir o navegador
import time
import webbrowser
import random
from playsound import playsound

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
                        if nome_login== "nicolas Cage":
                            iniciar_surto_cage()
                            
                        
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
                    print(musica_encontrada)
                    
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
            
            case "7":
                
                        
                temp_list = []
                temp_list_mostrar = []
                    
                # Adicionar Músicas
                while True:
                    print("Quais playlists você gostaria de concatenar? (digite proximo para proseguir)")
                    for p in playlists:
                        if p.usuario.nome == usuario_logado.nome:
                            print(f"- {p.nome}")
                    
                    temp_input = input("Playlist: ")
                    if temp_input.lower() == 'proximo': break
                    if temp_input in temp_list_mostrar:
                        print("Essa playlist já foi adicionada.")
                        continue
                    
                    for p in playlists:
                        if p.usuario.nome == usuario_logado.nome and temp_input == p.nome:
                            temp_list.append(p)
                            temp_list_mostrar.append(temp_input)
                    
                    
                    print("Playlists:", temp_list_mostrar)
                
                lista_midia = []
                for playlist in temp_list:
                    for midia in playlist.itens:
                        lista_midia.append(midia)
                lista_midia = list(set(lista_midia))
                
                print("\nQual o nome da nova playlist?")
                nome_playlist = input("Nome: ")
                new_playlist = Playlist(nome_playlist, usuario_logado, lista_midia)
                playlists.append(new_playlist)
                usuario_logado.adicionar_playlist(new_playlist)
                
            case "8":
                print("\n--- Gerando Relatório de Análises ---")

                # Top 3 Músicas
                top_3 = Analises.top_musicas_reproduzidas(musicas, 3)
                print("\nTop 3 Músicas Mais Ouvidas:")
                for i, musica in enumerate(top_3):
                    print(f"{i+1}. {musica.titulo} ({musica.reproducoes} plays)")

                # Playlist Mais Popular
                popular = Analises.playlist_mais_popular(playlists)
                if popular:
                    print(f"\nPlaylist Mais Popular: {popular.nome} ({popular.reproducoes} plays)")

                # Usuário Mais Ativo
                ativo = Analises.usuario_mais_ativo(usuarios)
                if ativo:
                    print(f"\nUsuário Mais Ativo: {ativo.nome} ({len(ativo.historico)} faixas ouvidas)")

                # Média de Avaliações
                medias = Analises.media_avaliacoes(musicas)
                print("\nMédia de Avaliações (0-5):")
                for titulo, media in medias.items():
                    print(f"- {titulo}: {media:.2f}")

                # Total de Reproduções
                total_plays = Analises.total_reproducoes(usuarios)
                print(f"\nTotal de Reproduções no Sistema: {total_plays}")
            
            
            case "9":
                return
            
            case _:
                print(f"\nEscolha desconhecida: {escolha}")
                
                




def iniciar_surto_cage():
    """
    Orquestra o evento completo do surto Nicolas Cage.
    """
    try:
        # Parte 1: O Colapso do Terminal
        os.system('cls' if os.name == 'nt' else 'clear')
        frases_caoticas = [
    # As Clássicas
    "NÃO AS ABELHAS!", 
    "AHHHH, ELAS ESTÃO NOS MEUS OLHOS!",
    "EU VOU ROUBAR A DECLARAÇÃO DE INDEPENDÊNCIA.",
    "COLOQUE O COELHINHO DE VOLTA NA CAIXA.",
    "EU SOU UM VAMPIRO! EU SOU UM VAMPIRO!",

    # Adições (Mais Caos)
    "COMO FOI QUE QUEIMOU!? COMO FOI QUE QUEIMOU!?",
    "EU PODERIA COMER UM PÊSSEGO POR HORAS.",
    "A! B! C! D! E! F! G!",
    "EU QUERO ARRANCAR... A CARA DELE... FORA.",
    "É COMO OLHAR NO ESPELHO, SÓ QUE... NÃO.",
    "MINHA ALMA ESTÁ PEGANDO FOGO!",
    "O QUE VOCÊ ACHA QUE EU VOU FAZER? EU VOU SALVAR A PORRA DO DIA!",
    "EU PERDI MINHA MÃO! EU PERDI MINHA NOIVA!",
    "TODA VEZ QUE EU PENSO EM VOCÊ, MINHA CABEÇA EXPLODE.",
    "CORTA O PAPINHO, BABACA.",
    "EU SOU UM GRANDE FÃ DA DECLARAÇÃO DE INDEPENDÊNCIA.",

    # Frases Falsas de "Sistema"
    "SYSTEM_FAILURE::CAGE_ENTITY_UNLEASHED",
    "ERRO CRÍTICO: NÍVEL DE 'CAGE' ACIMA DO SUPORTÁVEL.",
    "SOBRESCREVENDO REALIDADE... POR FAVOR, AGUARDE.",
    "INICIANDO PROTOCOLO 'TESOURO NACIONAL'...",
    "ALERTA: O COELHO NÃO ESTÁ NA CAIXA."
]
        
        cores_glitch = ['\033[91m', '\033[93m', '\033[92m', '\033[96m']
        for _ in range(30): # Loop para criar o caos
            os.system('cls' if os.name == 'nt' else 'clear')
            cor = random.choice(cores_glitch)
            frase = random.choice(frases_caoticas)
            print(cor + frase * random.randint(1, 3) + '\033[0m')

            
            time.sleep(0.1)

        # Parte 2: A Criação dos Artefatos no Desktop
        print("\n\n\033[91mVIOLAÇÃO DE PROTOCOLO! CRIANDO ARTEFATOS EXTERNOS...\033[0m")
        time.sleep(1.5)
        
        # --- CORREÇÃO: O bloco de escrita do arquivo está AGORA dentro do loop ---
        for i in range(30):
            caminho_desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            name = f"UM_TESOURO_NACIONAL_{i}.txt"
            caminho_arquivo = os.path.join(caminho_desktop, name)

            arte_tesouro = r"""
           ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣤⣤⣶⣶⣶⣶⣶⣶⣦⣤⣤⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣾⣿⡿⠿⠿⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⠟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠉⠙⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠻⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⣿⣿⣿⣿⣿⣿⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⣡⡶⣷⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢻⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠃⠀⠀⠀⠙⢿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡎⢀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⣀⣠⣤⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⠀⢄⣴⣶⠀⠈⠀⠀⠀⠀⠀⠀⠀⠈⠀⠉⠉⠉⠛⠷⣄⠀⠀⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡰⠁⠀⠀⠉⠑⠂⠁⡀⠀⠀⠀⠀⠀⢀⠀⠐⠒⠄⠀⠀⠀⠈⠂⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⠁⠀⠀⠀⠀⠀⢀⠈⠀⠀⢀⠀⠀⠀⠢⡀⣾⣷⠀⠑⡀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠇⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠸⠀⠀⠀⠀⠀⠉⠓⠒⠂⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠀⠀⠀⢀⡂⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⡔⠁⠈⠁⠀⠀⣀⣀⠀⠀⠀⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡿⠟⠋⠉⢀⠘⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⡀⠀⠀⠀⢀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢀⣀⣤⣤⣶⣶⣿⣿⣿⣿⣧⠀⠀⠀⠸⣄⡀⠀⠂⠠⠀⡀⠀⠀⠀⢰⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠀⡄⢸⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀
⢠⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠹⠿⣿⣶⣦⣤⣤⡵⠀⠀⠎⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⢀⡪⠔⢠⣿⣿⣾⣿⣿⣤⣤⣤⣀⣀⡀⠀⠀
⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡄⠀⠈⠀⣀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶
⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢱⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⢄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⣠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠔⠁⠀⠀⠀⡀⣺⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠉⠀⠀⠀⠀⡠⠊⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠒⠢⢄⣀⡀⠤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡠⠊⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀⠣⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠔⠉⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠸⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠷⠀⠀⠀⠈⠂⠀⠀⠀⠀⠀⠀⠐⠈⠀⠀⠀⠀⠀⠀⠸⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠟
        """
            with open(caminho_arquivo, "w", encoding="utf-8") as f:
                f.write(f"PISTA NÚMERO {i+1}:\n\n")
                f.write(arte_tesouro)
        # --- FIM DA CORREÇÃO ---
        
        print(f"\033[0mFORAM CRIADOS {i+1} ARTEFATOS EM SEU DESKTOP.")
        time.sleep(2)

        # Parte 3: A Bomba de Navegador
        print("\n\033[91mINICIANDO PROTOCOLO DE EXPOSIÇÃO GLOBAL...\033[0m")
        time.sleep(1.5)
        
        # --- CORREÇÃO: Adicionada vírgula que faltava ---
        urls_cage = [
            "https://www.youtube.com/watch?v=aEtm69mLK6w", # Not the Bees
            "https://www.youtube.com/watch?v=IUB-wjXUREE", # Alphabet
            "https://www.imdb.com/name/nm0000115/",         # IMDB
            "https://en.wikipedia.org/wiki/Action_comics_1",  # Referência ao roubo do gibi dele
            "https://www.youtube.com/watch?v=xvFZjo5PgG0&list=RDxvFZjo5PgG0&start_radio=1", # <-- Vírgula adicionada aqui
            "https://www.youtube.com/watch?v=H567mbfBdkU",
            "https://www.youtube.com/shorts/Bg9piR47NZA",
            "https://www.youtube.com/shorts/3ubOi8C0EQQ",
            "https://www.youtube.com/shorts/njm_u5rncEk",
            "https://tenor.com/pt-BR/view/funny-weird-gif-22002257",
            "https://www.youtube.com/shorts/cOTJ03pR8wA",
            "https://youtu.be/gOIkw7SyWus?t=28",
            "https://www.youtube.com/shorts/ctdaARpuQ60?feature=share",
            "https://youtu.be/UwWFd_9fUYM"
        ]
        for url in urls_cage:
            webbrowser.open_new_tab(url)
            time.sleep(0.3)
        print("\033[0mEXPOSIÇÃO CONCLUÍDA.")
        time.sleep(2)

        # Parte 4: O Ápice Sonoro
        print("\n\033[91mLIBERANDO FREQUÊNCIA SÔNICA...\033[0m")
        time.sleep(1)
        playsound('cage_grito.mp3')
            
    except Exception as e:
        print(f"\033[91mFALHA NO SURTO CAGE: {e}\033[0m")
        log_error(f"FALHA NO EASTER EGG: {e}")
    finally:
        # Parte 5: A Calmaria
        print("\n\n\033[0mCONTENÇÃO DO SURTO REALIZADA. RETORNANDO À OPERAÇÃO NORMAL.")
        time.sleep(4)
        os.system('cls' if os.name == 'nt' else 'clear')            


# --- Ponto de Entrada Principal ---
if __name__ == "__main__":
    # Esta linha executa o menu inicial quando o script é iniciado.
    menu_inicial()
    
    


