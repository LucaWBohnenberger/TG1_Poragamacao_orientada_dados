from .arquivo_de_midia import ArquivoDeMidia

class Musica(ArquivoDeMidia):
    """Representa uma única faixa de música, herdando de ArquivoDeMidia.

    Esta classe adiciona atributos específicos de música, como gênero e
    um sistema de avaliações, além de manter um registro de todos os
    títulos de músicas criados.

    Attributes:
        titulo (str): O título da música.
        duracao (int): A duração da música em segundos.
        artista (str): O nome do artista ou da banda.
        reproducoes (int): Contador de quantas vezes a música foi tocada.
        genero (str): O gênero musical da faixa.
        avaliacoes (list[int]): Uma lista contendo as notas (0-5) que a música recebeu.
        titulos (list[str]): Atributo de classe que armazena os títulos de todas as
                             instâncias de Musica criadas.
    """

    # Atributo de classe para rastrear todos os títulos de músicas instanciados.
    titulos = []

    def __init__(self, titulo: str, duracao: int, artista: str, genero: str, reproducoes: int = 0):
        """Inicializa um novo objeto Musica.

        Args:
            titulo (str): O título da música.
            duracao (int): A duração da faixa em segundos.
            artista (str): O nome do artista ou banda.
            genero (str): O gênero musical.
            reproducoes (int, optional): O número inicial de reproduções. Padrão é 0.
        """
        # Chama o construtor da classe pai (ArquivoDeMidia) para inicializar atributos comuns.
        super().__init__(titulo, duracao, artista, reproducoes)
        self.genero = genero
        
        # Atributos de interação específicos da música.
        self.avaliacoes = []

        # Adiciona o título desta instância à lista de títulos da classe.
        Musica.titulos.append(self.titulo)
    
    def __str__(self) -> str:
        """Retorna uma representação da música legível e concisa para o usuário."""
        minutos, segundos = divmod(self.duracao, 60)
        return f"'{self.titulo}' por {self.artista} - {self.genero} [{minutos:02d}:{segundos:02d}]"

    def __repr__(self) -> str:
        """Retorna uma representação inequívoca do objeto, útil para depuração."""
        return (f"Musica(titulo='{self.titulo}', duracao={self.duracao}, "
                f"artista='{self.artista}', genero='{self.genero}')")

    def avaliar(self, nota: int):
        """Adiciona uma nota à lista de avaliações da música.

        Args:
            nota (int): Um valor inteiro representando a avaliação.

        Raises:
            ValueError: Se a nota não for um inteiro ou estiver fora do
                        intervalo permitido de 0 a 5.
        """
        if not isinstance(nota, int):
            raise ValueError("A nota deve ser um número inteiro.")
            
        if 0 <= nota <= 5:
            self.avaliacoes.append(nota)
        else:
            # Lança o erro apenas se a nota estiver fora do intervalo.
            raise ValueError("A nota deve ser um valor inteiro entre 0 e 5.")

    @classmethod
    def lista_titulos(cls):
        """Imprime no console a lista de títulos de todas as músicas criadas."""
        print("\nMúsicas registradas no sistema:")
        if not cls.titulos:
            print("Nenhuma música registrada.")
            return

        for titulo in cls.titulos:
            # Validação simples para não imprimir entradas vazias caso existam.
            if titulo:
                print(f"- {titulo}")
    
    def reproduzir(self):
        """Incrementa o contador de reproduções e simula a reprodução da música."""
        self.reproducoes += 1
        # Esta mensagem é útil para a interface do console.
        print(f"Tocando música: {self.titulo} de {self.artista}")