from flask import Blueprint, jsonify, request, current_app
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import func, text
from marshmallow import ValidationError
from app.model import Ponto, Usuario
from app.schema import PontoSchema, UsuarioSchema
from app.util import formataHora
from datetime import time

pontoBlueprint = Blueprint("ponto", __name__)

pontos_schema = PontoSchema(many = True)
ponto_schema = PontoSchema()
usuario_schema = UsuarioSchema()

@pontoBlueprint.route("/ponto/<int:id>/", methods=["GET"])
def pontoUsuario(id):
	try:
		usuario = Usuario.query.get(id)
		if not usuario:
			return jsonify({ "erro": "Usuário não existe no banco." }), 400
		pontos = Ponto.query.filter(Ponto.usuario == id)
		
		totalHoras = current_app.db.session.query(func.sum(func.timestampdiff(text("SECOND"), Ponto.data_entrada, Ponto.data_saida)).label("horasTrabalhadas")).filter(Ponto.usuario == id, Ponto.data_saida != None).group_by(Ponto.usuario)
		
		if totalHoras.count() == 0:
			totalTrabalhado = 0
		else:
			totalTrabalhado = totalHoras.first().horasTrabalhadas
		
		horasTrabalhadas = formataHora(totalTrabalhado)
		
		#horasTrabalhadas = Ponto.query.filter(Ponto.usuario == id, Ponto.data_saida != None).count()
		return jsonify(
			{ 
				"usuario": usuario_schema.dump(usuario),
				"pontos": pontos_schema.dump(pontos),
				"horasTrabalhadas": horasTrabalhadas
			}
		), 200
	except SQLAlchemyError as mensagem: 
		return jsonify({ "erro": str(mensagem) }), 400

@pontoBlueprint.route("/ponto", methods=["POST"])
def novoPonto():
	try:
		tipo = request.json.get("tipo", None)
		id_usuario = request.json.get("usuario", None)
		data = request.json.get("data", None)
		if not tipo:
			return jsonify({ "erro": "Tipo de Batida inválido (Deve ser [E]ntrada ou [S]aída)" }), 400
		if tipo.lower() == "e" or tipo.lower() == "entrada":
			usuario = Usuario.query.get(id_usuario)
			if not usuario:
				return jsonify({ "erro": "Usuário não existe no banco." }), 400
			ponto = Ponto.query.filter(Ponto.usuario == id_usuario, Ponto.data_saida == None)
			if ponto.count() == 0:
				ponto = ponto_schema.load({ "usuario": id_usuario, "data_entrada": data }, partial = ("data_saida",))
				current_app.db.session.add(ponto)
				current_app.db.session.commit()
			else:
				return jsonify({ "erro": "Usuário já possui uma entrada registrada. Registre uma saída antes de registrar uma nova entrada." }), 400
		elif tipo.lower() == "s" or tipo.lower() == "saida" or tipo.lower() == "saída":
			usuario = Usuario.query.get(id_usuario)
			if not usuario:
				return jsonify({ "erro": "Usuário não existe no banco." }), 400
			ponto = Ponto.query.filter(Ponto.usuario == id_usuario, Ponto.data_saida == None)
			if ponto.count() != 0:
				ponto = Ponto.query.filter(Ponto.usuario == id_usuario, Ponto.data_entrada < data, Ponto.data_saida == None)
				if ponto.count() != 0:
					ponto = ponto_schema.load({ "usuario": id_usuario, "data_saida": data }, instance = ponto.first(), partial = ("data_entrada",))
					current_app.db.session.add(ponto)
					current_app.db.session.commit()
				else:
					return jsonify({ "erro": "Usuário possui entrada registrada, porém a data de entrada é maior que a data de saída." }), 400
			else:
				return jsonify({ "erro": "Usuário não possui entrada registrada. Registre uma entrada antes de registrar uma nova saída." }), 400
		else:
			return jsonify({ "erro": "Tipo de Batida inválido (Deve ser [E]ntrada ou [S]aída)" }), 400
		return jsonify(ponto_schema.dump(ponto)), 200
	except ValidationError as err: 
		return jsonify({ "erro": str(err.messages) }), 400
	except SQLAlchemyError as mensagem: 
		return jsonify({ "erro": str(mensagem) }), 400