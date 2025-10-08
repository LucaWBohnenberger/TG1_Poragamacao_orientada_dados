# Streaming/analises.py

# Imports necessários para as anotações de tipo
from .musica import Musica
from .playlist import Playlist
from .usuario import Usuario

class Analises:
    """
    Esta classe provê um conjunto de métodos estáticos para gerar estatísticas
    e análises a partir dos dados do sistema de streaming.
    """

    @staticmethod
    def top_musicas_reproduzidas(musicas: list[Musica], top_n: int) -> list[Musica]:
        """
        Retorna as top_n músicas mais reproduzidas. [cite: 1]

        Args:
            musicas (list[Musica]): A lista de todas as músicas do sistema.
            top_n (int): O número de músicas a serem retornadas no ranking.

        Returns:
            list[Musica]: Uma lista ordenada com as músicas mais populares.
        """
        # Ordena a lista de músicas em ordem decrescente com base no atributo 'reproducoes'
        musicas_ordenadas = sorted(musicas, key=lambda musica: musica.reproducoes, reverse=True)
        
        # Retorna os N primeiros elementos da lista ordenada
        return musicas_ordenadas[:top_n]

    @staticmethod
    def playlist_mais_popular(playlists: list[Playlist]) -> Playlist | None:
        """
        Retorna a playlist mais ouvida. [cite: 1]

        Args:
            playlists (list[Playlist]): A lista de todas as playlists do sistema.

        Returns:
            Playlist | None: O objeto da playlist mais popular ou None se a lista estiver vazia.
        """
        if not playlists:
            return None
        
        # Usa a função max() para encontrar a playlist com o maior número de reproduções
        return max(playlists, key=lambda playlist: playlist.reproducoes)

    @staticmethod
    def usuario_mais_ativo(usuarios: list[Usuario]) -> Usuario | None:
        """
        Retorna o usuário com mais músicas no histórico. [cite: 1]

        Args:
            usuarios (list[Usuario]): A lista de todos os usuários do sistema.

        Returns:
            Usuario | None: O objeto do usuário mais ativo ou None se a lista estiver vazia.
        """
        if not usuarios:
            return None
            
        # Usa a função max() para encontrar o usuário cujo histórico tem o maior comprimento
        # Assumindo que a classe Usuario possui um atributo 'historico' que é uma lista.
        return max(usuarios, key=lambda usuario: len(usuario.historico))

    @staticmethod
    def media_avaliacoes(musicas: list[Musica]) -> dict[str, float]:
        """
        Retorna um dicionário com a média de avaliação de cada música. [cite: 1]

        Args:
            musicas (list[Musica]): A lista de todas as músicas do sistema.

        Returns:
            dict[str, float]: Um dicionário mapeando o título de cada música à sua média.
        """
        medias = {}
        for musica in musicas:
            # Verifica se a lista de avaliações não está vazia para evitar divisão por zero
            if musica.avaliacoes:
                media = sum(musica.avaliacoes) / len(musica.avaliacoes)
                medias[musica.titulo] = round(media, 2) # Arredonda para 2 casas decimais
            else:
                medias[musica.titulo] = 0.0
        return medias

    @staticmethod
    def total_reproducoes(usuarios: list[Usuario]) -> int:
        """
        [cite_start]Retorna o total de reproduções feitas por todos os usuários. [cite: 1]

        Args:
            usuarios (list[Usuario]): A lista de todos os usuários do sistema.

        Returns:
            int: O número total de reproduções.
        """
        # Soma o tamanho do histórico de cada usuário para obter o total de reproduções
        total = sum(len(usuario.historico) for usuario in usuarios)
        return total