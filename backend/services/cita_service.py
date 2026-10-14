from typing import List
from repository.clinica_repository import ClinicaRepository
from entity.cita import Cita
from entity.servicio import Servicio
from entity.factura import Factura

class CitaService:
    def __init__(self, clinica_repo: ClinicaRepository):
        # Inyección de dependencias: El servicio necesita el repositorio para buscar datos
        self._clinica_repo = clinica_repo

    def programar_cita(self, nit_clinica: str, nueva_cita: Cita) -> bool:
        clinica = self._clinica_repo.buscar_por_nit(nit_clinica)
        if not clinica:
            raise ValueError("Error: Clínica no encontrada.")

        # Reglas de negocio 2 y 3: Validar cruce de horarios para Veterinario y Mascota
        for cita_existente in clinica.citas:
            if cita_existente.estado == "Programada" and cita_existente.fecha == nueva_cita.fecha and cita_existente.hora == nueva_cita.hora:
                if cita_existente.veterinario.cedula == nueva_cita.veterinario.cedula:
                    raise ValueError(f"Error: El veterinario {nueva_cita.veterinario.nombre} ya tiene una cita en ese horario.")
                if cita_existente.mascota.nombre == nueva_cita.mascota.nombre:
                    raise ValueError(f"Error: La mascota {nueva_cita.mascota.nombre} ya tiene una cita en ese horario.")

        # Si pasa las validaciones, se agrega al historial de la clínica
        clinica.agregar_cita(nueva_cita)
        return True

    def cancelar_cita(self, nit_clinica: str, codigo_cita: str) -> bool:
        clinica = self._clinica_repo.buscar_por_nit(nit_clinica)
        if not clinica:
            raise ValueError("Error: Clínica no encontrada.")

        # Buscar la cita en el historial
        cita_encontrada = None
        for cita in clinica.citas:
            if cita.codigo == codigo_cita:
                cita_encontrada = cita
                break

        if not cita_encontrada:
            raise ValueError("Error: Cita no encontrada.")

        # Regla de negocio 4: Solo se cancelan citas "Programadas"
        if cita_encontrada.estado != "Programada":
            raise ValueError(f"Error: La cita no se puede cancelar porque está en estado '{cita_encontrada.estado}'.")

        # Cambiamos el estado
        cita_encontrada.cancelar()
        return True

    def atender_cita(self, nit_clinica: str, codigo_cita: str, servicios_extra: List[Servicio], numero_factura: str) -> Factura:
        clinica = self._clinica_repo.buscar_por_nit(nit_clinica)
        if not clinica:
            raise ValueError("Error: Clínica no encontrada.")

        # Buscar la cita
        cita_encontrada = None
        for cita in clinica.citas:
            if cita.codigo == codigo_cita:
                cita_encontrada = cita
                break

        if not cita_encontrada:
            raise ValueError("Error: Cita no encontrada.")

        # Regla de negocio 5: Solo se atienden citas "Programadas"
        if cita_encontrada.estado != "Programada":
            raise ValueError(f"Error: La cita no se puede atender porque está en estado '{cita_encontrada.estado}'.")

        # Bloque opcional (opt): Agregar servicios adicionales
        if servicios_extra:
            for servicio in servicios_extra:
                cita_encontrada.agregar_servicio_adicional(servicio)

        # Cambiamos el estado a Atendida
        cita_encontrada.atender()

        # Generamos y retornamos la factura (Regla 6)
        factura_generada = cita_encontrada.generar_factura(numero_factura)
        return factura_generada