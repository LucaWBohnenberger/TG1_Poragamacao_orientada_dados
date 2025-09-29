from Streaming.usuario import Usuario

usuarios = []


nome = ""
lista1 = []


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


def log_error(log):
    with open("log.txt", "a") as file:
        file.write(str(log) + "\n")

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
                            logado()
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




def logado():
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
            case "9":
                menu_inicial()
            case _:
                print(f"Escolha desconhecida: {escolha}")
                pass












menu_inicial()

