class MainController:
    def __init__(self, clinica_service, cita_service):
        self._clinica_service = clinica_service
        self._cita_service = cita_service

    def ejecutar_menu(self):
        while True:
            print("\n--- SISTEMA DE GESTIÓN VETERINARIA ---")
            print("1. Registrar Clínica")
            print("2. Programar Cita")
            print("3. Cargar Datos de Prueba Automáticos")
            print("4. Salir")
            
            opcion = input("Seleccione una opción: ")
            
            if opcion == "1":
                # Lógica de captura por consola
                pass
            elif opcion == "3":
                print("Cargando datos de prueba (Huellitas y Patitas Felices)...")
                # Llamar método que puebla repositorios
            elif opcion == "4":
                break