# ============================================
# GESTIÓN DE CITAS PARA CLÍNICAS VETERINARIAS
# Valery Montes - 01240372023
# Gabriel Plata - 01240372047
# ============================================

!pip install -q gradio

import re
from datetime import date, datetime
from enum import Enum

import gradio as gr
import pandas as pd


# ============================================
# EXCEPCIONES
# ============================================

class ClinicaVeterinariaError(Exception):
    """Excepción base: todas las demás heredan de ella."""


class DatoInvalidoError(ClinicaVeterinariaError):
    """Un dato ingresado está vacío, mal formado o fuera de rango."""


class DuplicadoError(ClinicaVeterinariaError):
    """Se intenta registrar algo que ya existe."""


class NoEncontradoError(ClinicaVeterinariaError):
    """No existe la clínica, propietario, mascota, servicio, etc. buscado."""


class ReglaNegocioError(ClinicaVeterinariaError):
    """Se incumple una regla de negocio."""


class ConflictoHorarioError(ReglaNegocioError):
    """El veterinario o la mascota ya tienen una cita programada a esa hora."""


class EstadoCitaInvalidoError(ReglaNegocioError):
    """La cita no está en el estado requerido para la operación."""


# ============================================
# VALIDACIONES
# ============================================

def texto_obligatorio(valor, campo):
    if valor is None or not str(valor).strip():
        raise DatoInvalidoError(f"El campo '{campo}' es obligatorio.")
    return str(valor).strip()


def solo_digitos(valor, campo, minimo=1, maximo=15):
    texto = texto_obligatorio(valor, campo)
    if not texto.isdigit() or not minimo <= len(texto) <= maximo:
        if minimo == maximo:
            rango = f"{minimo} dígitos"
        else:
            rango = f"entre {minimo} y {maximo} dígitos"
        raise DatoInvalidoError(
            f"El campo '{campo}' debe contener solo números ({rango})."
        )
    return texto


def nit_valido(valor):
    texto = texto_obligatorio(valor, "NIT")
    if not re.fullmatch(r"\d{6,10}(-\d)?", texto):
        raise DatoInvalidoError("El NIT debe tener un formato como 901456789-1.")
    return texto


def numero_positivo(valor, campo):
    if valor is None or valor == "":
        raise DatoInvalidoError(f"El campo '{campo}' es obligatorio.")
    try:
        numero = float(valor)
    except (TypeError, ValueError):
        raise DatoInvalidoError(f"El campo '{campo}' debe ser un número.")
    if numero <= 0:
        raise DatoInvalidoError(f"El campo '{campo}' debe ser mayor que 0.")
    return numero


# ============================================
# CLASE MUNICIPIO
# ============================================

class Municipio:

    def __init__(self, codigo_dane, nombre, departamento):
        self._codigo_dane = solo_digitos(codigo_dane, "Código DANE", 5, 5)
        self._nombre = texto_obligatorio(nombre, "Municipio")
        self._departamento = texto_obligatorio(departamento, "Departamento")

    @property
    def codigo_dane(self):
        return self._codigo_dane

    @property
    def nombre(self):
        return self._nombre

    @property
    def departamento(self):
        return self._departamento

    def __str__(self):
        return f"{self._nombre}, {self._departamento}"


# ============================================
# CLASE VETERINARIO
# ============================================

class Veterinario:

    def __init__(self, cedula, nombre, tarjeta_profesional):
        self._cedula = solo_digitos(cedula, "Cédula del veterinario", 6, 10)
        self._nombre = texto_obligatorio(nombre, "Nombre del veterinario")
        self._tarjeta_profesional = texto_obligatorio(
            tarjeta_profesional, "Tarjeta profesional"
        )

    @property
    def cedula(self):
        return self._cedula

    @property
    def nombre(self):
        return self._nombre

    @property
    def tarjeta_profesional(self):
        return self._tarjeta_profesional

    def __str__(self):
        return self._nombre


# ============================================
# CLASE SERVICIO
# ============================================

class Servicio:
    """Servicio del catálogo de una clínica (código, nombre y tarifa)."""

    def __init__(self, codigo, nombre, tarifa):
        self._codigo = texto_obligatorio(codigo, "Código del servicio").upper()
        self._nombre = texto_obligatorio(nombre, "Nombre del servicio")
        self._tarifa = numero_positivo(tarifa, "Tarifa")

    @property
    def codigo(self):
        return self._codigo

    @property
    def nombre(self):
        return self._nombre

    @property
    def tarifa(self):
        return self._tarifa

    def __str__(self):
        return f"{self._codigo} - {self._nombre}"


# ============================================
# CLASE MASCOTA
# ============================================

