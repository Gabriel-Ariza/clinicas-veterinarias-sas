"""Controlador: inicio con clínicas, página de cada clínica y formularios (Gradio)."""

from datetime import datetime
from html import escape

import gradio as gr
import pandas as pd

from resources.excepciones import ClinicaVeterinariaError, DatoInvalidoError

# --------------------------------------------
# Campos del formulario de la clínica: (clave, etiqueta, tipo)
# El orden de esta lista es el orden en que se muestran.
# --------------------------------------------
CAMPOS = [
    ("cedula_vet", "Cédula del veterinario", "texto"),
    ("nombre_vet", "Nombre completo del veterinario", "texto"),
    ("tarjeta", "Tarjeta profesional", "texto"),
    ("codigo_serv", "Código del servicio (ej. CG)", "texto"),
    ("nombre_serv", "Nombre del servicio", "texto"),
    ("tarifa", "Tarifa", "decimal"),
    ("cedula_prop", "Cédula del propietario", "texto"),
    ("nombre_prop", "Nombre del propietario", "texto"),
    ("telefono", "Teléfono", "texto"),
    ("municipio_res", "Municipio de residencia", "texto"),
    ("nombre_masc", "Nombre de la mascota", "texto"),
    ("especie", "Especie", "texto"),
    ("raza", "Raza", "texto"),
    ("anio", "Año aproximado de nacimiento", "entero"),
    ("peso", "Peso (kg)", "decimal"),
    ("fecha", "Fecha (AAAA-MM-DD)", "texto"),
    ("hora", "Hora (HH:MM, formato 24 horas)", "texto"),
    ("servicio_cita", "Tipo de servicio", "servicio"),
    ("codigo_cita", "Código de la cita", "texto"),
    ("accion", "¿Qué deseas hacer con la cita?", "accion"),
    ("adicionales", "Servicios adicionales (solo al atender)", "servicios"),
    ("fecha_operacion", "Fecha de la operación (AAAA-MM-DD)", "texto"),
]

CLAVES = [c[0] for c in CAMPOS]

PLACEHOLDERS = {
    "fecha": "2026-11-10",
    "hora": "09:00",
    "codigo_serv": "CG",
    "codigo_cita": "CIT-001",
    "fecha_operacion": "Opcional",
}

ACCION_CANCELAR = "Cancelar la cita"
ACCION_ATENDER = "Atender la cita y generar la factura"

# Opción -> campos visibles (clave: etiqueta alternativa o None)
OPCIONES = {
    "Crear cita": {
        "cedula_prop": "Cédula del dueño de la mascota",
        "nombre_prop": "Nombre del dueño",
        "telefono": "Teléfono del dueño (solo si es la primera vez)",
        "municipio_res": "Municipio de residencia del dueño (solo si es la primera vez)",
        "nombre_masc": None, "especie": None, "raza": None,
        "anio": None, "peso": None,
        "fecha": None, "hora": None, "servicio_cita": None,
    },
    "Editar cita existente": {
        "codigo_cita": None, "accion": None, "adicionales": None,
        "fecha_operacion": "Fecha de la operación (AAAA-MM-DD; opcional: al cancelar es hoy, "
                           "al atender es la fecha de la cita)",
    },
    "Consultar citas por fecha": {
        "fecha": "Fecha a consultar (AAAA-MM-DD)",
    },
    "Historial de una mascota": {
        "cedula_prop": "Cédula del dueño", "nombre_masc": None,
    },
    "Registrar veterinario": {
        "cedula_vet": None, "nombre_vet": None, "tarjeta": None,
    },
    "Registrar servicio": {
        "codigo_serv": None, "nombre_serv": None, "tarifa": None,
    },
    "Registrar propietario": {
        "cedula_prop": None, "nombre_prop": None, "telefono": None, "municipio_res": None,
    },
    "Registrar mascota": {
        "cedula_prop": "Cédula del dueño", "nombre_masc": None, "especie": None,
        "raza": None, "anio": None, "peso": None,
    },
}

