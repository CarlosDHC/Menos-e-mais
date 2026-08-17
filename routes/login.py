from flask import Blueprint, render_template, request, redirect, url_for, session
from models import Usuario


login_bp = Blueprint(
    'login',
    __name__
)


# ============================================================
# LOGIN
# ============================================================

@login_bp.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form.get('email')
        senha = request.form.get('senha')

        # Busca o usuário pelo e-mail
        usuario = Usuario.query.filter_by(
            email=email
        ).first()

        # Verifica se o usuário existe e se a senha corresponde
        if usuario and usuario.senha == senha:

            # Dados do usuário na sessão
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

            # Administrador
            elif usuario.tipo == 'admin':
                return redirect(
                    url_for('painel_admin_geral')
                )

            # Outros usuários, como aluno
            return redirect(
                url_for('missoes')
            )

        # Login inválido
        return render_template(
            'login.html',
            erro='Email ou senha incorretos'
        )

    return render_template('login.html')


# ============================================================
# LOGOUT
# ============================================================

@login_bp.route('/logout')
def logout():

    session.clear()

    return redirect(
        url_for('login.login')
    )