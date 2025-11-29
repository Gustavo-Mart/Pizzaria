#  Sistema de Pizzaria - Mama Mia

##  Integrantes
- Beatriz Mendes Chuva - chuva@unisantos.br
- Gustavo Martins da Silva - gustavomsilva@unisantos.br
- Jennyfer Forte Almeida Costa - jennyfercosta@unisantos.br


##  Descrição
Sistema web para gerenciamento de pizzaria com pedidos online e painel administrativo. Desenvolvido em Python/Flask aplicando conceitos de POO (herança, polimorfismo, abstração, encapsulamento) o projeto automatiza operações desde o cardápio até a entrega. Oferece cardápio interativo com personalização de pizzas (tamanhos, ingredientes, borda recheada), carrinho de compras e checkout com múltiplas formas de pagamento (cartão, PIX, dinheiro), além de painel administrativo com gerenciamento de pedidos.

**Funcionalidades:**
- Cardápio interativo com personalização de pizzas
- Carrinho de compras e checkout
- Painel admin com estatísticas e gerenciamento de pedidos

##  Tecnologias
Python 3.x, Flask, HTML/CSS/JavaScript

##  Como Executar

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/pizzaria-mama-mia.git
cd pizzaria-mama-mia

# Instale dependências
pip install flask

# Execute
python main.py

# Acesse: http://localhost:5000
```

##  Acesso Admin
- URL: `/admin`
- Email: `admin@admin.com`
- Senha: `123456789`

##  Estrutura
```
pizzaria/
├── main.py           # Aplicação Flask
├── pizza.py          # Classe Pizza
├── pedido.py         # Classe Pedido
├── usuario.py        # Classes Usuario/Cliente/Administrador
├── pizzaria.py       # Classe Pizzaria
├── templates/        # HTML
└── static/          # CSS
```
