# Clínicas Veterinarias — gestión de citas

Aplicación en Python (interfaz web con Gradio) para que las clínicas veterinarias gestionen
sus veterinarios, servicios, propietarios, mascotas y citas.

## Estructura

```
proyecto/
├── controllers/
│   └── menuController.py        # Interfaz Gradio: inicio, página de la clínica y formularios
├── repository/
│   ├── clinica_repository.py    # Almacenamiento en memoria y consecutivos (CIT-###, FAC-###)
│   └── entity/                  # Clases del dominio
│       ├── Clinica.py  Municipio.py  Veterinario.py  Servicio.py
│       └── Propietario.py  Mascota.py  Cita.py  Factura.py
├── services/
│   ├── clinica_service.py       # Clínicas, veterinarios, servicios, propietarios y mascotas
│   └── cita_service.py          # Programar, cancelar, atender/facturar y consultar citas
├── resources/
│   ├── datos_ejemplo.py         # Clínicas de ejemplo (se cargan al iniciar)
│   ├── excepciones.py           # Excepciones personalizadas
│   └── validaciones.py          # Validaciones de datos
├── main.py                      # Clase Main: inicia la aplicación
├── requirements.txt
├── .gitignore
└── readme.md
```

## Cómo ejecutarla

```bash
pip install -r requirements.txt
python main.py          # ejecutar desde la carpeta raíz del proyecto
```

En Google Colab:

```python
!git clone <URL_DEL_REPOSITORIO>
%cd <carpeta_del_repositorio>/proyecto
!pip install -q -U gradio
!python main.py
```

(En Colab, para abrir la interfaz usa el enlace público que muestra Gradio.)

## Uso

1. En el **inicio** aparecen las clínicas disponibles (las dos de ejemplo ya vienen cargadas) y la opción **Agregar clínica**.
2. Al **ingresar a una clínica** se ve su nombre, ubicación y la tabla de servicios con precios.
3. Desde ahí: **Crear cita**, **Editar cita existente** (cancelar o atender con servicios adicionales y factura) y, en *Más opciones*, consultar citas por fecha, historial de una mascota y registrar veterinarios, servicios, propietarios y mascotas.
4. Al crear una cita el sistema asigna el veterinario disponible y entrega un **código único** (CIT-001, …) que se debe guardar para cancelar o atender la cita.

## Reglas de negocio principales

- Estados de la cita: Programada, Cancelada, Atendida (al crearse queda Programada).
- Un veterinario o una mascota no pueden tener dos citas programadas en la misma fecha y hora.
- Solo se cancela una cita Programada y antes de su fecha; las canceladas se conservan en el historial.
- Solo se atiende una cita Programada; al atenderla se genera la factura (número único, detalle y total).
- No se repite el NIT de una clínica, ni la cédula de un propietario ni el código de un servicio dentro de la misma clínica.
- Cuando una regla se incumple, la aplicación muestra el motivo y no se detiene.

## Autores
Valery Montes Echavez -01240372023
Jose Gabriel Plata Ariza -01240372047
