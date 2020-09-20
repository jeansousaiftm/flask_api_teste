from app import create_app
import unittest

from mockito import when, mock, unstub

class TesteUnitario(unittest.TestCase):

	def setUp(self):
		self.app = create_app()
		self.app.testing = True
		self.app_context = self.app.test_request_context()
		self.app_context.push()
		self.client = self.app.test_client()
		#self.app.db.create_all()

	def tearDown(self):
		self.app.db.engine.execute("DELETE FROM ponto;")
		self.app.db.engine.execute("DELETE FROM usuario;")

	def testeCadastroUsuario(self):
		data1 = {
			"nome": "Jean Sousa",
			"email": "jeanlucasdesousa@gmail.com",
			"cpf": "03753398764",
			"data_cadastro": "2020-09-20"
		}

		response = self.app.test_client().post("/usuario", json = data1, content_type = "application/json")
		
		id_cadastrado = response.get_json().get("id")
		data1["id"] = id_cadastrado

		self.assertEqual(response.get_json(), data1)
		
		response = self.app.test_client().get("/usuario/" + str(id_cadastrado) + "/", content_type = "application/json")
		
		self.assertEqual(response.get_json(), data1)
		
		response = self.app.test_client().get("/usuario", content_type = "application/json")
		
		self.assertEqual(response.get_json(), [ data1 ])
		
	def testeCadastroUsuarioCPFRepetido(self):
		data1 = {
			"nome": "Fulano de Tal",
			"email": "teste@teste.com.br",
			"cpf": "03753398764",
			"data_cadastro": "2020-09-20"
		}

		response = self.app.test_client().post("/usuario", json = data1, content_type = "application/json")
	
		self.assertEqual(response.get_json(), { 'erro': "{'cpf': ['CPF já cadastrado no sistema']}"} )
		
	def testeCadastroUsuarioCPFInvalido(self):
		data1 = {
			"nome": "Fulano de Tal",
			"email": "teste@teste.com.br",
			"cpf": "03753398763",
			"data_cadastro": "2020-09-20"
		}

		response = self.app.test_client().post("/usuario", json = data1, content_type = "application/json")

		self.assertEqual(response.get_json(), { 'erro': "{'cpf': ['CPF inválido']}"} )
		
	def testeCadastroUsuarioEmailRepetido(self):
		data1 = {
			"nome": "Fulano de Tal",
			"email": "jeanlucasdesousa@gmail.com",
			"cpf": "52402867442",
			"data_cadastro": "2020-09-20"
		}

		response = self.app.test_client().post("/usuario", json = data1, content_type = "application/json")
	
		self.assertEqual(response.get_json(), { 'erro': "{'email': ['E-mail já cadastrado no sistema']}"} )
		
	def testeCadastroUsuarioEmailInvalido(self):
		data1 = {
			"nome": "Fulano de Tal",
			"email": "jeanlucasdesousa",
			"cpf": "45871251803",
			"data_cadastro": "2020-09-20"
		}

		response = self.app.test_client().post("/usuario", json = data1, content_type = "application/json")
	
		self.assertEqual(response.get_json(), { 'erro': "{'email': ['E-mail inválido']}"} )
		
	def testeCadastroUsuarioDadosVazios(self):
		data1 = {
			"email": "fulano@gmail.com",
			"cpf": "52402867442",
			"data_cadastro": "2020-09-20"
		}

		response = self.app.test_client().post("/usuario", json = data1, content_type = "application/json")

		self.assertEqual(response.get_json(), {'erro': "{'nome': ['Missing data for required field.']}"} )
	
	def testeAtualizaUsuario(self):
		data1 = {
			"nome": "Jean Sousa",
			"email": "email_novo@gmail.com",
			"cpf": "95480472682",
			"data_cadastro": "2020-09-20"
		}

		response = self.app.test_client().post("/usuario", json = data1, content_type = "application/json")
		
		id_cadastrado = response.get_json().get("id")
		data1["id"] = id_cadastrado

		self.assertEqual(response.get_json(), data1)
		
		data2 = {
			"nome": "Novo Nome",
			"email": "email_novo@gmail.com",
			"cpf": "95480472682"
		}

		response = self.app.test_client().put("/usuario/" + str(id_cadastrado) + "/", json = data2, content_type = "application/json")

		data2["id"] = id_cadastrado
		data2["data_cadastro"] = data1["data_cadastro"]

		self.assertEqual(response.get_json(), data2)
	
	def testeInsereBatida(self):
		data1 = {
			"nome": "Jean Sousa",
			"email": "email_novo222@gmail.com",
			"cpf": "28520768105",
			"data_cadastro": "2020-09-20"
		}
		
		response = self.app.test_client().post("/usuario", json = data1, content_type = "application/json")
		
		id_cadastrado = response.get_json().get("id")
		data1["id"] = id_cadastrado

		self.assertEqual(response.get_json(), data1)
		
		data2 = {
			"usuario": id_cadastrado,
			"tipo": "entrada",
			"data": "2020-09-09 08:00:00"
		}
		
		response = self.app.test_client().post("/ponto", json = data2, content_type = "application/json")
		
		data2_ret = {
			"id": response.get_json().get("id"),
			"usuario": id_cadastrado,
			"data_entrada": "2020-09-09T08:00:00",
			"data_saida": response.get_json().get("data_saida")
		}		
		self.assertEqual(response.get_json(), data2_ret)
		
		data3 = {
			"usuario": id_cadastrado,
			"tipo": "saida",
			"data": "2020-09-09 12:00:00"
		}
		
		response = self.app.test_client().post("/ponto", json = data3, content_type = "application/json")
		
		data3_ret = {
			"id": response.get_json().get("id"),
			"usuario": id_cadastrado,
			"data_entrada": response.get_json().get("data_entrada"),
			"data_saida": "2020-09-09T12:00:00"
		}	
		
		self.assertEqual(response.get_json(), data3_ret)
		
		response = self.app.test_client().get("/ponto/" + str(id_cadastrado) + "/", content_type = "application/json")
		
		self.assertEqual(response.get_json().get("horasTrabalhadas"), "4:00:00")
		
	def testeInsereBatidaRepetida(self):
		data1 = {
			"nome": "Jean Sousa 2",
			"email": "email_novo222333@gmail.com",
			"cpf": "84333423392",
			"data_cadastro": "2020-09-20"
		}
		
		response = self.app.test_client().post("/usuario", json = data1, content_type = "application/json")
		
		id_cadastrado = response.get_json().get("id")
		data1["id"] = id_cadastrado

		self.assertEqual(response.get_json(), data1)
		
		data2 = {
			"usuario": id_cadastrado,
			"tipo": "entrada",
			"data": "2020-09-09 08:00:00"
		}
		
		response = self.app.test_client().post("/ponto", json = data2, content_type = "application/json")
		
		data2_ret = {
			"id": response.get_json().get("id"),
			"usuario": id_cadastrado,
			"data_entrada": "2020-09-09T08:00:00",
			"data_saida": response.get_json().get("data_saida")
		}		
		self.assertEqual(response.get_json(), data2_ret)
		
		data3 = {
			"usuario": id_cadastrado,
			"tipo": "entrada",
			"data": "2020-09-09 12:00:00"
		}
		
		response = self.app.test_client().post("/ponto", json = data3, content_type = "application/json")
	

		self.assertEqual(response.get_json(), {"erro": "Usuário já possui uma entrada registrada. Registre uma saída antes de registrar uma nova entrada."})
		
		response = self.app.test_client().get("/ponto/" + str(id_cadastrado) + "/", content_type = "application/json")
		
		self.assertEqual(response.get_json().get("horasTrabalhadas"), "0:00:00")
	
	
	def testeInsereBatidaDataErrada(self):
		data1 = {
			"nome": "Jean Sousa",
			"email": "email_novo222333444@gmail.com",
			"cpf": "16671720266",
			"data_cadastro": "2020-09-20"
		}
		
		response = self.app.test_client().post("/usuario", json = data1, content_type = "application/json")
		
		id_cadastrado = response.get_json().get("id")
		data1["id"] = id_cadastrado

		self.assertEqual(response.get_json(), data1)
		
		data2 = {
			"usuario": id_cadastrado,
			"tipo": "entrada",
			"data": "2020-09-09 08:00:00"
		}
		
		response = self.app.test_client().post("/ponto", json = data2, content_type = "application/json")
		
		data2_ret = {
			"id": response.get_json().get("id"),
			"usuario": id_cadastrado,
			"data_entrada": "2020-09-09T08:00:00",
			"data_saida": response.get_json().get("data_saida")
		}		
		self.assertEqual(response.get_json(), data2_ret)
		
		data3 = {
			"usuario": id_cadastrado,
			"tipo": "saida",
			"data": "2020-09-09 07:00:00"
		}
		
		response = self.app.test_client().post("/ponto", json = data3, content_type = "application/json")

		self.assertEqual(response.get_json(), {"erro": "Usuário possui entrada registrada, porém a data de entrada é maior que a data de saída."})
		
		response = self.app.test_client().get("/ponto/" + str(id_cadastrado) + "/", content_type = "application/json")
		
		self.assertEqual(response.get_json().get("horasTrabalhadas"), "0:00:00")
		
	def testeInsereBatidaUsuarioInexistente(self):	
		data2 = {
			"usuario": 0,
			"tipo": "entrada",
			"data": "2020-09-09 08:00:00"
		}
		
		response = self.app.test_client().post("/ponto", json = data2, content_type = "application/json")
		
		self.assertEqual(response.get_json(), {"erro": "Usuário não existe no banco."})
		
if __name__ == '__main__':
    unittest.main()