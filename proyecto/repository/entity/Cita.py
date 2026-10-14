from enum import Enum

from resources.excepciones import EstadoCitaInvalidoError, ReglaNegocioError
from repository.entity.Factura import Factura


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
