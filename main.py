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


                
            



while(True):
    print("----------Menu----------")
    print("1) Entrar como usuário")
    print("2) Criar novo usuário")
    print("3) Listar usuários")
    print("4) Sair")
    escolha = input()
    if not escolha in "1 2 3 4".split():
        print("Por favor, digite um numero entre 1 a 4")
        pass
    if escolha == "1":
        print(usuarios[0])
    if escolha == "4":
        break

