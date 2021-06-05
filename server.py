from flask import Flask
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from database.db import initialize_db
from database.models import Alumno
from resources.routes import initialize_routes
import os

server = Flask(__name__, static_folder="docs")
CORS(server)
enviroment_configuration=os.environ.get('CONFIGURATION_SETUP')
server.config.from_object(enviroment_configuration)
#print(server.config["JSON_AS_ASCII"])
print(enviroment_configuration)


api=Api(server)
bcrypt=Bcrypt(server)
jwt=JWTManager(server)

initialize_db(server)
initialize_routes(api)

#if __name__=="__main__":
 #   app.run(host='0.0.0.0',port=5000)
#{
  #"matricula":"201756568",
  #"mail":"mycorreo2@mail.com",
  #"name": "pepe pollo",
 # "password": "ajioajio"
#}

