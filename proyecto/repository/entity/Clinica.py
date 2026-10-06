class Clinica:
    def __init__(self, nit: str, nombre: str, codigo_dane: str):
        self._nit = nit
        self._nombre = nombre
        self._codigo_dane = codigo_dane
        self._veterinarios = []
        self._servicios = []
        self._citas = []

    @property
    def nit(self) -> str:
        return self._nit

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def citas(self) -> list:
        return self._citas