# Imports de tipo para clareza e robustez do código
from .musica import Musica
from .playlist import Playlist
from .usuario import Usuario

# Imports de módulos padrão para manipulação de arquivos e tempo
import os
from datetime import datetime
import traceback # Usado para depuração detalhada de erros


class Analises:
    """Agrupa um conjunto de métodos estáticos para análise de dados.

    Esta classe funciona como um namespace de utilitários para gerar
    estatísticas e relatórios a partir das listas de dados principais
    do sistema de streaming. Não é destinada a ser instanciada.
    """

    @staticmethod
    def top_musicas_reproduzidas(musicas: list[Musica], top_n: int) -> list[Musica]:
        """Encontra as músicas mais reproduzidas a partir de uma lista.

        Args:
            musicas (list[Musica]): A lista completa de objetos Musica.
            top_n (int): O número de músicas que devem compor o ranking (e.g., 3 para um Top 3).

        Returns:
            list[Musica]: Uma nova lista contendo as 'top_n' músicas mais populares,
                          ordenadas da maior para a menor.
        """
        # A função sorted é usada com uma chave lambda para ordenar diretamente pelo atributo 'reproducoes'.
        musicas_ordenadas = sorted(musicas, key=lambda musica: musica.reproducoes, reverse=True)
        return musicas_ordenadas[:top_n]

    @staticmethod
    def playlist_mais_popular(playlists: list[Playlist]) -> Playlist | None:
        """Encontra a playlist com o maior número de reproduções.

        Args:
            playlists (list[Playlist]): A lista completa de objetos Playlist.

        Returns:
            Playlist | None: O objeto Playlist mais popular, ou None se a lista de entrada
                            estiver vazia.
        """
        if not playlists:
            return None
        # A função max() é uma forma eficiente de encontrar o item com o maior valor para uma chave.
        return max(playlists, key=lambda playlist: playlist.reproducoes)

    @staticmethod
    def usuario_mais_ativo(usuarios: list[Usuario]) -> Usuario | None:
        """Encontra o usuário com o maior histórico de mídias ouvidas.

        Este método assume que a classe Usuario possui um atributo 'historico'
        que é uma lista de mídias ouvidas.

        Args:
            usuarios (list[Usuario]): A lista completa de objetos Usuario.

        Returns:
            Usuario | None: O objeto Usuario mais ativo, ou None se a lista de entrada
                           estiver vazia.
        """
        if not usuarios:
            return None
        return max(usuarios, key=lambda usuario: len(usuario.historico))

    @staticmethod
    def media_avaliacoes(musicas: list[Musica]) -> dict[str, float]:
        """Calcula a média de avaliação para cada música.

        Args:
            musicas (list[Musica]): A lista completa de objetos Musica.

        Returns:
            dict[str, float]: Um dicionário onde as chaves são os títulos das músicas
                              e os valores são suas médias de avaliação arredondadas.
                              Retorna 0.0 para músicas sem avaliações.
        """
        medias = {}
        for musica in musicas:
            # Garante que a lista de avaliações não está vazia para evitar divisão por zero.
            if musica.avaliacoes:
                media = sum(musica.avaliacoes) / len(musica.avaliacoes)
                medias[musica.titulo] = round(media, 2)
            else:
                medias[musica.titulo] = 0.0
        return medias

    @staticmethod
    def total_reproducoes(usuarios: list[Usuario]) -> int:
        """Calcula o número total de reproduções em todo o sistema.

        Args:
            usuarios (list[Usuario]): A lista completa de objetos Usuario.

        Returns:
            int: A soma total de todas as mídias ouvidas por todos os usuários.
        """
        # Uma 'generator expression' dentro de sum() é uma forma eficiente de somar
        # o tamanho do histórico de cada usuário sem criar uma lista intermediária.
        return sum(len(usuario.historico) for usuario in usuarios)
    
    @staticmethod
    def gerar_relatorio_completo(musicas: list[Musica], playlists: list[Playlist], usuarios: list[Usuario]):
        """Orquestra a geração de um relatório completo e o salva em um arquivo.

        Este método utiliza as outras funções de análise da classe para coletar
        os dados, formata-os em um relatório de texto e o escreve no arquivo
        'relatorios/relatorio.txt', criando o diretório se necessário.

        Args:
            musicas (list[Musica]): A lista completa de objetos Musica.
            playlists (list[Playlist]): A lista completa de objetos Playlist.
            usuarios (list[Usuario]): A lista completa de objetos Usuario.

        Returns:
            str | Exception: O caminho do arquivo do relatório em caso de sucesso,
                             ou o objeto de exceção em caso de falha.
        """
        try:
            # Garante que o diretório de saída exista antes de prosseguir.
            caminho_dir = "relatorios"
            if not os.path.exists(caminho_dir):
                os.makedirs(caminho_dir)
            caminho_arquivo = os.path.join(caminho_dir, "relatorio.txt")

            # Cria um novo arquivo de relatório (ou sobrescreve um antigo) e escreve o cabeçalho.
            with open(caminho_arquivo, "w", encoding="utf-8") as f:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"Relatório de Análises do Sistema de Streaming\n")
                f.write(f"Gerado em: {timestamp}\n")
                f.write("="*50 + "\n\n")

                # Coleta as métricas e escreve cada seção formatada no arquivo.
                f.write("--- Top 3 Músicas Mais Ouvidas ---\n")
                top_3 = Analises.top_musicas_reproduzidas(musicas, 3)
                for i, musica in enumerate(top_3):
                    f.write(f"{i+1}. {musica.titulo} - {musica.artista} ({musica.reproducoes} reproduções)\n")
                f.write("\n")

                f.write("--- Playlist Mais Popular ---\n")
                popular = Analises.playlist_mais_popular(playlists)
                if popular and popular.usuario:
                    f.write(f"'{popular.nome}' por {popular.usuario.nome} ({popular.reproducoes} reproduções)\n")
                elif popular:
                    f.write(f"'{popular.nome}' (dono desconhecido) ({popular.reproducoes} reproduções)\n")
                else:
                    f.write("Nenhuma playlist encontrada.\n")
                f.write("\n")

                f.write("--- Usuário Mais Ativo ---\n")
                ativo = Analises.usuario_mais_ativo(usuarios)
                if ativo:
                    f.write(f"{ativo.nome} ({len(ativo.historico)} faixas ouvidas)\n")
                else:
                    f.write("Nenhum usuário encontrado.\n")
                f.write("\n")

                f.write("--- Média de Avaliações (0-5) ---\n")
                medias = Analises.media_avaliacoes(musicas)
                if medias:
                    for titulo, media in medias.items():
                        f.write(f"- {titulo}: {media:.2f}\n")
                else:
                    f.write("Nenhuma música com avaliação.\n")
                f.write("\n")

                f.write("--- Estatísticas Gerais ---\n")
                total_plays = Analises.total_reproducoes(usuarios)
                f.write(f"Total de reproduções no sistema: {total_plays}\n")
            
            return caminho_arquivo

        except Exception as e:
            # Em caso de qualquer erro, imprime um diagnóstico detalhado no console.
            print("\n" + "="*20 + " ERRO NA GERAÇÃO DO RELATÓRIO " + "="*20)
            print(f"A função 'gerar_relatorio_completo' encontrou uma exceção: {e}")
            traceback.print_exc()
            print("="*70 + "\n")
            return e