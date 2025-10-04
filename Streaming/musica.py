from Streaming.arquivo_de_midia import ArquivoDeMidia

class Musica(ArquivoDeMidia):
    titulos = []


    def __init__(self, titulo:str, duracao:int, artista:str, genero:str, reproducoes: int = 0):
       super().__init__(titulo, duracao, artista, reproducoes)
       self.genero = genero
       self.avaliacoes = []
       Musica.titulos.append(self.titulo)
       
    def avaliar(self, nota):
        if isinstance(nota, int):
            if nota >= 0 and nota <=5:
                self.avaliacoes.append(nota)
            raise ValueError("A nota deve ser valores inteiros entre 0 a 5")
        raise ValueError("A nota deve ser um numero inteiro")
    

    @classmethod
    def lista_titulos(cls):
        """ Imprime a lista de musicas atualmente inicializadas """
        print("Musicas registradas:")
        for titulo in cls.titulos:
            if titulo is not None:
                print("- " + titulo)
        return
    

    def reproduzir(self):
        self.reproducoes += 1
        print(f"Tocando música: {self.titulo} de {self.artista}")