class Mascota:
    """Mascota de un propietario (asociación con Propietario)."""

    def __init__(self, propietario, nombre, especie, raza, anio_nacimiento, peso):
        self._propietario = propietario
        self._nombre = texto_obligatorio(nombre, "Nombre de la mascota")
        self._especie = texto_obligatorio(especie, "Especie")
        self._raza = texto_obligatorio(raza, "Raza")
        self._anio_nacimiento = self._validar_anio(anio_nacimiento)
        self._peso = numero_positivo(peso, "Peso (kg)")

    @staticmethod
    def _validar_anio(valor):
        if valor is None or valor == "":
            raise DatoInvalidoError("El campo 'Año de nacimiento' es obligatorio.")
        try:
            anio = int(valor)
        except (TypeError, ValueError):
            raise DatoInvalidoError("El año de nacimiento debe ser un número entero.")
        if not 1980 <= anio <= date.today().year:
            raise DatoInvalidoError(
                f"El año de nacimiento debe estar entre 1980 y {date.today().year}."
            )
        return anio

    @property
    def propietario(self):
        return self._propietario

    @property
    def nombre(self):
        return self._nombre

    @property
    def especie(self):
        return self._especie

    @property
    def raza(self):
        return self._raza

    @property
    def anio_nacimiento(self):
        return self._anio_nacimiento

    @property
    def peso(self):
        return self._peso

    def __str__(self):
        return f"{self._nombre} ({self._especie}, {self._raza})"


# ============================================
# CLASE PROPIETARIO
# ============================================

class Propietario:
    """Propietario de una o varias mascotas (agregación de Mascota)."""

    def __init__(self, cedula, nombre, telefono, municipio_residencia):
        self._cedula = solo_digitos(cedula, "Cédula del propietario", 6, 10)
        self._nombre = texto_obligatorio(nombre, "Nombre del propietario")
        self._telefono = solo_digitos(telefono, "Teléfono", 7, 10)
        self._municipio_residencia = texto_obligatorio(
            municipio_residencia, "Municipio de residencia"
        )
        self._mascotas = {}  # nombre en minúsculas -> Mascota

    @property
    def cedula(self):
        return self._cedula

    @property
    def nombre(self):
        return self._nombre

    @property
    def telefono(self):
        return self._telefono

    @property
    def municipio_residencia(self):
        return self._municipio_residencia

    @property
    def mascotas(self):
        return list(self._mascotas.values())

    def agregar_mascota(self, mascota):
        clave = mascota.nombre.lower()
        if clave in self._mascotas:
            raise DuplicadoError(
                f"{self._nombre} ya tiene una mascota llamada '{mascota.nombre}'."
            )
        self._mascotas[clave] = mascota

    def buscar_mascota(self, nombre):
        nombre = texto_obligatorio(nombre, "Nombre de la mascota")
        return self._mascotas.get(nombre.lower())

    def obtener_mascota(self, nombre):
        nombre = texto_obligatorio(nombre, "Nombre de la mascota")
        mascota = self._mascotas.get(nombre.lower())
        if mascota is None:
            raise NoEncontradoError(
                f"{self._nombre} no tiene una mascota llamada '{nombre}'."
            )
        return mascota

    def __str__(self):
        return self._nombre


# ============================================
# CLASE FACTURA
# ============================================

class Factura:
    """Factura expedida al atender una cita."""

    def __init__(self, numero, fecha, propietario, mascota, servicios):
        self._numero = numero
        self._fecha = fecha
        self._propietario = propietario
        self._mascota = mascota
        self._servicios = list(servicios)

    @property
    def numero(self):
        return self._numero

    @property
    def fecha(self):
        return self._fecha

    @property
    def propietario(self):
        return self._propietario

    @property
    def mascota(self):
        return self._mascota

    @property
    def servicios(self):
        return list(self._servicios)

    @property
    def total(self):
        return sum(servicio.tarifa for servicio in self._servicios)


# ============================================
# CLASE CITA
# ============================================

class EstadoCita(Enum):
    PROGRAMADA = "Programada"
    CANCELADA = "Cancelada"
    ATENDIDA = "Atendida"


class Cita:
    """Cita de una mascota con un veterinario para un servicio."""

    def __init__(self, codigo, fecha, hora, mascota, veterinario, servicio):
        self._codigo = codigo
        self._fecha = fecha
        self._hora = hora
        self._mascota = mascota
        self._veterinario = veterinario
        self._servicio = servicio
        self._estado = EstadoCita.PROGRAMADA
        self._servicios_adicionales = []
        self._factura = None

    @property
    def codigo(self):
        return self._codigo

    @property
    def fecha(self):
        return self._fecha

    @property
    def hora(self):
        return self._hora

    @property
    def mascota(self):
        return self._mascota

    @property
    def veterinario(self):
        return self._veterinario

    @property
    def servicio(self):
        return self._servicio

    @property
    def estado(self):
        return self._estado

    @property
    def servicios_adicionales(self):
        return list(self._servicios_adicionales)

    @property
    def factura(self):
        return self._factura

    def esta_programada(self):
        return self._estado == EstadoCita.PROGRAMADA

    def cancelar(self, fecha_operacion):
        if not self.esta_programada():
            raise EstadoCitaInvalidoError(
                f"La cita {self._codigo} no se puede cancelar porque está "
                f"en estado {self._estado.value}."
            )
        if fecha_operacion >= self._fecha:
            raise ReglaNegocioError(
                f"La cita {self._codigo} solo se puede cancelar antes de su fecha "
                f"({self._fecha.isoformat()})."
            )
        self._estado = EstadoCita.CANCELADA

    def verificar_atendible(self):
        if not self.esta_programada():
            raise EstadoCitaInvalidoError(
                f"La cita {self._codigo} no se puede atender porque está "
                f"en estado {self._estado.value}."
            )

    def atender(self, numero_factura, fecha_atencion, servicios_adicionales=None):
        self.verificar_atendible()
        adicionales = list(servicios_adicionales or [])
        self._factura = Factura(
            numero_factura,
            fecha_atencion,
            self._mascota.propietario,
            self._mascota,
            [self._servicio] + adicionales,
        )
        self._servicios_adicionales = adicionales
        self._estado = EstadoCita.ATENDIDA
        return self._factura


