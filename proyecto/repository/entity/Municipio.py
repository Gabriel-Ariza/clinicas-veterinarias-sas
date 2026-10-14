from resources.validaciones import solo_digitos, texto_obligatorio


class Municipio:

    def __init__(self, codigo_dane, nombre, departamento):
        self._codigo_dane = solo_digitos(codigo_dane, "Código DANE", 5, 5)
        self._nombre = texto_obligatorio(nombre, "Municipio")
        self._departamento = texto_obligatorio(departamento, "Departamento")

    @property
    def codigo_dane(self):
        return self._codigo_dane

    @property
    def nombre(self):
        return self._nombre

    @property
    def departamento(self):
        return self._departamento

    def __str__(self):
        return f"{self._nombre}, {self._departamento}"
