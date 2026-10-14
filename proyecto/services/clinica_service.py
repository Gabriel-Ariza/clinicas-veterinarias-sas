"""Servicio de clínicas: registro de clínicas, veterinarios, servicios, propietarios y mascotas."""

from repository.entity.Clinica import Clinica
from repository.entity.Mascota import Mascota
from repository.entity.Municipio import Municipio
from repository.entity.Propietario import Propietario
from repository.entity.Servicio import Servicio
from repository.entity.Veterinario import Veterinario
from resources.datos_ejemplo import DATOS_EJEMPLO
from resources.excepciones import DuplicadoError, NoEncontradoError, ReglaNegocioError
from resources.validaciones import nit_valido


class ClinicaService:

    def __init__(self, repositorio):
        self._repositorio = repositorio

    # ---------- consulta de clínicas ----------
    def obtener_clinica(self, nit):
        nit = nit_valido(nit)
        clinica = self._repositorio.obtener(nit)
        if clinica is None:
            raise NoEncontradoError(f"No existe una clínica con el NIT {nit}.")
        return clinica

    def obtener_clinica_operativa(self, nit):
        clinica = self.obtener_clinica(nit)
        if not clinica.puede_operar:
            raise ReglaNegocioError(
                f"{clinica.nombre} debe tener al menos un veterinario y un servicio "
                "registrados antes de registrar propietarios o tramitar citas."
            )
        return clinica

    def listar_clinicas(self):
        return self._repositorio.listar()

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

    def registrar_veterinario(self, nit, cedula, nombre, tarjeta_profesional):
        clinica = self.obtener_clinica(nit)
        veterinario = Veterinario(cedula, nombre, tarjeta_profesional)
        clinica.agregar_veterinario(veterinario)
        return veterinario

    def registrar_servicio(self, nit, codigo, nombre, tarifa):
        clinica = self.obtener_clinica(nit)
        servicio = Servicio(codigo, nombre, tarifa)
        clinica.agregar_servicio(servicio)
        return servicio

    def registrar_propietario(self, nit, cedula, nombre, telefono, municipio_residencia):
        clinica = self.obtener_clinica_operativa(nit)
        propietario = Propietario(cedula, nombre, telefono, municipio_residencia)
        clinica.agregar_propietario(propietario)
        return propietario

    def registrar_mascota(self, nit, cedula_propietario, nombre, especie,
                          raza, anio_nacimiento, peso):
        clinica = self.obtener_clinica_operativa(nit)
        propietario = clinica.obtener_propietario(cedula_propietario)
        mascota = Mascota(propietario, nombre, especie, raza, anio_nacimiento, peso)
        propietario.agregar_mascota(mascota)
        return mascota

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
