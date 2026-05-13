from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:5500", "http://localhost:5500"])

# ============================================================
# Caminhos dos arquivos JSON
# ============================================================
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
DADOS_DIR  = os.path.join(BASE_DIR, 'dados')

ARQ_USUARIOS = os.path.join(DADOS_DIR, 'usuarios.json')
ARQ_PRODUTOS = os.path.join(DADOS_DIR, 'produtos.json')
ARQ_PEDIDOS  = os.path.join(DADOS_DIR, 'pedidos.json')

os.makedirs(DADOS_DIR, exist_ok=True)


# ============================================================
# Helpers: ler / salvar JSON  
# ============================================================
def ler(arquivo):
    if not os.path.exists(arquivo):
        return []
    with open(arquivo, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except (json.JSONDecodeError, ValueError):
            return []

def salvar(arquivo, dados):
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def proximo_id(lista):
    if not lista:
        return 1
    return max(item['id'] for item in lista) + 1


# ============================================================
# Seed: popula com dados de exemplo se os arquivos estiverem
#       vazios (roda apenas uma vez)
# ============================================================
def seed():
    # --- Usuários ---
    if not ler(ARQ_USUARIOS):
        salvar(ARQ_USUARIOS, [
            {
                "id": 1, "nome": "João Silva",
                "email": "joao@email.com", "senha": "senha123",
                "cpf": "123.456.789-00", "telefone": "(11) 98888-7777",
                "rua": "Rua das Flores", "numero": "10",
                "bairro": "Centro", "cidade": "Indaiatuba",
                "cep": "13330-000", "complemento": "",
                "meta_calorias": 2000, "meta_proteina": 150,
                "meta_carboidratos": 250, "meta_gordura": 70,
                "status": "ativo", "admin": False
            },
            {
                "id": 99, "nome": "Admin GENIUS",
                "email": "admin@genius.com", "senha": "admin123",
                "cpf": "000.000.000-00", "telefone": "(19) 99999-0000",
                "rua": "Av. Central", "numero": "1",
                "bairro": "Centro", "cidade": "Indaiatuba",
                "cep": "13330-000", "complemento": "",
                "meta_calorias": 2500, "meta_proteina": 180,
                "meta_carboidratos": 300, "meta_gordura": 80,
                "status": "ativo", "admin": True
            }
        ])
        print("✅ Usuários criados")

    # --- Produtos ---
    if not ler(ARQ_PRODUTOS):
        salvar(ARQ_PRODUTOS, [
            {"id":1,"nome":"Frango Grelhado","marca":"Saudável+","preco":25.90,"categoria":"Proteínas",
             "imagem":"https://images.unsplash.com/photo-1598103442097-8b74394b95c3?w=400&q=80",
             "estoque":50,"calorias":165,"proteina":31,"carboidratos":0,"gordura":3.6,"saudavel":True,"ativo":True},
            {"id":2,"nome":"Salada de Quinoa","marca":"NutriVerde","preco":18.50,"categoria":"Saladas",
             "imagem":"https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=400&q=80",
             "estoque":30,"calorias":120,"proteina":4,"carboidratos":22,"gordura":2,"saudavel":True,"ativo":True},
            {"id":3,"nome":"Iogurte Grego Natural","marca":"Lacfree","preco":12.90,"categoria":"Laticínios",
             "imagem":"https://images.unsplash.com/photo-1488477181946-6428a0291777?w=400&q=80",
             "estoque":80,"calorias":59,"proteina":10,"carboidratos":4,"gordura":0.4,"saudavel":True,"ativo":True},
            {"id":4,"nome":"Abacate Orgânico","marca":"Campo Verde","preco":8.90,"categoria":"Frutas",
             "imagem":"https://images.unsplash.com/photo-1519162808019-7de1683fa2ad?w=400&q=80",
             "estoque":45,"calorias":160,"proteina":2,"carboidratos":9,"gordura":15,"saudavel":True,"ativo":True},
            {"id":5,"nome":"Granola Integral","marca":"BioMix","preco":22.00,"categoria":"Cereais",
             "imagem":"https://images.unsplash.com/photo-1517686469429-8bdb88b9f907?w=400&q=80",
             "estoque":60,"calorias":400,"proteina":12,"carboidratos":65,"gordura":10,"saudavel":False,"ativo":True},
            {"id":6,"nome":"Salmão Grelhado","marca":"OceanFresh","preco":45.00,"categoria":"Proteínas",
             "imagem":"https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=400&q=80",
             "estoque":25,"calorias":208,"proteina":20,"carboidratos":0,"gordura":13,"saudavel":True,"ativo":True},
            {"id":7,"nome":"Mix de Castanhas","marca":"NutriSeeds","preco":32.50,"categoria":"Snacks",
             "imagem":"https://images.unsplash.com/photo-1508061253366-f7da158b6d46?w=400&q=80",
             "estoque":70,"calorias":580,"proteina":20,"carboidratos":20,"gordura":50,"saudavel":False,"ativo":True},
            {"id":8,"nome":"Banana Prata","marca":"FrutaFácil","preco":5.90,"categoria":"Frutas",
             "imagem":"https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?w=400&q=80",
             "estoque":100,"calorias":89,"proteina":1,"carboidratos":23,"gordura":0.3,"saudavel":True,"ativo":True},
            {"id":9,"nome":"Ovo Caipira Dúzia","marca":"Galinha Feliz","preco":15.00,"categoria":"Proteínas",
             "imagem":"https://images.unsplash.com/photo-1582722872445-44dc5f7e3c8f?w=400&q=80",
             "estoque":40,"calorias":155,"proteina":13,"carboidratos":1,"gordura":11,"saudavel":True,"ativo":True},
            {"id":10,"nome":"Wrap Integral","marca":"GrãoBom","preco":9.90,"categoria":"Cereais",
             "imagem":"https://images.unsplash.com/photo-1626700051175-6818013e1d4f?w=400&q=80",
             "estoque":55,"calorias":240,"proteina":8,"carboidratos":42,"gordura":4,"saudavel":False,"ativo":True},
            {"id":11,"nome":"Pepino Japonês","marca":"Horta Viva","preco":4.50,"categoria":"Verduras",
             "imagem":"https://images.unsplash.com/photo-1604977042946-1eecc30f269e?w=400&q=80",
             "estoque":90,"calorias":16,"proteina":0.7,"carboidratos":4,"gordura":0.1,"saudavel":True,"ativo":True},
            {"id":12,"nome":"Whey Protein Baunilha","marca":"MaxPro","preco":89.90,"categoria":"Suplementos",
             "imagem":"https://images.unsplash.com/photo-1593095948071-474c5cc2989d?w=400&q=80",
             "estoque":20,"calorias":120,"proteina":25,"carboidratos":3,"gordura":2,"saudavel":False,"ativo":True},
        ])
        print("✅ Produtos criados")

    # --- Pedidos ---
    if not ler(ARQ_PEDIDOS):
        salvar(ARQ_PEDIDOS, [])
        print("✅ Arquivo de pedidos criado")


# ============================================================
# Rotas – Autenticação
# ============================================================

@app.route('/login', methods=['POST'])
def login():
    dados = request.get_json()
    email = (dados.get('email') or '').strip().lower()
    senha = dados.get('senha') or ''

    usuarios = ler(ARQ_USUARIOS)
    usuario = next((u for u in usuarios
                    if u['email'].lower() == email and u['senha'] == senha), None)

    if not usuario:
        return jsonify({'erro': 'E-mail ou senha incorretos'}), 401

    if usuario.get('status') == 'inativo':
        return jsonify({'erro': 'Conta desativada. Entre em contato com o suporte.'}), 403

    sem_senha = {k: v for k, v in usuario.items() if k != 'senha'}
    return jsonify(sem_senha), 200


@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    dados = request.get_json()

    obrigatorios = ['nome', 'email', 'senha', 'telefone', 'rua', 'numero', 'bairro', 'cidade', 'cep']
    for campo in obrigatorios:
        if not dados.get(campo):
            return jsonify({'erro': f'Campo "{campo}" é obrigatório'}), 400

    if len(dados['senha']) < 6:
        return jsonify({'erro': 'Senha deve ter pelo menos 6 caracteres'}), 400

    usuarios = ler(ARQ_USUARIOS)

    if any(u['email'].lower() == dados['email'].lower() for u in usuarios):
        return jsonify({'erro': 'E-mail já cadastrado'}), 409

    novo = {
        'id': proximo_id(usuarios),
        'nome':         dados['nome'],
        'email':        dados['email'],
        'senha':        dados['senha'],
        'cpf':          dados.get('cpf', ''),
        'telefone':     dados.get('telefone', ''),
        'rua':          dados.get('rua', ''),
        'numero':       dados.get('numero', ''),
        'bairro':       dados.get('bairro', ''),
        'cidade':       dados.get('cidade', ''),
        'cep':          dados.get('cep', ''),
        'complemento':  dados.get('complemento', ''),
        'meta_calorias':    2000,
        'meta_proteina':    150,
        'meta_carboidratos': 250,
        'meta_gordura':     70,
        'status': 'ativo',
        'admin':  False
    }

    usuarios.append(novo)
    salvar(ARQ_USUARIOS, usuarios)

    sem_senha = {k: v for k, v in novo.items() if k != 'senha'}
    return jsonify(sem_senha), 201
 

# ============================================================
# Rotas – Produtos (público)
# ============================================================

@app.route('/produtos', methods=['GET'])
def listar_produtos():
    produtos = ler(ARQ_PRODUTOS)
    ativos = [p for p in produtos if p.get('ativo', True)]
    return jsonify(ativos), 200


@app.route('/produtos/<int:pid>', methods=['GET'])
def detalhe_produto(pid):
    produtos = ler(ARQ_PRODUTOS)
    p = next((x for x in produtos if x['id'] == pid), None)
    if not p:
        return jsonify({'erro': 'Produto não encontrado'}), 404
    return jsonify(p), 200


# ============================================================
# Rotas – Pedidos
# ============================================================

@app.route('/pedidos', methods=['POST'])
def criar_pedido():
    dados = request.get_json()

    if not dados.get('usuario_id') or not dados.get('itens'):
        return jsonify({'erro': 'Dados incompletos'}), 400

    pedidos = ler(ARQ_PEDIDOS)

    novo = {
        'id':                proximo_id(pedidos),
        'usuario_id':        dados['usuario_id'],
        'data':              datetime.now().strftime('%Y-%m-%d'),
        'itens':             dados.get('itens', []),
        'total_preco':       dados.get('total_preco', 0),
        'total_calorias':    dados.get('total_calorias', 0),
        'total_proteina':    dados.get('total_proteina', 0),
        'total_carboidratos':dados.get('total_carboidratos', 0),
        'total_gordura':     dados.get('total_gordura', 0),
        'entrega':           dados.get('entrega', 'domicilio'),
        'pagamento':         dados.get('pagamento', 'pix'),
        'endereco':          dados.get('endereco', ''),
        'status':            'confirmado'
    }

    pedidos.append(novo)
    salvar(ARQ_PEDIDOS, pedidos)
    return jsonify(novo), 201


@app.route('/pedidos/<int:uid>', methods=['GET'])
def pedidos_usuario(uid):
    todos = ler(ARQ_PEDIDOS)
    meus  = [p for p in todos if p['usuario_id'] == uid]
    meus.sort(key=lambda x: x['id'], reverse=True)
    return jsonify(meus), 200


# ============================================================
# Rotas – Área do cliente
# ============================================================

@app.route('/usuario/<int:uid>/metas', methods=['PUT'])
def atualizar_metas(uid):
    dados    = request.get_json()
    usuarios = ler(ARQ_USUARIOS)
    usuario  = next((u for u in usuarios if u['id'] == uid), None)

    if not usuario:
        return jsonify({'erro': 'Usuário não encontrado'}), 404

    for campo in ['meta_calorias','meta_proteina','meta_carboidratos','meta_gordura']:
        if campo in dados:
            usuario[campo] = int(dados[campo])

    salvar(ARQ_USUARIOS, usuarios)
    sem_senha = {k: v for k, v in usuario.items() if k != 'senha'}
    return jsonify(sem_senha), 200


@app.route('/admin/pedidos', methods=['GET'])
def admin_pedidos():
    todos = ler(ARQ_PEDIDOS)
    todos.sort(key=lambda x: x['id'], reverse=True)
    return jsonify(todos), 200


# ============================================================
# Rotas – Admin / Produtos
# ============================================================

@app.route('/admin/produtos', methods=['GET'])
def admin_produtos():
    return jsonify(ler(ARQ_PRODUTOS)), 200


@app.route('/admin/produtos', methods=['POST'])
def admin_criar_produto():
    dados    = request.get_json()
    produtos = ler(ARQ_PRODUTOS)

    if not dados.get('nome') or dados.get('preco') is None:
        return jsonify({'erro': 'Nome e preço são obrigatórios'}), 400

    novo = {
        'id':           proximo_id(produtos),
        'nome':         dados.get('nome', ''),
        'marca':        dados.get('marca', ''),
        'preco':        float(dados.get('preco', 0)),
        'categoria':    dados.get('categoria', 'Outros'),
        'imagem':       dados.get('imagem', ''),
        'estoque':      int(dados.get('estoque', 0)),
        'calorias':     int(dados.get('calorias', 0)),
        'proteina':     float(dados.get('proteina', 0)),
        'carboidratos': float(dados.get('carboidratos', 0)),
        'gordura':      float(dados.get('gordura', 0)),
        'saudavel':     bool(dados.get('saudavel', False)),
        'ativo':        True
    }

    produtos.append(novo)
    salvar(ARQ_PRODUTOS, produtos)
    return jsonify(novo), 201


@app.route('/admin/produtos/<int:pid>', methods=['PUT'])
def admin_editar_produto(pid):
    dados    = request.get_json()
    produtos = ler(ARQ_PRODUTOS)
    produto  = next((p for p in produtos if p['id'] == pid), None)

    if not produto:
        return jsonify({'erro': 'Produto não encontrado'}), 404

    campos = ['nome','marca','preco','categoria','imagem','estoque',
              'calorias','proteina','carboidratos','gordura','saudavel','ativo']
    for c in campos:
        if c in dados:
            produto[c] = dados[c]

    salvar(ARQ_PRODUTOS, produtos)
    return jsonify(produto), 200


@app.route('/admin/produtos/<int:pid>', methods=['DELETE'])
def admin_deletar_produto(pid):
    produtos = ler(ARQ_PRODUTOS)
    novos    = [p for p in produtos if p['id'] != pid]

    if len(novos) == len(produtos):
        return jsonify({'erro': 'Produto não encontrado'}), 404

    salvar(ARQ_PRODUTOS, novos)
    return jsonify({'ok': True}), 200


# ============================================================
# Rotas – Admin / Usuários
# ============================================================

@app.route('/admin/usuarios', methods=['GET'])
def admin_usuarios():
    usuarios = ler(ARQ_USUARIOS)
    sem_senha = [{k: v for k, v in u.items() if k != 'senha'} for u in usuarios]
    return jsonify(sem_senha), 200


@app.route('/admin/usuarios/<int:uid>', methods=['PUT'])
def admin_editar_usuario(uid):
    dados    = request.get_json()
    usuarios = ler(ARQ_USUARIOS)
    usuario  = next((u for u in usuarios if u['id'] == uid), None)

    if not usuario:
        return jsonify({'erro': 'Usuário não encontrado'}), 404

    if 'status' in dados:
        usuario['status'] = dados['status']
    if 'admin' in dados:
        usuario['admin'] = dados['admin']

    salvar(ARQ_USUARIOS, usuarios)
    sem_senha = {k: v for k, v in usuario.items() if k != 'senha'}
    return jsonify(sem_senha), 200


# ============================================================
# Start
# ============================================================
if __name__ == '__main__':
    seed()
    print("\n🌿 GENIUS Hortifruit – backend rodando em http://127.0.0.1:5000")
    print("   Demo cliente: joao@email.com / senha123")
    print("   Demo admin:   admin@genius.com / admin123\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
