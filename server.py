from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib import parse

class Servidor(BaseHTTPRequestHandler):
    def do_GET(self):
        ruta = self.path if self.path != "/" else "/index.html"
        try:
            with open("." + ruta, "rb") as archivo:
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                self.wfile.write(archivo.read())
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 - No encontrado")

    def do_POST(self):
        longitud = int(self.headers['Content-Length'])
        datos = self.rfile.read(longitud).decode("utf-8")
        datos = parse.unquote(datos)

        print(f"Datos recibidos: {datos}")

        self.send_response(200)
        self.end_headers()
        self.wfile.write(datos.encode("utf-8"))

if __name__ == "__main__":
    puerto = 3000
    print(f"Servidor ejecutándose en el puerto {puerto}")
    HTTPServer(("localhost", puerto), Servidor).serve_forever()
