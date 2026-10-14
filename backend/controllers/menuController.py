from services.cita_service import CitaService
from repository.clinica_repository import ClinicaRepository
from entity.clinica import Clinica
from entity.veterinario import Veterinario
from entity.servicio import Servicio
from entity.propietario import Propietario
from entity.mascota import Mascota
from entity.cita import Cita

class MainController:
    def __init__(self, clinica_service, cita_service: CitaService, clinica_repo: ClinicaRepository):
        self._cita_service = cita_service
        self._clinica_repo = clinica_repo

    def cargar_datos_prueba(self):
        """Carga exactamente los datos del Caso 1 del parcial"""
        huellitas = Clinica("901456789-1", "Clínica Veterinaria Huellitas", "68679", "Santander", "Calle 12 # 9-40", "Centro")
        patitas = Clinica("900987654-3", "Clínica Veterinaria Patitas Felices", "68276", "Santander", "Carrera 27 # 30-15", "Cañaveral")

        # Catálogos
        juliana = Veterinario("63512478", "Juliana Ortiz Ramírez", "TP-18452")
        serv_cg = Servicio("CG", "Consulta general", 60000.0)
        serv_vac = Servicio("VAC", "Vacunación", 45000.0)

        # Propietario y mascota
        laura = Propietario("1098765432", "Laura Méndez Plata", "3157894561", "Bucaramanga")
        rocky = Mascota("Rocky", "perro", "criolla", 2023, 18.0)
        laura.agregar_mascota(rocky)

        # Inyectar datos en la clínica
        huellitas.registrar_veterinario(juliana)
        huellitas.registrar_servicio(serv_cg)
        huellitas.registrar_servicio(serv_vac)
        huellitas.registrar_propietario(laura)

        # Crear la cita inicial de Rocky en estado "Programada"
        cita001 = Cita("CIT-001", "10 de noviembre de 2026", "9:00 a. m.", rocky, juliana)
        cita001.agregar_servicio_adicional(serv_cg)  # La cita base incluye consulta general
        huellitas.agregar_cita(cita001)

        # Guardar en la base de datos (repositorio)
        self._clinica_repo.guardar(huellitas)
        self._clinica_repo.guardar(patitas)
        print("=== Datos de prueba cargados exitosamente en memoria ===")

    def ejecutar_menu(self):
        while True:
            print("\n" + "="*30)
            print("🏥 SISTEMA VETERINARIO 🏥")
            print("="*30)
            print("1. Programar Cita (Pendiente UI)")
            print("2. Cancelar Cita (Probar Casos 3 y 4)")
            print("3. Atender Cita y Facturar (Probar Caso 1)")
            print("4. Salir")
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                print("\n[Módulo en construcción...]")
                
            elif opcion == "2":
                print("\n--- CANCELAR CITA ---")
                nit = input("NIT de la clínica (Ej. 901456789-1): ")
                codigo = input("Código de la cita (Ej. CIT-001): ")
                try:
                    self._cita_service.cancelar_cita(nit, codigo)
                    print("✅ ÉXITO: ¡Cita cancelada correctamente!")
                except ValueError as e:
                    print(f"❌ {e}")

            elif opcion == "3":
                print("\n--- ATENDER CITA ---")
                nit = input("NIT de la clínica (Ej. 901456789-1): ")
                codigo = input("Código de la cita (Ej. CIT-001): ")
                
                print("\n¿Desea agregar el servicio extra de Vacunación? (s/n)")
                resp = input().lower()
                servicios_extra = []
                if resp == 's':
                    servicios_extra.append(Servicio("VAC", "Vacunación", 45000.0))

                try:
                    factura = self._cita_service.atender_cita(nit, codigo, servicios_extra, "FAC-001")
                    print("\n✅ ÉXITO: Cita atendida.")
                    print("-" * 25)
                    print(f"📄 FACTURA GENERADA: {factura.numero}")
                    print(f"📅 Fecha: {factura.fecha_emision}")
                    print(f"💰 VALOR TOTAL A PAGAR: $ {factura.valor_total}")
                    print("-" * 25)
                except ValueError as e:
                    print(f"❌ {e}")

            elif opcion == "4":
                print("Saliendo del sistema... ¡Hasta luego!")
                break
            else:
                print("❌ Opción inválida.")