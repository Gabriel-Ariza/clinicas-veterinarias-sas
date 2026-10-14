"""Funciones de validación reutilizadas por las clases de la lógica."""

import re

from resources.excepciones import DatoInvalidoError


def texto_obligatorio(valor, campo):
    if valor is None or not str(valor).strip():
        raise DatoInvalidoError(f"El campo '{campo}' es obligatorio.")
    return str(valor).strip()


def solo_digitos(valor, campo, minimo=1, maximo=15):
    texto = texto_obligatorio(valor, campo)
    if not texto.isdigit() or not minimo <= len(texto) <= maximo:
        if minimo == maximo:
            rango = f"{minimo} dígitos"
        else:
            rango = f"entre {minimo} y {maximo} dígitos"
        raise DatoInvalidoError(
            f"El campo '{campo}' debe contener solo números ({rango})."
        )
    return texto


def nit_valido(valor):
    texto = texto_obligatorio(valor, "NIT")
    if not re.fullmatch(r"\d{6,10}(-\d)?", texto):
        raise DatoInvalidoError("El NIT debe tener un formato como 901456789-1.")
    return texto


def numero_positivo(valor, campo):
    if valor is None or valor == "":
        raise DatoInvalidoError(f"El campo '{campo}' es obligatorio.")
    try:
        numero = float(valor)
    except (TypeError, ValueError):
        raise DatoInvalidoError(f"El campo '{campo}' debe ser un número.")
    if numero <= 0:
        raise DatoInvalidoError(f"El campo '{campo}' debe ser mayor que 0.")
    return numero
