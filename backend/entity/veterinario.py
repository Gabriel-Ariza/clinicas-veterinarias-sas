class Veterinario:
    def __init__(self, cedula: str, nombre: str, tarjeta_profesional: str):
        self._cedula = cedula
        self._nombre = nombre
        self._tarjeta_profesional = tarjeta_profesional

    @property
    def cedula(self) -> str:
        return self._cedula

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def tarjeta_profesional(self) -> str:
        return self._tarjeta_profesional