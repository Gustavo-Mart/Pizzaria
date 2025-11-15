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
        self.ingredientes_extras = [
            "Mussarela",
            "Manjericão",
            "Calabresa",
            "Cebola",
            "Presunto",
            "Ovos",
            "Parmesão",
            "Provolone",
            "Catupiry",
            "Frango",
            "Bacon",
            "Carne seca",
            "Brocolis",
            "Alho frito",
            "Mussarela de búfala",
            "Tomate-cereja"
        ]            

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