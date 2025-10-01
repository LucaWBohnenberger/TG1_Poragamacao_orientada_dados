from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # Precisamos evitar imports circulares
    from playlist import Playlist
    from arquivo_de_midia import ArquivoDeMidia

class Usuario:
    """ 
    Classe de usuarios.

    nome:str: Nome do usuario, identificador. 
    playlists:Playlist: Identificador do objeto playlists. @String
    historico:list[Musica]: Musicas reproduzidas pelo usuario. 
    """
    qntd_instancias = 0
    nomes = []

    def __init__(self, nome:str, playlists:list['Playlist']=None, historico:list['ArquivoDeMidia.titulo']=None):
        """ Inicializador da classe """
        self.nome = nome
        self.playlists = playlists if playlists is not None else []
        self.historico = historico if historico is not None else []
        Usuario.new_user()
        Usuario.nomes.append(self.nome) # append para poder guardar nomes, usado em alguns metodos

    def __str__(self):
        return f"Nome: {self.nome} \nPlaylists: {self.playlists} \nHistórico: {self.historico}\nPlaylists: {self.playlists}"
        



    @classmethod
    def new_user(cls):
        cls.qntd_instancias += 1

    @classmethod
    def lista_nomes(cls):
        """ Imprime a lista de usuarios atualmente inicializados """
        print("Usuários registrados:")
        for nome in cls.nomes:
            if nome is not None:
                print("- " + nome)
        return
    
    @classmethod
    def usuario_existente(cls, nome):
        """ Valida se o usuario existe, um simples verdadeiro ou falso """
        if(nome in cls.nomes):
            return True
        return False
    
        
    @classmethod
    def criar_playlist(cls, nome):
        """ Adiciona uma playlist nova na conta do usuário """
        if(nome in cls.playlist.nomes):
            print("Uma playlist com esse nome já existe na sua conta!")
            print("Gostaria de adicionar musicas nessa playlist?\n S|N")
            escolha = input()
            match escolha:
                case "S":
                    pass
                case "N":
                    return
                case _:
                    print("Valor inválido")
                    raise ValueError("criar_playlist: Valor de input não reconhecido")

        midias = []
        while(True):
            print("Digite o nome da mídia que gostaria de adicionar na playlist:")
            midias.append()
        # TO-DO: When we have the musicas and podcasts lists we can send them as a parameter
        # and make the comparisons here, until then we are stuck
        cls.playlists.append(Playlist(nome, cls, ))

        

        
        