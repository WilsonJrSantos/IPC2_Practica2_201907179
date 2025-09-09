"""
Módulo que maneja la lógica de negocio del sistema de turnos médicos.
"""

from datetime import datetime
from models.cola import Cola
from models.paciente import Paciente
from utils.constantes import TIEMPOS_ATENCION


class TurnoService:
    """
    Servicio que gestiona la lógica de turnos médicos.
    
    Attributes:
        cola_turnos (Cola): Cola dinámica que almacena los turnos
    """
    
    def __init__(self):
        """Inicializa el servicio de turnos."""
        self.cola_turnos = Cola()
    
    def registrar_turno(self, nombre, edad, especialidad):
        """
        Registra un nuevo turno en la cola.
        
        Args:
            nombre (str): Nombre del paciente
            edad (int): Edad del paciente
            especialidad (str): Especialidad médica requerida
            
        Returns:
            Paciente: El paciente registrado
            
        Raises:
            ValueError: Si los datos proporcionados no son válidos
        """
        # Validar datos de entrada
        if not nombre or not nombre.strip():
            raise ValueError("El nombre no puede estar vacío")
        
        if not isinstance(edad, int) or edad <= 0 or edad > 120:
            raise ValueError("La edad debe ser un número válido entre 1 y 120")
        
        if especialidad not in TIEMPOS_ATENCION:
            raise ValueError(f"Especialidad '{especialidad}' no válida")
        
        # Crear y registrar paciente
        paciente = Paciente(nombre.strip(), edad, especialidad)
        self.cola_turnos.encolar(paciente)
        
        return paciente
    
    def atender_siguiente_paciente(self):
        """
        Atiende al siguiente paciente en la cola.
        
        Returns:
            Paciente: El paciente atendido
            
        Raises:
            IndexError: Si no hay pacientes en espera
        """
        if self.cola_turnos.esta_vacia():
            raise IndexError("No hay pacientes en espera")
        
        return self.cola_turnos.desencolar()
    
    def ver_siguiente_paciente(self):
        """
        Muestra el siguiente paciente sin atenderlo.
        
        Returns:
            Paciente: El siguiente paciente en la cola o None si está vacía
        """
        if self.cola_turnos.esta_vacia():
            return None
        
        return self.cola_turnos.ver_frente()
    
    def obtener_todos_turnos(self):
        """
        Obtiene todos los turnos en la cola.
        
        Returns:
            list: Lista de todos los pacientes en la cola
        """
        return self.cola_turnos.obtener_todos_elementos()
    
    def calcular_tiempo_espera_paciente(self, posicion):
        """
        Calcula el tiempo estimado de espera para un paciente en determinada posición.
        
        Args:
            posicion (int): Posición del paciente en la cola (0 = siguiente)
            
        Returns:
            int: Tiempo de espera estimado en minutos
        """
        if posicion < 0 or posicion >= self.cola_turnos.obtener_tamaño():
            return 0
        
        tiempo_espera = 0
        pacientes = self.obtener_todos_turnos()
        
        # Sumar tiempos de atención de pacientes anteriores
        for i in range(posicion):
            tiempo_atencion = TIEMPOS_ATENCION.get(pacientes[i].especialidad, 10)
            tiempo_espera += tiempo_atencion
        
        return tiempo_espera
    
    def obtener_tiempo_atencion(self, especialidad):
        """
        Obtiene el tiempo de atención para una especialidad.
        
        Args:
            especialidad (str): Especialidad médica
            
        Returns:
            int: Tiempo de atención en minutos
        """
        return TIEMPOS_ATENCION.get(especialidad, 10)
    
    def obtener_estadisticas(self):
        """
        Obtiene estadísticas de la cola de turnos.
        
        Returns:
            dict: Diccionario con estadísticas de la cola
        """
        if self.cola_turnos.esta_vacia():
            return {
                "total_pacientes": 0,
                "tiempo_total_estimado": 0,
                "especialidades": {}
            }
        
        pacientes = self.obtener_todos_turnos()
        especialidades_count = {}
        tiempo_total = 0
        
        for paciente in pacientes:
            # Contar especialidades
            if paciente.especialidad in especialidades_count:
                especialidades_count[paciente.especialidad] += 1
            else:
                especialidades_count[paciente.especialidad] = 1
            
            # Sumar tiempo de atención
            tiempo_total += self.obtener_tiempo_atencion(paciente.especialidad)
        
        return {
            "total_pacientes": len(pacientes),
            "tiempo_total_estimado": tiempo_total,
            "especialidades": especialidades_count
        }
    
    def limpiar_turnos(self):
        """Limpia todos los turnos de la cola."""
        self.cola_turnos.limpiar()
    
    def hay_turnos_pendientes(self):
        """
        Verifica si hay turnos pendientes.
        
        Returns:
            bool: True si hay turnos pendientes, False en caso contrario
        """
        return not self.cola_turnos.esta_vacia()
    
    def obtener_numero_turnos(self):
        """
        Obtiene el número total de turnos en la cola.
        
        Returns:
            int: Cantidad de turnos pendientes
        """
        return self.cola_turnos.obtener_tamaño()