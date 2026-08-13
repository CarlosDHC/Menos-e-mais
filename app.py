from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'uma_chave_super_secreta_aqui'

# ================= ROTAS PÚBLICAS ================= #

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/sobre')
def sobre():
    return "Página Sobre em construção"

@app.route('/contato')
def contato():
    return "Página de Contato em construção"


# ================= ROTAS DE NAVEGAÇÃO INTERNA ================= #

@app.route('/missoes')
def missoes():
    return "Página de Missões em construção"

@app.route('/conquistas')
def conquistas():
    return "Página de Conquistas em construção"

@app.route('/perfis')
def perfis():
    return "Página de Perfis em construção"


# ================= AUTENTICAÇÃO E LOGIN ================= #

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        sucesso_no_login = True 
        
        if sucesso_no_login:
            session['token'] = "token_recebido_do_backend"
            session['user_email'] = email
            
            is_first_login = False 
            role = 'professor' 
            session['role'] = role

            if is_first_login:
                return redirect(url_for('simulado'))
            else:
                if role == 'professor':
                    return redirect(url_for('painel_professor'))
                elif role == 'diretoria':
                    return redirect(url_for('painel_diretoria'))
        else:
            return render_template('login.html', erro="Email ou senha incorretos")

    return render_template('login.html')


# ================= PAINÉIS RESTRITOS ================= #

@app.route('/simulado')
def simulado():
    return "Página do Simulado"

@app.route('/professor/painel')
def painel_professor():
    return render_template('dash_professor/painel.html')


# ================= INICIALIZAÇÃO ================= #

if __name__ == '__main__':
    app.run(debug=True)