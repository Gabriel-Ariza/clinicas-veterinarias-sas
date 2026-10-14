import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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
    huellitas = Clinica("901456789-1", "Clínica Veterinaria Huellitas", "68679", "Santander", "Calle 12 # 9-40", "Centro", password="1234")
    patitas = Clinica("900987654-3", "Clínica Veterinaria Patitas Felices", "68276", "Santander", "Carrera 27 # 30-15", "Cañaveral", password="1234")

    juliana = Veterinario("63512478", "Juliana Ortiz Ramírez", "TP-18452")
    carlos = Veterinario("13896542", "Carlos Alberto Pérez", "TP-20914")
    andrea = Veterinario("37894123", "Andrea Lucía Gómez", "TP-15480")

    serv_cg = Servicio("CG", "Consulta general", 60000.0)
    serv_vac = Servicio("VAC", "Vacunación antirrábica y múltiple", 45000.0)
    serv_des = Servicio("DES", "Desparasitación interna y externa", 35000.0)
    serv_lab = Servicio("LAB", "Examen de laboratorio clínico", 85000.0)
    serv_ban = Servicio("BAN", "Baño medicado y peluquería", 55000.0)

    huellitas.registrar_veterinario(juliana)
    huellitas.registrar_veterinario(carlos)
    huellitas.registrar_servicio(serv_cg)
    huellitas.registrar_servicio(serv_vac)
    huellitas.registrar_servicio(serv_des)
    huellitas.registrar_servicio(serv_lab)
    huellitas.registrar_servicio(serv_ban)

    patitas.registrar_veterinario(andrea)
    patitas.registrar_servicio(serv_cg)
    patitas.registrar_servicio(serv_vac)
    patitas.registrar_servicio(serv_des)

    laura = Propietario("1098765432", "Laura Méndez Plata", "3157894561", "Bucaramanga")
    rocky = Mascota("Rocky", "perro", "criolla", 2023, 18.0)
    laura.agregar_mascota(rocky)
    huellitas.registrar_propietario(laura)

    camilo = Propietario("1095432187", "Camilo Andrés Rueda", "3164567890", "Bucaramanga")
    luna = Mascota("Luna", "gato", "angora", 2022, 4.5)
    camilo.agregar_mascota(luna)
    huellitas.registrar_propietario(camilo)

    # Cita inicial ajustada con hora universal en formato 24h ("09:00")
    cita001 = Cita("CIT-001", "10 de noviembre de 2026", "09:00", rocky, juliana)
    cita001.agregar_servicio_adicional(serv_cg)
    huellitas.agregar_cita(cita001)

    clinica_repo.guardar(huellitas)
    clinica_repo.guardar(patitas)

def main():
    clinica_repo = ClinicaRepository()
    cita_service = CitaService(clinica_repo)
    
    cargar_datos_iniciales(clinica_repo)
    
    root = tk.Tk()
    app = AppVeterinaria(root, cita_service, clinica_repo)
    root.mainloop()

if __name__ == "__main__":
    main()