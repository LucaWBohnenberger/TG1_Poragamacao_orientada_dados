# main.py

# Importa a nova classe StreamingApp
from Streaming.menu import Menu

# --- Ponto de Entrada Principal ---
if __name__ == "__main__":
    # Cria uma instância da sua aplicação de streaming
    app = Menu()
    # Inicia o menu principal
    app.menu_inicial()