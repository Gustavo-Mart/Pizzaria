from typing import List

class Pizza():
  nome : str
  preco : float
  tamanho : List
  ingredientes : List
  borda_rech : bool
  meio_meio : bool
  
  def __init__(self, nome,preco,borda,meio):
    self.nome = nome
    self.preco = preco
    self.tamanho = ['Pequena','Média','Grande']
    self.ingredientes = []
    self.borda_rech = borda
    self.meio_meio = meio
    
class Pizzas(Pizza):
    pizzas : List[Pizza]
    def __init__(self):
      self.pizzas = []
    
    def adicionar_pizza(self, p: Pizza):
      self.pizzas.append(p)
      
    def listar_pizzas(self):
      return self.pizzas
    
if __name__ == "__main__":
    p1 = Pizza("Margherita", 25.0, False, False)
    p2 = Pizza("Pepperoni", 30.0, True, False)
    
    cardapio = Pizzas()
    cardapio.adicionar_pizza(p1)
    cardapio.adicionar_pizza(p2)
    
    for pizza in cardapio.listar_pizzas():
        print(f"Pizza: {pizza.nome}, Preço: {pizza.preco}")