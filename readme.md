# Sistema de Gestión de Clínicas Veterinarias 🐾

## Descripción del proyecto

Este proyecto consiste en una aplicación de escritorio desarrollada en **Python** para gestionar operaciones básicas de una clínica veterinaria. Su propósito es aplicar los principios de la **Programación Orientada a Objetos (POO)** y organizar el código mediante una arquitectura por capas, separando la interfaz gráfica, la lógica de negocio, las entidades y el acceso a los datos.

La aplicación permite iniciar sesión como clínica veterinaria y acceder a opciones para programar citas, cancelar citas y atender citas con su correspondiente proceso de facturación.

## Objetivos

- Aplicar los conceptos de clases, objetos, atributos y métodos.
- Representar las entidades principales de un sistema veterinario.
- Separar las responsabilidades del programa mediante una estructura organizada por capas.
- Gestionar el ciclo básico de las citas veterinarias desde una interfaz gráfica.
- Documentar el diseño del sistema mediante diagramas UML y diagramas de secuencia.

## Funcionalidades

- **Inicio de sesión:** acceso mediante el NIT y la contraseña de la clínica.
- **Gestión de citas:** programación de citas indicando fecha, hora, mascota y veterinario.
- **Cancelación de citas:** selección y cancelación de citas que se encuentren programadas.
- **Atención y facturación:** acceso al proceso de atención de citas y generación de la factura correspondiente.
- **Datos de ejemplo:** carga inicial de clínicas, veterinarios, servicios, propietarios, mascotas y una cita de prueba.
- **Interfaz gráfica:** ventanas y controles creados con Tkinter.

> **Nota:** el proyecto incluye datos de prueba definidos en el código. La persistencia de la información depende de la implementación del repositorio; no se debe asumir que los cambios se guardan permanentemente entre ejecuciones.

## Tecnologías utilizadas

- **Python 3:** lenguaje de programación.
- **Tkinter:** construcción de la interfaz gráfica de escritorio.
- **Programación Orientada a Objetos:** modelado de las entidades y sus relaciones.
- **Git y GitHub:** control de versiones y alojamiento del código fuente.
- **Mermaid e imágenes PNG:** documentación visual de la arquitectura y los diagramas.

## Estructura del proyecto

```text
POO_python/
├── backend/
│   ├── controllers/
│   │   └── menuController.py
│   ├── entity/
│   │   ├── cita.py
│   │   ├── clinica.py
│   │   ├── factura.py
│   │   ├── mascota.py
│   │   ├── propietario.py
│   │   ├── servicio.py
│   │   └── veterinario.py
│   ├── repository/
│   │   └── clinica_repository.py
│   ├── services/
│   │   ├── cita_service.py
│   │   └── clinica_service.py
│   └── main.py
├── frontend/
│   └── app.py
├── resources/
│   ├── diagrams_mermaid/
│   ├── diagrama_capas.png
│   ├── diagrama_clases.png
│   ├── diagrama_dominio.png
│   ├── diagrama_objetos.png
│   ├── secuencia_atender_cita.png
│   ├── secuencia_cancelar_cita.png
│   └── secuencia_programar_cita.png
└── README.md
```

### Organización por capas

- **Entity:** contiene las clases del dominio, como `Clinica`, `Cita`, `Mascota`, `Propietario`, `Veterinario`, `Servicio` y `Factura`.
- **Repository:** centraliza las operaciones de consulta y almacenamiento de las clínicas.
- **Services:** contiene reglas y operaciones de negocio relacionadas con clínicas y citas.
- **Controllers:** agrupa componentes de control de la aplicación.
- **Frontend:** implementa las ventanas y la interacción con el usuario.
- **Main:** carga los datos iniciales y pone en marcha la aplicación.
- **Resources:** contiene los diagramas y recursos visuales del proyecto.

## Requisitos

- Python 3 instalado.
- Tkinter disponible en la instalación de Python.
- Git, si se desea clonar el repositorio.

El proyecto utiliza módulos de la biblioteca estándar de Python para su interfaz, por lo que no requiere instalar paquetes externos para ejecutar la interfaz básica.

## Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone URL_DEL_REPOSITORIO
```

Reemplaza `URL_DEL_REPOSITORIO` por la dirección real del repositorio de GitHub.

### 2. Entrar en la carpeta del proyecto

```bash
cd POO_python
```

### 3. Ejecutar la aplicación

En la terminal, entra en la carpeta `backend` y ejecuta el archivo principal:

```bash
cd backend
python main.py
```

En algunos sistemas puede ser necesario utilizar `python3 main.py` en lugar de `python main.py`.

## Datos de acceso de prueba

El código carga dos clínicas de ejemplo. Para ingresar con la primera clínica, utiliza los siguientes datos:

- **NIT:** `901456789-1`
- **Contraseña:** `1234`

Estas credenciales son únicamente para pruebas académicas. No deben utilizarse como mecanismo de autenticación para un sistema real.

## Diagramas y documentación visual

En la carpeta `resources/` se incluyen diagramas para comprender el diseño del sistema:

- Diagrama de capas.
- Diagrama de clases.
- Diagrama de dominio.
- Diagrama de objetos.
- Diagramas de secuencia para programar, cancelar y atender una cita.

También se incluyen archivos `.mermaid` con versiones textuales de algunos diagramas, útiles para consultarlos o editarlos.

## Conceptos de POO aplicados

El proyecto organiza la información en clases que representan elementos del dominio veterinario. Cada objeto mantiene datos y comportamientos relacionados con su responsabilidad. Las relaciones entre clínicas, propietarios, mascotas, veterinarios, servicios y citas permiten modelar el funcionamiento básico del negocio.

La separación entre entidades, servicios, repositorio e interfaz facilita la lectura, el mantenimiento y la ampliación del programa.

## Alcance académico

Este proyecto fue desarrollado con fines educativos para practicar Python, programación orientada a objetos, organización por capas, modelado UML y diseño de una aplicación de escritorio.

## Posibles mejoras futuras

- Incorporar una base de datos para conservar la información entre ejecuciones.
- Añadir validaciones más completas para fechas, horarios y datos de entrada.
- Mejorar la gestión de usuarios y el almacenamiento seguro de contraseñas.
- Incorporar pruebas automatizadas para las reglas de negocio.
- Ampliar los reportes de citas, servicios y facturación.

## Autores

- Jose Gabriel Plata Ariza - 01240372047
- Valery Montes Echavez - 01240372023
