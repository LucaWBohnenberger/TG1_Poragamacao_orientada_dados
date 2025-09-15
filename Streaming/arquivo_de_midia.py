from abc import ABC, abstractmethod

class ArquivoDeMidia(ABC):
    @abstractmethod
    def __init__(self, titulo:str, duracao:int, artista:str, reproducoes:int):
        self.titulo = titulo
        self.duracao = duracao
        self.artista = artista
        self.reproducoes = reproducoes
        
        
    @abstractmethod
    def reproduzir(self):
        pass
    
    def __eq__(self, other):
        return self.titulo == other.titulo and self.artista == other.artista
    
    