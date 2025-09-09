"""
Módulo que define la clase Paciente para el sistema de turnos médicos.
"""

from datetime import datetime


class Paciente:
    """
    Clase que representa a un paciente en el sistema de turnos.
    
    Attributes:
        nombre (str): Nombre del paciente
        edad (int): Edad del paciente
        especialidad (str): Especialidad médica requerida
        hora_llegada (datetime): Momento en que se registró el turno
        numero_turno (int): Número de turno asignado
    """
    
    contador_turnos = 0  # Variable de clase para enumerar turnos
    
    def __init__(self, nombre, edad, especialidad):
        """
        Inicializa un nuevo paciente.
        
        Args:
            nombre (str): Nombre del paciente
            edad (int): Edad del paciente
            especialidad (str): Especialidad médica requerida
        """
        self.nombre = nombre
        self.edad = edad
        self.especialidad = especialidad
        self.hora_llegada = datetime.now()
        
        # Incrementar contador y asignar número de turno
        Paciente.contador_turnos += 1
        self.numero_turno = Paciente.contador_turnos
    
    def tiempo_espera_actual(self):
        """
        Calcula el tiempo de espera actual del paciente.
        
        Returns:
            int: Tiempo de espera en minutos
        """
        tiempo_transcurrido = datetime.now() - self.hora_llegada
        return int(tiempo_transcurrido.total_seconds() / 60)
    
    def __str__(self):
        """
        Representación en cadena del paciente.
        
        Returns:
            str: Información del paciente formateada
        """
        return f"Turno {self.numero_turno}: {self.nombre} ({self.edad} años) - {self.especialidad}"
    
    def __repr__(self):
        """
        Representación para depuración.
        
        Returns:
            str: Información detallada del paciente
        """
        return f"Paciente('{self.nombre}', {self.edad}, '{self.especialidad}', turno={self.numero_turno})"