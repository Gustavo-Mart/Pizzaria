from abc import ABC, abstractmethod
from typing import List

class Usuario(ABC):
    nome: str
    email: str
    telefone: int
    
    def __init__(self, nome, email, telefone):
        self.nome = nome
        self.email = email
        self.telefone = telefone
    
    @abstractmethod
    def exibir_informacoes(self) -> str:
        pass
    
    def __str__(self) -> str:
        return self.exibir_informacoes()

class Cliente(Usuario):
    endereco: str
    pedidos: List
    
    def __init__(self, nome, email, telefone, endereco):
        super().__init__(nome, email, telefone)
        self.endereco = endereco
        self.pedidos = []
    
    def adicionar_pedido(self, pedido):
        self.pedidos.append(pedido)
    
    def exibir_informacoes(self):
        return f"Cliente: {self.nome}\nEmail: {self.email}\nTelefone: {self.telefone}\nEndereço: {self.endereco}"

class Administrador(Usuario):
    __senha: str 
    
    def __init__(self, nome, email, telefone, senha):
        super().__init__(nome, email, telefone)
        self.__senha = senha
    
    def verificar_senha(self, senha_digitada):
        return senha_digitada == self.__senha
    
    def exibir_relatorio_vendas(self, pizzaria, senha):
        total_vendas = sum(pedido.valor_total for pedido in pizzaria.pedidos)
        total_pedidos = len(pizzaria.pedidos)
        total_clientes = len(pizzaria.clientes)

        print("\n")
        print(f"RELATORIO DE VENDAS - {pizzaria.nome}")
        print(f"Total de pedidos: {total_pedidos}")
        print(f"Total de clientes: {total_clientes}")
        print(f"Faturamento total: R$ {total_vendas:.2f}")
        
        if pizzaria.pedidos:
            print(f"\nUltimos pedidos:")
            for pedido in pizzaria.pedidos: 
                print(f" - {pedido.cliente.nome}: R$ {pedido.valor_total:.2f}")
    
    def exibir_todos_pedidos(self, pizzaria, senha):        
        if not pizzaria.pedidos:
            print("\033[33mNenhum pedido realizado.\033[0m")
            return
        
        print("\n")
        print(f"TODOS OS PEDIDOS - {pizzaria.nome}")
        for pedido in pizzaria.pedidos:
            print(f"\nPedido #{pedido.id_pedido}:")
            print(f"Cliente: {pedido.cliente.nome}")
            print(f"Telefone: {pedido.cliente.telefone}")
            print(f"Endereço: {pedido.cliente.endereco}")
            print(f"Pizzas:")
            for pizza in pedido.pizzas:
                print(f"  - {pizza}")
            print(f"Total: R$ {pedido.valor_total:.2f}")
    
    def exibir_dados_clientes(self, pizzaria, senha):        
        if not pizzaria.clientes:
            print("\033[33mNenhum cliente cadastrado.\033[0m")
            return
        
        print("\n")
        print(f"DADOS DOS CLIENTES - {pizzaria.nome}")
        for cliente in pizzaria.clientes:
            print(f"Nome: {cliente.nome}")
            print(f"Email: {cliente.email}")
            print(f"Telefone: {cliente.telefone}")
            print(f"Endereço: {cliente.endereco}")
            print(f"Total de pedidos: {len(cliente.pedidos)}")

    def exibir_informacoes(self):
        return f"Administrador: {self.nome}\nEmail: {self.email}\nTelefone: {self.telefone}"