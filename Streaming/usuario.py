from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # Precisamos evitar imports circulares
    from Streaming.playlist import Playlist
    from Streaming.arquivo_de_midia import ArquivoDeMidia

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
    
    def ouvir_midia(self, midia):
        """
        Adiciona uma mídia ao histórico de reprodução do usuário.
        """
        # A especificação  indica um atributo 'historico'
        if not hasattr(self, 'historico'):
            self.historico = []
        self.historico.append(midia)
        
    def adicionar_playlist(self, playlist: 'Playlist'):
        """
        Adiciona uma playlist nova a lista de playlists do usuario
        Args:
            playlist (Playlist): Um conjunto de objetos de Arquivos de Midia
        """
        self.playlists.append(playlist)
        



    @classmethod
    def new_user(cls):
        cls.qntd_instancias += 1

        


        

        
        