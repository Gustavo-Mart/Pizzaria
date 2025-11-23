from usuario import *
from pedido import *
from pizza import *
from typing import List

class Pizzaria:
    nome : str
    telefone : int
    pedidos : List
    clientes : List
    
    def __init__(self, nome, telefone):
        self.nome = nome
        self.telefone = telefone
        self.pedidos = []
        self.clientes = []
        self.cardapio = {
            "Marguerita": ["Mussarela", "Manjericão"],
            "Calabresa": ["Calabresa", "Cebola"],
            "Portuguesa": ["Mussarela", "Presunto", "Ovos", "Cebola"],
            "Quatro Queijos": ["Mussarela", "Parmesão", "Provolone", "Catupiry"],
            "Frango com Catupiry": ["Mussarela", "Frango", "Catupiry"],
            "Chuvinha": ["Mussarela", "Bacon", "Carne seca", "Catupiry", "Cebola"],
            "Kuribara": ["Mussarela", "Brocolis", "Bacon"],
            "Chennifer": ["Mussarela", "Alho frito"],
            "Tailandesa": ["Mussarela", "Calabresa"],
            "Camela": ["Mussarela", "Brocolis", "Catupiry", "Alho frito"],
            "Debra":["Mussarela de búfala", "Tomate-cereja", "Manjericão"],
        }
        self.cardapio_doces = {
            "Era o meu Sonho": ["Chocolate branco", "Morango", "Leite Ninho"],
            "Chocolate": ["Chocolate ao leite", "Granulado"],
            "Chocolate com Morango": ["Chocolate ao leite", "Morangos frescos"],
            "Prestígio": ["Chocolate", "Coco ralado"],
            "Banana com Camela": ["Banana", "Açúcar", "Canela"],
            "Nutella com Morango": ["Creme de avelã", "Morangos frescos"],
            "Miguelito": ["Chocolate branco", "Biscoito Oreo triturado"]
        }
        self.ingredientes_extras = {
            "Mussarela": 2.00,
            "Calabresa": 2.00,
            "Cebola": 2.00,
            "Presunto": 2.00,
            "Ovos": 2.00,
            "Parmesão": 2.00,
            "Provolone": 2.00,
            "Catupiry": 2.00,
            "Frango": 2.00,
            "Bacon": 2.00,
            "Carne seca": 2.00,
            "Brocolis": 2.00,
            "Alho frito": 2.00,
            "Mussarela de búfala": 2.00,
            "Tomate-cereja": 2.00,
            "Borda Recheada": 5.00
        }           

    def exibir_cardapio(self):
        print(f"\n\033[33m{'.'*30}")
        print(f"CARDÁPIO - {self.nome}")
        print(f"{'.'*30}\033[0m")

        print("\n\033[32m--------PIZZAS SALGADAS--------")
        for sabor, ingredientes in self.cardapio.items():
            print(f"\033[32m{sabor}......... {', '.join(ingredientes)}\033[0m")

        print("\n\033[31m--------PIZZAS DOCES--------")
        for sabor, ingredientes in self.cardapio_doces.items():
            print(f"\033[31m{sabor}......... {', '.join(ingredientes)}\033[0m")

        print(f"\n--------TAMANHOS DISPONIVEIS--------")
        for tamanho in TamanhoPizza:
            print(f" -> {tamanho.descricao}: R$ {tamanho.preco_base:.2f}")

        print(f"\n--------EXTRAS--------")
        print(f" -> Borda recheada: R$ 5,00")
        print(f" -> Ingrediente extra: R$ 2,00 cada")