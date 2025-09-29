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
        return f"Nome: {self.nome} \nPlaylists: {self.playlists} \nHistórico: {self.historico}"
        



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

        

        
        