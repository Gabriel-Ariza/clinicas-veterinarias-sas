from resources.excepciones import DuplicadoError, NoEncontradoError
from resources.validaciones import solo_digitos, texto_obligatorio


class Propietario:
    """Propietario de una o varias mascotas (agregación de Mascota)."""

    def __init__(self, cedula, nombre, telefono, municipio_residencia):
        self._cedula = solo_digitos(cedula, "Cédula del propietario", 6, 10)
        self._nombre = texto_obligatorio(nombre, "Nombre del propietario")
        self._telefono = solo_digitos(telefono, "Teléfono", 7, 10)
        self._municipio_residencia = texto_obligatorio(
            municipio_residencia, "Municipio de residencia"
        )
        self._mascotas = {}  # nombre en minúsculas -> Mascota

    @property
    def cedula(self):
        return self._cedula

    @property
    def nombre(self):
        return self._nombre

    @property
    def telefono(self):
        return self._telefono

    @property
    def municipio_residencia(self):
        return self._municipio_residencia

    @property
    def mascotas(self):
        return list(self._mascotas.values())

    def agregar_mascota(self, mascota):
        clave = mascota.nombre.lower()
        if clave in self._mascotas:
            raise DuplicadoError(
                f"{self._nombre} ya tiene una mascota llamada '{mascota.nombre}'."
            )
        self._mascotas[clave] = mascota

    def buscar_mascota(self, nombre):
        nombre = texto_obligatorio(nombre, "Nombre de la mascota")
        return self._mascotas.get(nombre.lower())

    def obtener_mascota(self, nombre):
        nombre = texto_obligatorio(nombre, "Nombre de la mascota")
        mascota = self._mascotas.get(nombre.lower())
        if mascota is None:
            raise NoEncontradoError(
                f"{self._nombre} no tiene una mascota llamada '{nombre}'."
            )
        return mascota

    def __str__(self):
        return self._nombre
