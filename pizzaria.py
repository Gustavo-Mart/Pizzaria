from pizza import *
from typing import List
class Pizzaria:
    cardapio : List [Pizza]
    lista_pedidos: list

    def __init__(self, cardapio: List [Pizza]):
         
        self.cardapio = []
    
    def exibir_cardapio(self):
        return 