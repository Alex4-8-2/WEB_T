// Utilidades
const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => document.querySelectorAll(sel);

// Navegación dinámica: mostrar solo la sección activa
function mostrarSeccion(id) {
  $$('.section').forEach(sec => sec.classList.add('hidden'));
  const target = $('#' + id);
  if (target) {
    target.classList.remove('hidden');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }
}

// Menú superior
document.querySelectorAll('a[href^="#"]').forEach(link => {
  link.addEventListener('click', (e) => {
    const id = link.getAttribute('href').replace('#', '');
    const target = document.getElementById(id);
    if (target) {
      e.preventDefault();
      mostrarSeccion(id);
    }
  });
});

// CTA del hero: pedir acceso (login/registro) pero navegar a paquetes
$('#ctaReservar')?.addEventListener('click', (e) => {
  e.preventDefault();
  mostrarSeccion('paquetes');
});

// Modales: abrir/cerrar
function openModal(id) {
  const m = $(id);
  if (m) m.setAttribute('aria-hidden', 'false');
}
function closeModal(id) {
  const m = $(id);
  if (m) m.setAttribute('aria-hidden', 'true');
}
$('#btnCliente')?.addEventListener('click', () => openModal('#modalLogin'));
$('#btnNuevoCliente')?.addEventListener('click', () => openModal('#modalRegistro'));
document.addEventListener('click', (e) => {
  const closeSel = e.target.getAttribute('data-close');
  if (closeSel) closeModal(closeSel);
});
$('#openRegistroFromLogin')?.addEventListener('click', () => {
  closeModal('#modalLogin');
  openModal('#modalRegistro');
});

// Estado simple de usuarios y sesión
const state = {
  users: JSON.parse(localStorage.getItem('users') || '[]'), // {usuario, pass}
  sessionUser: null,
  lastDestino: null,
  preReserva: null,
  pendingDestinoForLogin: null, // para volver al flujo después de login
};

// Login: tras login, volver a paquetes y continuar si había intento de reservar
$('#formLogin')?.addEventListener('submit', (e) => {
  e.preventDefault();
  const u = $('#loginUsuario'), p = $('#loginPassword'), fb = $('#loginFeedback');
  let ok = true;
  if (!u.value.trim()) { setError(u, 'Datos incompletos'); ok = false; } else setError(u, '');
  if (!p.value.trim()) { setError(p, 'Datos incompletos'); ok = false; } else setError(p, '');
  if (!ok) return;

  const match = state.users.find(x => x.usuario === u.value.trim());
  if (!match || match.pass !== p.value) { fb.textContent = 'Usuario o contraseña incorrecto'; return; }
  fb.textContent = '';

  state.sessionUser = match.usuario;
  closeModal('#modalLogin');
  mostrarSeccion('paquetes');

  // Si el usuario vino por intentar reservar, abre pre-reserva con el destino guardado
  if (state.pendingDestinoForLogin) {
    state.lastDestino = { ...state.pendingDestinoForLogin };
    state.pendingDestinoForLogin = null;
    openModal('#modalPreReserva');
  }
});

// Registro
$('#formRegistro')?.addEventListener('submit', (e) => {
  e.preventDefault();
  const nombres = $('#regNombres'), apellidos = $('#regApellidos'), nac = $('#regNacimiento'),
        ci = $('#regCI'), correo = $('#regCorreo'), contacto = $('#regContacto'),
        usuario = $('#regUsuario'), pass = $('#regPass'), pass2 = $('#regPass2');
  const fb = $('#registroFeedback');
  const required = [nombres, apellidos, nac, ci, correo, contacto, usuario, pass, pass2];
  let ok = true;

  required.forEach(el => {
    if (!el.value.trim()) { setError(el, 'Datos incompletos'); ok = false; }
    else setError(el, '');
  });

  if (ok && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(correo.value.trim())) { setError(correo, 'Correo no válido'); ok = false; }
  if (ok && pass.value.length < 6) { setError(pass, 'Mínimo 6 caracteres'); ok = false; }
  if (ok && pass.value !== pass2.value) { setError(pass2, 'No coinciden'); ok = false; }
  if (!ok) { fb.textContent = 'Corrige los campos marcados.'; return; }

  state.users.push({ usuario: usuario.value.trim(), pass: pass.value });
  localStorage.setItem('users', JSON.stringify(state.users));
  fb.textContent = '';
  closeModal('#modalRegistro');
  openModal('#modalLogin');
});

// Helper de errores
function setError(input, msg) {
  const field = input.closest('.field');
  const small = field?.querySelector('.error');
  if (small) small.textContent = msg || '';
  input.setAttribute('aria-invalid', msg ? 'true' : 'false');
}

