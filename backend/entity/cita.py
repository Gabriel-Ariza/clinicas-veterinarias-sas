from typing import List, Optional
from entity.mascota import Mascota
from entity.veterinario import Veterinario
from entity.servicio import Servicio
from entity.factura import Factura

class Cita:
    def __init__(self, codigo: str, fecha: str, hora: str, mascota: Mascota, veterinario: Veterinario):
        self._codigo = codigo
        self._fecha = fecha
        self._hora = hora
        self._estado = "Programada"  # Estado inicial por defecto
        self._mascota = mascota
        self._veterinario = veterinario
        self._servicios: List[Servicio] = []
        self._factura: Optional[Factura] = None

    @property
    def codigo(self) -> str:
        return self._codigo

    @property
    def fecha(self) -> str:
        return self._fecha

    @property
    def hora(self) -> str:
        return self._hora

    @property
    def estado(self) -> str:
        return self._estado

    @property
    def mascota(self) -> Mascota:
        return self._mascota

    @property
    def veterinario(self) -> Veterinario:
        return self._veterinario

    @property
    def servicios(self) -> List[Servicio]:
        return self._servicios
        
    @property
    def factura(self) -> Optional[Factura]:
        return self._factura

    def agregar_servicio_adicional(self, servicio: Servicio) -> None:
        self._servicios.append(servicio)

    def cancelar(self) -> None:
        self._estado = "Cancelada"

    def atender(self) -> None:
        self._estado = "Atendida"

    def generar_factura(self, numero_factura: str) -> Factura:
        self._factura = Factura(numero_factura, self._fecha, self._servicios)
        return self._factura