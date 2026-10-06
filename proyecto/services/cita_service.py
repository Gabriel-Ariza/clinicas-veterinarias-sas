class CitaService:
    def __init__(self, clinica_repository):
        self._clinica_repo = clinica_repository  # Inversión de dependencias (DIP)

    def programar_cita(self, nit_clinica: str, nueva_cita):
        clinica = self._clinica_repo.buscar_por_nit(nit_clinica)
        if not clinica:
            raise ValueError("La clínica no existe.")
        
        # Validar regla de negocio: Cruce de horarios de veterinario o mascota
        for cita in clinica.citas:
            if cita.fecha_hora == nueva_cita.fecha_hora and cita.estado == "Programada":
                if cita.veterinario.cedula == nueva_cita.veterinario.cedula:
                    raise ValueError("El veterinario ya tiene una cita a esa hora.")
                if cita.mascota.id == nueva_cita.mascota.id:
                    raise ValueError("La mascota ya tiene una cita programada a esa hora.")
        
        clinica.citas.append(nueva_cita)
        return True