// Botones "Reservar" en paquetes: exigir login antes de abrir pre-reserva
function initReservarBtns() {
  $$('.reservar-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const dep = btn.dataset.departamento;
      const prov = btn.dataset.provincia;
      // Si no hay sesión, pedir login y guardar destino pendiente
      if (!state.sessionUser) {
        state.pendingDestinoForLogin = { dep, prov };
        openModal('#modalLogin');
        return;
      }
      // Si hay sesión, continuar flujo normal
      state.lastDestino = { dep, prov };
      openModal('#modalPreReserva');
    });
  });
}

// Pre-reserva: validar y llevar a sección Reservas con datos
$('#formPreReserva')?.addEventListener('submit', (e) => {
  e.preventDefault();
  const dias = $('#preDias'), pers = $('#prePersonas'), tr = $('#preTransporte'),
        hosp = $('#preHospedaje'), fi = $('#preFechaInicio'), ff = $('#preFechaFin');
  let ok = true;

  [dias, pers, tr, hosp, fi, ff].forEach(el => {
    if (!el.value || (el.type === 'number' && +el.value < 1)) { setError(el, 'Este campo es obligatorio.'); ok = false; }
    else setError(el, '');
  });

  const f1 = new Date(fi.value), f2 = new Date(ff.value);
  if (ok && f1.toString() !== 'Invalid Date' && f2.toString() !== 'Invalid Date' && f2 <= f1) {
    setError(ff, 'La fecha fin debe ser posterior a la de inicio.'); ok = false;
  }
  if (!ok) return;

  state.preReserva = {
    destino: state.lastDestino,
    dias: +dias.value,
    personas: +pers.value,
    transporte: tr.value,
    hospedaje: hosp.value,
    fechaInicio: fi.value,
    fechaFin: ff.value
  };

  closeModal('#modalPreReserva');

  // Cargar en Reservas
  $('#destDeptoDisplay').value = state.lastDestino?.dep || '';
  $('#destProvDisplay').value = state.lastDestino?.prov || '';
  mostrarSeccion('reservas');
});

// Confirmar reserva: simular envío por WhatsApp/correo con QR y validar comprobante
$('#formFactura')?.addEventListener('submit', (e) => {
  e.preventDefault();

  const nombre = $('#nombreFactura'), nit = $('#nitFactura'), correo = $('#correoFactura'),
        cel = $('#celularFactura'), comp = $('#comprobante');
  let ok = true;

  [nombre, nit, correo, cel].forEach(el => {
    if (!el.value.trim()) { setError(el, 'Este campo es obligatorio.'); ok = false; }
    else setError(el, '');
  });

  if (ok && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(correo.value.trim())) { setError(correo, 'Correo no válido'); ok = false; }
  if (!ok) return;

  const resumen = `
Destino: ${$('#destDeptoDisplay').value} - ${$('#destProvDisplay').value}
Días: ${state.preReserva?.dias ?? '-'}
Personas: ${state.preReserva?.personas ?? '-'}
Transporte: ${state.preReserva?.transporte ?? '-'}
Hospedaje: ${state.preReserva?.hospedaje ?? '-'}
Fechas: ${state.preReserva?.fechaInicio ?? '-'} a ${state.preReserva?.fechaFin ?? '-'}
Factura: ${nombre.value} | NIT/CI: ${nit.value} | ${correo.value} | ${cel.value}
`.trim();

  $('#resumenContenido').textContent = resumen;
  $('#resumen').classList.remove('hidden');

  alert('Se envió un mensaje de WhatsApp y correo con el QR de pago (simulación).');

  // Validación de comprobante (obligatorio para confirmar)
  if (!comp.value.trim()) {
    setError(comp, 'Ingresa el número de comprobante luego del pago.');
    return;
  }
  setError(comp, '');

  // Guardado local de la reserva (sin BD)
  const reservas = JSON.parse(localStorage.getItem('reservas') || '[]');
  reservas.push({
    usuario: state.sessionUser,
    destino: state.lastDestino,
    preReserva: state.preReserva,
    factura: { nombre: nombre.value, nit: nit.value, correo: correo.value, celular: cel.value },
    comprobante: comp.value.trim(),
    createdAt: new Date().toISOString()
  });
  localStorage.setItem('reservas', JSON.stringify(reservas));

  alert('Reserva confirmada y validada');
});

// Init
document.addEventListener('DOMContentLoaded', () => {
  const hash = (window.location.hash || '#inicio').replace('#', '');
  mostrarSeccion(hash || 'inicio');
  initReservarBtns();
});
