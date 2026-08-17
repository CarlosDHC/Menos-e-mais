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
    return render_template('sobre.html') # Já atualizado para usar template!

@app.route('/contato')
def contato():
    return render_template('contato.html') # Já atualizado para usar template!

@app.route('/livros')
def livros():
     return render_template('livros.html') # Rota nova que não tinha antes!

# ============================================================
# ROTAS DE NAVEGAÇÃO INTERNA
# ============================================================
@app.route('/missoes')
def missoes():
    return render_template('dash_usuario/missoes.html') # Já aponta para a subpasta

@app.route('/conquistas')
def conquistas():
    return render_template('dash_usuario/conquistas.html') # Já aponta para a subpasta

@app.route('/perfis')
def perfis():
    return render_template('perfis.html') # Rota nova

@app.route('/quiz')
def quiz():
     return render_template('quiz.html') # Rota nova

# ============================================================
# AUTENTICAÇÃO E LOGIN
# ============================================================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        # Busca o usuário pelo e-mail
        usuario = Usuario.query.filter_by(email=email).first()
        
        # Verifica se o usuário existe e se a senha corresponde
        if usuario and usuario.senha == senha:
            session['id_usuario'] = usuario.id_usuario
            session['user_email'] = usuario.email
            session['nome_usuario'] = usuario.nome
            session['role'] = usuario.tipo
            session['primeiro_acesso'] = usuario.primeiro_acesso
            
            # Primeiro acesso
            if usuario.primeiro_acesso:
                return redirect(url_for('simulado'))
            
            # Redirecionamento por tipo de usuário (Role)
            if usuario.tipo == 'professor':
                return redirect(url_for('painel_professor'))
            
            elif usuario.tipo in ['diretor', 'gestor']:
                return redirect(url_for('painel_diretoria'))
            
            elif usuario.tipo == 'admin':
                 return redirect(url_for('painel_admin_geral'))
            
            # Outros usuários (aluno, etc)
            return redirect(url_for('missoes')) # Modificado: aluno logado vai para missões, não home
        
        return render_template('login.html', erro='Email ou senha incorretos')
    
    return render_template('login.html')

# ============================================================
# PAINÉIS RESTRITOS
# ============================================================
@app.route('/simulado')
def simulado():
    if 'id_usuario' not in session:
        return redirect(url_for('login'))
    return "Página do Simulado"

@app.route('/professor/painel')
def painel_professor():
    if 'id_usuario' not in session:
        return redirect(url_for('login'))
    if session.get('role') != 'professor':
        return redirect(url_for('home'))
    # Apontando para a possível subpasta que você criar para o professor
    return render_template('dash_professor/painel.html') 

@app.route('/diretoria/painel')
def painel_diretoria():
    if 'id_usuario' not in session:
        return redirect(url_for('login'))
    if session.get('role') not in ['diretor', 'gestor']:
        return redirect(url_for('home'))
    return "Página da Diretoria"

@app.route('/admin/geral')
def painel_admin_geral():
    if 'id_usuario' not in session:
        return redirect(url_for('login'))
    if session.get('role') != 'admin':
         return redirect(url_for('home'))
    return render_template('dash_admin/geral.html')


# ============================================================
# LOGOUT
# ============================================================
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ============================================================
# INICIALIZAÇÃO
# ============================================================
if __name__ == '__main__':
    app.run(debug=True)