import json
from pedido import FormaPagamento, Pedido
from pizzaria import Pizzaria
from pizza import Pizza, TamanhoPizza
from flask import Flask, jsonify, render_template, request, redirect, url_for, session
from usuario import Cliente, Administrador

app = Flask(__name__)
app.secret_key = 'minha-chave-secreta-123!'

# Instâncias globais
pizzaria_global = Pizzaria("Mama Mia Pizzaria", 40028922)
admin_global = None


@app.route("/")
def index():
    global pizzaria_global
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
        pizzaria=pizzaria_global,
        tamanhos_disponiveis=TamanhoPizza,
        extras_disponiveis=pizzaria_global.ingredientes_extras.keys(),
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
    global pizzaria_global
    cart_data = session.get('cart', [])
    
    carrinho_de_pizzas = []
    total_carrinho = 0.0
    for item_data in cart_data:
        tamanho_enum = TamanhoPizza[item_data['tamanho']]
        tem_borda = item_data.get('borda', False)
        pizza = Pizza(item_data['sabor'], tamanho_enum, tem_borda)
        
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
        pizzaria=pizzaria_global,
        tamanhos_disponiveis=TamanhoPizza,
        extras_disponiveis=pizzaria_global.ingredientes_extras.keys()
    )


@app.route("/finalizar_pedido", methods=['POST'])
def finalizar_pedido():
    global pizzaria_global
    
    nome = request.form.get('nome')
    telefone = request.form.get('telefone')
    endereco = request.form.get('endereco')
    forma_pagamento_str = request.form.get('forma_pagamento')
    
    # --- CORREÇÃO: Validação dos dados ---
    # Se algum desses campos for None ou vazio, não podemos criar o Cliente.
    if not nome or not telefone or not endereco:
        # Você pode redirecionar de volta para o checkout ou home
        return redirect(url_for('checkout')) 
    # -------------------------------------

    cart_data = session.get('cart', [])
    
    if not cart_data:
        return redirect(url_for('index'))
    
    # Agora o Python sabe que 'nome', 'telefone' e 'endereco' não são None
    cliente = Cliente(nome, telefone, endereco)
    
    # Verificar se cliente já existe
    cliente_existente = None
    for c in pizzaria_global.clientes:
        # Comparar como string para evitar problemas de tipo
        if str(c.telefone) == str(telefone):
            cliente_existente = c
            break
    
    if not cliente_existente:
        pizzaria_global.clientes.append(cliente)
    else:
        cliente = cliente_existente
        cliente.endereco = endereco
    
    pizzas_pedido = []
    for item_data in cart_data:
        tamanho_enum = TamanhoPizza[item_data['tamanho']]
        tem_borda = item_data.get('borda', False)
        pizza = Pizza(item_data['sabor'], tamanho_enum, tem_borda)
        
        for ing in item_data.get('ingredientes_extras', []):
            if ing != "Borda Recheada":
                pizza.adicionar_ingrediente(ing)
        
        pizzas_pedido.append(pizza)
    
    # Converter forma de pagamento
    forma_pagamento = None
    # Verifica se a string existe antes de iterar
    if forma_pagamento_str:
        for forma in FormaPagamento:
            if forma.value == forma_pagamento_str:
                forma_pagamento = forma
                break
    
    if not forma_pagamento:
        forma_pagamento = FormaPagamento.PIX
    
    novo_pedido = Pedido(cliente, pizzas_pedido, forma_pagamento, endereco)
    
    pizzaria_global.pedidos.append(novo_pedido)
    cliente.adicionar_pedido(novo_pedido)
    
    session.pop('cart', None)
    
    return render_template('confirmacao.html', pedido=novo_pedido)


@app.route("/admin", methods=['GET', 'POST'])
def admin():
    global admin_global, pizzaria_global
    
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        # Criar admin se não existir
        if not admin_global:
            admin_global = Administrador("Admin", email, "123456789", senha)
        
        # Verificar senha
        if admin_global.verificar_senha(senha):
            session['is_admin'] = True
            session['admin_email'] = email
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('login.html', erro="Senha incorreta!")
    
    # Se já estiver logado, redirecionar para dashboard
    if session.get('is_admin'):
        return redirect(url_for('admin_dashboard'))
    
    return render_template('login.html')


