from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()


# ============================================================
# TABELA INTERMEDIÁRIA: USUARIO <-> TURMA
# ============================================================

usuario_turma = db.Table(
    "usuario_turma",

    db.Column(
        "id_usuario",
        db.Integer,
        db.ForeignKey(
            "usuario.id_usuario",
            ondelete="CASCADE"
        ),
        primary_key=True
    ),

    db.Column(
        "id_turma",
        db.Integer,
        db.ForeignKey(
            "turma.id_turma",
            ondelete="CASCADE"
        ),
        primary_key=True
    )
)


# ============================================================
# USUÁRIO
# ============================================================

class Usuario(db.Model):

    __tablename__ = "usuario"

    id_usuario = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    nome = db.Column(
        db.String(150),
        nullable=False
    )

    email = db.Column(
        db.String(150),
        unique=True,
        nullable=False
    )

    senha = db.Column(
        db.String(255),
        nullable=False
    )

    tipo = db.Column(
        db.Enum(
            "aluno",
            "professor",
            "coordenador",
            "diretor",
            "gestor",
            "equipe_limpeza",
            "equipe_cozinha",
            "admin"
        ),
        nullable=False
    )

    data_criacao = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.current_timestamp()
    )

    primeiro_acesso = db.Column(
        db.Boolean,
        default=True
    )

    # Relacionamento com turmas
    turmas = db.relationship(
        "Turma",
        secondary=usuario_turma,
        back_populates="usuarios"
    )

    # Relacionamentos
    respostas = db.relationship(
        "Resposta",
        back_populates="usuario",
        cascade="all, delete-orphan"
    )

    diagnosticos = db.relationship(
        "Diagnostico",
        back_populates="usuario",
        cascade="all, delete-orphan"
    )

    pontuacoes = db.relationship(
        "Pontuacao",
        back_populates="usuario",
        cascade="all, delete-orphan"
    )

    planos_acao = db.relationship(
        "PlanoAcao",
        back_populates="usuario",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Usuario {self.nome} - {self.tipo}>"


# ============================================================
# ESCOLA
# ============================================================

class Escola(db.Model):

    __tablename__ = "escola"

    id_escola = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    nome = db.Column(
        db.String(150),
        nullable=False
    )

    cidade = db.Column(
        db.String(100),
        nullable=False
    )

    estado = db.Column(
        db.String(50),
        nullable=False
    )

    # Relacionamentos
    turmas = db.relationship(
        "Turma",
        back_populates="escola",
        cascade="all, delete-orphan"
    )

    relatorios = db.relationship(
        "Relatorio",
        back_populates="escola",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Escola {self.nome}>"


# ============================================================
# TURMA
# ============================================================

class Turma(db.Model):

    __tablename__ = "turma"

    id_turma = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    nome = db.Column(
        db.String(100),
        nullable=False
    )

    id_escola = db.Column(
        db.Integer,
        db.ForeignKey(
            "escola.id_escola",
            ondelete="CASCADE",
            onupdate="CASCADE"
        ),
        nullable=False
    )

    # Relacionamento com escola
    escola = db.relationship(
        "Escola",
        back_populates="turmas"
    )

    # Relacionamento com usuários
    usuarios = db.relationship(
        "Usuario",
        secondary=usuario_turma,
        back_populates="turmas"
    )

    def __repr__(self):
        return f"<Turma {self.nome}>"


# ============================================================
# QUESTIONÁRIO
# ============================================================

class Questionario(db.Model):

    __tablename__ = "questionario"

    id_questionario = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    titulo = db.Column(
        db.String(150),
        nullable=False
    )

    descricao = db.Column(
        db.Text
    )

    publico_alvo = db.Column(
        db.String(100)
    )

    data_criacao = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.current_timestamp()
    )

    # Relacionamento com perguntas
    perguntas = db.relationship(
        "Pergunta",
        back_populates="questionario",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Questionario {self.titulo}>"


# ============================================================
# PERGUNTA
# ============================================================

class Pergunta(db.Model):

    __tablename__ = "pergunta"

    id_pergunta = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    texto = db.Column(
        db.Text,
        nullable=False
    )

    tipo = db.Column(
        db.String(50),
        nullable=False
    )

    id_questionario = db.Column(
        db.Integer,
        db.ForeignKey(
            "questionario.id_questionario",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    # Relacionamento com questionário
    questionario = db.relationship(
        "Questionario",
        back_populates="perguntas"
    )

    # Relacionamento com respostas
    respostas = db.relationship(
        "Resposta",
        back_populates="pergunta",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Pergunta {self.id_pergunta}>"


# ============================================================
# RESPOSTA
# ============================================================

class Resposta(db.Model):

    __tablename__ = "resposta"

    id_resposta = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    id_usuario = db.Column(
        db.Integer,
        db.ForeignKey(
            "usuario.id_usuario",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    id_pergunta = db.Column(
        db.Integer,
        db.ForeignKey(
            "pergunta.id_pergunta",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    resposta = db.Column(
        db.Text
    )

    pontuacao = db.Column(
        db.Integer
    )

    data_resposta = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.current_timestamp()
    )

    # Relacionamentos
    usuario = db.relationship(
        "Usuario",
        back_populates="respostas"
    )

    pergunta = db.relationship(
        "Pergunta",
        back_populates="respostas"
    )

    def __repr__(self):
        return f"<Resposta {self.id_resposta}>"


# ============================================================
# DIAGNÓSTICO
# ============================================================

class Diagnostico(db.Model):

    __tablename__ = "diagnostico"

    id_diagnostico = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    id_usuario = db.Column(
        db.Integer,
        db.ForeignKey(
            "usuario.id_usuario",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    nivel = db.Column(
        db.Integer
    )

    pontuacao_total = db.Column(
        db.Integer
    )

    data = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.current_timestamp()
    )

    # Relacionamentos
    usuario = db.relationship(
        "Usuario",
        back_populates="diagnosticos"
    )

    devolutivas = db.relationship(
        "Devolutiva",
        back_populates="diagnostico",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Diagnostico {self.id_diagnostico} - Nível {self.nivel}>"


# ============================================================
# PONTUAÇÃO
# ============================================================

class Pontuacao(db.Model):

    __tablename__ = "pontuacao"

    id_pontuacao = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    id_usuario = db.Column(
        db.Integer,
        db.ForeignKey(
            "usuario.id_usuario",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    pontos = db.Column(
        db.Integer,
        nullable=False
    )

    origem = db.Column(
        db.String(100)
    )

    data = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.current_timestamp()
    )

    # Relacionamento
    usuario = db.relationship(
        "Usuario",
        back_populates="pontuacoes"
    )

    def __repr__(self):
        return f"<Pontuacao {self.pontos} - {self.origem}>"


# ============================================================
# PLANO DE AÇÃO
# ============================================================

class PlanoAcao(db.Model):

    __tablename__ = "plano_acao"

    id_plano = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    id_usuario = db.Column(
        db.Integer,
        db.ForeignKey(
            "usuario.id_usuario",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    titulo = db.Column(
        db.String(150)
    )

    descricao = db.Column(
        db.Text
    )

    nivel_relacionado = db.Column(
        db.Integer
    )

    prioridade = db.Column(
        db.String(50)
    )

    data_criacao = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.current_timestamp()
    )

    # Relacionamentos
    usuario = db.relationship(
        "Usuario",
        back_populates="planos_acao"
    )

    metas = db.relationship(
        "Meta",
        back_populates="plano",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<PlanoAcao {self.titulo}>"


# ============================================================
# META
# ============================================================

class Meta(db.Model):

    __tablename__ = "meta"

    id_meta = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    id_plano = db.Column(
        db.Integer,
        db.ForeignKey(
            "plano_acao.id_plano",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    titulo = db.Column(
        db.String(150)
    )

    descricao = db.Column(
        db.Text
    )

    status = db.Column(
        db.Enum(
            "pendente",
            "em_andamento",
            "concluida"
        ),
        default="pendente"
    )

    progresso = db.Column(
        db.Integer,
        default=0
    )

    data_inicio = db.Column(
        db.Date
    )

    data_fim = db.Column(
        db.Date
    )

    # Relacionamento
    plano = db.relationship(
        "PlanoAcao",
        back_populates="metas"
    )

    def __repr__(self):
        return f"<Meta {self.titulo} - {self.status}>"


# ============================================================
# DEVOLUTIVA
# ============================================================

class Devolutiva(db.Model):

    __tablename__ = "devolutiva"

    id_devolutiva = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    id_diagnostico = db.Column(
        db.Integer,
        db.ForeignKey(
            "diagnostico.id_diagnostico",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    descricao = db.Column(
        db.Text
    )

    pilar = db.Column(
        db.String(50)
    )

    data = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.current_timestamp()
    )

    # Relacionamento
    diagnostico = db.relationship(
        "Diagnostico",
        back_populates="devolutivas"
    )

    def __repr__(self):
        return f"<Devolutiva {self.id_devolutiva}>"


# ============================================================
# RELATÓRIO
# ============================================================

class Relatorio(db.Model):

    __tablename__ = "relatorio"

    id_relatorio = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    id_escola = db.Column(
        db.Integer,
        db.ForeignKey(
            "escola.id_escola",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    descricao = db.Column(
        db.Text
    )

    periodo_inicio = db.Column(
        db.Date
    )

    periodo_fim = db.Column(
        db.Date
    )

    data_geracao = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.current_timestamp()
    )

    # Relacionamento
    escola = db.relationship(
        "Escola",
        back_populates="relatorios"
    )

    def __repr__(self):
        return f"<Relatorio {self.id_relatorio}>"