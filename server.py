from flask import Flask
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from database.db import initialize_db
from database.models import Alumno
from resources.routes import initialize_routes

server=Flask(__name__)
server.config.from_envvar("SUPER_SECRET_KEY")
api=Api(server)
bcrypt=Bcrypt(server)
jwt=JWTManager(server)

server.config["MONGODB_SETTINGS"]={
        "host":"mongodb+srv://servidor_social:elhuesodeduraznomelapelax4@schedulerbackend.lhw5y.mongodb.net/scheduler?retryWrites=true&w=majority"
        }

initialize_db(server)
initialize_routes(api)
server.run()
#{
  #"matricula":"201756568",
  #"mail":"mycorreo2@mail.com",
  #"name": "pepe pollo",
 # "password": "ajioajio"
#}

