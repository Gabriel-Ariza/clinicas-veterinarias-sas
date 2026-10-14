from datetime import date

from resources.excepciones import DatoInvalidoError
from resources.validaciones import numero_positivo, texto_obligatorio


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
