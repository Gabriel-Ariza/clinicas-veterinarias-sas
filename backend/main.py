import sys
import os

# Permite importar los módulos de backend y frontend al ejecutar este archivo.
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(BASE_DIR)
sys.path.append(os.path.abspath(os.path.join(BASE_DIR, "..")))

import tkinter as tk

from repository.clinica_repository import ClinicaRepository
from services.cita_service import CitaService
from frontend.app import AppVeterinaria

from entity.clinica import Clinica
from entity.veterinario import Veterinario
from entity.servicio import Servicio
from entity.propietario import Propietario
from entity.mascota import Mascota
from entity.cita import Cita


def cargar_datos_iniciales(clinica_repo):
    """
    Carga datos de prueba para ejecutar los escenarios solicitados.
    Las citas y los registros se guardan en memoria; se reinician al cerrar
    y volver a abrir el programa.
    """

    # ---------------------------------------------------------
    # 1. CLÍNICAS
    # ---------------------------------------------------------
    huellitas = Clinica(
        "901456789-1",
        "Clínica Veterinaria Huellitas",
        "68679",
        "Santander",
        "Calle 12 # 9-40",
        "Centro",
        password="1234",
    )

    patitas = Clinica(
        "900987654-3",
        "Clínica Veterinaria Patitas Felices",
        "68276",
        "Santander",
        "Carrera 27 # 30-15",
        "Cañaveral",
        password="1234",
    )

    # ---------------------------------------------------------
    # 2. VETERINARIOS
    # ---------------------------------------------------------
    juliana = Veterinario("63512478", "Juliana Ortiz Ramírez", "TP-18452")
    carlos = Veterinario("13896542", "Carlos Alberto Pérez", "TP-20914")
    andrea = Veterinario("37894123", "Andrea Lucía Gómez", "TP-15480")

    # Personal indicado para Patitas Felices.
    sergio = Veterinario("13745821", "Sergio Arenas Villamizar", "TP-30001")
    diana = Veterinario("37896542", "Diana Carolina Rey Moreno", "TP-30002")
    felipe = Veterinario("109865321", "Felipe Castellanos Díaz", "TP-30003")

    for veterinario in (juliana, carlos):
        huellitas.registrar_veterinario(veterinario)

    for veterinario in (andrea, sergio, diana, felipe):
        patitas.registrar_veterinario(veterinario)

    # ---------------------------------------------------------
    # 3. SERVICIOS Y TARIFAS
    # Consulta general ($60.000) + vacunación ($45.000) = $105.000.
    # ---------------------------------------------------------
    serv_cg = Servicio("CG", "Consulta general", 60000.0)
    serv_vac = Servicio("VAC", "Vacunación antirrábica y múltiple", 45000.0)
    serv_des = Servicio("DES", "Desparasitación interna y externa", 35000.0)
    serv_lab = Servicio("LAB", "Examen de laboratorio clínico", 85000.0)
    serv_ban = Servicio("BAN", "Baño medicado y peluquería", 55000.0)
    serv_eco = Servicio("ECO", "Ecografía", 90000.0)

    for servicio in (serv_cg, serv_vac, serv_des, serv_lab, serv_ban, serv_eco):
        huellitas.registrar_servicio(servicio)

    for servicio in (serv_cg, serv_vac, serv_des, serv_lab, serv_eco):
        patitas.registrar_servicio(servicio)

    # ---------------------------------------------------------
    # 4. PROPIETARIOS Y MASCOTAS DE HUELLITAS
    # ---------------------------------------------------------
    laura = Propietario(
        "1098765432",
        "Laura Méndez Plata",
        "3157894561",
        "Bucaramanga, Santander",
    )
    rocky = Mascota("Rocky", "perro", "criollo", 2023, 18.0)
    laura.agregar_mascota(rocky)
    huellitas.registrar_propietario(laura)

    camila = Propietario(
        "1005678912",
        "Camila Duarte Serrano",
        "3204567812",
        "San Gil, Santander",
    )
    copito = Mascota("Copito", "conejo", "cabeza de león", 2025, 1.5)
    camila.agregar_mascota(copito)
    huellitas.registrar_propietario(camila)

    # Se conservan estos datos adicionales para probar el historial de Huellitas.
    propietario_luna_huellitas = Propietario(
        "1095432187",
        "Camilo Andrés Rueda",
        "3164567890",
        "Bucaramanga, Santander",
    )
    luna_huellitas = Mascota("Luna", "gato", "angora", 2022, 4.5)
    propietario_luna_huellitas.agregar_mascota(luna_huellitas)
    huellitas.registrar_propietario(propietario_luna_huellitas)

    # ---------------------------------------------------------
    # 5. PROPIETARIO Y MASCOTA DE PATITAS FELICES
    # ---------------------------------------------------------
    andres = Propietario(
        "1102345678",
        "Andrés Rueda Ardila",
        "301678923",
        "Piedecuesta, Santander",
    )
    luna = Mascota("Luna", "gata", "siamés", 2022, 4.0)
    andres.agregar_mascota(luna)
    patitas.registrar_propietario(andres)

    # ---------------------------------------------------------
    # 6. CITA INICIAL CIT-001
    # Se deja programada para poder atenderla y generar FAC-001.
    # La consulta general cuesta $60.000; al añadir vacunación
    # desde la pantalla de atención, el total será $105.000.
    # ---------------------------------------------------------
    cita001 = Cita(
        "CIT-001",
        "10 de noviembre de 2026",
        "09:00",
        rocky,
        juliana,
    )
    cita001.agregar_servicio_adicional(serv_cg)
    huellitas.agregar_cita(cita001)

    # Guardar las clínicas en el repositorio.
    clinica_repo.guardar(huellitas)
    clinica_repo.guardar(patitas)


def main():
    clinica_repo = ClinicaRepository()
    cita_service = CitaService(clinica_repo)

    cargar_datos_iniciales(clinica_repo)

    root = tk.Tk()
    AppVeterinaria(root, cita_service, clinica_repo)
    root.mainloop()


if __name__ == "__main__":
    main()
