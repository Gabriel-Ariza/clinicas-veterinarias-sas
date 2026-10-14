from typing import List, Optional
from entity.clinica import Clinica

class ClinicaRepository:
    def __init__(self):
        # Esta lista es nuestra "base de datos" principal en memoria
        self._clinicas: List[Clinica] = []

    def guardar(self, clinica: Clinica) -> None:
        """Guarda una nueva clínica en el repositorio."""
        self._clinicas.append(clinica)

    def buscar_por_nit(self, nit: str) -> Optional[Clinica]:
        """
        Busca una clínica por su NIT.
        Retorna el objeto Clinica si lo encuentra, o None si no existe.
        """
        for clinica in self._clinicas:
            if clinica.nit == nit:
                return clinica
        return None

    def obtener_todas(self) -> List[Clinica]:
        """Retorna la lista completa de clínicas registradas."""
        return self._clinicas