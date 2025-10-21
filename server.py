from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib import parse
import json
import crud_usuario
import crud_alumno
import crud_academico
import os

port = 3000

crudUsuario = crud_usuario.crud_usuario()
crudAlumno = crud_alumno.crud_alumno()
db = crud_academico.crud()


class miServidor(SimpleHTTPRequestHandler):
    def do_GET(self):
        """Maneja peticiones GET para servir archivos estáticos"""
        if self.path in ["/", "/login"]:
            self.path = "login.html"
        elif self.path == "/index":
            self.path = "index.html"
        return SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        """Maneja peticiones POST (login, CRUDs, etc.)"""
       
        if self.path != "/api":
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Ruta no encontrada")
            return

       
        longitud = int(self.headers.get('Content-Length', 0))
        datos = self.rfile.read(longitud).decode("utf-8")

      
        try:
            datos_json = json.loads(datos)
        except Exception:
            try:
                parsed = parse.parse_qs(datos)
                if 'data' in parsed:
                    datos_json = json.loads(parsed['data'][0])
                else:
                    datos_json = {k: v[0] for k, v in parsed.items()}
            except Exception as e:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({
                    "ok": False,
                    "msg": "JSON inválido",
                    "error": str(e)
                }).encode("utf-8"))
                return

        print("📩 Datos recibidos:", datos_json)  

        accion = datos_json.get("accion", "").lower()

       
        if accion == "login":
            sql = "SELECT * FROM usuarios WHERE usuario=%s AND clave=%s"
            valores = (datos_json.get("usuario"), datos_json.get("clave"))
            cursor = db.conexion.cursor(dictionary=True)
            cursor.execute(sql, valores)
            usuario = cursor.fetchone()
            resp = {"ok": True, "msg": "ok"} if usuario else {"ok": False, "msg": "error"}

        
        elif accion.startswith("alumno"):
            resultado = crudAlumno.administrar(datos_json)
            resp = resultado if isinstance(resultado, dict) else {"ok": True, "msg": resultado}

      
        elif accion.startswith("usuario"):
            resultado = crudUsuario.administrar(datos_json)
            resp = resultado if isinstance(resultado, dict) else {"ok": True, "msg": resultado}

        else:
            resp = {"ok": False, "msg": "Acción no reconocida"}

        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(resp).encode("utf-8"))

    def do_OPTIONS(self):
        """Permitir preflight de CORS"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()


if __name__ == "__main__":
    
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print(f"Servidor ejecutándose en http://localhost:{port}")
    server = HTTPServer(("localhost", port), miServidor)
    server.serve_forever()
