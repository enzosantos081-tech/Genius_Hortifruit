# 🌿 GENIUS Hortifruit — Como Rodar

## Estrutura do Projeto

```
genius_new/
├── backend/
│   ├── app.py              ← Flask com todas as rotas
│   ├── requirements.txt
│   └── dados/              ← criado automaticamente
│       ├── usuarios.json
│       ├── produtos.json
│       └── pedidos.json
├── index.html
├── loja.html
├── produto.html
├── carrinho.html
├── checkout.html
├── login.html
├── cliente.html
├── admin.html
├── style.css
└── js/
    ├── app.js
    └── header.js
```

---

## 1. Rodar o Backend (Flask)

```bash
cd backend

# Instalar dependências (só na primeira vez)
pip install flask flask-cors

# Iniciar o servidor
python app.py
```

O servidor vai rodar em: **http://127.0.0.1:5000**

Na primeira execução, os arquivos JSON são criados automaticamente com dados de exemplo.

---

## 2. Abrir o Frontend

Abra os arquivos HTML diretamente no navegador **com um servidor local**.

**Opção mais fácil (VS Code):**
- Instale a extensão **Live Server**
- Clique com botão direito em `index.html` → **Open with Live Server**

**Ou via Python:**
```bash
cd genius_new
python -m http.server 8080
# Acesse: http://localhost:8080
```

> ⚠️ **Não abra os arquivos diretamente** como `file://` — o `fetch` da API não funciona assim.

---

## 3. Credenciais de Demo

| Tipo    | E-mail               | Senha      |
|---------|----------------------|------------|
| Cliente | joao@email.com       | senha123   |
| Admin   | admin@genius.com     | admin123   |

---

## Rotas da API

| Método | Rota                        | Descrição                  |
|--------|-----------------------------|----------------------------|
| POST   | /login                      | Login                      |
| POST   | /cadastrar                  | Cadastro de usuário        |
| GET    | /produtos                   | Listar produtos ativos     |
| GET    | /produtos/<id>              | Detalhe do produto         |
| POST   | /pedidos                    | Criar pedido               |
| GET    | /pedidos/<usuario_id>       | Pedidos de um usuário      |
| PUT    | /usuario/<id>/metas         | Atualizar metas nutricionais|
| GET    | /admin/produtos             | Admin: listar todos        |
| POST   | /admin/produtos             | Admin: criar produto       |
| PUT    | /admin/produtos/<id>        | Admin: editar produto      |
| DELETE | /admin/produtos/<id>        | Admin: deletar produto     |
| GET    | /admin/usuarios             | Admin: listar usuários     |
| PUT    | /admin/usuarios/<id>        | Admin: ativar/desativar    |
| GET    | /admin/pedidos              | Admin: todos os pedidos    |