# ============================================
# CLASE CLINICA
# ============================================

class Clinica:
    """Clínica veterinaria.

    Compone a sus veterinarios, servicios, propietarios y citas.
    """

    def __init__(self, nit, nombre, municipio, direccion, barrio):
        self._nit = nit_valido(nit)
        self._nombre = texto_obligatorio(nombre, "Nombre de la clínica")
        self._municipio = municipio
        self._direccion = texto_obligatorio(direccion, "Dirección")
        self._barrio = texto_obligatorio(barrio, "Barrio")
        self._veterinarios = {}   # cédula -> Veterinario
        self._servicios = {}      # código -> Servicio
        self._propietarios = {}   # cédula -> Propietario
        self._citas = {}          # código -> Cita

    # ---------- propiedades ----------
    @property
    def nit(self):
        return self._nit

    @property
    def nombre(self):
        return self._nombre

    @property
    def municipio(self):
        return self._municipio

    @property
    def direccion(self):
        return self._direccion

    @property
    def barrio(self):
        return self._barrio

    @property
    def veterinarios(self):
        return list(self._veterinarios.values())

    @property
    def servicios(self):
        return list(self._servicios.values())

    @property
    def propietarios(self):
        return list(self._propietarios.values())

    @property
    def citas(self):
        return list(self._citas.values())

    @property
    def puede_operar(self):
        """La clínica ya tiene veterinarios y catálogo de servicios."""
        return bool(self._veterinarios) and bool(self._servicios)

    # ---------- registros ----------
    def agregar_veterinario(self, veterinario):
        if veterinario.cedula in self._veterinarios:
            raise DuplicadoError(
                f"Ya existe un veterinario con la cédula {veterinario.cedula} "
                f"en {self._nombre}."
            )
        self._veterinarios[veterinario.cedula] = veterinario

    def agregar_servicio(self, servicio):
        if servicio.codigo in self._servicios:
            raise DuplicadoError(
                f"Ya existe un servicio con el código {servicio.codigo} "
                f"en {self._nombre}."
            )
        self._servicios[servicio.codigo] = servicio

    def agregar_propietario(self, propietario):
        if propietario.cedula in self._propietarios:
            raise DuplicadoError(
                f"Ya existe un propietario con la cédula {propietario.cedula} "
                f"en {self._nombre}."
            )
        self._propietarios[propietario.cedula] = propietario

    def agregar_cita(self, cita):
        self._citas[cita.codigo] = cita

    # ---------- búsquedas ----------
    def obtener_veterinario(self, cedula):
        cedula = solo_digitos(cedula, "Cédula del veterinario", 6, 10)
        veterinario = self._veterinarios.get(cedula)
        if veterinario is None:
            raise NoEncontradoError(
                f"No existe un veterinario con la cédula {cedula} en {self._nombre}."
            )
        return veterinario

    def obtener_servicio(self, codigo):
        texto = texto_obligatorio(codigo, "Tipo de servicio")
        servicio = self._servicios.get(texto.upper())
        if servicio is None:  # también se acepta el nombre del servicio
            for candidato in self._servicios.values():
                if candidato.nombre.lower() == texto.lower():
                    return candidato
            raise NoEncontradoError(
                f"{self._nombre} no ofrece el servicio '{texto}'. "
                "Usa el código o el nombre del catálogo."
            )
        return servicio

    def obtener_propietario(self, cedula):
        cedula = solo_digitos(cedula, "Cédula del propietario", 6, 10)
        propietario = self._propietarios.get(cedula)
        if propietario is None:
            raise NoEncontradoError(
                f"No existe un propietario con la cédula {cedula} en {self._nombre}."
            )
        return propietario

    def buscar_propietario(self, cedula):
        cedula = solo_digitos(cedula, "Cédula del propietario", 6, 10)
        return self._propietarios.get(cedula)

    def buscar_cita(self, codigo):
        return self._citas.get(codigo)

    # ---------- reglas de disponibilidad ----------
    def _cita_programada_veterinario(self, veterinario, fecha, hora):
        for cita in self._citas.values():
            if (cita.esta_programada() and cita.veterinario is veterinario
                    and cita.fecha == fecha and cita.hora == hora):
                return cita
        return None

    def asignar_veterinario(self, fecha, hora, cedula=None):
        """Devuelve el veterinario pedido (si está libre) o uno disponible."""
        if cedula:
            veterinario = self.obtener_veterinario(cedula)
            conflicto = self._cita_programada_veterinario(veterinario, fecha, hora)
            if conflicto:
                raise ConflictoHorarioError(
                    f"{veterinario.nombre} ya tiene la cita {conflicto.codigo} "
                    f"el {fecha.isoformat()} a las {hora.strftime('%H:%M')}."
                )
            return veterinario

        for veterinario in self._veterinarios.values():
            if self._cita_programada_veterinario(veterinario, fecha, hora) is None:
                return veterinario
        raise ConflictoHorarioError(
            f"No hay veterinarios disponibles el {fecha.isoformat()} "
            f"a las {hora.strftime('%H:%M')}."
        )

    def validar_mascota_libre(self, mascota, fecha, hora):
        for cita in self._citas.values():
            if (cita.esta_programada() and cita.mascota is mascota
                    and cita.fecha == fecha and cita.hora == hora):
                raise ConflictoHorarioError(
                    f"{mascota.nombre} ya tiene la cita {cita.codigo} "
                    f"el {fecha.isoformat()} a las {hora.strftime('%H:%M')}."
                )

    # ---------- consultas ----------
    def citas_en_fecha(self, fecha):
        citas = [c for c in self._citas.values() if c.fecha == fecha]
        return sorted(citas, key=lambda c: c.hora)

    def citas_de_mascota(self, mascota):
        citas = [c for c in self._citas.values() if c.mascota is mascota]
        return sorted(citas, key=lambda c: (c.fecha, c.hora))

    def __str__(self):
        return self._nombre


