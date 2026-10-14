class Servicio:
    def __init__(self, codigo: str, nombre: str, tarifa: float):
        self._codigo = codigo
        self._nombre = nombre
        self._tarifa = tarifa

    @property
    def codigo(self) -> str:
        return self._codigo

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def tarifa(self) -> float:
        return self._tarifa