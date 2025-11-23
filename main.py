from pedido import FormaPagamento, Pedido
from pizzaria import Pizzaria
from pizza import Pizza, TamanhoPizza
from flask import Flask, render_template, request, redirect, url_for, session

from usuario import Cliente, Usuario

app = Flask(__name__)

app.secret_key = 'minha-chave-secreta-123!'

@app.route("/")
def index():
    pizzaria = Pizzaria("Mama Mia Pizzaria", 40028922)
    cart_data = session.get('cart', [])
    
    carrinho_de_pizzas = []
    total_pedido = 0.0
    for item_data in cart_data:
        tamanho_enum = TamanhoPizza[item_data['tamanho']]
        tem_borda = "Borda Recheada" in item_data.get('ingredientes_extras', [])
        pizza = Pizza(item_data['sabor'], tamanho_enum, tem_borda)
        for ing in item_data.get('ingredientes_extras', []):
            if ing != "Borda Recheada":
                pizza.adicionar_ingrediente(ing)
            
        carrinho_de_pizzas.append(pizza)
        total_pedido += pizza.calcular_preco()

    return render_template(
        'index.html',
        pizzaria=pizzaria,
        tamanhos_disponiveis=TamanhoPizza,
        extras_disponiveis=pizzaria.ingredientes_extras.keys(),
        carrinho=carrinho_de_pizzas,
        total=total_pedido          
    )


@app.route("/add_pizza", methods=['POST'])
def add_pizza():
    sabor = request.form.get('sabor')
    tamanho_str = request.form.get('tamanho')
    extras_selecionados = request.form.getlist('ingredientes_extras')
    
    if not tamanho_str:
        return redirect(url_for('index'))
    
    tem_borda = "Borda Recheada" in extras_selecionados
    
    nova_pizza_data = {
        "sabor": sabor,
        "tamanho": tamanho_str,
        "borda": tem_borda,
        "ingredientes_extras": extras_selecionados
    }
    
    cart_data = session.get('cart', [])
    cart_data.append(nova_pizza_data)
    session['cart'] = cart_data
    
    return redirect(url_for('index'))


@app.route("/clear_cart")
def clear_cart():
    session.pop('cart', None)
    return redirect(url_for('index'))

@app.route("/checkout")
def checkout():
    pizzaria = Pizzaria("Mama Mia Pizzaria", 40028922)
    cart_data = session.get('cart', [])
    
    carrinho_de_pizzas = []
    total_carrinho = 0.0
    for item_data in cart_data:
        tamanho_enum = TamanhoPizza[item_data['tamanho']]
        tem_borda = item_data.get('borda', False)
        pizza = Pizza(item_data['sabor'], tamanho_enum, tem_borda)
        
        # Adicionar ingredientes extras (excluindo "Borda Recheada")
        for ing in item_data.get('ingredientes_extras', []):
            if ing != "Borda Recheada":
                pizza.adicionar_ingrediente(ing)
            
        carrinho_de_pizzas.append(pizza)
        total_carrinho += pizza.calcular_preco()
    
    return render_template(
        'checkout.html',
        formas_pagamento=[forma.value for forma in FormaPagamento],
        carrinho=carrinho_de_pizzas,
        total_carrinho=total_carrinho,
        pizzaria=pizzaria,
        tamanhos_disponiveis=TamanhoPizza,
        extras_disponiveis=pizzaria.ingredientes_extras.keys()
    )
    
@app.route("/finalizar_pedido", methods=['POST'])
def finalizar_pedido():
    nome_cliente = request.form.get('nome_cliente')
    telefone_cliente = request.form.get('telefone_cliente')
    endereco_entrega = request.form.get('endereco_entrega')
    forma_pagamento_str = request.form.get('forma_pagamento')
    
    cart_data = session.get('cart', [])
    
    if not cart_data:
        return redirect(url_for('index'))
    
    cliente = Cliente(nome_cliente, telefone_cliente)
    
    pizzas_pedido = []
    for item_data in cart_data:
        tamanho_enum = TamanhoPizza[item_data['tamanho']]
        tem_borda = item_data.get('borda', False)
        pizza = Pizza(item_data['sabor'], tamanho_enum, tem_borda)
        
        for ing in item_data.get('ingredientes_extras', []):
            if ing != "Borda Recheada":
                pizza.adicionar_ingrediente(ing)
        
        pizzas_pedido.append(pizza)
    
    forma_pagamento_enum = FormaPagamento(forma_pagamento_str)
    
    novo_pedido = Pedido(
        cliente,
        pizzas_pedido,
        forma_pagamento_enum,
        endereco_entrega
    )
    
    session.pop('cart', None)
    
    return render_template('confirmacao.html', pedido=novo_pedido)

if __name__ == "__main__":
    app.run(debug=True)