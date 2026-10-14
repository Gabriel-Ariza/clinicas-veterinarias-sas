class Mascota:
    def __init__(self, nombre: str, especie: str, raza: str, anio_nacimiento: int, peso: float):
        self._nombre = nombre
        self._especie = especie
        self._raza = raza
        self._anio_nacimiento = anio_nacimiento
        self._peso = peso

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def especie(self) -> str:
        return self._especie

    @property
    def raza(self) -> str:
        return self._raza

    @property
    def anio_nacimiento(self) -> int:
        return self._anio_nacimiento

    @property
    def peso(self) -> float:
        return self._peso