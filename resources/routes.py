from .auth import SignupApi,LoginApi
from .statusForTest import StatusTest
from .plan import Plan_res
from .plan_alumno import PlanDeAlumno
from .programa_disponible import Programa
from .documentation import Documentacion
from .horario import HorarioRecomendado
from .horario_alumno import HorarioDeAlumno
def initialize_routes(api):
    api.add_resource(StatusTest,"/")
    api.add_resource(SignupApi,"/api/auth/signup")
    api.add_resource(LoginApi,"/api/auth/login")
    api.add_resource(Plan_res,"/api/plan" )
    api.add_resource(PlanDeAlumno,"/api/plan/<matricula>")
    api.add_resource(Programa,"/api/programa-disponible")
    api.add_resource(HorarioRecomendado,"/api/horario")
    api.add_resource(HorarioDeAlumno,"/api/horario/<matricula>")
    api.add_resource(Documentacion,"/api/docs")
