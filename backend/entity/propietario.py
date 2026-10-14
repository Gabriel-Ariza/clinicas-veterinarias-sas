from typing import List
from entity.mascota import Mascota

class Propietario:
    def __init__(self, cedula: str, nombre: str, telefono: str, municipio: str):
        self._cedula = cedula
        self._nombre = nombre
        self._telefono = telefono
        self._municipio = municipio
        self._mascotas: List[Mascota] = []

    @property
    def cedula(self) -> str:
        return self._cedula

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def telefono(self) -> str:
        return self._telefono

    @property
    def municipio(self) -> str:
        return self._municipio

    @property
    def mascotas(self) -> List[Mascota]:
        return self._mascotas

    def agregar_mascota(self, mascota: Mascota) -> None:
        self._mascotas.append(mascota)