# ============================================
# DATOS: REPOSITORIO
# ============================================

class RepositorioClinicas:

    def __init__(self):
        self._clinicas = {}          # NIT -> Clinica
        self._contador_citas = 0
        self._contador_facturas = 0

    def existe(self, nit):
        return nit in self._clinicas

    def agregar(self, clinica):
        self._clinicas[clinica.nit] = clinica

    def obtener(self, nit):
        return self._clinicas.get(nit)

    def listar(self):
        return list(self._clinicas.values())

    def siguiente_codigo_cita(self):
        self._contador_citas += 1
        return f"CIT-{self._contador_citas:03d}"

    def siguiente_numero_factura(self):
        self._contador_facturas += 1
        return f"FAC-{self._contador_facturas:03d}"


# ============================================
# DATOS: EJEMPLO
# ============================================

DATOS_EJEMPLO = [
    {
        "nit": "901456789-1",
        "nombre": "Clínica Veterinaria Huellitas",
        "codigo_dane": "68679",
        "municipio": "San Gil",
        "departamento": "Santander",
        "direccion": "Calle 12 # 9-40",
        "barrio": "Centro",
        # (cédula, nombre, tarjeta profesional)
        "veterinarios": [
            ("63512478", "Juliana Ortiz Ramírez", "TP-18452"),
            ("91254863", "Mauricio Pinzón Gómez", "TP-20117"),
        ],
        # (código, nombre, tarifa)
        "servicios": [
            ("CG", "Consulta general", 60000),
            ("VAC", "Vacunación", 45000),
            ("DES", "Desparasitación", 30000),
            ("PEL", "Baño y peluquería", 50000),
        ],
    },
    {
        "nit": "900987654-3",
        "nombre": "Clínica Veterinaria Patitas Felices",
        "codigo_dane": "68276",
        "municipio": "Floridablanca",
        "departamento": "Santander",
        "direccion": "Carrera 27 # 30-15",
        "barrio": "Cañaveral",
        "veterinarios": [
            ("13745821", "Sergio Arenas Villamizar", "TP-15893"),
            ("37896542", "Diana Carolina Rey Moreno", "TP-22406"),
            ("1098654321", "Felipe Castellanos Díaz", "TP-31578"),
        ],
        "servicios": [
            ("CG", "Consulta general", 65000),
            ("VAC", "Vacunación", 48000),
            ("DES", "Desparasitación", 32000),
            ("ECO", "Ecografía", 120000),
        ],
    },
]


# ============================================
# LÓGICA: SERVICIO DE CLÍNICAS
# ============================================

