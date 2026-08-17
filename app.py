from flask import Flask, render_template, redirect, url_for, session
from dotenv import load_dotenv
from models import db
from sqlalchemy import text

from routes.usuarios import usuarios_bp
from routes.login import login_bp

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
# BLUEPRINTS
# ============================================================

app.register_blueprint(usuarios_bp)
app.register_blueprint(login_bp)


# ============================================================
# ROTAS PÚBLICAS
# ============================================================

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/sobre')
def sobre():
    return render_template('sobre.html')


@app.route('/contato')
def contato():
    return render_template('contato.html')


@app.route('/livros')
def livros():
    return render_template('livros.html')


# ============================================================
# ROTAS DE NAVEGAÇÃO INTERNA
# ============================================================

@app.route('/missoes')
def missoes():
    return render_template(
        'dash_usuario/missoes.html'
    )


@app.route('/conquistas')
def conquistas():
    return render_template(
        'dash_usuario/conquistas.html'
    )


@app.route('/perfis')
def perfis():
    return render_template('perfis.html')


@app.route('/quiz')
def quiz():
    return render_template('quiz.html')


# ============================================================
# PAINÉIS RESTRITOS
# ============================================================

@app.route('/simulado')
def simulado():

    if 'id_usuario' not in session:
        return redirect(
            url_for('login.login')
        )

    return "Página do Simulado"


@app.route('/professor/painel')
def painel_professor():

    if 'id_usuario' not in session:
        return redirect(
            url_for('login.login')
        )

    if session.get('role') != 'professor':
        return redirect(
            url_for('home')
        )

    return render_template(
        'dash_professor/painel.html'
    )


# ============================================================
# TURMAS DO PROFESSOR
# ============================================================

@app.route('/professor/turmas')
def professor_turmas():

    if 'id_usuario' not in session:
        return redirect(
            url_for('login.login')
        )

    if session.get('role') != 'professor':
        return redirect(
            url_for('home')
        )

    turmas = db.session.execute(
        text("""
            SELECT
                t.id_turma,
                t.nome AS turma,
                e.id_escola,
                e.nome AS escola
            FROM usuario_turma ut
            JOIN turma t
                ON t.id_turma = ut.id_turma
            JOIN escola e
                ON e.id_escola = t.id_escola
            WHERE ut.id_usuario = :id_usuario
        """),
        {
            'id_usuario': session['id_usuario']
        }
    ).mappings().all()

    return {
        'professor': session['nome_usuario'],
        'turmas': [
            dict(turma)
            for turma in turmas
        ]
    }


# ============================================================
# DIRETORIA
# ============================================================

@app.route('/diretoria/painel')
def painel_diretoria():

    if 'id_usuario' not in session:
        return redirect(
            url_for('login.login')
        )

    if session.get('role') not in ['diretor', 'gestor']:
        return redirect(
            url_for('home')
        )

    return "Página da Diretoria"


# ============================================================
# ADMIN
# ============================================================

@app.route('/admin/geral')
def painel_admin_geral():

    if 'id_usuario' not in session:
        return redirect(
            url_for('login.login')
        )

    if session.get('role') != 'admin':
        return redirect(
            url_for('home')
        )

    return render_template(
        'dash_admin/geral.html'
    )


# ============================================================
# INICIALIZAÇÃO
# ============================================================

if __name__ == '__main__':
    app.run(debug=True)