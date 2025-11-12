from enum import Enum
from typing import List

class TamanhoPizza(Enum): #o enum é uma tabela fixa, só pode pedir isso q esta ai e simplifica alterações
    BROTO = ("Broto", 25.00)
    MEDIA = ("Média", 35.00)
    GRANDE = ("Grande", 45.00)
    
    def __init__(self, descricao, preco_base):
        self.descricao = descricao
        self.preco_base = preco_base

class Pizza():
    sabor : str
    tamanho : str
    borda_recheada : bool
    ingrediente : List

    def __init__(self, sabor, tamanho, borda_recheada=False):
        self.sabor = sabor
        self.tamanho = tamanho
        self.borda_recheada = borda_recheada
        self.ingredientes = []
    
    def adicionar_ingrediente(self, ingrediente):
        self.ingredientes.append(ingrediente)
    
    def calcular_preco(self):
        preco = self.tamanho.preco_base # type: ignore
        if self.borda_recheada == True:
            preco += 5.00
        preco += len(self.ingredientes) * 2.00 #o len pega a quantidade dentro de uma lista, aqui esta pegando os ingredientes adicionados
        return preco
    
    def __str__(self):
        if self.borda_recheada == True:
            borda = "com borda recheada"
        else:
            borda = "sem borda recheada"

        if self.ingredientes:
            ingredientes_str = f" + {', '.join(self.ingredientes)}" #join é para colocar as virgulas caso tenha mais de um ingrediente
        else:
            ingredientes_str = ""
        
        return f"Pizza de {self.sabor} ({self.tamanho.descricao}) {borda}{ingredientes_str} - R$ {self.calcular_preco():.2f}" # type: ignore