from pizzaria import *
from pizza import *

##USUARIO CLIENTE E ADM

def main():
    pizzaria = Pizzaria("Mama Mia Pizzaria", 40028922)
    
    pizzaria.exibir_cardapio()

    pizza1 = Pizza("Calabresa", TamanhoPizza.MEDIA, True)
    pizza1.adicionar_ingrediente("Catupiry")

    pizza2 = Pizza("Era o meu Sonho", TamanhoPizza.BROTO)

    print("\n--------PEDIDOS--------")
    print(pizza1)
    print(pizza2)

    total = pizza1.calcular_preco() + pizza2.calcular_preco()
    print(f"\n  Total do pedido: R$ {total:.2f}")

if __name__ == "__main__":
    main()