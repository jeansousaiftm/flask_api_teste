# Test

API de teste usando as bibliotecas Flask, SQLAlchemy, Marshmallow, Alembic e Mockito.

## Use

Após configurar a URL de conexão em app/__init.py__, realize os seguintes comandos:

```bash
set FLASK_APP=app
flask db init
flask db migrate
flask db upgrade
flask run
```

## Endpoints da API

### Inserir um Usuário [POST]
URL: /usuario
Funcionalidade: Permite inserir um usuário. 
Requisição de entrada:
	Content-Type: JSON
	Passar parâmetros na Body
		+ nome (string) - Nome Completo
		+ cpf (string) - CPF
		+ email (string) - E-mail
		+ data_cadastro (date) - Data de Cadastro
Retorno: JSON, 200

### Atualizar um Usuário [PUT]
URL: /usuario/<id>/
Funcionalidade: Permite atualizar um usuário com o id fornecido.
Requisição de entrada:
	Content-Type: JSON
	Passar parâmetros na Body
		+ nome (string) - Nome Completo
		+ cpf (string) - CPF
		+ email (string) - E-mail
Retorno: JSON, 200

### Listar um Usuário [GET]
URL: /usuario/<id>/
Funcionalidade: Permite retornar um usuário com o id fornecido.
Retorno: JSON, 200

### Listar todos os Usuários [GET]
URL: /usuario
Funcionalidade: Permite retornar todos os usuários registrados.
Retorno: JSON, 200

### Inserir uma Batida de ponto [POST]
URL: /ponto
Funcionalidade: Permite inserir uma batida de ponto. 
Requisição de entrada:
	Content-Type: JSON
	Passar parâmetros na Body
		+ usuario (int) - Id de Usuário
		+ data (datetime) - Data da Batida
		+ tipo (string) - Tipo de Batida (Entrada ou Saída)
Retorno: JSON, 200

### Listar todos os Pontos de um usuário [GET]
URL: /ponto/<usuario>/
Funcionalidade: Permite retornar todas as batidas de ponto de um usuário registrado.
Retorno: JSON, 200