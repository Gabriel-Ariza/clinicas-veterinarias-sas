from resources.validaciones import numero_positivo, texto_obligatorio


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
