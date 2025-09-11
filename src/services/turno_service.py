# src/services/turno_service.py
"""
Módulo que maneja la lógica de negocio del sistema de turnos médicos.
"""
from models.cola import Cola
from models.paciente import Paciente

from utils.constantes import (
    ESPECIALIDAD_1, TIEMPO_ATENCION_1,
    ESPECIALIDAD_2, TIEMPO_ATENCION_2,
    ESPECIALIDAD_3, TIEMPO_ATENCION_3,
    ESPECIALIDAD_4, TIEMPO_ATENCION_4
)
from models.reporte import ReporteEstadisticas, NodoEstadistica

class TurnoService:
    """
    Servicio que gestiona la lógica de turnos médicos.
    """
    
    def __init__(self):
        """Inicializa el servicio de turnos."""
        self.cola_turnos = Cola()
    
    def registrar_turno(self, nombre, edad, especialidad):
        """Registra un nuevo turno en la cola."""
        if not nombre or not nombre.strip():
            raise ValueError("El nombre no puede estar vacío")
        
        if not isinstance(edad, int) or edad <= 0 or edad > 120:
            raise ValueError("La edad debe ser un número válido entre 1 y 120")
        
        # Validación sin usar diccionarios o listas
        if especialidad not in (ESPECIALIDAD_1, ESPECIALIDAD_2, ESPECIALIDAD_3, ESPECIALIDAD_4):
            raise ValueError(f"Especialidad '{especialidad}' no válida")
        
        paciente = Paciente(nombre.strip(), edad, especialidad)
        self.cola_turnos.encolar(paciente)
        return paciente
    
    def atender_siguiente_paciente(self):
        """Atiende al siguiente paciente en la cola."""
        if self.cola_turnos.esta_vacia():
            raise IndexError("No hay pacientes en espera")
        return self.cola_turnos.desencolar()
    
    def ver_siguiente_paciente(self):
        """Muestra el siguiente paciente sin atenderlo."""
        if self.cola_turnos.esta_vacia():
            return None
        return self.cola_turnos.ver_frente()
    
    def obtener_todos_turnos(self):
        """
        Devuelve la cola iterable directamente, no una lista.
        """
        return self.cola_turnos
    
    def calcular_tiempo_espera_paciente(self, posicion):
        """
        Calcula el tiempo de espera iterando sobre la cola, sin convertirla a lista.
        """
        if posicion < 0 or posicion >= self.cola_turnos.obtener_tamaño():
            return 0
        
        tiempo_espera = 0
        contador_actual = 0
        
        # Itera sobre la cola y se detiene cuando llega a la posición deseada
        for paciente in self.cola_turnos:
            if contador_actual < posicion:
                tiempo_espera += self.obtener_tiempo_atencion(paciente.especialidad)
                contador_actual += 1
            else:
                break # Deja de sumar cuando alcanza la posición
        
        return tiempo_espera
    
    def obtener_tiempo_atencion(self, especialidad):
        """
        Obtiene el tiempo de atención usando condicionales, no un diccionario.
        """
        if especialidad == ESPECIALIDAD_1:
            return TIEMPO_ATENCION_1
        elif especialidad == ESPECIALIDAD_2:
            return TIEMPO_ATENCION_2
        elif especialidad == ESPECIALIDAD_3:
            return TIEMPO_ATENCION_3
        elif especialidad == ESPECIALIDAD_4:
            return TIEMPO_ATENCION_4
        else:
            return 10 # Un valor por defecto si algo falla

    def obtener_estadisticas(self):
        """
        Calcula y devuelve las estadísticas usando el objeto ReporteEstadisticas.
        """
        if self.cola_turnos.esta_vacia():
            return ReporteEstadisticas()

        reporte = ReporteEstadisticas()
        reporte.total_pacientes = self.cola_turnos.obtener_tamaño()
        
        tiempo_total = 0
        conteo_e1, conteo_e2, conteo_e3, conteo_e4 = 0, 0, 0, 0

        for paciente in self.cola_turnos:
            tiempo_total += self.obtener_tiempo_atencion(paciente.especialidad)
            if paciente.especialidad == ESPECIALIDAD_1:
                conteo_e1 += 1
            elif paciente.especialidad == ESPECIALIDAD_2:
                conteo_e2 += 1
            elif paciente.especialidad == ESPECIALIDAD_3:
                conteo_e3 += 1
            elif paciente.especialidad == ESPECIALIDAD_4:
                conteo_e4 += 1
        
        reporte.tiempo_total_estimado = tiempo_total
        
        # Construye la lista enlazada de Nodos de estadística
        nodo1 = NodoEstadistica(ESPECIALIDAD_1, conteo_e1)
        nodo2 = NodoEstadistica(ESPECIALIDAD_2, conteo_e2)
        nodo3 = NodoEstadistica(ESPECIALIDAD_3, conteo_e3)
        nodo4 = NodoEstadistica(ESPECIALIDAD_4, conteo_e4)
        
        nodo1.siguiente = nodo2
        nodo2.siguiente = nodo3
        nodo3.siguiente = nodo4
        
        reporte.conteo_especialidades = nodo1
        
        return reporte
    
    def limpiar_turnos(self):
        """Limpia todos los turnos de la cola."""
        self.cola_turnos.limpiar()
    
    def hay_turnos_pendientes(self):
        """Verifica si hay turnos pendientes."""
        return not self.cola_turnos.esta_vacia()
    
    def obtener_numero_turnos(self):
        """Obtiene el número total de turnos en la cola."""
        return self.cola_turnos.obtener_tamaño()