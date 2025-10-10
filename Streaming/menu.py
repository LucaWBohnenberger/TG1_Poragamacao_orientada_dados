# streaming_app.py

# Imports necessários do seu sistema
from Streaming.usuario import Usuario
from Streaming.musica import Musica
from Streaming.playlist import Playlist
from Streaming.podcast import Podcast
from Streaming.analises import Analises

import os
from datetime import datetime
import traceback # Necessário para logs de erro detalhados

# Imports necessários para a Inovação (Abrir no Navegador)
from youtubesearchpython import VideosSearch
import webbrowser 
import time
import random

    # --- Função de Log (mantida global por ser um utilitário geral) ---
def log_error(log):
    """
    Registra uma mensagem de erro em um arquivo de log dentro da pasta 'logs',
    com timestamp formatado.
    """
    try:
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        log_file_path = os.path.join(log_dir, "log.txt")
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {type(log).__name__}: {str(log)}"
        
        with open(log_file_path, "a", encoding="utf-8") as file:
            file.write(log_message + "\n")
            
    except Exception as e:
        print(f"ERRO CRÍTICO NO SISTEMA DE LOG: {e}")


class Menu:
    def __init__(self, dados_file="config/dados.md"):
        self.usuarios = []
        self.playlists = []
        self.podcasts = []
        self.musicas = []
        self.dados_file = dados_file
        self._carregar_dados()

    def _carregar_dados(self):
        """
        Carrega os dados de usuários, músicas, podcasts e playlists do arquivo dados.md.
        Inclui validações para usuários e playlists duplicadas, e itens de playlist.
        """
        try:
            with open(self.dados_file, encoding="utf-8") as f:
                nome_variavel_leitura = ""
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
                            nome_variavel_leitura = " ".join(arr[2:])
                        elif arr[0].startswith("playlists:"):
                            usuario_ja_existe = False
                            for u in self.usuarios:
                                if u.nome.lower() == nome_variavel_leitura.lower():
                                    usuario_ja_existe = True
                                    break

                            if not usuario_ja_existe:
                                conteudo = " ".join(arr[1:])
                                conteudo = conteudo.strip("[]")
                                lista1 = [p.strip() for p in conteudo.split(",") if p.strip()]
                                
                                usuario_obj = Usuario(nome=nome_variavel_leitura, playlists=lista1)
                                self.usuarios.append(usuario_obj)
                            else:
                                mensagem_erro = f"Usuário duplicado encontrado no arquivo '{self.dados_file}': '{nome_variavel_leitura}'. O usuário não foi adicionado novamente."
                                print(f"Aviso: {mensagem_erro}")
                                log_error(ValueError(mensagem_erro))

                            nome_variavel_leitura = ""
                    
                    elif tipo == "Músicas":
                        if arr[0] == "-" and arr[1] == "titulo:":
                            titulo = " ".join(arr[2:])
                        elif arr[0] == "artista:":
                            artista = " ".join(arr[1:])
                        elif arr[0] == "genero:":
                            genero = " ".join(arr[1:])
                        elif arr[0] == "duracao:":
                            duracao = int(arr[1])
                            self.musicas.append(Musica(titulo=titulo, artista=artista, genero=genero, duracao=duracao))
                    
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
                            self.podcasts.append(Podcast(titulo=titulo, temporada=temporada, episodio=episodio, host=host, duracao=duracao))

                    elif tipo == "Playlists":
                        if arr[0] == "-" and arr[1] == "nome:":
                            nome_playlist = " ".join(arr[2:])
                        elif arr[0] == "usuario:":
                            usuario_playlist = " ".join(arr[1:])
                        elif arr[0].startswith("itens:"):
                            conteudo = " ".join(arr[1:])
                            conteudo = conteudo.strip("[]")
                            nomes_dos_itens = [p.strip() for p in conteudo.split(",") if p.strip()]

                            usuario_obj = None
                            for usuario in self.usuarios:
                                if usuario.nome == usuario_playlist:
                                    usuario_obj = usuario
                                    break

                            if usuario_obj is not None:
                                playlist_ja_existe = False
                                for p in self.playlists:
                                    if p.usuario == usuario_obj and p.nome.lower() == nome_playlist.lower():
                                        playlist_ja_existe = True
                                        break

                                if not playlist_ja_existe:
                                    itens_validados = []
                                    todas_as_midias = self.musicas + self.podcasts

                                    for nome_item in nomes_dos_itens:
                                        item_encontrado = None
                                        for midia in todas_as_midias:
                                            if midia.titulo.lower() == nome_item.lower():
                                                item_encontrado = midia
                                                break
                                        
                                        if item_encontrado:
                                            itens_validados.append(item_encontrado)
                                        else:
                                            mensagem_erro = f"Item '{nome_item}' listado na playlist '{nome_playlist}' do usuário '{usuario_obj.nome}' no arquivo '{self.dados_file}' não foi encontrado e será ignorado."
                                            print(f"Aviso: {mensagem_erro}")
                                            log_error(ValueError(mensagem_erro))

                                    self.playlists.append(Playlist(nome=nome_playlist, usuario=usuario_obj, itens=itens_validados))
                                else:
                                    mensagem_erro = f"Playlist duplicada para o usuário '{usuario_obj.nome}' no arquivo '{self.dados_file}': '{nome_playlist}'. A playlist não foi carregada novamente."
                                    print(f"Aviso: {mensagem_erro}")
                                    log_error(ValueError(mensagem_erro))
                            else:
                                print(f"Aviso: usuário '{usuario_playlist}' não encontrado para a playlist '{nome_playlist}' no arquivo '{self.dados_file}'")
                                log_error(ValueError(f"Usuário '{usuario_playlist}' não encontrado para a playlist '{nome_playlist}'."))

        except FileNotFoundError:
            print(f"Erro: Arquivo '{self.dados_file}' não encontrado. Certifique-se de que ele existe na pasta 'config'.")
            log_error(FileNotFoundError(f"Arquivo '{self.dados_file}' não encontrado."))
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")
            log_error(e)


    def menu_inicial(self):
        """
        Exibe o menu inicial e gerencia as opções do usuário.
        """
        while True:
            try:
                print("\n----------Menu----------")
                print("1) Entrar como usuário")
                print("2) Criar novo usuário")
                print("3) Listar usuários")
                print("4) Sair")
                escolha = input(">> ")

                match escolha:
                    case "1":
                        while True:
                            print("\nQual o nome do seu usuário?")
                            print("Digite 'Retorno' para retornar")
                            nome_login = input(">> ")

                            if nome_login.lower() == "retorno":
                                break
                            if nome_login == "nicolas Cage":
                                iniciar_surto_cage()
                                continue # Após o easter egg, volta para a escolha de login
                            
                            usuario_encontrado = None
                            for u in self.usuarios:
                                if u.nome.lower() == nome_login.lower():
                                    usuario_encontrado = u
                                    break

                            if usuario_encontrado:
                                print(f"\nUsuário válido, bem vindo {usuario_encontrado.nome}")
                                self._menu_logado(usuario_encontrado)
                                break # Sai do loop de login após logar
                            else:
                                print("\nUsuário inválido!")
                                raise ValueError(f"Tentativa de login com usuário não existente: '{nome_login}'")

                    case "2":
                        print("\nQual o nome do usuario novo?")
                        print("Nota: por favor não use o nome de um usuário já existente")
                        tentativa_nome = input(">> ")
                        
                        usuario_ja_existe = False
                        for u in self.usuarios:
                            if u.nome.lower() == tentativa_nome.lower():
                                usuario_ja_existe = True
                                break

                        if not usuario_ja_existe:
                            print("Usuário válido")
                            self.usuarios.append(Usuario(nome=tentativa_nome))
                            print("Usuário criado")
                        else:
                            print("Usuário inválido!")
                            raise ValueError(f"Usuário já existente na base de dados: '{tentativa_nome}'")
                        
                    case "3":
                        print("\n--- Usuários Cadastrados ---")
                        if not self.usuarios:
                            print("Nenhum usuário cadastrado.")
                        else:
                            for u in self.usuarios:
                                print(f"- {u.nome}")

                    case "4":
                        print("\nObrigado por utilizar nosso serviço!")
                        return # Sai do loop principal do menu inicial
                    
                    case _:
                        print(f"\nEscolha desconhecida: {escolha}")

            except Exception as e:
                print(f"\nOcorreu um erro no menu inicial: {e}")
                log_error(e)
                continue

    def _menu_logado(self, usuario_logado: Usuario):
        """
        Exibe o menu do usuário logado e gerencia suas opções.
        """
        while True:
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
                        if not self.musicas:
                            print("Nenhuma música cadastrada.")
                            continue
                        for m in self.musicas:
                            print(f"- {m.titulo}")
                        nome_musica = input(">> ")

                        musica_encontrada = None
                        for m in self.musicas:
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
                    if not self.musicas:
                        print("Nenhuma música cadastrada.")
                    else:
                        for m in self.musicas:
                            print(f"- {m.titulo} por {m.artista}")

                case "3":
                    print("\n--- Podcasts Disponíveis ---")
                    if not self.podcasts:
                        print("Nenhum podcast cadastrado.")
                    else:
                        for p in self.podcasts:
                            print(f"- {p.titulo} ({p.temporada} E{p.episodio})")

                case "4":
                    print(f"\n--- Playlists de {usuario_logado.nome} ---")
                    playlists_do_usuario = [p for p in self.playlists if p.usuario.nome == usuario_logado.nome]
                    if not playlists_do_usuario:
                        print(f"Você ainda não criou nenhuma playlist.")
                    else:
                        for p in playlists_do_usuario:
                            print(f"- {p.nome}")
                            
                case "5":
                    try:
                        print("\nQual playlist deseja ouvir?")
                        print(f"--- Playlists de {usuario_logado.nome} ---")
                        
                        playlists_do_usuario = [p for p in self.playlists if p.usuario.nome == usuario_logado.nome]

                        if not playlists_do_usuario:
                            print("Você ainda não criou nenhuma playlist.")
                            continue
                        
                        for p in playlists_do_usuario:
                            print(f"- {p.nome}")

                        nome_play = input("Playlist: ")
                        
                        playlist_tocada = False
                        for p in playlists_do_usuario: # Busca apenas nas playlists do usuário
                            if p.nome.lower() == nome_play.lower():
                                print(f"\nReproduzindo a playlist '{p.nome}'...")
                                p.ouvir_playlist() # Incrementa reproduções da playlist
                                
                                print("Adicionando faixas ao seu histórico de reprodução...")
                                for midia_item in p.itens:
                                    usuario_logado.ouvir_midia(midia_item)
                                
                                print(f"\nPlaylist '{p.nome}' finalizada. Itens adicionados ao seu histórico.")
                                print(f"Reproduções totais desta playlist: {p.reproducoes}")
                                playlist_tocada = True
                                break
                        
                        if not playlist_tocada:
                            print("Playlist não encontrada.")

                    except Exception as e:
                        print(f"\nOcorreu um erro ao reproduzir a playlist: {e}")
                        log_error(e)

                case "6":
                    try:
                        temp_list = [] # Armazenará objetos de Musica/Podcast
                        temp_list_mostrar = [] # Armazenará títulos para exibição
                        
                        # Adicionar Músicas
                        while True:
                            print("\nEscolha quais musicas adicionar (Digite 'proximo' para continuar):")
                            if not self.musicas:
                                print("Nenhuma música disponível para adicionar.")
                                break
                            for m in self.musicas: print(f"- {m.titulo}")
                            
                            temp_input = input("Musica: ")
                            if temp_input.lower() == 'proximo': break

                            if temp_input in temp_list_mostrar:
                                print("Essa musica já foi adicionada.")
                                continue
                            
                            musica_adicionada = False
                            for m in self.musicas:
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
                            if not self.podcasts:
                                print("Nenhum podcast disponível para adicionar.")
                                break
                            for p in self.podcasts: print(f"- {p.titulo}")
                            
                            temp_input = input("Podcast: ")
                            if temp_input.lower() == 'proximo': break

                            if temp_input in temp_list_mostrar:
                                print("Esse podcast já foi adicionado.")
                                continue

                            podcast_adicionado = False
                            for p in self.podcasts:
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

                        nome_ja_existe = False
                        for p in self.playlists:
                            if p.usuario.nome == usuario_logado.nome and p.nome.lower() == nome_playlist.lower():
                                nome_ja_existe = True
                                break

                        if nome_ja_existe:
                            mensagem_erro = f"Você já possui uma playlist com o nome '{nome_playlist}'. Por favor, escolha outro nome."
                            print(f"\nERRO: {mensagem_erro}")
                            log_error(ValueError(mensagem_erro))
                        else:
                            new_playlist = Playlist(nome_playlist, usuario_logado, temp_list)
                            
                            # A lógica de adicionar_playlist já lida com a existência do método
                            if hasattr(usuario_logado, 'adicionar_playlist'):
                                usuario_logado.adicionar_playlist(new_playlist)
                            else: # Fallback defensivo
                                if not hasattr(usuario_logado, 'playlists'): usuario_logado.playlists = []
                                usuario_logado.playlists.append(new_playlist)

                            self.playlists.append(new_playlist)
                            print("\nPlaylist nova adicionada com sucesso!")

                    except Exception as e:
                        print(f"\nOcorreu um erro ao criar a playlist: {e}")
                        log_error(e)
                
                case "7":
                    try:
                        playlists_selecionadas_para_concatenar = []
                        nomes_playlists_selecionadas = []
                        
                        while True:
                            print("\nQuais playlists você gostaria de concatenar? (digite 'proximo' para prosseguir)")
                            playlists_do_usuario = [p for p in self.playlists if p.usuario.nome == usuario_logado.nome]
                            if not playlists_do_usuario:
                                print("Você ainda não criou nenhuma playlist para concatenar.")
                                break # Sai do loop de seleção se não há playlists
                            
                            for p in playlists_do_usuario:
                                print(f"- {p.nome}")
                            
                            temp_input = input("Playlist: ")
                            if temp_input.lower() == 'proximo':
                                if len(playlists_selecionadas_para_concatenar) < 2:
                                    print("Por favor, selecione pelo menos duas playlists para concatenar.")
                                    continue
                                break

                            if temp_input in nomes_playlists_selecionadas:
                                print("Essa playlist já foi selecionada.")
                                continue
                            
                            playlist_encontrada = False
                            for p in playlists_do_usuario:
                                if p.nome.lower() == temp_input.lower():
                                    playlists_selecionadas_para_concatenar.append(p)
                                    nomes_playlists_selecionadas.append(p.nome)
                                    playlist_encontrada = True
                                    print(f"Playlist '{p.nome}' adicionada para concatenação.")
                                    break
                            
                            if not playlist_encontrada:
                                print("Playlist não encontrada ou não pertence a você.")
                            
                            print("Playlists selecionadas:", nomes_playlists_selecionadas)
                        
                        if len(playlists_selecionadas_para_concatenar) < 2:
                            print("Concatenação cancelada: número insuficiente de playlists selecionadas.")
                            continue # Volta ao menu logado

                        lista_midia_concatenada = []
                        for playlist in playlists_selecionadas_para_concatenar:
                            for midia_obj in playlist.itens:
                                lista_midia_concatenada.append(midia_obj)
                        
                        lista_midia_concatenada_unica_titulos = list(set([m.titulo for m in lista_midia_concatenada]))
                        # Re-obter os objetos reais com base nos títulos únicos
                        itens_finais_concatenados = []
                        todas_as_midias_disponiveis = self.musicas + self.podcasts
                        for titulo_unico in lista_midia_concatenada_unica_titulos:
                            for midia_obj in todas_as_midias_disponiveis:
                                if midia_obj.titulo.lower() == titulo_unico.lower():
                                    itens_finais_concatenados.append(midia_obj)
                                    break


                        print("\nQual o nome da nova playlist concatenada?")
                        nome_nova_playlist_concatenada = input("Nome: ")

                        # Verifica se o nome da nova playlist concatenada já existe para o usuário
                        nome_concatenada_ja_existe = False
                        for p in self.playlists:
                            if p.usuario.nome == usuario_logado.nome and p.nome.lower() == nome_nova_playlist_concatenada.lower():
                                nome_concatenada_ja_existe = True
                                break
                        
                        if nome_concatenada_ja_existe:
                            mensagem_erro = f"Você já possui uma playlist com o nome '{nome_nova_playlist_concatenada}'. Por favor, escolha outro nome para a playlist concatenada."
                            print(f"\nERRO: {mensagem_erro}")
                            log_error(ValueError(mensagem_erro))
                            continue # Volta ao menu logado
                        
                        new_playlist_concatenada = Playlist(nome_nova_playlist_concatenada, usuario_logado, itens_finais_concatenados)
                        
                        if hasattr(usuario_logado, 'adicionar_playlist'):
                            usuario_logado.adicionar_playlist(new_playlist_concatenada)
                        else:
                            if not hasattr(usuario_logado, 'playlists'): usuario_logado.playlists = []
                            usuario_logado.playlists.append(new_playlist_concatenada)

                        self.playlists.append(new_playlist_concatenada)
                        print(f"\nPlaylist '{nome_nova_playlist_concatenada}' criada com sucesso a partir da concatenação!")

                    except Exception as e:
                        print(f"\nOcorreu um erro ao concatenar playlists: {e}")
                        log_error(e)
                
                case "8":
                    print("\n--- Gerando Relatório de Análises ---")

                    # EXIBIÇÃO NO CONSOLE
                    top_3 = Analises.top_musicas_reproduzidas(self.musicas, 3)
                    print("\nTop 3 Músicas Mais Ouvidas:")
                    for i, musica in enumerate(top_3):
                        print(f"{i+1}. {musica.titulo} ({musica.reproducoes} plays)")

                    popular = Analises.playlist_mais_popular(self.playlists)
                    if popular:
                        print(f"\nPlaylist Mais Popular: {popular.nome} ({popular.reproducoes} plays)")
                    else:
                        print("\nNenhuma playlist popular encontrada.")


                    ativo = Analises.usuario_mais_ativo(self.usuarios)
                    if ativo:
                        print(f"\nUsuário Mais Ativo: {ativo.nome} ({len(ativo.historico)} faixas ouvidas)")
                    else:
                        print("\nNenhum usuário ativo encontrado.")

                    total_plays = Analises.total_reproducoes(self.usuarios)
                    print(f"\nTotal de Reproduções no Sistema: {total_plays}")

                    # GERAÇÃO DO ARQUIVO DE RELATÓRIO
                    print("\nGerando arquivo de relatório...")
                    resultado = Analises.gerar_relatorio_completo(self.musicas, self.playlists, self.usuarios)

                    if isinstance(resultado, str):
                        print(f"Relatório salvo com sucesso em: '{resultado}'")
                    else:
                        print(f"Ocorreu um erro ao gerar o relatório: {resultado}")
                        log_error(resultado)
                    
                case "9":
                    return # Sai do loop do menu logado
                
                case _:
                    print(f"\nEscolha desconhecida: {escolha}")
                    log_error(ValueError(f"Escolha de menu desconhecida no modo logado: {escolha}"))
                    
                    
                    



