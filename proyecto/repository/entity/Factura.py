class Factura:
    """Factura expedida al atender una cita."""

    def __init__(self, numero, fecha, propietario, mascota, servicios):
        self._numero = numero
        self._fecha = fecha
        self._propietario = propietario
        self._mascota = mascota
        self._servicios = list(servicios)

    @property
    def numero(self):
        return self._numero

    @property
    def fecha(self):
        return self._fecha

    @property
    def propietario(self):
        return self._propietario

    @property
    def mascota(self):
        return self._mascota

    @property
    def servicios(self):
        return list(self._servicios)

    @property
    def total(self):
        return sum(servicio.tarifa for servicio in self._servicios)