class ServicioClinicas:

    def __init__(self, repositorio):
        self._repositorio = repositorio

    # ---------- utilidades internas ----------
    def _clinica(self, nit):
        nit = nit_valido(nit)
        clinica = self._repositorio.obtener(nit)
        if clinica is None:
            raise NoEncontradoError(f"No existe una clínica con el NIT {nit}.")
        return clinica

    def _clinica_operativa(self, nit):
        clinica = self._clinica(nit)
        if not clinica.puede_operar:
            raise ReglaNegocioError(
                f"{clinica.nombre} debe tener al menos un veterinario y un servicio "
                "registrados antes de registrar propietarios o tramitar citas."
            )
        return clinica

    def _buscar_cita(self, codigo):
        codigo = texto_obligatorio(codigo, "Código de la cita").upper()
        for clinica in self._repositorio.listar():
            cita = clinica.buscar_cita(codigo)
            if cita is not None:
                return clinica, cita
        raise NoEncontradoError(f"No existe una cita con el código {codigo}.")

    # ---------- 1. clínicas ----------
    def registrar_clinica(self, nit, nombre, codigo_dane, municipio,
                          departamento, direccion, barrio):
        nit = nit_valido(nit)
        if self._repositorio.existe(nit):
            raise DuplicadoError(f"Ya existe una clínica con el NIT {nit}.")
        clinica = Clinica(
            nit, nombre, Municipio(codigo_dane, municipio, departamento),
            direccion, barrio,
        )
        self._repositorio.agregar(clinica)
        return clinica

    def listar_clinicas(self):
        return self._repositorio.listar()

    # ---------- 2. veterinarios y servicios ----------
    def registrar_veterinario(self, nit, cedula, nombre, tarjeta_profesional):
        clinica = self._clinica(nit)
        veterinario = Veterinario(cedula, nombre, tarjeta_profesional)
        clinica.agregar_veterinario(veterinario)
        return veterinario

    def registrar_servicio(self, nit, codigo, nombre, tarifa):
        clinica = self._clinica(nit)
        servicio = Servicio(codigo, nombre, tarifa)
        clinica.agregar_servicio(servicio)
        return servicio

    # ---------- 3. propietarios y mascotas ----------
    def registrar_propietario(self, nit, cedula, nombre, telefono, municipio_residencia):
        clinica = self._clinica_operativa(nit)
        propietario = Propietario(cedula, nombre, telefono, municipio_residencia)
        clinica.agregar_propietario(propietario)
        return propietario

    def registrar_mascota(self, nit, cedula_propietario, nombre, especie,
                          raza, anio_nacimiento, peso):
        clinica = self._clinica_operativa(nit)
        propietario = clinica.obtener_propietario(cedula_propietario)
        mascota = Mascota(propietario, nombre, especie, raza, anio_nacimiento, peso)
        propietario.agregar_mascota(mascota)
        return mascota

    # ---------- 4. programar cita ----------
    def programar_cita(self, nit, cedula, nombre_propietario, telefono,
                       municipio_residencia, nombre_mascota, especie, raza,
                       anio_nacimiento, peso, fecha, hora, tipo_servicio):
        """Programa una cita a partir de los datos del dueño y de la mascota.

        - Si el propietario o la mascota no están registrados, se registran
          (solo si la cita se puede programar).
        - El veterinario disponible lo asigna el sistema.
        - El código de la cita lo genera el sistema.
        Devuelve (cita, propietario_nuevo, mascota_nueva).
        """
        clinica = self._clinica_operativa(nit)
        servicio = clinica.obtener_servicio(tipo_servicio)

        # Se arma todo primero y se guarda solo si las reglas se cumplen.
        propietario = clinica.buscar_propietario(cedula)
        propietario_nuevo = propietario is None
        if propietario_nuevo:
            propietario = Propietario(cedula, nombre_propietario, telefono,
                                      municipio_residencia)
        else:
            nombre = texto_obligatorio(nombre_propietario, "Nombre del propietario")
            if nombre.lower() != propietario.nombre.lower():
                raise DatoInvalidoError(
                    f"La cédula {propietario.cedula} está registrada a nombre de "
                    f"{propietario.nombre}, no de {nombre}."
                )

        mascota = None if propietario_nuevo else propietario.buscar_mascota(nombre_mascota)
        mascota_nueva = mascota is None
        if mascota_nueva:
            mascota = Mascota(propietario, nombre_mascota, especie, raza,
                              anio_nacimiento, peso)

        veterinario = clinica.asignar_veterinario(fecha, hora)
        if not mascota_nueva:
            clinica.validar_mascota_libre(mascota, fecha, hora)

        # Todas las reglas se cumplieron: ahora sí se guarda y se genera el código.
        if propietario_nuevo:
            clinica.agregar_propietario(propietario)
        if mascota_nueva:
            propietario.agregar_mascota(mascota)
        codigo = self._repositorio.siguiente_codigo_cita()
        cita = Cita(codigo, fecha, hora, mascota, veterinario, servicio)
        clinica.agregar_cita(cita)
        return cita, propietario_nuevo, mascota_nueva

    # ---------- 5. cancelar cita ----------
    def cancelar_cita(self, codigo, fecha_operacion=None):
        _, cita = self._buscar_cita(codigo)
        cita.cancelar(fecha_operacion or date.today())
        return cita

    # ---------- 6. atender cita y facturar ----------
    def atender_cita(self, codigo, codigos_adicionales=None, fecha_atencion=None):
        clinica, cita = self._buscar_cita(codigo)
        cita.verificar_atendible()
        adicionales = [clinica.obtener_servicio(c) for c in (codigos_adicionales or [])]
        numero = self._repositorio.siguiente_numero_factura()
        return cita.atender(numero, fecha_atencion or cita.fecha, adicionales)

    # ---------- 7 y 8. consultas ----------
    def consultar_citas_clinica(self, nit, fecha):
        return self._clinica(nit).citas_en_fecha(fecha)

    def consultar_historial_mascota(self, nit, cedula_propietario, nombre_mascota):
        clinica = self._clinica(nit)
        propietario = clinica.obtener_propietario(cedula_propietario)
        mascota = propietario.obtener_mascota(nombre_mascota)
        return mascota, clinica.citas_de_mascota(mascota)

    # ---------- datos de ejemplo ----------
    def cargar_datos_ejemplo(self):
        """Registra las clínicas de ejemplo; devuelve cuántas se cargaron."""
        cargadas = 0
        for datos in DATOS_EJEMPLO:
            if self._repositorio.existe(datos["nit"]):
                continue
            self.registrar_clinica(
                datos["nit"], datos["nombre"], datos["codigo_dane"],
                datos["municipio"], datos["departamento"],
                datos["direccion"], datos["barrio"],
            )
            for cedula, nombre, tarjeta in datos["veterinarios"]:
                self.registrar_veterinario(datos["nit"], cedula, nombre, tarjeta)
            for codigo, nombre, tarifa in datos["servicios"]:
                self.registrar_servicio(datos["nit"], codigo, nombre, tarifa)
            cargadas += 1
        return cargadas