AYUDAS = {
    "Crear cita": "El sistema asigna el veterinario disponible y genera el código de la cita. "
                  "Si el dueño o la mascota aún no están registrados, se registran con estos datos.",
    "Editar cita existente": "Escribe el código que recibiste al crear la cita para cancelarla "
                             "o atenderla (puedes agregar servicios adicionales).",
    "Consultar citas por fecha": "Muestra las citas de la clínica en esa fecha con su estado.",
    "Historial de una mascota": "Muestra todas las citas de la mascota (programadas, canceladas y atendidas).",
    "Registrar veterinario": "Agrega un veterinario a esta clínica.",
    "Registrar servicio": "Agrega un servicio al catálogo de esta clínica.",
    "Registrar propietario": "Registra un propietario en esta clínica.",
    "Registrar mascota": "Registra una mascota de un propietario ya registrado.",
}

OPCION_INICIAL = "Crear cita"

CAMPOS_CLINICA = ["nit", "nombre", "codigo_dane", "municipio", "departamento",
                  "direccion", "barrio"]

COLOR = "#0d9488"

CSS = """
<style>
.barra-superior { align-items: center !important; gap: 12px; }
.tarjeta-clinica { border: 1px solid var(--border-color-primary, #d1d5db);
                   border-radius: 14px; padding: 14px; }
.fila-acciones button { font-size: 1.1rem !important; padding: 14px 10px !important; }
button.primary { background: #0d9488 !important; border-color: #0d9488 !important;
                 color: #ffffff !important; }
button.primary:hover { background: #0f766e !important; }
.tabla-servicios td, .tabla-servicios th { border-left: none !important;
                                           border-right: none !important; }
</style>
"""

BARRA_SUPERIOR = f"""
<div style="display:flex;align-items:center;gap:14px;
            background:linear-gradient(90deg,#0f766e,{COLOR});color:#fff;
            padding:10px 18px;border-radius:12px;">
  <svg width="46" height="46" viewBox="0 0 64 64" aria-label="logo">
    <circle cx="32" cy="32" r="30" fill="white" fill-opacity="0.2"/>
    <ellipse cx="32" cy="43" rx="12" ry="9" fill="white"/>
    <ellipse cx="14" cy="31" rx="5" ry="7" fill="white" transform="rotate(-20 14 31)"/>
    <ellipse cx="24" cy="19" rx="5" ry="7.5" fill="white" transform="rotate(-8 24 19)"/>
    <ellipse cx="40" cy="19" rx="5" ry="7.5" fill="white" transform="rotate(8 40 19)"/>
    <ellipse cx="50" cy="31" rx="5" ry="7" fill="white" transform="rotate(20 50 31)"/>
  </svg>
  <span style="font-size:1.7rem;font-weight:800;letter-spacing:.5px;color:#ffffff !important;">Clínicas Veterinarias</span>
</div>
"""

TITULO_INICIO = """
<div style="text-align:center;margin:18px 0 6px;">
  <h2 style="margin:0;font-size:1.9rem;">Clínicas disponibles</h2>
  <p style="opacity:.75;margin:4px 0 0;">Elige una clínica para ver sus servicios y agendar tu cita.</p>
</div>
"""


# --------------------------------------------
# Utilidades de formato y conversión
# --------------------------------------------
def pesos(valor):
    return "$ " + f"{valor:,.0f}".replace(",", ".")


def a_fecha(texto, campo="Fecha"):
    for formato in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(str(texto).strip(), formato).date()
        except ValueError:
            continue
    raise DatoInvalidoError(
        f"{campo} inválida. Usa el formato AAAA-MM-DD (por ejemplo 2026-11-10)."
    )


def a_fecha_opcional(texto, campo="Fecha"):
    if texto is None or not str(texto).strip():
        return None
    return a_fecha(texto, campo)


def a_hora(texto):
    try:
        return datetime.strptime(str(texto).strip(), "%H:%M").time()
    except ValueError:
        raise DatoInvalidoError("Hora inválida. Usa el formato HH:MM (por ejemplo 09:00).")


