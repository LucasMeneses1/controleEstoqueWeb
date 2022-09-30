from Estoque import database, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuarios.query.get(int(id_usuario))

class Itens(database.Model):
    id_item = database.Column(database.Integer, primary_key=True)
    cod_item = database.Column(database.String, nullable=False)
    nome_item = database.Column(database.String, nullable=False)
    lote_item = database.Column(database.String, nullable=False)
    quantidade_item = database.Column(database.Integer, nullable=False)
    #reg_historico = database.relationship('Historico', backref='reg_item', lazy=True)

class Usuarios(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)

class Historico(database.Model):
    id_registro = database.Column(database.Integer, primary_key=True)
    data_edicao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    id_item = database.Column(database.Integer, nullable=False)
    usuario = database.Column(database.String, nullable=False)
    acao = database.Column(database.String, nullable=False)
    cod_item = database.Column(database.String, nullable=False)
    cod_item_ed = database.Column(database.String, nullable=False)
    nome_item = database.Column(database.String, nullable=False)
    nome_item_ed = database.Column(database.String, nullable=False)
    lote_item = database.Column(database.String, nullable=False)
    lote_item_ed = database.Column(database.String, nullable=False)
    quantidade_item = database.Column(database.Integer, nullable=False)
    quantidade_item_ed = database.Column(database.Integer, nullable=False)
    #fk_id_item = database.Column(database.Integer, database.ForeignKey('itens.id_item'), nullable=False)
