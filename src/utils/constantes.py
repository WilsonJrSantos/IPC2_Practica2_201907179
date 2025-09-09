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
VENTANA_ANCHO = 850
VENTANA_ALTO = 650

# Colores de la interfaz (Paleta estilo moderno)
COLOR_FONDO = "#f0f2f5"
COLOR_PRIMARIO = "#005f73"  # Un azul oscuro/verde azulado
COLOR_SECUNDARIO = "#0a9396" # Un turquesa
COLOR_EXITO = "#94d2bd"     # Un verde menta claro
COLOR_ERROR = "#d00000"     # Un rojo fuerte

# Configuración de fuentes
FUENTE_TITULO = ("Segoe UI", 16, "bold")
FUENTE_NORMAL = ("Segoe UI", 10)
FUENTE_PEQUEÑA = ("Segoe UI", 8)

# Mensajes del sistema
MENSAJE_COLA_VACIA = "No hay pacientes en espera."
MENSAJE_PACIENTE_ATENDIDO = "Paciente atendido correctamente."
MENSAJE_ERROR_CAMPOS = "Por favor, complete todos los campos."
MENSAJE_ERROR_EDAD = "La edad debe ser un número válido."

# Configuración de Graphviz
GRAPHVIZ_FORMATO = "png"
GRAPHVIZ_ENGINE = "dot"
GRAPHVIZ_ARCHIVO = "cola_turnos"