class MenuController:

    def __init__(self, clinica_service, cita_service):
        self._clinica_service = clinica_service
        self._cita_service = cita_service
        self._acciones = {
            "Crear cita": self._crear_cita,
            "Editar cita existente": self._editar_cita,
            "Consultar citas por fecha": self._consultar_citas,
            "Historial de una mascota": self._consultar_historial,
            "Registrar veterinario": self._registrar_veterinario,
            "Registrar servicio": self._registrar_servicio,
            "Registrar propietario": self._registrar_propietario,
            "Registrar mascota": self._registrar_mascota,
        }

    def iniciar_sistema(self):
        self._construir_interfaz().launch()

    # --------------------------------------------
    # Piezas de presentación (HTML)
    # --------------------------------------------
    def _lista_clinicas(self):
        return [
            {
                "nit": c.nit,
                "nombre": c.nombre,
                "ubicacion": str(c.municipio),
                "direccion": f"{c.direccion}, barrio {c.barrio}",
            }
            for c in self._clinica_service.listar_clinicas()
        ]

    @staticmethod
    def _html_tarjeta(c):
        return (
            f"<div style='padding:4px 2px;'>"
            f"<div style='font-size:1.3rem;font-weight:700;color:{COLOR};'>{escape(c['nombre'])}</div>"
            f"<div style='margin-top:6px;'>📍 {escape(c['ubicacion'])}</div>"
            f"<div style='opacity:.75;font-size:.95rem;'>{escape(c['direccion'])}</div>"
            f"</div>"
        )

    @staticmethod
    def _html_encabezado(clinica):
        m = clinica.municipio
        return (
            f"<div style='display:flex;justify-content:space-between;align-items:flex-end;"
            f"flex-wrap:wrap;gap:12px;padding:8px 4px 10px;border-bottom:3px solid {COLOR};'>"
            f"<div style='font-size:2.5rem;font-weight:800;line-height:1.1;color:{COLOR};'>"
            f"{escape(clinica.nombre)}</div>"
            f"<div style='text-align:right;font-size:1rem;opacity:.85;'>"
            f"📍 {escape(str(m))}<br>{escape(clinica.direccion)} · Barrio {escape(clinica.barrio)}"
            f"</div></div>"
        )

    @staticmethod
    def _html_servicios(clinica):
        titulo = ("<div style='text-align:center;font-size:1.35rem;font-weight:700;"
                  "margin:22px 0 10px;'>Servicios y tarifas</div>")
        if not clinica.servicios:
            return (titulo + "<p style='text-align:center;opacity:.75;'>Esta clínica aún no tiene "
                    "servicios registrados. Agrégalos en «Más opciones → Registrar servicio».</p>")
        filas = "".join(
            f"<tr><td style='padding:10px 16px;border-bottom:1px solid "
            f"var(--border-color-primary,#e5e7eb);'>{escape(s.nombre)}</td>"
            f"<td style='padding:10px 16px;text-align:right;font-weight:600;border-bottom:1px solid "
            f"var(--border-color-primary,#e5e7eb);'>{pesos(s.tarifa)}</td></tr>"
            for s in clinica.servicios
        )
        return (
            titulo +
            f"<table class='tabla-servicios' style='margin:0 auto;width:min(620px,100%);border-collapse:collapse;"
            f"border:1px solid var(--border-color-primary,#e5e7eb);border-radius:10px;'>"
            f"<thead><tr style='background:{COLOR};'>"
            f"<th style='padding:10px 16px;text-align:left;color:#ffffff !important;"
            f"background:{COLOR};'>Servicio</th>"
            f"<th style='padding:10px 16px;text-align:right;color:#ffffff !important;"
            f"background:{COLOR};'>Precio</th></tr></thead>"
            f"<tbody>{filas}</tbody></table>"
        )

    @staticmethod
    def _opciones_servicios(clinica):
        """(texto completo para el usuario, código corto para el programa)."""
        return [(f"{s.nombre} ({pesos(s.tarifa)})", s.codigo) for s in clinica.servicios]

    @staticmethod
    def _vistas(vista):
        return [
            gr.update(visible=vista == "inicio"),
            gr.update(visible=vista == "clinica"),
            gr.update(visible=vista == "agregar"),
            gr.update(visible=vista != "inicio"),   # botón «Otras clínicas»
        ]

    # --------------------------------------------
    # Navegación
    # --------------------------------------------
    def entrar_clinica(self, nit):
        clinica = self._clinica_service.obtener_clinica(nit)
        opciones = self._opciones_servicios(clinica)
        return [nit] + self._vistas("clinica") + [
            self._html_encabezado(clinica),
            self._html_servicios(clinica),
            gr.update(choices=opciones, value=None),
            gr.update(choices=opciones, value=[]),
            gr.update(visible=False),   # panel del formulario
            "",                          # mensaje
            gr.update(visible=False),   # resultado
        ]

    def ir_inicio(self):
        return [None] + self._vistas("inicio") + [gr.update(visible=False), ""]

    def ir_agregar_clinica(self):
        return self._vistas("agregar") + [""]

    def guardar_clinica(self, *valores):
        datos = dict(zip(CAMPOS_CLINICA, valores))
        try:
            clinica = self._clinica_service.registrar_clinica(
                datos["nit"], datos["nombre"], datos["codigo_dane"], datos["municipio"],
                datos["departamento"], datos["direccion"], datos["barrio"],
            )
        except ClinicaVeterinariaError as error:
            return ([gr.update()] + self._vistas("agregar") + ["", f"⚠️ {error}"]
                    + [gr.update() for _ in CAMPOS_CLINICA])
        except Exception as error:
            return ([gr.update()] + self._vistas("agregar")
                    + ["", f"⚠️ Ocurrió un error inesperado: {error}"]
                    + [gr.update() for _ in CAMPOS_CLINICA])
        return ([self._lista_clinicas()] + self._vistas("inicio") + [
            f"✅ Clínica **{clinica.nombre}** registrada. Ingresa a ella para registrar "
            "sus veterinarios y su catálogo de servicios.",
            "",
        ] + [gr.update(value="") for _ in CAMPOS_CLINICA])

    # --------------------------------------------
    # Formulario de la clínica
    # --------------------------------------------
    def mostrar_opcion(self, opcion):
        campos = OPCIONES.get(opcion, {})
        cambios = []
        for clave in CLAVES:
            if clave in campos:
                if campos[clave]:
                    cambios.append(gr.update(visible=True, label=campos[clave]))
                else:
                    cambios.append(gr.update(visible=True))
            else:
                cambios.append(gr.update(visible=False))
        return cambios + [AYUDAS.get(opcion, ""), gr.update(visible=False), ""]

    def abrir_opcion(self, opcion):
        return [gr.update(value=opcion), gr.update(visible=True)] + self.mostrar_opcion(opcion)

    # --------------------------------------------
    # Acciones: cada una devuelve (mensaje, DataFrame o None)
    # --------------------------------------------
    def _registrar_veterinario(self, d):
        vet = self._clinica_service.registrar_veterinario(
            d["nit"], d["cedula_vet"], d["nombre_vet"], d["tarjeta"]
        )
        return f"✅ Veterinario **{vet.nombre}** registrado.", None

    def _registrar_servicio(self, d):
        serv = self._clinica_service.registrar_servicio(
            d["nit"], d["codigo_serv"], d["nombre_serv"], d["tarifa"]
        )
        return f"✅ Servicio **{serv.nombre}** registrado con tarifa {pesos(serv.tarifa)}.", None

    def _registrar_propietario(self, d):
        prop = self._clinica_service.registrar_propietario(
            d["nit"], d["cedula_prop"], d["nombre_prop"], d["telefono"], d["municipio_res"]
        )
        return f"✅ Propietario **{prop.nombre}** registrado. Ahora puedes registrar sus mascotas.", None

    def _registrar_mascota(self, d):
        masc = self._clinica_service.registrar_mascota(
            d["nit"], d["cedula_prop"], d["nombre_masc"], d["especie"],
            d["raza"], d["anio"], d["peso"],
        )
        return f"✅ Mascota **{masc.nombre}** registrada para {masc.propietario.nombre}.", None

    def _crear_cita(self, d):
        fecha = a_fecha(d["fecha"])
        hora = a_hora(d["hora"])
        cita, prop_nuevo, masc_nueva = self._cita_service.programar_cita(
            d["nit"], d["cedula_prop"], d["nombre_prop"], d["telefono"],
            d["municipio_res"], d["nombre_masc"], d["especie"], d["raza"],
            d["anio"], d["peso"], fecha, hora, d["servicio_cita"],
        )
        nuevos = []
        if prop_nuevo:
            nuevos.append(f"propietario {cita.mascota.propietario.nombre}")
        if masc_nueva:
            nuevos.append(f"mascota {cita.mascota.nombre}")
        registro = f"  \nSe registró además: {' y '.join(nuevos)}." if nuevos else ""
        mensaje = (
            f"✅ Cita programada.  \n"
            f"## Código de la cita: {cita.codigo}  \n"
            f"📌 **Guarda este código**: lo necesitarás para cancelar o atender la cita "
            f"y para cualquier cambio futuro.  \n\n"
            f"Mascota: {cita.mascota.nombre} · Servicio: {cita.servicio.nombre} · "
            f"Fecha: {fecha.isoformat()} a las {hora.strftime('%H:%M')} · "
            f"Veterinario asignado: {cita.veterinario.nombre}{registro}"
        )
        return mensaje, None

    def _editar_cita(self, d):
        accion = d["accion"]
        if accion == ACCION_CANCELAR:
            fecha = a_fecha_opcional(d["fecha_operacion"], "Fecha de cancelación")
            cita = self._cita_service.cancelar_cita(d["codigo_cita"], fecha, d["nit"])
            return f"✅ La cita **{cita.codigo}** quedó en estado **{cita.estado.value}**.", None
        if accion == ACCION_ATENDER:
            return self._atender(d)
        raise DatoInvalidoError("Elige si deseas cancelar o atender la cita.")

    def _atender(self, d):
        fecha = a_fecha_opcional(d["fecha_operacion"], "Fecha de atención")
        codigos = list(d["adicionales"] or [])
        factura = self._cita_service.atender_cita(d["codigo_cita"], codigos, fecha, d["nit"])
        filas = [[s.nombre, pesos(s.tarifa)] for s in factura.servicios]
        filas.append(["TOTAL", pesos(factura.total)])
        tabla = pd.DataFrame(filas, columns=["Servicio", "Tarifa"])
        mensaje = (
            f"✅ Cita atendida. **Factura {factura.numero}** — {factura.fecha.isoformat()}  \n"
            f"Propietario: {factura.propietario.nombre} (CC {factura.propietario.cedula}) · "
            f"Mascota: {factura.mascota.nombre} ({factura.mascota.especie})  \n"
            f"**Total: {pesos(factura.total)}**"
        )
        return mensaje, tabla

    def _consultar_citas(self, d):
        fecha = a_fecha(d["fecha"])
        citas = self._cita_service.consultar_citas_clinica(d["nit"], fecha)
        if not citas:
            return f"ℹ️ No hay citas el {fecha.isoformat()}.", None
        filas = [
            [c.codigo, c.hora.strftime("%H:%M"), c.mascota.nombre,
             c.mascota.propietario.nombre, c.veterinario.nombre,
             c.servicio.nombre, c.estado.value]
            for c in citas
        ]
        tabla = pd.DataFrame(
            filas,
            columns=["Código", "Hora", "Mascota", "Propietario",
                     "Veterinario", "Servicio", "Estado"],
        )
        return f"📅 {len(citas)} cita(s) el {fecha.isoformat()}.", tabla

    def _consultar_historial(self, d):
        mascota, citas = self._cita_service.consultar_historial_mascota(
            d["nit"], d["cedula_prop"], d["nombre_masc"]
        )
        if not citas:
            return f"ℹ️ {mascota.nombre} aún no tiene citas.", None
        filas = [
            [c.codigo, c.fecha.isoformat(), c.hora.strftime("%H:%M"),
             c.servicio.nombre, c.veterinario.nombre, c.estado.value,
             c.factura.numero if c.factura else "—",
             pesos(c.factura.total) if c.factura else "—"]
            for c in citas
        ]
        tabla = pd.DataFrame(
            filas,
            columns=["Código", "Fecha", "Hora", "Servicio", "Veterinario",
                     "Estado", "Factura", "Total"],
        )
        return f"📋 Historial de {mascota.nombre}: {len(citas)} cita(s).", tabla

    # --------------------------------------------
    # Botón Ejecutar
    # --------------------------------------------
    def ejecutar(self, nit, opcion, *valores):
        if not nit:
            return [gr.update(), gr.update(), gr.update(),
                    "⚠️ Primero elige una clínica.", gr.update(visible=False)]

        datos = dict(zip(CLAVES, valores))
        datos["nit"] = nit
        tabla = None
        try:
            if opcion not in self._acciones:
                raise DatoInvalidoError("Selecciona una opción.")
            mensaje, tabla = self._acciones[opcion](datos)
        except ClinicaVeterinariaError as error:
            mensaje = f"⚠️ {error}"
        except Exception as error:  # imprevistos: la aplicación no se detiene
            mensaje = f"⚠️ Ocurrió un error inesperado: {error}"

        clinica = self._clinica_service.obtener_clinica(nit)
        opciones = self._opciones_servicios(clinica)
        resultado = gr.update(visible=False) if tabla is None else gr.update(value=tabla, visible=True)
        return [
            self._html_servicios(clinica),
            gr.update(choices=opciones),
            gr.update(choices=opciones),
            mensaje,
            resultado,
        ]

    # --------------------------------------------
    # Interfaz Gradio
    # --------------------------------------------
    def _construir_interfaz(self):
        with gr.Blocks(title="Clínicas Veterinarias") as app:

            gr.HTML(CSS)
            clinica_actual = gr.State(None)
            estado_clinicas = gr.State(self._lista_clinicas())

            # ---------- BARRA SUPERIOR ----------
            with gr.Row(elem_classes="barra-superior"):
                gr.HTML(BARRA_SUPERIOR)
                boton_otras = gr.Button("🏠 Otras clínicas", visible=False, scale=0, min_width=190)

            # ---------- INICIO ----------
            with gr.Column(visible=True) as vista_inicio:
                gr.HTML(TITULO_INICIO)
                mensaje_inicio = gr.Markdown()

                @gr.render(inputs=estado_clinicas)
                def tarjetas(lista):
                    if not lista:
                        gr.HTML("<p style='text-align:center;opacity:.75;'>Aún no hay clínicas "
                                "registradas.</p>")
                    for i in range(0, len(lista), 3):
                        with gr.Row():
                            for c in lista[i:i + 3]:
                                with gr.Column(elem_classes="tarjeta-clinica", min_width=240):
                                    gr.HTML(self._html_tarjeta(c))
                                    boton = gr.Button("Ingresar a la clínica", variant="primary")
                                    boton.click(
                                        lambda nit=c["nit"]: self.entrar_clinica(nit),
                                        None,
                                        salidas_entrar,
                                    )

                boton_agregar = gr.Button("➕ Agregar clínica", variant="secondary", size="lg")

            # ---------- AGREGAR CLÍNICA ----------
            with gr.Column(visible=False) as vista_agregar:
                gr.HTML("<div style='text-align:center;font-size:1.6rem;font-weight:700;"
                        "margin:18px 0 6px;'>Agregar clínica</div>")
                campos_clinica = [
                    gr.Textbox(label="NIT", placeholder="901456789-1"),
                    gr.Textbox(label="Nombre de la clínica"),
                    gr.Textbox(label="Código DANE del municipio", placeholder="68679"),
                    gr.Textbox(label="Municipio"),
                    gr.Textbox(label="Departamento"),
                    gr.Textbox(label="Dirección"),
                    gr.Textbox(label="Barrio"),
                ]
                with gr.Row():
                    boton_guardar_clinica = gr.Button("Guardar clínica", variant="primary")
                    boton_cancelar_clinica = gr.Button("Cancelar")
                mensaje_agregar = gr.Markdown()

            # ---------- PÁGINA DE LA CLÍNICA ----------
            with gr.Column(visible=False) as vista_clinica:
                encabezado = gr.HTML()
                tabla_servicios = gr.HTML()

                gr.HTML("<div style='height:26px'></div>")
                with gr.Row(elem_classes="fila-acciones"):
                    boton_crear = gr.Button("📅 Crear cita", variant="primary", size="lg")
                    boton_editar = gr.Button("✏️ Editar cita existente", variant="secondary", size="lg")

                with gr.Accordion("Más opciones de la clínica", open=False):
                    with gr.Row():
                        boton_consultar = gr.Button("📆 Consultar citas por fecha")
                        boton_historial = gr.Button("📋 Historial de una mascota")
                    with gr.Row():
                        boton_vet = gr.Button("🩺 Registrar veterinario")
                        boton_serv = gr.Button("💲 Registrar servicio")
                    with gr.Row():
                        boton_prop = gr.Button("👤 Registrar propietario")
                        boton_masc = gr.Button("🐾 Registrar mascota")

                # ----- Formulario (se muestra al elegir una opción) -----
                with gr.Column(visible=False) as panel_form:
                    opcion = gr.Dropdown(
                        choices=list(OPCIONES.keys()), value=OPCION_INICIAL, label="Opción"
                    )
                    ayuda = gr.Markdown(AYUDAS[OPCION_INICIAL])

                    componentes = []
                    for clave, etiqueta, tipo in CAMPOS:
                        if tipo == "texto":
                            comp = gr.Textbox(label=etiqueta, visible=False,
                                              placeholder=PLACEHOLDERS.get(clave, ""))
                        elif tipo == "entero":
                            comp = gr.Number(label=etiqueta, precision=0, value=None, visible=False)
                        elif tipo == "decimal":
                            comp = gr.Number(label=etiqueta, value=None, visible=False)
                        elif tipo == "servicio":
                            comp = gr.Dropdown(choices=[], value=None, label=etiqueta, visible=False)
                        elif tipo == "servicios":
                            comp = gr.Dropdown(choices=[], value=[], multiselect=True,
                                               label=etiqueta, visible=False)
                        else:  # accion
                            comp = gr.Radio(choices=[ACCION_CANCELAR, ACCION_ATENDER],
                                            value=None, label=etiqueta, visible=False)
                        componentes.append(comp)
                    por_clave = dict(zip(CLAVES, componentes))

                    boton_ejecutar = gr.Button("Ejecutar", variant="primary")
                    mensaje = gr.Markdown()
                    resultado = gr.Dataframe(interactive=False, visible=False)

            # ---------- EVENTOS ----------
            vistas = [vista_inicio, vista_clinica, vista_agregar, boton_otras]

            salidas_entrar = [
                clinica_actual, *vistas, encabezado, tabla_servicios,
                por_clave["servicio_cita"], por_clave["adicionales"],
                panel_form, mensaje, resultado,
            ]

            boton_otras.click(
                self.ir_inicio, None,
                [clinica_actual, *vistas, panel_form, mensaje_inicio],
            )
            boton_agregar.click(self.ir_agregar_clinica, None, [*vistas, mensaje_agregar])
            boton_cancelar_clinica.click(
                lambda: self._vistas("inicio") + [""], None, [*vistas, mensaje_agregar]
            )
            boton_guardar_clinica.click(
                self.guardar_clinica,
                inputs=campos_clinica,
                outputs=[estado_clinicas, *vistas, mensaje_inicio, mensaje_agregar,
                         *campos_clinica],
            )

            botones = {
                "Crear cita": boton_crear,
                "Editar cita existente": boton_editar,
                "Consultar citas por fecha": boton_consultar,
                "Historial de una mascota": boton_historial,
                "Registrar veterinario": boton_vet,
                "Registrar servicio": boton_serv,
                "Registrar propietario": boton_prop,
                "Registrar mascota": boton_masc,
            }
            salidas_form = componentes + [ayuda, resultado, mensaje]
            for nombre_op, boton in botones.items():
                boton.click(
                    lambda op=nombre_op: self.abrir_opcion(op),
                    None,
                    [opcion, panel_form] + salidas_form,
                )

            opcion.change(self.mostrar_opcion, opcion, salidas_form)

            boton_ejecutar.click(
                self.ejecutar,
                inputs=[clinica_actual, opcion] + componentes,
                outputs=[tabla_servicios, por_clave["servicio_cita"],
                         por_clave["adicionales"], mensaje, resultado],
            )

        return app