# ============================================
# PRESENTACIÓN: INTERFAZ GRADIO
# ============================================

# --------------------------------------------
# Campos del formulario: (clave, etiqueta, tipo)
# --------------------------------------------
CAMPOS = [
    ("nit", "NIT de la clínica", "texto"),
    ("nombre_clinica", "Nombre de la clínica", "texto"),
    ("codigo_dane", "Código DANE del municipio", "texto"),
    ("municipio", "Municipio", "texto"),
    ("departamento", "Departamento", "texto"),
    ("direccion", "Dirección", "texto"),
    ("barrio", "Barrio", "texto"),
    ("cedula_vet", "Cédula del veterinario", "texto"),
    ("nombre_vet", "Nombre completo del veterinario", "texto"),
    ("tarjeta", "Tarjeta profesional", "texto"),
    ("codigo_serv", "Código del servicio", "texto"),
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
    ("servicio_cita", "Tipo de servicio (código o nombre)", "texto"),
    ("codigo_cita", "Código de la cita", "texto"),
    ("adicionales", "Servicios adicionales (códigos separados por coma)", "texto"),
    ("fecha_operacion", "Fecha de la operación (AAAA-MM-DD)", "texto"),
]

CLAVES = [c[0] for c in CAMPOS]

PLACEHOLDERS = {
    "nit": "901456789-1",
    "fecha": "2026-11-10",
    "hora": "09:00",
    "servicio_cita": "CG",
    "codigo_cita": "CIT-001",
    "adicionales": "VAC, DES",
    "fecha_operacion": "Opcional",
}

# Opción del menú -> campos que se muestran (clave: etiqueta alternativa o None)
OPCIONES = {
    "Cargar datos de ejemplo": {},
    "Registrar clínica": {
        "nit": None, "nombre_clinica": None, "codigo_dane": None,
        "municipio": None, "departamento": None, "direccion": None, "barrio": None,
    },
    "Registrar veterinario": {
        "nit": None, "cedula_vet": None, "nombre_vet": None, "tarjeta": None,
    },
    "Registrar servicio": {
        "nit": None, "codigo_serv": None, "nombre_serv": None, "tarifa": None,
    },
    "Registrar propietario": {
        "nit": None, "cedula_prop": None, "nombre_prop": None,
        "telefono": None, "municipio_res": None,
    },
    "Registrar mascota": {
        "nit": None, "cedula_prop": None, "nombre_masc": None, "especie": None,
        "raza": None, "anio": None, "peso": None,
    },
    "Programar cita": {
        "nit": None,
        "cedula_prop": "Cédula del dueño de la mascota",
        "nombre_prop": "Nombre del dueño",
        "telefono": "Teléfono del dueño (solo si es la primera vez)",
        "municipio_res": "Municipio de residencia del dueño (solo si es la primera vez)",
        "nombre_masc": None, "especie": None, "raza": None,
        "anio": None, "peso": None,
        "fecha": None, "hora": None, "servicio_cita": None,
    },
    "Cancelar cita": {
        "codigo_cita": None,
        "fecha_operacion": "Fecha de cancelación (AAAA-MM-DD; opcional, por defecto hoy)",
    },
    "Atender cita": {
        "codigo_cita": None, "adicionales": None,
        "fecha_operacion": "Fecha de atención (AAAA-MM-DD; opcional, por defecto la fecha de la cita)",
    },
    "Consultar citas de una clínica": {
        "nit": None, "fecha": "Fecha a consultar (AAAA-MM-DD)",
    },
    "Consultar historial de una mascota": {
        "nit": None, "cedula_prop": None, "nombre_masc": None,
    },
}

