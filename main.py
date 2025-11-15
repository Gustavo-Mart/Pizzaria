from pizzaria import *
from pizza import *
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def exibir_pedido_na_web():
    # 1. Cria os objetos necessários
    pizzaria = Pizzaria("Mama Mia Pizzaria", 40028922)
    pizza1 = Pizza("Calabresa", TamanhoPizza.MEDIA, True)
    pizza1.adicionar_ingrediente("Catupiry")
    pizza2 = Pizza("Era o meu Sonho", TamanhoPizza.BROTO)
    total = pizza1.calcular_preco() + pizza2.calcular_preco()

    # 2. Renderiza o template e passa as variáveis
    return render_template(
        'index.html',
        pizzaria = pizzaria,
        tamanhos_pizza = TamanhoPizza,
        p1 = pizza1, 
        p2 = pizza2, 
        total = total
    )
    
if __name__ == "__main__":
    app.run(debug=True)