from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Motorista(db.Model):
    __tablename__ = 'motorista'
    id_motorista = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cnh = db.Column(db.String(20), unique=True, nullable=False)
    categoria_cnh = db.Column(db.String(5), nullable=False)
    telefone = db.Column(db.String(20))
    veiculos = db.relationship('Veiculo', backref='motorista', lazy=True)

class Veiculo(db.Model):
    __tablename__ = 'veiculo'
    id_veiculo = db.Column(db.Integer, primary_key=True)
    placa = db.Column(db.String(10), unique=True, nullable=False)
    modelo = db.Column(db.String(50), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    quilometragem = db.Column(db.Integer, nullable=False)
    id_motorista = db.Column(db.Integer, db.ForeignKey('motorista.id_motorista'))
    manutencoes = db.relationship('Manutencao', backref='veiculo', lazy=True)

class Mecanico(db.Model):
    __tablename__ = 'mecanico'
    id_mecanico = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    especialidade = db.Column(db.String(50), nullable=False)
    turno = db.Column(db.String(20), nullable=False)
    manutencoes = db.relationship('Manutencao', backref='mecanico', lazy=True)

class Peca(db.Model):
    __tablename__ = 'peca'
    id_peca = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    fabricante = db.Column(db.String(100))
    valor = db.Column(db.Float, nullable=False)
    qtd_estoque = db.Column(db.Integer, nullable=False, default=0)
    estoque_minimo = db.Column(db.Integer, default=5)

class Manutencao(db.Model):
    __tablename__ = 'manutencao'
    id_manutencao = db.Column(db.Integer, primary_key=True)
    data_manutencao = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    tipo = db.Column(db.String(20), nullable=False) # Preventiva ou Corretiva
    descricao = db.Column(db.Text)
    custo_total = db.Column(db.Float, default=0.0)
    id_veiculo = db.Column(db.Integer, db.ForeignKey('veiculo.id_veiculo'), nullable=False)
    id_mecanico = db.Column(db.Integer, db.ForeignKey('mecanico.id_mecanico'), nullable=False)
    itens = db.relationship('ItemManutencao', backref='manutencao', cascade="all, delete-orphan")

class ItemManutencao(db.Model):
    __tablename__ = 'item_manutencao'
    id_item = db.Column(db.Integer, primary_key=True)
    id_manutencao = db.Column(db.Integer, db.ForeignKey('manutencao.id_manutencao'), nullable=False)
    id_peca = db.Column(db.Integer, db.ForeignKey('peca.id_peca'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    valor_unitario = db.Column(db.Float, nullable=False)
    peca = db.relationship('Peca')