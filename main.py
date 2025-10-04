from Streaming.usuario import Usuario
from Streaming.musica import Musica
from Streaming.playlist import Playlist
from Streaming.podcast import Podcast
usuarios = []
playlists = []
podcasts = []
musicas = []

nome = ""
lista1 = []


def log_error(log):
    with open("log.txt", "a") as file:
        file.write(str(log) + "\n")
    


# Need to read and store an array for playlists, musicas and podcasts
try:
    with open("config/dados.md", encoding="utf-8") as f:
        nome = ""
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
                    nome = arr[2]
                elif arr[0].startswith("playlists:"):
                    conteudo = " ".join(arr[1:])
                    conteudo = conteudo.strip("[]")
                    lista1 = [p.strip() for p in conteudo.split(",") if p.strip()]
                    usuarios.append(Usuario(nome=nome, playlists=lista1))
            
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
                pass
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
                pass
            elif tipo == "Playlists":
                if arr[0] == "-" and arr[1] == "nome:":
                    nome = " ".join(arr[2:])
                elif arr[0] == "usuario:":
                    usuario_playlist = " ".join(arr[1:])
                elif arr[0].startswith("itens:"):
                    conteudo = " ".join(arr[1:])
                    conteudo = conteudo.strip("[]")
                    itens = [p.strip() for p in conteudo.split(",") if p.strip()]

                    # Acha o usuario na lista de usuarios, isso é seguro já que os usuarios são todos registrados primeiro
                    usuario_obj = None
                    for usuario in usuarios:
                        if usuario.nome == usuario_playlist:
                            usuario_obj = usuario
                            break

                    # Valida se o usuário existe, se não loga o erro
                    if usuario_obj is not None:
                        playlists.append(Playlist(nome=nome, usuario=usuario_obj, itens=itens))
                    else:
                        print(f"Aviso: usuário '{usuario_playlist}' não encontrado para a playlist '{nome}'")
                        ValueError(f"Usuário '{usuario_playlist}' não encontrado para a playlist '{nome}'.")

except Exception as e:
    log_error(e)


def menu_inicial():
    while(True):
        try:
            print("\n----------Menu----------")
            print("1) Entrar como usuário")
            print("2) Criar novo usuário")
            print("3) Listar usuários")
            print("4) Sair")
            escolha = input()

            match escolha:
                case "1":
                    while(True):
                        print("Qual o nome do seu usuário?")
                        print("Digite 'Retorno' para retornar")
                        nome_login = input()

                        # Checando retorno para evitar check extra
                        if(nome_login == "Retorno"):
                            break

                        # Validação se usuario existe para login
                        tentativa_login = Usuario.usuario_existente(nome_login)
                        if(tentativa_login):
                            print("Usuário válido, bem vindo")
                            logado(nome_login)
                            break
                        else:
                            print("Usuário inválido!")
                            raise ValueError("Nome não existente na base de dados")

                case "2":
                    print("Qual o nome do usuario novo?")
                    print("\nNota-se, por favor não use o nome de um usuário já existente")
                    tentativa_nome = input()
                    tentativa_criar = Usuario.usuario_existente(tentativa_nome)
                    if(not tentativa_criar):
                        print("Usuário válido")
                        usuarios.append(Usuario(nome=tentativa_nome))
                        # Sera que pode dar algum erro?
                        print("Usuário criado")
                    else:
                        print("Usuário inválido!")
                        raise ValueError("Usuário já existente na base de dados!")
                case "3":
                    Usuario.lista_nomes()
                case "4":
                    print("Obrigado por utilizar nosso serviço!")
                    return
                case _:
                    print(f"Escolha desconhecida: {escolha}")
                    pass

        except Exception as e:
            log_error(e)
            continue




def logado(nome):
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
        escolha = input()

        match escolha:
            case "2":
                Musica.lista_titulos()
                pass
            case "3":
                Podcast.lista_titulos()
                pass
            case "4":
                Playlist.lista_nome(nome, playlists)
                pass
            case "9":
                return
            case _:
                print(f"Escolha desconhecida: {escolha}")
                pass



menu_inicial()

