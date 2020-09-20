from flask_marshmallow import Marshmallow
from marshmallow import validates, pre_load, ValidationError
import re
from .model import Usuario, Ponto
from .util import validaData, validaEmail, validaCPF

ma = Marshmallow()

def configure(app):
	ma.init_app(app)
	
class UsuarioSchema(ma.SQLAlchemyAutoSchema):

	class Meta:
		model = Usuario
		include_relationships = True
		load_instance = True

	@pre_load
	def removeMascara(self, in_data, **kwargs):
		if in_data.get("cpf"):
			in_data["cpf"] = in_data["cpf"].replace("-", "").replace(".", "")
		return in_data

	@validates("nome") 
	def validatesNome(self, value):
		if not value:
			raise ValidationError("Nome obrigatório")
		return value
		
	@validates("email") 
	def validatesEmail(self, value):
		if not value:
			raise ValidationError("E-mail obrigatório")
		if not validaEmail(value):	
			raise ValidationError("E-mail inválido")
		if self.instance:
			if Usuario.query.filter(Usuario.email == value, Usuario.id != self.instance.id).count() > 0:
				raise ValidationError("E-mail já cadastrado no sistema")
		else:
			if Usuario.query.filter(Usuario.email == value).count() > 0:
				raise ValidationError("E-mail já cadastrado no sistema")
		return value
		
	@validates("cpf") 
	def validatesCPF(self, value):
		if not value:
			raise ValidationError("CPF obrigatório")
		if self.instance:
			if Usuario.query.filter(Usuario.cpf == value, Usuario.id != self.instance.id).count() > 0:
				raise ValidationError("CPF já cadastrado no sistema")
		else:
			if Usuario.query.filter(Usuario.cpf == value).count() > 0:
				raise ValidationError("CPF já cadastrado no sistema")
		if not validaCPF(value):
			raise ValidationError("CPF inválido")
		return value
		
	@validates("data_cadastro") 
	def validatesData(self, value):
		if not value:
			raise ValidationError("Data de Cadastro obrigatória")
		if not validaData(value):
			raise ValidationError("Data de Cadastro inválida")
		return value
	
class PontoSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = Ponto
		include_relationships = True
		include_fk = True
		load_instance = True
		
	@validates("usuario") 
	def validaUsuario(self, value):
		if not value:
			raise ValidationError("Usuário obrigatório")
		if Usuario.query.filter(Usuario.id == value).count() == 0:
			raise ValidationError("Usuário não existe no banco")
		return value