from Streaming.arquivo_de_midia import ArquivoDeMidia

class Podcast(ArquivoDeMidia):
    titulos = []


    def __init__(self, titulo:str, temporada:str, episodio:int, host:str, duracao:int):
        self.titulo = titulo
        self.temporada = temporada
        self.episodio = episodio
        self.host = host
        self.duracao = duracao

        Podcast.titulos.append(self.titulo)

    def __repr__(self):
        return f"Podcast(titulo={self.titulo}, host={self.host})"
    
    @classmethod
    def lista_titulos(cls):
        """ Imprime a lista de podcasts atualmente inicializadas """
        print("Podcasts registradas:")
        for titulo in cls.titulos:
            if titulo is not None:
                print("- " + titulo)
        return

    def reproduzir(self):
            self.reproducoes += 1
            print(f"Tocando música: {self.titulo} de {self.artista}")