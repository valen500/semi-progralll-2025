from http.server import HTTPServer, BaseHTTPRequestHandler

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

HTTPServer(("localhost", 3000), Servidor).serve_forever()
