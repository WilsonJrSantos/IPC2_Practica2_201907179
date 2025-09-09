"""
Módulo que define las constantes utilizadas en el sistema de turnos médicos.
"""

# Tiempos de atención por especialidad (en minutos)
TIEMPOS_ATENCION = {
    "Medicina General": 10,
    "Pediatría": 15,
    "Ginecología": 20,
    "Dermatología": 25
}

# Lista de especialidades disponibles
ESPECIALIDADES = [
    "Medicina General",
    "Pediatría", 
    "Ginecología",
    "Dermatología"
]

# Configuración de la interfaz gráfica
VENTANA_TITULO = "Sistema de Turnos Médicos"
VENTANA_ANCHO = 800
VENTANA_ALTO = 600

# Colores de la interfaz
COLOR_FONDO = "#f0f0f0"
COLOR_PRIMARIO = "#2E86AB"
COLOR_SECUNDARIO = "#A23B72"
COLOR_EXITO = "#F18F01"
COLOR_ERROR = "#C73E1D"

# Configuración de fuentes
FUENTE_TITULO = ("Arial", 14, "bold")
FUENTE_NORMAL = ("Arial", 10)
FUENTE_PEQUEÑA = ("Arial", 8)

# Mensajes del sistema
MENSAJE_COLA_VACIA = "No hay pacientes en espera"
MENSAJE_PACIENTE_ATENDIDO = "Paciente atendido correctamente"
MENSAJE_ERROR_CAMPOS = "Por favor, complete todos los campos"
MENSAJE_ERROR_EDAD = "La edad debe ser un número válido"

# Configuración de Graphviz
GRAPHVIZ_FORMATO = "png"
GRAPHVIZ_ENGINE = "dot"
GRAPHVIZ_ARCHIVO = "cola_turnos"