def iniciar_surto_cage():
    """
    Orquestra o evento completo do surto Nicolas Cage.
    """
    try:
        # Parte 1: O Colapso do Terminal
        os.system('cls' if os.name == 'nt' else 'clear')
        frases_caoticas = [
            "NÃO AS ABELHAS!", "AHHHH, ELAS ESTÃO NOS MEUS OLHOS!",
            "EU VOU ROUBAR A DECLARAÇÃO DE INDEPENDÊNCIA.",
            "COLOQUE O COELHINHO DE VOLTA NA CAIXA.",
            "EU SOU UM VAMPIRO! EU SOU UM VAMPIRO!",
            "COMO FOI QUE QUEIMOU!? COMO FOI QUE QUEIMOU!?",
            "EU PODERIA COMER UM PÊSSEGO POR HORAS.", "A! B! C! D! E! F! G!",
            "EU QUERO ARRANCAR... A CARA DELE... FORA.",
            "É COMO OLHAR NO ESPELHO, SÓ QUE... NÃO.",
            "MINHA ALMA ESTÁ PEGANDO FOGO!",
            "O QUE VOCÊ ACHA QUE EU VOU FAZER? EU VOU SALVAR A PORRA DO DIA!",
            "EU PERDI MINHA MÃO! EU PERDI MINHA NOIVA!",
            "TODA VEZ QUE EU PENSO EM VOCÊ, MINHA CABEÇA EXPLODE.",
            "CORTA O PAPINHO, BABACA.",
            "EU SOU UM GRANDE FÃ DA DECLARAÇÃO DE INDEPENDÊNCIA.",
            "SYSTEM_FAILURE::CAGE_ENTITY_UNLEASHED",
            "ERRO CRÍTICO: NÍVEL DE 'CAGE' ACIMA DO SUPORTÁVEL.",
            "SOBRESCREVENDO REALIDADE... POR FAVOR, AGUARDE.",
            "INICIANDO PROTOCOLO 'TESOURO NACIONAL'...",
            "ALERTA: O COELHO NÃO ESTÁ NA CAIXA."
        ]
        
        cores_glitch = ['\033[91m', '\033[93m', '\033[92m', '\033[96m']
        for _ in range(30):
            os.system('cls' if os.name == 'nt' else 'clear')
            cor = random.choice(cores_glitch)
            frase = random.choice(frases_caoticas)
            print(cor + frase * random.randint(1, 3) + '\033[0m')
            time.sleep(0.1)

        # Parte 2: A Criação dos Artefatos no Desktop
        print("\n\n\033[91mVIOLAÇÃO DE PROTOCOLO! CRIANDO ARTEFATOS EXTERNOS...\033[0m")
        time.sleep(1.5)
        
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
        
        print(f"\033[0mFORAM CRIADOS {i+1} ARTEFATOS EM SEU DESKTOP.")
        time.sleep(2)

        # Parte 3: A Bomba de Navegador
        print("\n\033[91mINICIANDO PROTOCOLO DE EXPOSIÇÃO GLOBAL...\033[0m")
        time.sleep(1.5)
        
        urls_cage = [
            "https://www.youtube.com/watch?v=aEtm69mLK6w", # Not the Bees
            "https://www.youtube.com/watch?v=IUB-wjXUREE", # Alphabet
            "https://www.imdb.com/name/nm0000115/",         # IMDB
            "https://en.wikipedia.org/wiki/Action_comics_1", # Referência ao roubo do gibi dele
            "https://www.youtube.com/watch?v=xvFZjo5PgG0&list=RDxvFZjo5PgG0&start_radio=1",
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
        # Nota: playsound precisa ser importado ou estar em um arquivo playsound.py
        # Se 'playsound' for uma biblioteca externa, certifique-se de que está instalada: pip install playsound
        try:
            from playsound import playsound
            playsound('cage_grito.mp3')
        except ImportError:
            print("AVISO: A biblioteca 'playsound' não está instalada ou 'cage_grito.mp3' não foi encontrada.")
            print("Instale com 'pip install playsound' se desejar a funcionalidade de áudio.")
            log_error("ImportError: playsound não encontrada ou 'cage_grito.mp3' ausente.")
            
    except Exception as e:
        print(f"\033[91mFALHA NO SURTO CAGE: {e}\033[0m")
        log_error(f"FALHA NO EASTER EGG: {e}")
    finally:
        # Parte 5: A Calmaria
        print("\n\n\033[0mCONTENÇÃO DO SURTO REALIZADA. RETORNANDO À OPERAÇÃO NORMAL.")
        time.sleep(4)
        os.system('cls' if os.name == 'nt' else 'clear')