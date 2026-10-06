from repository.clinica_repository import ClinicaRepository
from services.cita_service import CitaService
from controllers.menuController import MainController

def main():
    # Inicialización de dependencias (como un Spring IoC container manual)
    clinica_repo = ClinicaRepository()
    cita_service = CitaService(clinica_repo)
    
    # Aquí puedes pasar servicios al controlador
    controller = MainController(None, cita_service)
    controller.ejecutar_menu()

if __name__ == "__main__":
    main()