@app.route("/admin/dashboard")
def admin_dashboard():
    global pizzaria_global
    
    if not session.get('is_admin'):
        return redirect(url_for('admin'))
    
    # Calcular estatísticas
    total_vendas = sum(pedido.valor_total for pedido in pizzaria_global.pedidos)
    total_pedidos = len(pizzaria_global.pedidos)
    total_clientes = len(pizzaria_global.clientes)
    
    # Preparar dados dos pedidos para JSON
    pedidos_json = []
    for pedido in pizzaria_global.pedidos:
        pedidos_json.append({
            'id': pedido.id_pedido,
            'cliente_nome': pedido.cliente.nome,
            'cliente_telefone': pedido.cliente.telefone,
            'endereco': pedido.endereco_entrega,
            'forma_pagamento': pedido.forma_pagamento.name
        })
    
    return render_template(
        'admin.html',
        pizzaria=pizzaria_global,
        total_vendas=total_vendas,
        total_pedidos=total_pedidos,
        total_clientes=total_clientes,
        pedidos_json=json.dumps(pedidos_json),
        formas_pagamento=FormaPagamento
    )


@app.route("/admin/editar_pedido", methods=['POST'])
def editar_pedido():
    global pizzaria_global
    
    if not session.get('is_admin'):
        return redirect(url_for('admin'))
    
    # Conversão segura do ID (como fizemos antes)
    pedido_id_str = request.form.get('pedido_id')
    if not pedido_id_str:
        return redirect(url_for('admin_dashboard'))
    pedido_id = int(pedido_id_str)

    nome = request.form.get('nome')
    telefone = request.form.get('telefone')
    endereco = request.form.get('endereco')
    
    # --- CORREÇÃO AQUI ---
    forma_pagamento_str = request.form.get('forma_pagamento')

    # Encontrar o pedido
    pedido = None
    for p in pizzaria_global.pedidos:
        if p.id_pedido == pedido_id:
            pedido = p
            break
    
    if pedido:
        pedido.cliente.nome = nome
        pedido.cliente.telefone = telefone
        pedido.endereco_entrega = endereco
        
        # Só tenta atribuir se forma_pagamento_str não for None e existir no Enum
        if forma_pagamento_str and forma_pagamento_str in FormaPagamento.__members__:
            pedido.forma_pagamento = FormaPagamento[forma_pagamento_str]
    
    return redirect(url_for('admin_dashboard'))


@app.route("/admin/excluir_pedido", methods=['POST'])
def excluir_pedido():
    global pizzaria_global
    
    if not session.get('is_admin'):
        return redirect(url_for('admin'))
    
    pedido_id_str = request.form.get('pedido_id')
    if not pedido_id_str:
        return redirect(url_for('admin_dashboard'))

    pedido_id = int(pedido_id_str)
    
    # Encontrar e remover o pedido
    pedido_removido = None
    for i, pedido in enumerate(pizzaria_global.pedidos):
        if pedido.id_pedido == pedido_id:
            pedido_removido = pizzaria_global.pedidos.pop(i)
            break
    
    # Remover o pedido da lista do cliente
    if pedido_removido:
        for cliente in pizzaria_global.clientes:
            if pedido_removido in cliente.pedidos:
                cliente.pedidos.remove(pedido_removido)
                break
    
    return redirect(url_for('admin_dashboard'))


@app.route("/admin/remover_pizza", methods=['POST'])
def remover_pizza():
    global pizzaria_global
    
    if not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    pedido_id_str = request.form.get('pedido_id')
    pizza_index_str = request.form.get('pizza_index')

    if not pedido_id_str or not pizza_index_str:
        return jsonify({'error': 'Dados inválidos'}), 400

    pedido_id = int(pedido_id_str)
    pizza_index = int(pizza_index_str)
    
    # Encontrar o pedido
    pedido = None
    for p in pizzaria_global.pedidos:
        if p.id_pedido == pedido_id:
            pedido = p
            break
    
    if pedido and 0 <= pizza_index < len(pedido.pizzas):
        # Remover a pizza
        pedido.pizzas.pop(pizza_index)
        
        # Recalcular o valor total
        pedido.valor_total = pedido._calcular_total()
        
        # Se não houver mais pizzas, excluir o pedido
        if len(pedido.pizzas) == 0:
            pizzaria_global.pedidos.remove(pedido)
            for cliente in pizzaria_global.clientes:
                if pedido in cliente.pedidos:
                    cliente.pedidos.remove(pedido)
                    break
        
        return jsonify({'success': True})
    
    return jsonify({'error': 'Pedido ou pizza não encontrado'}), 404


@app.route("/logout")
def logout():
    session.pop('is_admin', None)
    session.pop('admin_email', None)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)