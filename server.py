from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib import parse

class Servidor(BaseHTTPRequestHandler):
    def do_GET(self):
        ruta = self.path if self.path != "/" else "/index.html"
        try:
            with open("." + ruta, "rb") as f:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(f.read())
        except:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 - No encontrado")

    def do_POST(self):
        longitud = int(self.headers['Content-Length'])
        datos = self.rfile.read(longitud)
        datos = datos.decode("utf-8")
        datos = parse.unquote(datos)

        self.send_response(200)
        self.end_headers()
        self.wfile.write(datos.encode("utf-8"))

print("Servidor ejecutándose en el puerto 3000")
HTTPServer(("localhost", 3000), Servidor).serve_forever()
