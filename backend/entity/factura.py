from typing import List
from entity.servicio import Servicio

class Factura:
    def __init__(self, numero: str, fecha_emision: str, detalle_servicios: List[Servicio]):
        self._numero = numero
        self._fecha_emision = fecha_emision
        self._detalle_servicios = detalle_servicios
        self._valor_total = self.calcular_total()

    @property
    def numero(self) -> str:
        return self._numero

    @property
    def fecha_emision(self) -> str:
        return self._fecha_emision

    @property
    def detalle_servicios(self) -> List[Servicio]:
        return self._detalle_servicios

    @property
    def valor_total(self) -> float:
        return self._valor_total

    def calcular_total(self) -> float:
        total = 0.0
        for servicio in self._detalle_servicios:
            total += servicio.tarifa
        return total