"""
Módulo que define las estructuras para los reportes de estadísticas.
"""
class ReporteEstadisticas:
    def __init__(self):
        self.total_pacientes = 0
        self.tiempo_total_estimado = 0
        self.conteo_especialidades = None # Será el inicio de una lista enlazada de NodoEstadistica

class NodoEstadistica:
    def __init__(self, especialidad, cantidad):
        self.especialidad = especialidad
        self.cantidad = cantidad
        self.siguiente = None