# crud_usuario.py
import hashlib
import crud_academico

db = crud_academico.crud()

def hash_pass(clave_plain):
    if clave_plain is None:
        return None
    # SHA-256 hex
    return hashlib.sha256(clave_plain.encode('utf-8')).hexdigest()

class crud_usuario:
    def listar(self, buscar=''):
        # devuelve lista de usuarios (sin clave)
        if buscar:
            sql = "SELECT idUsuario, usuario, nombre, direccion, telefono FROM usuarios WHERE usuario LIKE %s OR nombre LIKE %s"
            patron = f"%{buscar}%"
            return db.consultar("SELECT idUsuario, usuario, nombre, direccion, telefono FROM usuarios WHERE usuario LIKE '%" + buscar + "%' OR nombre LIKE '%" + buscar + "%'")
        else:
            return db.consultar("SELECT idUsuario, usuario, nombre, direccion, telefono FROM usuarios")

    def obtener(self, idUsuario):
        return db.consultar("SELECT idUsuario, usuario, nombre, direccion, telefono FROM usuarios WHERE idUsuario = " + str(int(idUsuario)))

    def administrar(self, datos):
        accion = datos.get('accion')

        if accion == "nuevo":
            # insertar nuevo usuario (guarda hash)
            sql = """
                INSERT INTO usuarios (usuario, clave, nombre, direccion, telefono)
                VALUES (%s, %s, %s, %s, %s)
            """
            hashed = hash_pass(datos.get('clave',''))
            valores = (datos.get('usuario'), hashed, datos.get('nombre',''), datos.get('direccion',''), datos.get('telefono',''))
            return db.ejecutar(sql, valores)

        if accion == "modificar":
            # si llega clave y no está vacía, la actualizamos; si no, no cambiamos clave
            idUser = int(datos.get('idUsuario'))
            if datos.get('clave'):
                sql = """
                    UPDATE usuarios SET usuario=%s, clave=%s, nombre=%s, direccion=%s, telefono=%s
                    WHERE idUsuario=%s
                """
                hashed = hash_pass(datos.get('clave'))
                valores = (datos.get('usuario'), hashed, datos.get('nombre',''), datos.get('direccion',''), datos.get('telefono',''), idUser)
            else:
                sql = """
                    UPDATE usuarios SET usuario=%s, nombre=%s, direccion=%s, telefono=%s
                    WHERE idUsuario=%s
                """
                valores = (datos.get('usuario'), datos.get('nombre',''), datos.get('direccion',''), datos.get('telefono',''), idUser)
            return db.ejecutar(sql, valores)

        if accion == "eliminar":
            sql = "DELETE FROM usuarios WHERE idUsuario=%s"
            valores = (datos.get('idUsuario'),)
            return db.ejecutar(sql, valores)

        if accion == "login":
            # buscar usuario y comparar hash
            usuario = datos.get('usuario','')
            clave = datos.get('clave','')
            if usuario == '' or clave == '':
                return {"ok": False, "msg": "Usuario y clave requeridos"}
            # consulta
            rows = db.consultar("SELECT idUsuario, usuario, clave, nombre FROM usuarios WHERE usuario = '" + usuario + "'")
            if not rows:
                return {"ok": False, "msg": "Usuario no registrado"}
            stored = rows[0]
            hashed_input = hash_pass(clave)
            if stored.get('clave') == hashed_input:
                # login exitoso -> devolver info básica
                return {"ok": True, "msg": "Login correcto", "usuario": {"idUsuario": stored.get('idUsuario'), "usuario": stored.get('usuario'), "nombre": stored.get('nombre')}}
            else:
                return {"ok": False, "msg": "Clave incorrecta"}

        if accion == "listar":
            # opcional: buscar por texto
            buscar = datos.get('buscar','')
            rows = self.listar(buscar)
            return rows

        # acción desconocida
        return {"ok": False, "msg": "Acción no soportada"}