OPCION_INICIAL = "Cargar datos de ejemplo"


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


class GestorVistaVeterinaria:

    def __init__(self, servicio):
        self._servicio = servicio
        self._acciones = {
            "Cargar datos de ejemplo": self._cargar_ejemplo,
            "Registrar clínica": self._registrar_clinica,
            "Registrar veterinario": self._registrar_veterinario,
            "Registrar servicio": self._registrar_servicio,
            "Registrar propietario": self._registrar_propietario,
            "Registrar mascota": self._registrar_mascota,
            "Programar cita": self._programar_cita,
            "Cancelar cita": self._cancelar_cita,
            "Atender cita": self._atender_cita,
            "Consultar citas de una clínica": self._consultar_citas,
            "Consultar historial de una mascota": self._consultar_historial,
        }

    def iniciar_sistema(self):
        self._construir_interfaz().launch()

    # --------------------------------------------
    # Tabla principal (presentación)
    # --------------------------------------------
    def _tabla_clinicas(self):
        return [
            [
                c.nit,
                c.nombre,
                str(c.municipio),
                f"{c.direccion}, {c.barrio}",
                len(c.veterinarios),
                len(c.servicios),
                len(c.propietarios),
                len(c.citas),
            ]
            for c in self._servicio.listar_clinicas()
        ]

    # --------------------------------------------
    # Acciones: cada una devuelve (mensaje, DataFrame o None)
    # --------------------------------------------
    def _cargar_ejemplo(self, d):
        cargadas = self._servicio.cargar_datos_ejemplo()
        if cargadas == 0:
            return "Los datos de ejemplo ya estaban cargados.", None
        return f"Se cargaron {cargadas} clínica(s) de ejemplo con sus veterinarios y servicios.", None

    def _registrar_clinica(self, d):
        clinica = self._servicio.registrar_clinica(
            d["nit"], d["nombre_clinica"], d["codigo_dane"], d["municipio"],
            d["departamento"], d["direccion"], d["barrio"],
        )
        return f"Clínica **{clinica.nombre}** registrada.", None

    def _registrar_veterinario(self, d):
        vet = self._servicio.registrar_veterinario(
            d["nit"], d["cedula_vet"], d["nombre_vet"], d["tarjeta"]
        )
        return f"Veterinario **{vet.nombre}** registrado.", None

    def _registrar_servicio(self, d):
        serv = self._servicio.registrar_servicio(
            d["nit"], d["codigo_serv"], d["nombre_serv"], d["tarifa"]
        )
        return f"Servicio **{serv.nombre}** ({serv.codigo}) registrado con tarifa {pesos(serv.tarifa)}.", None

    def _registrar_propietario(self, d):
        prop = self._servicio.registrar_propietario(
            d["nit"], d["cedula_prop"], d["nombre_prop"], d["telefono"], d["municipio_res"]
        )
        return f"Propietario **{prop.nombre}** registrado. Ahora puedes registrar sus mascotas.", None

    def _registrar_mascota(self, d):
        masc = self._servicio.registrar_mascota(
            d["nit"], d["cedula_prop"], d["nombre_masc"], d["especie"],
            d["raza"], d["anio"], d["peso"],
        )
        return f"Mascota **{masc.nombre}** registrada para {masc.propietario.nombre}.", None

    def _programar_cita(self, d):
        fecha = a_fecha(d["fecha"])
        hora = a_hora(d["hora"])
        cita, prop_nuevo, masc_nueva = self._servicio.programar_cita(
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
            f"Cita programada.  \n"
            f"## Código de la cita: {cita.codigo}  \n"
            f" **Guarda este código**: lo necesitarás para cancelar o atender la cita "
            f"y para cualquier cambio futuro.  \n\n"
            f"Mascota: {cita.mascota.nombre} · Servicio: {cita.servicio.nombre} · "
            f"Fecha: {fecha.isoformat()} a las {hora.strftime('%H:%M')} · "
            f"Veterinario asignado: {cita.veterinario.nombre}{registro}"
        )
        return mensaje, None

    def _cancelar_cita(self, d):
        fecha = a_fecha_opcional(d["fecha_operacion"], "Fecha de cancelación")
        cita = self._servicio.cancelar_cita(d["codigo_cita"], fecha)
        return f" La cita **{cita.codigo}** quedó en estado **{cita.estado.value}**.", None

    def _atender_cita(self, d):
        fecha = a_fecha_opcional(d["fecha_operacion"], "Fecha de atención")
        codigos = [c.strip() for c in (d["adicionales"] or "").split(",") if c.strip()]
        factura = self._servicio.atender_cita(d["codigo_cita"], codigos, fecha)
        filas = [[s.codigo, s.nombre, pesos(s.tarifa)] for s in factura.servicios]
        filas.append(["", "TOTAL", pesos(factura.total)])
        tabla = pd.DataFrame(filas, columns=["Código", "Servicio", "Tarifa"])
        mensaje = (
            f" Cita atendida. **Factura {factura.numero}** — {factura.fecha.isoformat()}  \n"
            f"Propietario: {factura.propietario.nombre} (CC {factura.propietario.cedula}) · "
            f"Mascota: {factura.mascota.nombre} ({factura.mascota.especie})  \n"
            f"**Total: {pesos(factura.total)}**"
        )
        return mensaje, tabla

    def _consultar_citas(self, d):
        fecha = a_fecha(d["fecha"])
        citas = self._servicio.consultar_citas_clinica(d["nit"], fecha)
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
        if not citas:
            return f" No hay citas el {fecha.isoformat()}.", None
        return f" {len(citas)} cita(s) el {fecha.isoformat()}.", tabla

    def _consultar_historial(self, d):
        mascota, citas = self._servicio.consultar_historial_mascota(
            d["nit"], d["cedula_prop"], d["nombre_masc"]
        )
        if not citas:
            return f" {mascota.nombre} aún no tiene citas.", None
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
        return f" Historial de {mascota.nombre}: {len(citas)} cita(s).", tabla

    # --------------------------------------------
    # Botón Ejecutar
    # --------------------------------------------
    def ejecutar(self, opcion, *valores):
        datos = dict(zip(CLAVES, valores))
        tabla = None
        try:
            if opcion not in self._acciones:
                raise DatoInvalidoError("Selecciona una opción.")
            mensaje, tabla = self._acciones[opcion](datos)
        except ClinicaVeterinariaError as error:
            mensaje = f" {error}"
        except Exception as error:  # imprevistos: la aplicación no se detiene
            mensaje = f" Ocurrió un error inesperado: {error}"

        if tabla is None:
            resultado = gr.update(visible=False)
        else:
            resultado = gr.update(value=tabla, visible=True)
        return self._tabla_clinicas(), mensaje, resultado

    # --------------------------------------------
    # Mostrar / ocultar campos según la opción
    # --------------------------------------------
    def cambiar_opcion(self, opcion):
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
        return cambios + [gr.update(visible=False), ""]

    # --------------------------------------------
    # Interfaz Gradio (una sola sección)
    # --------------------------------------------
    def _construir_interfaz(self):
        with gr.Blocks(title="Gestión de citas veterinarias") as app:

            gr.Markdown("# Gestión de citas veterinarias")

            # PRESENTACIÓN: tabla de clínicas
            tabla = gr.Dataframe(
                headers=["NIT", "Clínica", "Municipio", "Dirección",
                         "Veterinarios", "Servicios", "Propietarios", "Citas"],
                value=self._tabla_clinicas(),
                interactive=False,
            )

            # MENÚ DESPLEGABLE DE OPCIONES
            opcion = gr.Dropdown(
                choices=list(OPCIONES.keys()),
                value=OPCION_INICIAL,
                label="Opción",
            )

            # CAMPOS (visibles según la opción elegida)
            componentes = []
            for clave, etiqueta, tipo in CAMPOS:
                visible = clave in OPCIONES[OPCION_INICIAL]
                if tipo == "texto":
                    comp = gr.Textbox(
                        label=etiqueta, visible=visible,
                        placeholder=PLACEHOLDERS.get(clave, ""),
                    )
                elif tipo == "entero":
                    comp = gr.Number(label=etiqueta, precision=0, visible=visible)
                else:
                    comp = gr.Number(label=etiqueta, visible=visible)
                componentes.append(comp)

            # BOTÓN EJECUTAR
            boton_ejecutar = gr.Button("Ejecutar", variant="primary")

            # RESULTADOS
            mensaje = gr.Markdown()
            resultado = gr.Dataframe(interactive=False, visible=False)

            # EVENTOS
            opcion.change(
                self.cambiar_opcion,
                inputs=opcion,
                outputs=componentes + [resultado, mensaje],
            )
            boton_ejecutar.click(
                self.ejecutar,
                inputs=[opcion] + componentes,
                outputs=[tabla, mensaje, resultado],
            )

        return app


# ============================================
# MAIN
# ============================================

class Main:

    @staticmethod
    def iniciar():
        repositorio = RepositorioClinicas()
        servicio = ServicioClinicas(repositorio)
        vista = GestorVistaVeterinaria(servicio)
        vista.iniciar_sistema()


if __name__ == "__main__":
    Main.iniciar()
