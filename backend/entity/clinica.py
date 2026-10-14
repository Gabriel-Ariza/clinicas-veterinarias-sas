from typing import List
from entity.veterinario import Veterinario
from entity.servicio import Servicio
from entity.propietario import Propietario
from entity.cita import Cita

class Clinica:
    def __init__(self, nit: str, nombre: str, codigo_dane: str, departamento: str, direccion: str, barrio: str, password: str = "1234"):
        self._nit = nit
        self._nombre = nombre
        self._codigo_dane = codigo_dane
        self._departamento = departamento
        self._direccion = direccion
        self._barrio = barrio
        self._password = password  # <-- Atributo nuevo para el login
        self._veterinarios: List[Veterinario] = []
        self._servicios: List[Servicio] = []
        self._propietarios: List[Propietario] = []
        self._citas: List[Cita] = []

    @property
    def nit(self) -> str:
        return self._nit

    @property
    def nombre(self) -> str:
        return self._nombre
        
    @property
    def codigo_dane(self) -> str:
        return self._codigo_dane

    @property
    def departamento(self) -> str:
        return self._departamento

    @property
    def direccion(self) -> str:
        return self._direccion

    @property
    def barrio(self) -> str:
        return self._barrio

    @property
    def password(self) -> str:  # <-- Getter nuevo para validar el login
        return self._password

    @property
    def veterinarios(self) -> List[Veterinario]:
        return self._veterinarios

    @property
    def servicios(self) -> List[Servicio]:
        return self._servicios

    @property
    def propietarios(self) -> List[Propietario]:
        return self._propietarios

    @property
    def citas(self) -> List[Cita]:
        return self._citas

    def registrar_veterinario(self, vet: Veterinario) -> None:
        self._veterinarios.append(vet)

    def registrar_servicio(self, serv: Servicio) -> None:
        self._servicios.append(serv)

    def registrar_propietario(self, prop: Propietario) -> None:
        self._propietarios.append(prop)

    def agregar_cita(self, cita: Cita) -> None:
        self._citas.append(cita)