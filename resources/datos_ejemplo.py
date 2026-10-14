"""Datos de ejemplo (clínicas, veterinarios y catálogos) para agilizar pruebas."""

DATOS_EJEMPLO = [
    {
        "nit": "901456789-1",
        "nombre": "Clínica Veterinaria Huellitas",
        "codigo_dane": "68679",
        "municipio": "San Gil",
        "departamento": "Santander",
        "direccion": "Calle 12 # 9-40",
        "barrio": "Centro",
        # (cédula, nombre, tarjeta profesional)
        "veterinarios": [
            ("63512478", "Juliana Ortiz Ramírez", "TP-18452"),
            ("91254863", "Mauricio Pinzón Gómez", "TP-20117"),
        ],
        # (código, nombre, tarifa)
        "servicios": [
            ("CG", "Consulta general", 60000),
            ("VAC", "Vacunación", 45000),
            ("DES", "Desparasitación", 30000),
            ("PEL", "Baño y peluquería", 50000),
        ],
    },
    {
        "nit": "900987654-3",
        "nombre": "Clínica Veterinaria Patitas Felices",
        "codigo_dane": "68276",
        "municipio": "Floridablanca",
        "departamento": "Santander",
        "direccion": "Carrera 27 # 30-15",
        "barrio": "Cañaveral",
        "veterinarios": [
            ("13745821", "Sergio Arenas Villamizar", "TP-15893"),
            ("37896542", "Diana Carolina Rey Moreno", "TP-22406"),
            ("1098654321", "Felipe Castellanos Díaz", "TP-31578"),
        ],
        "servicios": [
            ("CG", "Consulta general", 65000),
            ("VAC", "Vacunación", 48000),
            ("DES", "Desparasitación", 32000),
            ("ECO", "Ecografía", 120000),
        ],
    },
]
