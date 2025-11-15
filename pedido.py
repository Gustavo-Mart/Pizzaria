from typing import List
from enum import Enum
from usuario import *
from pizza import *

class FormaPagamento(Enum):
    CARTAO_CREDITO = "Cartão de Crédito"
    CARTAO_DEBITO = "Cartão de Débito"
    PIX = "Pix"
    DINHEIRO = "Dinheiro"

class Pedido:
    id_pedido: int
    cliente: Cliente
    pizzas: List[Pizza]
    valor_total: float
    forma_pagamento: FormaPagamento
    endereco_entrega: str
    tempo : int
    
    contador_id = 1
    
    def __init__(self, cliente, pizzas, forma_pagamento, endereco_entrega):
        self.id_pedido = Pedido.contador_id
        Pedido.contador_id += 1
        
        self.cliente = cliente
        self.pizzas = pizzas
        self.forma_pagamento = forma_pagamento
        self.endereco_entrega = endereco_entrega
        self.valor_total = self._calcular_total()
        self.tempo = 40
    
    def _calcular_total(self):
        total = 0.0
        for pizza in self.pizzas:
            total += pizza.calcular_preco()
        return total
    
    def adicionar_pizza(self, pizza):
        self.pizzas.append(pizza)
        self.valor_total = self._calcular_total()
    
    def __str__(self):
        pizzas_str = "\n".join([f"  - {pizza}" for pizza in self.pizzas])
        return f"""Pedido #{self.id_pedido}
        Cliente: {self.cliente.nome}
        Forma de Pagamento: {self.forma_pagamento.value}
        Endereço de Entrega: {self.endereco_entrega}
        Pizzas:
        {pizzas_str}
        Valor Total: R$ {self.valor_total:.2f}
        Tempo Estimado: {self.tempo} minutos"""
    
    def resumo_pedido(self):
        return f"Pedido #{self.id_pedido} - {self.cliente.nome} - R$ {self.valor_total:.2f}"