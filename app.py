from flask import Flask, render_template, request, redirect, url_for, session
from dotenv import load_dotenv
from models import db, Usuario
import os


# Carrega as variáveis do arquivo .env
load_dotenv()


app = Flask(__name__)

app.secret_key = 'uma_chave_super_secreta_aqui'


# ============================================================
# BANCO DE DADOS
# ============================================================

app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+pymysql://menos_e_mais-user:{os.getenv('DB_PASSWORD')}"
    "@145.223.95.128:3306/MENOS_E_MAIS-DB"
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


# ============================================================
# ROTAS PÚBLICAS
# ============================================================

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/sobre')
def sobre():
    return "Página Sobre em construção"


@app.route('/contato')
def contato():
    return "Página de Contato em construção"


# ============================================================
# ROTAS DE NAVEGAÇÃO INTERNA
# ============================================================

@app.route('/missoes')
def missoes():
    return "Página de Missões em construção"


@app.route('/conquistas')
def conquistas():
    return "Página de Conquistas em construção"


@app.route('/perfis')
def perfis():
    return "Página de Perfis em construção"


# ============================================================
# AUTENTICAÇÃO E LOGIN
# ============================================================

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form.get('email')
        senha = request.form.get('senha')

        # Busca o usuário pelo e-mail
        usuario = Usuario.query.filter_by(
            email=email
        ).first()

        # Verifica se o usuário existe e se a senha
        # informada corresponde à cadastrada
        if usuario and usuario.senha == senha:

            session['id_usuario'] = usuario.id_usuario
            session['user_email'] = usuario.email
            session['nome_usuario'] = usuario.nome
            session['role'] = usuario.tipo
            session['primeiro_acesso'] = usuario.primeiro_acesso

            # Primeiro acesso
            if usuario.primeiro_acesso:
                return redirect(
                    url_for('simulado')
                )

            # Professor
            if usuario.tipo == 'professor':
                return redirect(
                    url_for('painel_professor')
                )

            # Diretoria
            elif usuario.tipo in ['diretor', 'gestor']:
                return redirect(
                    url_for('painel_diretoria')
                )

            # Outros usuários
            return redirect(
                url_for('home')
            )

        return render_template(
            'login.html',
            erro='Email ou senha incorretos'
        )

    return render_template('login.html')


# ============================================================
# PAINÉIS RESTRITOS
# ============================================================

@app.route('/simulado')
def simulado():

    if 'id_usuario' not in session:
        return redirect(
            url_for('login')
        )

    return "Página do Simulado"


@app.route('/professor/painel')
def painel_professor():

    if 'id_usuario' not in session:
        return redirect(
            url_for('login')
        )

    if session.get('role') != 'professor':
        return redirect(
            url_for('home')
        )

    return "Painel do Professor - acesso autorizado"


@app.route('/diretoria/painel')
def painel_diretoria():

    if 'id_usuario' not in session:
        return redirect(
            url_for('login')
        )

    if session.get('role') not in ['diretor', 'gestor']:
        return redirect(
            url_for('home')
        )

    return "Página da Diretoria"


# ============================================================
# LOGOUT
# ============================================================

@app.route('/logout')
def logout():

    session.clear()

    return redirect(
        url_for('login')
    )


# ============================================================
# INICIALIZAÇÃO
# ============================================================

if __name__ == '__main__':
    app.run(debug=True)