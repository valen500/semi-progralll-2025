async function postJSON(payload) {
  const res = await fetch('/', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(payload)
  });
  return await res.json();
}

async function cargarUsuarios(buscar='') {
  const payload = { accion: 'listar', buscar: buscar };
  const resp = await postJSON(payload);
  const data = resp; 
  let filas = [];
  if (Array.isArray(data)) filas = data;
  else if (data.msg && Array.isArray(data.msg)) filas = data.msg;
  else if (data.usuarios) filas = data.usuarios;
  else filas = data; 

  const tbody = document.querySelector('#tablaUsuarios tbody');
  tbody.innerHTML = '';
  filas.forEach(u => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${u.idUsuario}</td>
      <td>${u.usuario}</td>
      <td>${u.nombre || ''}</td>
      <td>${u.direccion || ''}</td>
      <td>${u.telefono || ''}</td>
      <td>
        <button class="edit" data-id="${u.idUsuario}">Editar</button>
        <button class="del" data-id="${u.idUsuario}">Eliminar</button>
      </td>
    `;
    tbody.appendChild(tr);
  });

  document.querySelectorAll('.edit').forEach(btn => {
    btn.onclick = async () => {
      const id = btn.dataset.id;
      const resp = await postJSON({accion: 'obtener', idUsuario: id});
      // resp puede venir como {ok:True,msg:...} o lista
      let user = null;
      if (resp.msg && Array.isArray(resp.msg) && resp.msg.length) user = resp.msg[0];
      else if (Array.isArray(resp) && resp.length) user = resp[0];
      else if (resp.usuario) user = resp.usuario;
      if (!user) { alert('No se obtuvo usuario'); return; }
      document.getElementById('idUsuario').value = user.idUsuario;
      document.getElementById('usuario').value = user.usuario;
      document.getElementById('nombre').value = user.nombre || '';
      document.getElementById('direccion').value = user.direccion || '';
      document.getElementById('telefono').value = user.telefono || '';
      document.getElementById('clave').value = '';
    };
  });

  document.querySelectorAll('.del').forEach(btn => {
    btn.onclick = async () => {
      if (!confirm('Eliminar este usuario?')) return;
      const id = btn.dataset.id;
      const r = await postJSON({accion: 'eliminar', idUsuario: id});
      alert(typeof r === 'object' ? (r.msg || JSON.stringify(r)) : r);
      cargarUsuarios(document.getElementById('buscar').value);
    };
  });
}

document.getElementById('formUsuario').addEventListener('submit', async (e) => {
  e.preventDefault();
  const idUsuario = document.getElementById('idUsuario').value;
  const usuario = document.getElementById('usuario').value.trim();
  const clave = document.getElementById('clave').value;
  const nombre = document.getElementById('nombre').value;
  const direccion = document.getElementById('direccion').value;
  const telefono = document.getElementById('telefono').value;

  let payload;
  if (idUsuario) {
    payload = { accion: 'modificar', idUsuario: idUsuario, usuario, nombre, direccion, telefono };
    if (clave) payload.clave = clave;
  } else {
    payload = { accion: 'nuevo', usuario, clave, nombre, direccion, telefono };
  }

  const r = await postJSON(payload);
  alert(typeof r === 'object' ? (r.msg || JSON.stringify(r)) : r);
  document.getElementById('formUsuario').reset();
  document.getElementById('idUsuario').value = '';
  cargarUsuarios(document.getElementById('buscar').value);
});

document.getElementById('btnBuscar').addEventListener('click', () => {
  cargarUsuarios(document.getElementById('buscar').value);
});

document.getElementById('btnReset').addEventListener('click', () => {
  document.getElementById('formUsuario').reset();
  document.getElementById('idUsuario').value = '';
});

document.getElementById('btnLogout').addEventListener('click', () => {
  sessionStorage.removeItem('usuario');
  window.location.href = 'index.html';
});


window.onload = function() {
  const user = sessionStorage.getItem('usuario');
  if (!user) {
    window.location.href = 'index.html';
    return;
  }
  cargarUsuarios();
};
