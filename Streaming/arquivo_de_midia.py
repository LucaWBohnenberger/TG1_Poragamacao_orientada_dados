from abc import ABC, abstractmethod

class ArquivoDeMidia(ABC):
    """Define uma interface base para todos os tipos de mídia no sistema.

    Como uma Classe Base Abstrata (ABC), esta classe não deve ser
    instanciada diretamente. Em vez disso, ela serve como um modelo,
    garantindo que todas as classes de mídia filhas (como Musica e Podcast)
    implementem os métodos e atributos essenciais.

    Attributes:
        titulo (str): O título da mídia.
        duracao (int): A duração da mídia em segundos.
        artista (str): O criador principal da mídia (e.g., artista, host).
        reproducoes (int): O contador de reproduções da mídia.
    """

    @abstractmethod
    def __init__(self, titulo: str, duracao: int, artista: str, reproducoes: int = 0):
        """Construtor abstrato para inicializar atributos comuns de mídia.

        Args:
            titulo (str): O título da mídia.
            duracao (int): A duração da mídia em segundos.
            artista (str): O nome do artista ou criador.
            reproducoes (int, optional): O número inicial de reproduções. Padrão é 0.
        """
        self.titulo = titulo
        self.duracao = duracao
        self.artista = artista
        self.reproducoes = reproducoes

    def __str__(self) -> str:
        """Retorna uma representação padrão legível da mídia."""
        return f"'{self.titulo}' por {self.artista}"

    def __repr__(self) -> str:
        """Retorna uma representação inequívoca do objeto, útil para depuração."""
        # Usa self.__class__.__name__ para mostrar o nome da classe filha (Musica, Podcast, etc.)
        return (f"{self.__class__.__name__}(titulo='{self.titulo}', "
                f"artista='{self.artista}', duracao={self.duracao})")

    def __eq__(self, outro_objeto: object) -> bool:
        """Sobrecarga do operador '==' para comparar duas mídias.

        Duas mídias são consideradas iguais se tiverem o mesmo título e o mesmo artista.
        """
        # Verifica se o outro objeto tem os atributos necessários antes de comparar
        if not hasattr(outro_objeto, 'titulo') or not hasattr(outro_objeto, 'artista'):
            return False
        return self.titulo == outro_objeto.titulo and self.artista == outro_objeto.artista

    @abstractmethod
    def reproduzir(self):
        """Método abstrato para simular a reprodução de uma mídia.

        Subclasses são obrigadas a implementar este método. A implementação base
        fornecida incrementa o contador de reproduções e pode ser chamada via super().
        """
        self.reproducoes += 1
        pass