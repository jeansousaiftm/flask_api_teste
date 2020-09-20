from flask import Flask
from flask_migrate import Migrate
from .model import configure as configurarDB
from .schema import configure as configurarSchema

def create_app():

	app = Flask(__name__)
	
	app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost:3306/api_teste"
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	
	configurarDB(app)
	configurarSchema(app)
	
	Migrate(app, app.db)
	
	from app.blueprints.usuario import usuarioBlueprint
	app.register_blueprint(usuarioBlueprint)
	
	from app.blueprints.ponto import pontoBlueprint
	app.register_blueprint(pontoBlueprint)
	
	return app