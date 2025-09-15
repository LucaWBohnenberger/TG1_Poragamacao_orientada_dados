from arquivo_de_midia import ArquivoDeMidia

class Musica(ArquivoDeMidia):
    def __init__(self, titulo:str, duracao:int, artista:str, reproducoes:int, genero:str):
       super().__init__(titulo, duracao, artista, reproducoes)
       self.genero = genero
       self.avaliacoes = []
       
    def avaliar(self, nota):
        if isinstance(nota, int):
            if nota >= 0 and nota <=5:
                self.avaliacoes.append(nota)
            raise ValueError("A nota deve ser valores inteiros entre 0 a 5")
        raise ValueError("A nota deve ser um numero inteiro")