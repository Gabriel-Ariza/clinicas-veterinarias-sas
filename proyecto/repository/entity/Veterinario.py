from resources.validaciones import solo_digitos, texto_obligatorio


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
