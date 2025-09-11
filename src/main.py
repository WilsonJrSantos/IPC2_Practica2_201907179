#!/usr/bin/env python3
"""
Sistema de Turnos Médicos con Colas Dinámicas y Tkinter

Práctica 2 - Introducción a la Programación y Computación 2
Universidad San Carlos de Guatemala
Facultad de Ingeniería - Ingeniería en Ciencias y Sistemas

Este programa implementa un sistema de gestión de turnos médicos utilizando:
- Estructuras de datos dinámicas (Cola implementada con nodos)
- Interfaz gráfica con Tkinter
- Visualización con Graphviz
- Lógica FIFO para atención de pacientes

Autor: Wilson Santos
Fecha: Septiembre 2025
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# Agregar el directorio del proyecto al path para imports locales
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from gui.interfaz import InterfazTurnos
    from utils.constantes import VENTANA_TITULO
except ImportError as e:
    print(f"Error al importar módulos: {e}")
    print("Asegúrese de que la estructura de archivos sea correcta y esté en el directorio 'src'.")
    sys.exit(1)


# ============================
#  VERIFICACIÓN DEPENDENCIAS
# ============================

def verificar_dependencias():
    """
    Verifica que las dependencias necesarias estén instaladas,
    sin utilizar listas u otras estructuras de datos nativas.
    
    Returns:
        bool: True si las dependencias esenciales están disponibles.
    """
    # Tkinter (esencial)
    try:
        import tkinter
    except ImportError:
        print("\n ERROR: Falta la dependencia 'tkinter'.")
        print("Tkinter es parte de la instalación estándar de Python. Verifique su instalación.")
        return False
    
    # PIL / Pillow (esencial para la GUI si usa imágenes)
    try:
        from PIL import Image, ImageTk
    except ImportError:
        print("\n ERROR: Falta la dependencia 'Pillow'.")
        print("Instálela con el comando: pip install Pillow")
        return False
    
    # Graphviz (opcional, recomendado para visualización)
    try:
        import graphviz
    except ImportError:
        print("\n Advertencia: Graphviz no está instalado.")
        print("La visualización gráfica de la cola no estará disponible.")
        print("Para instalarlo, use: pip install graphviz")
    
    return True


# ============================
#  INFORMACIÓN DEL SISTEMA
# ============================

def mostrar_info_sistema():
    """Muestra información general del sistema en la consola."""
    print("=" * 60)
    print(f"         {VENTANA_TITULO}")
    print("=" * 60)
    print("Características del sistema:")
    print("• Cola dinámica implementada con nodos enlazados")
    print("• Interfaz gráfica interactiva con Tkinter")
    print("• Gestión FIFO de turnos médicos")
    print("• Cálculo automático de tiempos de espera")
    print("• Visualización gráfica con Graphviz")
    print("• Soporte para múltiples especialidades médicas")
    print("=" * 60)


# ============================
#       FUNCIÓN PRINCIPAL
# ============================

def main():
    """
    Función principal del programa.
    Inicializa y ejecuta la aplicación de turnos médicos.
    """
    try:
        # Mostrar información del sistema en consola
        mostrar_info_sistema()
        
        # Verificar dependencias antes de continuar
        print("Verificando dependencias...")
        if not verificar_dependencias():
            print("\nNo se puede iniciar la aplicación debido a dependencias faltantes.")
            input("Presione Enter para salir...")
            return
        
        print("Todas las dependencias esenciales están disponibles.")
        print("Iniciando aplicación...")
        print("-" * 60)
        
        # Crear y ejecutar la aplicación
        app = InterfazTurnos()
        app.ejecutar()
        
    except KeyboardInterrupt:
        print("\n\nAplicación interrumpida por el usuario.")
        
    except Exception as e:
        print(f"\n Error fatal en la aplicación: {e}")
        
        # Intentar mostrar el error en una ventana emergente
        try:
            root = tk.Tk()
            root.withdraw()  # Ocultar la ventana principal vacía
            messagebox.showerror(
                "Error Fatal", 
                f"Ocurrió un error inesperado al ejecutar la aplicación:\n\n{str(e)}\n\n"
                "Consulte la consola para más detalles."
            )
            root.destroy()
        except Exception:
            # Si ni siquiera Tkinter funciona, la consola es la única opción
            pass
            
    finally:
        print("\n" + "=" * 60)
        print("Aplicación finalizada.")
        print("Gracias por usar el Sistema de Turnos Médicos.")
        print("=" * 60)


# ============================
#      PUNTO DE ENTRADA
# ============================

if __name__ == "__main__":
    # Verificar versión de Python
    if sys.version_info < (3, 6):
        print("Error: Este programa requiere Python 3.6 o superior.")
        print(f"Versión actual: {sys.version}")
        sys.exit(1)
    
    # Ejecutar programa principal
    main()