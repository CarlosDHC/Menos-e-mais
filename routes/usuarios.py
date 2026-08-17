from flask import Blueprint, request
from models import db, Usuario


usuarios_bp = Blueprint(
    'usuarios',
    __name__,
    url_prefix='/api/usuarios'
)


# ============================================================
# LISTAR USUÁRIOS
# ============================================================

@usuarios_bp.route('/', methods=['GET'])
def listar_usuarios():

    usuarios = Usuario.query.all()

    return {
        'usuarios': [
            {
                'id_usuario': usuario.id_usuario,
                'nome': usuario.nome,
                'email': usuario.email,
                'tipo': usuario.tipo,
                'primeiro_acesso': usuario.primeiro_acesso
            }
            for usuario in usuarios
        ]
    }


# ============================================================
# BUSCAR USUÁRIO
# ============================================================

@usuarios_bp.route('/<int:id_usuario>', methods=['GET'])
def buscar_usuario(id_usuario):

    usuario = Usuario.query.get(id_usuario)

    if not usuario:
        return {
            'erro': 'Usuário não encontrado'
        }, 404

    return {
        'id_usuario': usuario.id_usuario,
        'nome': usuario.nome,
        'email': usuario.email,
        'tipo': usuario.tipo,
        'primeiro_acesso': usuario.primeiro_acesso
    }


# ============================================================
# CADASTRAR USUÁRIO
# ============================================================

@usuarios_bp.route('/', methods=['POST'])
def cadastrar_usuario():

    dados = request.get_json()

    if not dados:
        return {
            'erro': 'Nenhum dado foi enviado'
        }, 400

    nome = dados.get('nome')
    email = dados.get('email')
    senha = dados.get('senha')
    tipo = dados.get('tipo')
    primeiro_acesso = dados.get('primeiro_acesso', 1)

    if not nome or not email or not senha or not tipo:
        return {
            'erro': 'Nome, email, senha e tipo são obrigatórios'
        }, 400

    # Verifica se o e-mail já está cadastrado
    usuario_existente = Usuario.query.filter_by(
        email=email
    ).first()

    if usuario_existente:
        return {
            'erro': 'Este e-mail já está cadastrado'
        }, 409

    usuario = Usuario(
        nome=nome,
        email=email,
        senha=senha,
        tipo=tipo,
        primeiro_acesso=primeiro_acesso
    )

    db.session.add(usuario)
    db.session.commit()

    return {
        'mensagem': 'Usuário cadastrado com sucesso',
        'usuario': {
            'id_usuario': usuario.id_usuario,
            'nome': usuario.nome,
            'email': usuario.email,
            'tipo': usuario.tipo,
            'primeiro_acesso': usuario.primeiro_acesso
        }
    }, 201


# ============================================================
# ATUALIZAR USUÁRIO
# ============================================================

@usuarios_bp.route('/<int:id_usuario>', methods=['PUT'])
def atualizar_usuario(id_usuario):

    usuario = Usuario.query.get(id_usuario)

    if not usuario:
        return {
            'erro': 'Usuário não encontrado'
        }, 404

    dados = request.get_json()

    if not dados:
        return {
            'erro': 'Nenhum dado foi enviado'
        }, 400

    if 'nome' in dados:
        usuario.nome = dados['nome']

    if 'email' in dados:
        usuario.email = dados['email']

    if 'senha' in dados:
        usuario.senha = dados['senha']

    if 'tipo' in dados:
        usuario.tipo = dados['tipo']

    if 'primeiro_acesso' in dados:
        usuario.primeiro_acesso = dados['primeiro_acesso']

    db.session.commit()

    return {
        'mensagem': 'Usuário atualizado com sucesso'
    }


# ============================================================
# EXCLUIR USUÁRIO
# ============================================================

@usuarios_bp.route('/<int:id_usuario>', methods=['DELETE'])
def excluir_usuario(id_usuario):

    usuario = Usuario.query.get(id_usuario)

    if not usuario:
        return {
            'erro': 'Usuário não encontrado'
        }, 404

    db.session.delete(usuario)
    db.session.commit()

    return {
        'mensagem': 'Usuário excluído com sucesso'
    }