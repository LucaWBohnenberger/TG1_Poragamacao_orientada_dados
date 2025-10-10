from .arquivo_de_midia import ArquivoDeMidia

class Podcast(ArquivoDeMidia):
    """Representa um episódio de podcast no sistema.

    Esta classe armazena informações sobre um episódio específico, como
    título, temporada, número do episódio, apresentador e duração.
    Ela herda funcionalidades básicas de ArquivoDeMidia.

    Attributes:
        titulo (str): O título do episódio do podcast.
        temporada (str): O número ou nome da temporada.
        episodio (int): O número do episódio.
        host (str): O nome do apresentador ou da rede do podcast.
        duracao (int): A duração do episódio em segundos.
        titulos (list[str]): Atributo de classe que armazena os títulos de todos
                             os episódios de podcast criados.
    """

    # Atributo de classe para rastrear todos os títulos de podcasts instanciados.
    titulos = []

    def __init__(self, titulo: str, temporada: str, episodio: int, host: str, duracao: int):
        """Inicializa um novo objeto Podcast.

        Args:
            titulo (str): O título do episódio.
            temporada (str): O identificador da temporada (e.g., "1", "2024").
            episodio (int): O número do episódio.
            host (str): O nome do apresentador principal ou da produtora.
            duracao (int): A duração do episódio em segundos.
        """
        self.titulo = titulo
        self.temporada = temporada
        self.episodio = episodio
        self.host = host
        self.duracao = duracao

        # Adiciona o título desta instância à lista de títulos da classe.
        Podcast.titulos.append(self.titulo)

    def __str__(self) -> str:
        """Retorna uma representação do podcast legível e concisa para o usuário."""
        # Formata a duração em minutos e segundos para melhor legibilidade.
        minutos, segundos = divmod(self.duracao, 60)
        return (f"'{self.titulo}' por {self.host} "
                f"(T{self.temporada} E{self.episodio}) [{minutos:02d}:{segundos:02d}]")

    def __repr__(self) -> str:
        """Retorna uma representação inequívoca do objeto, útil para depuração."""
        return (f"Podcast(titulo='{self.titulo}', temporada='{self.temporada}', "
                f"episodio={self.episodio}, host='{self.host}', duracao={self.duracao})")

    @classmethod
    def lista_titulos(cls):
        """Imprime no console a lista de títulos de todos os podcasts criados.
        
        Este é um método de classe que acessa o atributo 'titulos' compartilhado
        por todas as instâncias de Podcast.
        """
        print("Podcasts registradas:")
        for titulo in cls.titulos:
            if titulo is not None:
                print("- " + titulo)
        return

    def reproduzir(self):
        """Incrementa o contador de reproduções e imprime uma mensagem."""
        self.reproducoes += 1
        print(f"Tocando podcast: {self.titulo} de {self.host}")