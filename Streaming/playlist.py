from Streaming.arquivo_de_midia import ArquivoDeMidia
from Streaming.usuario import Usuario


class Playlist:
    """ 
    Classe de playlists.

    nome:str: nome da playlist.
    usuario:Usuario: criador da playlist.
    itens:list[ArquivoDeMidia]: lista de ArquivoDeMidia.
    reproducoes:int: contador de execuções.
    """
    qntd_instancias = 0
    nomes = []

    def __init__(self, nome:str, usuario:Usuario, itens:list[ArquivoDeMidia], reproducoes:int=0):
        """ Inicializador da classe """
        self.nome = nome
        self.usuario = usuario if usuario is not None else []
        self.itens = itens if itens is not None else []
        self.reproducoes = reproducoes

    def __str__(self):
        # Precisamos printar os itens também
        return f"Nome: {self.nome}\nUsuario: {self.usuario.nome}\nReproducoes: {self.reproducoes}"



    def __add__(self, playlist2):
        """ Combina duas playlists, o nome do primeiro é mantido """

        if not isinstance(playlist2, Playlist):
            # Temos que certificar que o usuario é o mesmo também (?)
            raise TypeError("Playlists podem ser combinadas apenas com outras playlists")

        # nova lista com todos os itens removendo duplicidade
        nova_lista= list(set(self.itens + playlist2.itens))

        return Playlist(nome=self.nome, usuario=self.usuario, itens=nova_lista )
    
    def __len__(self):
        return len(self.itens)
    
    def __getitem__(self, index):
        return self.itens[index]
        
    def __eq__(self, playlist2):
        if not isinstance(playlist2, Playlist):
            raise TypeError("Playlists podem ser comaparadas apenas com outras playlists")

        return self.nome == playlist2.nome and self.usuario.nome == playlist2.usuario.nome and set(self.itens) == set(playlist2.itens)


    @classmethod
    def adicionar_midia(cls, midia:ArquivoDeMidia):
        cls.itens.append(midia)

    @classmethod
    def remover_midia(cls, midia:ArquivoDeMidia):
        cls.itens.remove(midia)

    @classmethod
    def ouvir_playlist(cls):
        cls.reproducoes += 1 


    @classmethod
    def lista_nome(cls, nome:str, playlists:list['Playlist']):
        """ Imprime a lista de playlists atualmente inicializadas de um usuario """
        print("Suas playlists:")
        for playlist in playlists:
            if playlist.usuario.nome == nome:
                print("- " + playlist.nome)
        return