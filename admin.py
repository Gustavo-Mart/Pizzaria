import json
from flask import app, jsonify, redirect, render_template, request, session, url_for

from pizza import Pizza, TamanhoPizza

# Instância global da pizzaria (mover para fora das rotas)
pizzaria_global = Pizzaria("Mama Mia Pizzaria", 40028922)
admin_global = None

@app.route("/admin", methods=['GET', 'POST'])
def admin():
    global admin_global, pizzaria_global
    
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        # Criar admin se não existir
        if not admin_global:
            from usuario import Administrador
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
    
    pedido_id = int(request.form.get('pedido_id'))
    nome = request.form.get('nome')
    telefone = request.form.get('telefone')
    endereco = request.form.get('endereco')
    forma_pagamento_str = request.form.get('forma_pagamento')
    
    # Encontrar o pedido
    pedido = None
    for p in pizzaria_global.pedidos:
        if p.id_pedido == pedido_id:
            pedido = p
            break
    
    if pedido:
        # Atualizar dados do cliente
        pedido.cliente.nome = nome
        pedido.cliente.telefone = telefone
        pedido.cliente.endereco = endereco
        
        # Atualizar endereço de entrega
        pedido.endereco_entrega = endereco
        
        # Atualizar forma de pagamento
        pedido.forma_pagamento = FormaPagamento[forma_pagamento_str]
    
    return redirect(url_for('admin_dashboard'))


@app.route("/admin/excluir_pedido", methods=['POST'])
def excluir_pedido():
    global pizzaria_global
    
    if not session.get('is_admin'):
        return redirect(url_for('admin'))
    
    pedido_id = int(request.form.get('pedido_id'))
    
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
    
    pedido_id = int(request.form.get('pedido_id'))
    pizza_index = int(request.form.get('pizza_index'))
    
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


# Modificar a rota index para usar pizzaria_global
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


# Modificar finalizar_pedido para usar pizzaria_global
@app.route("/finalizar_pedido", methods=['POST'])
def finalizar_pedido():
    global pizzaria_global
    
    nome = request.form.get('nome')
    telefone = request.form.get('telefone')
    endereco = request.form.get('endereco')
    forma_pagamento_str = request.form.get('forma_pagamento')
    
    cart_data = session.get('cart', [])
    
    if not cart_data:
        return redirect(url_for('index'))
    
    cliente = Cliente(nome, telefone, endereco)
    
    # Verificar se cliente já existe
    cliente_existente = None
    for c in pizzaria_global.clientes:
        if c.telefone == telefone:
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