"""Excepciones personalizadas de la aplicación."""


class ClinicaVeterinariaError(Exception):
    """Excepción base: todas las demás heredan de ella."""


class DatoInvalidoError(ClinicaVeterinariaError):
    """Un dato ingresado está vacío, mal formado o fuera de rango."""


class DuplicadoError(ClinicaVeterinariaError):
    """Se intenta registrar algo que ya existe."""


class NoEncontradoError(ClinicaVeterinariaError):
    """No existe la clínica, propietario, mascota, servicio, etc. buscado."""


class ReglaNegocioError(ClinicaVeterinariaError):
    """Se incumple una regla de negocio."""


class ConflictoHorarioError(ReglaNegocioError):
    """El veterinario o la mascota ya tienen una cita programada a esa hora."""


class EstadoCitaInvalidoError(ReglaNegocioError):
    """La cita no está en el estado requerido para la operación."""
