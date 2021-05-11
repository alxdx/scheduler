from flask_restful import Resource

class Programa(Resource):
    def get(self):
        payload={
                "carrera": "ICC",
                "nivel": "todos",
                "materias": [
                    {
                        "asignatura": "DHPC"
                    },
                    {
                    "asignatura": "Matemáticas"
                    }
                    ]
        }
        return payload
