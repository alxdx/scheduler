from .auth import SignupApi,LoginApi
from .statusForTest import StatusTest
from .programas import ProgramaCompleto 
def initialize_routes(api):
    api.add_resource(StatusTest,"/")
    api.add_resource(SignupApi,"/api/auth/signup")
    api.add_resource(LoginApi,"/api/auth/login")
    api.add_resource(ProgramaCompleto,"/api/programa/<carrera>" )
