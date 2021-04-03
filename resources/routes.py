from .auth import SignupApi,LoginApi
from .statusForTest import StatusTest
from .plan import Plan_r
from .documentation import Documentacion
def initialize_routes(api):
    api.add_resource(StatusTest,"/")
    api.add_resource(SignupApi,"/api/auth/signup")
    api.add_resource(LoginApi,"/api/auth/login")
    api.add_resource(Plan_r,"/api/plan" )
    api.add_resource(Documentacion,"/api/docs")
