from .arquivo_de_midia import ArquivoDeMidia
from .usuario import Usuario

class Playlist:
    """Representa uma coleção de mídias criada por um usuário.

    A classe gerencia uma lista de itens de mídia (músicas ou podcasts),
    associada a um nome e um usuário. Ela sobrecarrega vários operadores
    para permitir interações intuitivas, como somar playlists (+),
    verificar o tamanho (len), e acessar itens por índice ([]).

    Attributes:
        nome (str): O nome da playlist.
        usuario (Usuario): O objeto Usuario que criou a playlist.
        itens (list[ArquivoDeMidia]): Uma lista com os objetos de mídia da playlist.
        reproducoes (int): O número de vezes que a playlist foi ouvida.
        qntd_instancias (int): Atributo de classe para contar instâncias (não utilizado no código atual).
        nomes (list): Atributo de classe para armazenar nomes (não utilizado no código atual).
    """
    
    # Atributos de classe, atualmente não utilizados na lógica principal.
    qntd_instancias = 0
    nomes = []

    def __init__(self, nome: str, usuario: Usuario, itens: list[ArquivoDeMidia], reproducoes: int = 0):
        """Inicializa um novo objeto Playlist.

        Args:
            nome (str): O nome para a nova playlist.
            usuario (Usuario): O usuário dono da playlist.
            itens (list[ArquivoDeMidia]): Uma lista de mídias para popular a playlist.
            reproducoes (int, optional): O contador de reproduções inicial. Padrão é 0.
        """
        self.nome = nome
        self.usuario = usuario if usuario is not None else []
        self.itens = itens if itens is not None else []
        self.reproducoes = reproducoes

    def __str__(self) -> str:
        """Retorna uma representação da playlist legível e concisa para o usuário."""
        # Acesso ao nome do usuário pode causar erro se o usuário for uma lista vazia.
        nome_usuario = self.usuario.nome if hasattr(self.usuario, 'nome') else "Desconhecido"
        return f"Playlist '{self.nome}' por {nome_usuario} ({len(self.itens)} faixas)"

    def __repr__(self) -> str:
        """Retorna uma representação inequívoca do objeto, útil para depuração."""
        # repr(self.usuario) é usado para obter a representação do objeto Usuario.
        return (f"Playlist(nome='{self.nome}', usuario={repr(self.usuario)}, "
                f"itens=[{len(self.itens)} Mídias])")

    def __add__(self, outra_playlist: 'Playlist') -> 'Playlist':
        """Sobrecarga do operador '+' para combinar duas playlists.

        Cria e retorna uma nova Playlist contendo os itens únicos de ambas as
        playlists. O nome e o usuário da primeira playlist são mantidos.

        Args:
            outra_playlist (Playlist): A segunda playlist a ser combinada.

        Returns:
            Playlist: Um novo objeto Playlist com os itens combinados.

        Raises:
            TypeError: Se o objeto a ser somado não for uma instância de Playlist.
        """
        if not isinstance(outra_playlist, Playlist):
            # Temos que certificar que o usuario é o mesmo também (?)
            raise TypeError("Playlists podem ser combinadas apenas com outras playlists")

        # Usa a conversão para set para remover itens duplicados de forma eficiente.
        nova_lista_itens = list(set(self.itens + outra_playlist.itens))
        return Playlist(nome=self.nome, usuario=self.usuario, itens=nova_lista_itens)

    def __len__(self) -> int:
        """Sobrecarga da função len() para retornar o número de itens na playlist."""
        return len(self.itens)

    def __getitem__(self, index: int) -> ArquivoDeMidia:
        """Sobrecarga do acesso por índice (ex: playlist[0]) para obter um item."""
        return self.itens[index]

    def __eq__(self, outra_playlist: object) -> bool:
        """Sobrecarga do operador de igualdade '==' para comparar duas playlists.

        Duas playlists são consideradas iguais se tiverem o mesmo nome, o mesmo
        nome de usuário, e o mesmo conjunto de itens, independentemente da ordem.
        """
        if not isinstance(outra_playlist, Playlist):
            return False

        # Compara nome, nome do usuário e o conteúdo dos itens (ignorando a ordem).
        mesmo_nome = self.nome == outra_playlist.nome
        mesmo_usuario = self.usuario.nome == outra_playlist.usuario.nome
        mesmos_itens = set(self.itens) == set(outra_playlist.itens)
        return mesmo_nome and mesmo_usuario and mesmos_itens

    @classmethod
    def adicionar_midia(cls, midia: ArquivoDeMidia):
        """Método de classe que tenta adicionar uma mídia a 'cls.itens'."""
        cls.itens.append(midia)

    @classmethod
    def remover_midia(cls, midia: ArquivoDeMidia):
        """Método de classe que tenta remover uma mídia de 'cls.itens'."""
        cls.itens.remove(midia)

    def ouvir_playlist(self):
        """Incrementa o contador de reproduções da playlist e de cada mídia individual nela.
        
        Este método primeiro incrementa o contador da própria playlist e depois
        itera sobre todos os seus itens (músicas e podcasts), chamando o método
        `reproduzir()` de cada um para que eles também registrem a reprodução.
        """
        # Incrementa o contador da própria playlist
        self.reproducoes += 1
        
        # Percorre cada objeto de mídia na lista de itens
        print(f"\n--- Tocando Playlist: {self.nome} ---")
        for midia in self.itens:
            # Chama o método 'reproduzir()' de cada música ou podcast
            midia.reproduzir()
        print(f"--- Fim da Playlist: {self.nome} ---")

    @classmethod
    def lista_nome(cls, nome: str, playlists: list['Playlist']):
        """Imprime os nomes das playlists de um usuário específico de uma lista fornecida.

        Args:
            nome (str): O nome do usuário cujas playlists serão listadas.
            playlists (list[Playlist]): A lista de todas as playlists do sistema para buscar.
        """
        print("Suas playlists:")
        for playlist in playlists:
            if playlist.usuario.nome == nome:
                print("- " + playlist.nome)
        return