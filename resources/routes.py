from .auth import SignupApi,LoginApi
from .statusForTest import StatusTest
from .programas import * 
def initialize_routes(api):
    api.add_resource(StatusTest,"/")
    api.add_resource(SignupApi,"/api/auth/signup")
    api.add_resource(LoginApi,"/api/auth/login")
    #api.add_resource(ProgramaCompleto,"/api/programa/<carrera>" )
    api.add_resource(ProgramaBasico,"/api/prog-basico/<carrera>")
    api.add_resource(ProgramaFormativo,"/api/prog-formativo/<carrera>")
    api.add_resource(ProgramaOptativas,"/api/prog-optativas/<carrera>")
