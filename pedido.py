from typing import List

class Pedido:
    id_pedido : int
    cliente : str
    carrinho : str
    valor_total : float
    pagamento : List
    status : str
    endereco_entrega : str

    def __init__(self, cliente, carrinho, valor_total, status, endereco_entrega):
        self.cliente = cliente
        self.carrinho = carrinho
        self.valor_total = valor_total
        self.pagamento = ["Cartão", "Pix", "Dinheiro"]
        self.status = status
        self.endereco_entrega = endereco_entrega

