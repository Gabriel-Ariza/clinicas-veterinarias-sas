from resources.excepciones import (
    ConflictoHorarioError,
    DuplicadoError,
    NoEncontradoError,
)
from resources.validaciones import nit_valido, solo_digitos, texto_obligatorio


class Clinica:
    """Clínica veterinaria.

    Compone a sus veterinarios, servicios, propietarios y citas.
    """

    def __init__(self, nit, nombre, municipio, direccion, barrio):
        self._nit = nit_valido(nit)
        self._nombre = texto_obligatorio(nombre, "Nombre de la clínica")
        self._municipio = municipio
        self._direccion = texto_obligatorio(direccion, "Dirección")
        self._barrio = texto_obligatorio(barrio, "Barrio")
        self._veterinarios = {}   # cédula -> Veterinario
        self._servicios = {}      # código -> Servicio
        self._propietarios = {}   # cédula -> Propietario
        self._citas = {}          # código -> Cita

    # ---------- propiedades ----------
    @property
    def nit(self):
        return self._nit

    @property
    def nombre(self):
        return self._nombre

    @property
    def municipio(self):
        return self._municipio

    @property
    def direccion(self):
        return self._direccion

    @property
    def barrio(self):
        return self._barrio

    @property
    def veterinarios(self):
        return list(self._veterinarios.values())

    @property
    def servicios(self):
        return list(self._servicios.values())

    @property
    def propietarios(self):
        return list(self._propietarios.values())

    @property
    def citas(self):
        return list(self._citas.values())

    @property
    def puede_operar(self):
        """La clínica ya tiene veterinarios y catálogo de servicios."""
        return bool(self._veterinarios) and bool(self._servicios)

    # ---------- registros ----------
    def agregar_veterinario(self, veterinario):
        if veterinario.cedula in self._veterinarios:
            raise DuplicadoError(
                f"Ya existe un veterinario con la cédula {veterinario.cedula} "
                f"en {self._nombre}."
            )
        self._veterinarios[veterinario.cedula] = veterinario

    def agregar_servicio(self, servicio):
        if servicio.codigo in self._servicios:
            raise DuplicadoError(
                f"Ya existe un servicio con el código {servicio.codigo} "
                f"en {self._nombre}."
            )
        self._servicios[servicio.codigo] = servicio

    def agregar_propietario(self, propietario):
        if propietario.cedula in self._propietarios:
            raise DuplicadoError(
                f"Ya existe un propietario con la cédula {propietario.cedula} "
                f"en {self._nombre}."
            )
        self._propietarios[propietario.cedula] = propietario

    def agregar_cita(self, cita):
        self._citas[cita.codigo] = cita

    # ---------- búsquedas ----------
    def obtener_veterinario(self, cedula):
        cedula = solo_digitos(cedula, "Cédula del veterinario", 6, 10)
        veterinario = self._veterinarios.get(cedula)
        if veterinario is None:
            raise NoEncontradoError(
                f"No existe un veterinario con la cédula {cedula} en {self._nombre}."
            )
        return veterinario

    def obtener_servicio(self, codigo):
        texto = texto_obligatorio(codigo, "Tipo de servicio")
        servicio = self._servicios.get(texto.upper())
        if servicio is None:  # también se acepta el nombre del servicio
            for candidato in self._servicios.values():
                if candidato.nombre.lower() == texto.lower():
                    return candidato
            raise NoEncontradoError(
                f"{self._nombre} no ofrece el servicio '{texto}'. "
                "Usa el código o el nombre del catálogo."
            )
        return servicio

    def obtener_propietario(self, cedula):
        cedula = solo_digitos(cedula, "Cédula del propietario", 6, 10)
        propietario = self._propietarios.get(cedula)
        if propietario is None:
            raise NoEncontradoError(
                f"No existe un propietario con la cédula {cedula} en {self._nombre}."
            )
        return propietario

    def buscar_propietario(self, cedula):
        cedula = solo_digitos(cedula, "Cédula del propietario", 6, 10)
        return self._propietarios.get(cedula)

    def buscar_cita(self, codigo):
        return self._citas.get(codigo)

    # ---------- reglas de disponibilidad ----------
    def _cita_programada_veterinario(self, veterinario, fecha, hora):
        for cita in self._citas.values():
            if (cita.esta_programada() and cita.veterinario is veterinario
                    and cita.fecha == fecha and cita.hora == hora):
                return cita
        return None

    def asignar_veterinario(self, fecha, hora, cedula=None):
        """Devuelve el veterinario pedido (si está libre) o uno disponible."""
        if cedula:
            veterinario = self.obtener_veterinario(cedula)
            conflicto = self._cita_programada_veterinario(veterinario, fecha, hora)
            if conflicto:
                raise ConflictoHorarioError(
                    f"{veterinario.nombre} ya tiene la cita {conflicto.codigo} "
                    f"el {fecha.isoformat()} a las {hora.strftime('%H:%M')}."
                )
            return veterinario

        for veterinario in self._veterinarios.values():
            if self._cita_programada_veterinario(veterinario, fecha, hora) is None:
                return veterinario
        raise ConflictoHorarioError(
            f"No hay veterinarios disponibles el {fecha.isoformat()} "
            f"a las {hora.strftime('%H:%M')}."
        )

    def validar_mascota_libre(self, mascota, fecha, hora):
        for cita in self._citas.values():
            if (cita.esta_programada() and cita.mascota is mascota
                    and cita.fecha == fecha and cita.hora == hora):
                raise ConflictoHorarioError(
                    f"{mascota.nombre} ya tiene la cita {cita.codigo} "
                    f"el {fecha.isoformat()} a las {hora.strftime('%H:%M')}."
                )

    # ---------- consultas ----------
    def citas_en_fecha(self, fecha):
        citas = [c for c in self._citas.values() if c.fecha == fecha]
        return sorted(citas, key=lambda c: c.hora)

    def citas_de_mascota(self, mascota):
        citas = [c for c in self._citas.values() if c.mascota is mascota]
        return sorted(citas, key=lambda c: (c.fecha, c.hora))

    def __str__(self):
        return self._nombre
