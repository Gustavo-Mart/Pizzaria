class Cliente:
    __nome : str
    __telefone : int
    __endereco : str

    def __init__(self, nome, telefone, endereco):
        self.__nome = nome
        self.__telefone = telefone
        self.__endereco = endereco

    def __str__(self):
        txt = "Nome: {self.__nome}\n"
        txt += "Telefone: {self.__telefone}\n"
        txt += "Endereço para entrega: {self.__endereco}\n"
        return txt