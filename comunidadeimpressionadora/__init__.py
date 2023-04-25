# pip install flask-login
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
import sqlalchemy

# render_template -> renderiza o template
# url_for -> pega o link associado a funcão
# flash -> exibe mensagem de alerta
# redirect -> redireciona

# Ligação entre as páginas
app = Flask(__name__)

# Criando o token -> Terminal digita python -> import secrets -> secrets.token_hex(16) -> exit()
app.config['SECRET_KEY'] = 'd8ae853565951fa59d8508bd61078acc'
if os.getenv("DATABASE_URL"):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'alert-info'

from comunidadeimpressionadora import models
engine = sqlalchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
inspection = sqlalchemy.inspect(engine)
if not inspection.has_table("usuario"):
    with app.app_context():
        database.drop_all()
        database.create_all()
        print("Base de Dados criado")
else:
    print("Base de Dados já existente")

# Importando as rotas do site
from comunidadeimpressionadora import routes