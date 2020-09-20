from flask import Blueprint, jsonify, request, current_app
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
from app.model import Usuario
from app.schema import UsuarioSchema

usuarioBlueprint = Blueprint("usuario", __name__)

usuarios_schema = UsuarioSchema(many = True)
usuario_schema = UsuarioSchema()

@usuarioBlueprint.route("/usuario", methods=["GET"])
def todosUsuarios():
	try:
		usuarios = Usuario.query.all()
		return jsonify(usuarios_schema.dump(usuarios)), 200
	except SQLAlchemyError as mensagem: 
		return jsonify({ "erro": str(mensagem) }), 400

@usuarioBlueprint.route("/usuario", methods=["POST"])
def novoUsuario():
	try:
		usuario = usuario_schema.load(request.json)
		current_app.db.session.add(usuario)
		current_app.db.session.commit()
		return jsonify(usuario_schema.dump(usuario)), 200
	except ValidationError as err: 
		return jsonify({ "erro": str(err.messages) }), 400
	except SQLAlchemyError as mensagem: 
		return jsonify({ "erro": str(mensagem) }), 400
	
@usuarioBlueprint.route("/usuario/<int:id>/", methods=["GET"])
def obterUsuario(id):
	try:
		usuario = Usuario.query.get(id)
		return jsonify(usuario_schema.dump(usuario)), 200
	except SQLAlchemyError as mensagem: 
		return jsonify({ "erro": str(mensagem) }), 400

@usuarioBlueprint.route('/usuario/<int:id>/', methods=["PUT"])
def atualizarUsuario(id):
	try:
		usuario = Usuario.query.get(id)
		if not usuario:
			return jsonify({ "erro": "Usuário não existe no banco" }), 400
		usuario = usuario_schema.load(request.json, instance = usuario, partial = ("data_cadastro",))
		current_app.db.session.add(usuario)
		current_app.db.session.commit()
		return jsonify(usuario_schema.dump(usuario)), 200
	except ValidationError as err: 
		return jsonify({ "erro": str(err.messages) }), 400
	except SQLAlchemyError as mensagem: 
		return jsonify({ "erro": str(mensagem) }), 400