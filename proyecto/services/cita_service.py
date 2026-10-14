"""Servicio de citas: programar, cancelar, atender (facturar) y consultar."""

from datetime import date

from repository.entity.Cita import Cita
from repository.entity.Mascota import Mascota
from repository.entity.Propietario import Propietario
from resources.excepciones import DatoInvalidoError, NoEncontradoError
from resources.validaciones import texto_obligatorio


class CitaService:

    def __init__(self, repositorio, clinica_service):
        self._repositorio = repositorio
        self._clinica_service = clinica_service

    def _buscar_cita(self, codigo, nit=None):
        codigo = texto_obligatorio(codigo, "Código de la cita").upper()
        if nit:  # la cita debe pertenecer a la clínica seleccionada
            clinica = self._clinica_service.obtener_clinica(nit)
            cita = clinica.buscar_cita(codigo)
            if cita is None:
                raise NoEncontradoError(
                    f"No existe una cita con el código {codigo} en {clinica.nombre}."
                )
            return clinica, cita
        for clinica in self._repositorio.listar():
            cita = clinica.buscar_cita(codigo)
            if cita is not None:
                return clinica, cita
        raise NoEncontradoError(f"No existe una cita con el código {codigo}.")

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
        clinica = self._clinica_service.obtener_clinica_operativa(nit)
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

    def cancelar_cita(self, codigo, fecha_operacion=None, nit=None):
        _, cita = self._buscar_cita(codigo, nit)
        cita.cancelar(fecha_operacion or date.today())
        return cita

    def atender_cita(self, codigo, codigos_adicionales=None, fecha_atencion=None,
                     nit=None):
        clinica, cita = self._buscar_cita(codigo, nit)
        cita.verificar_atendible()
        adicionales = [clinica.obtener_servicio(c) for c in (codigos_adicionales or [])]
        numero = self._repositorio.siguiente_numero_factura()
        return cita.atender(numero, fecha_atencion or cita.fecha, adicionales)

    def consultar_citas_clinica(self, nit, fecha):
        return self._clinica_service.obtener_clinica(nit).citas_en_fecha(fecha)

    def consultar_historial_mascota(self, nit, cedula_propietario, nombre_mascota):
        clinica = self._clinica_service.obtener_clinica(nit)
        propietario = clinica.obtener_propietario(cedula_propietario)
        mascota = propietario.obtener_mascota(nombre_mascota)
        return mascota, clinica.citas_de_mascota(mascota)
