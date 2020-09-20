from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import validates

db = SQLAlchemy()

def configure(app):
	db.init_app(app)
	app.db = db
	
class Usuario(db.Model):
	__tablename__ = "usuario"
	id = db.Column(db.Integer, primary_key = True, nullable = False)
	nome = db.Column(db.String(200), nullable = False)
	email = db.Column(db.String(100), nullable = False, unique = True)
	cpf = db.Column(db.String(20), nullable = False, unique = True)
	data_cadastro = db.Column(db.Date, nullable = False)

class Ponto(db.Model):
	__tablename__ = "ponto"
	id = db.Column(db.Integer, primary_key = True, nullable = False)
	usuario = db.Column(db.Integer, ForeignKey("usuario.id"), nullable = False)
	data_entrada = db.Column(db.DateTime, nullable = False)
	data_saida = db.Column(db.DateTime, nullable = True)