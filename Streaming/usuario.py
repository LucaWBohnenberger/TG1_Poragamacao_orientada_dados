class Usuario:
    qntd_instancias = 0
    def __init__(self, nome, playlists=None, historico=None):
        self.nome = nome
        self.playlists = playlists if playlists is not None else []
        self.historico = historico if historico is not None else []
        Usuario.new_user()

        
    @classmethod
    def new_user(cls):
        cls.qntd_instancias += 1
        
    def __str__(self):
        return f"Nome: {self.nome} \nPlaylists: {self.playlists} \nHistórico: {self.historico}"
        
        