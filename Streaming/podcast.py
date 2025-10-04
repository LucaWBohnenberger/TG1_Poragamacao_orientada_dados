class Podcast:
    def __init__(self, titulo, temporada, episodio, host, duracao):
        self.titulo = titulo
        self.temporada = temporada
        self.episodio = episodio
        self.host = host
        self.duracao = duracao

    def __repr__(self):
        return f"Podcast(titulo={self.titulo}, host={self.host})"