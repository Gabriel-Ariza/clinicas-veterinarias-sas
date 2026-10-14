"""Punto de entrada de la aplicación."""

from controllers.menuController import MenuController
from repository.clinica_repository import ClinicaRepository
from services.cita_service import CitaService
from services.clinica_service import ClinicaService


class Main:

    @staticmethod
    def iniciar():
        repositorio = ClinicaRepository()
        clinica_service = ClinicaService(repositorio)
        cita_service = CitaService(repositorio, clinica_service)

        # Las clínicas de ejemplo aparecen desde el inicio.
        clinica_service.cargar_datos_ejemplo()

        menu = MenuController(clinica_service, cita_service)
        menu.iniciar_sistema()


if __name__ == "__main__":
    Main.iniciar()
    
