"""Capa de datos: almacenamiento en memoria de las clínicas y los consecutivos."""


class ClinicaRepository:

    def __init__(self):
        self._clinicas = {}          # NIT -> Clinica
        self._contador_citas = 0
        self._contador_facturas = 0

    def existe(self, nit):
        return nit in self._clinicas

    def agregar(self, clinica):
        self._clinicas[clinica.nit] = clinica

    def obtener(self, nit):
        return self._clinicas.get(nit)

    def listar(self):
        return list(self._clinicas.values())

    def siguiente_codigo_cita(self):
        self._contador_citas += 1
        return f"CIT-{self._contador_citas:03d}"

    def siguiente_numero_factura(self):
        self._contador_facturas += 1
        return f"FAC-{self._contador_facturas:03d}"
