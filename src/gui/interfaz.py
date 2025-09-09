"""
Módulo que implementa la interfaz gráfica del sistema de turnos médicos usando Tkinter.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from PIL import Image, ImageTk
import os
import threading

from services.turno_service import TurnoService
from services.graphviz_service import GraphvizService
from utils.constantes import (
    VENTANA_TITULO, VENTANA_ANCHO, VENTANA_ALTO,
    ESPECIALIDADES, COLOR_FONDO, COLOR_PRIMARIO,
    FUENTE_TITULO, FUENTE_NORMAL, MENSAJE_COLA_VACIA,
    MENSAJE_PACIENTE_ATENDIDO, MENSAJE_ERROR_CAMPOS,
    MENSAJE_ERROR_EDAD
)


class InterfazTurnos:
    """
    Clase que maneja la interfaz gráfica del sistema de turnos médicos.
    """
    
    def __init__(self):
        """Inicializa la interfaz gráfica."""
        self.turno_service = TurnoService()
        self.graphviz_service = GraphvizService()
        
        # Crear ventana principal
        self.root = tk.Tk()
        self.root.title(VENTANA_TITULO)
        self.root.geometry(f"{VENTANA_ANCHO}x{VENTANA_ALTO}")
        self.root.configure(bg=COLOR_FONDO)
        self.root.resizable(True, True)
        
        # Variables de la interfaz
        self.nombre_var = tk.StringVar()
        self.edad_var = tk.StringVar()
        self.especialidad_var = tk.StringVar(value=ESPECIALIDADES[0])
        
        self._crear_widgets()
        self._actualizar_display()
    
    def _crear_widgets(self):
        """Crea todos los widgets de la interfaz."""
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        titulo_label = ttk.Label(main_frame, text=VENTANA_TITULO, 
                                font=FUENTE_TITULO)
        titulo_label.pack(pady=(0, 20))
        
        # Frame superior para formulario
        form_frame = ttk.LabelFrame(main_frame, text="Registrar Nuevo Turno", 
                                   padding=20)
        form_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Campos del formulario
        self._crear_formulario(form_frame)
        
        # Frame para botones principales
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        self._crear_botones_principales(button_frame)
        
        # Frame para visualización
        display_frame = ttk.Frame(main_frame)
        display_frame.pack(fill=tk.BOTH, expand=True)
        
        self._crear_area_visualizacion(display_frame)
    
    def _crear_formulario(self, parent):
        """Crea el formulario de registro de turnos."""
        # Grid para organizar campos
        campos_frame = ttk.Frame(parent)
        campos_frame.pack(fill=tk.X)
        
        # Nombre
        ttk.Label(campos_frame, text="Nombre:", font=FUENTE_NORMAL).grid(
            row=0, column=0, sticky=tk.W, padx=(0, 10), pady=5)
        
        nombre_entry = ttk.Entry(campos_frame, textvariable=self.nombre_var, 
                                font=FUENTE_NORMAL, width=20)
        nombre_entry.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Edad
        ttk.Label(campos_frame, text="Edad:", font=FUENTE_NORMAL).grid(
            row=0, column=2, sticky=tk.W, padx=(20, 10), pady=5)
        
        edad_entry = ttk.Entry(campos_frame, textvariable=self.edad_var, 
                              font=FUENTE_NORMAL, width=10)
        edad_entry.grid(row=0, column=3, sticky=tk.W, pady=5)
        
        # Especialidad
        ttk.Label(campos_frame, text="Especialidad:", font=FUENTE_NORMAL).grid(
            row=1, column=0, sticky=tk.W, padx=(0, 10), pady=5)
        
        especialidad_combo = ttk.Combobox(campos_frame, textvariable=self.especialidad_var,
                                         values=ESPECIALIDADES, state="readonly",
                                         font=FUENTE_NORMAL, width=25)
        especialidad_combo.grid(row=1, column=1, columnspan=2, sticky=tk.W, pady=5)
        
        # Botón registrar
        registrar_btn = ttk.Button(campos_frame, text="Registrar Turno",
                                  command=self._registrar_turno)
        registrar_btn.grid(row=1, column=3, sticky=tk.E, padx=(10, 0), pady=5)
    
    def _crear_botones_principales(self, parent):
        """Crea los botones principales de acción."""
        # Botón atender paciente
        atender_btn = ttk.Button(parent, text="Atender Siguiente Paciente",
                                command=self._atender_paciente)
        atender_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón generar gráfico
        grafico_btn = ttk.Button(parent, text="Generar Gráfico",
                                command=self._generar_grafico)
        grafico_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón ver estadísticas
        stats_btn = ttk.Button(parent, text="Ver Estadísticas",
                              command=self._mostrar_estadisticas)
        stats_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón limpiar cola
        limpiar_btn = ttk.Button(parent, text="Limpiar Cola",
                                command=self._limpiar_cola)
        limpiar_btn.pack(side=tk.RIGHT)
    
    def _crear_area_visualizacion(self, parent):
        """Crea el área de visualización de turnos."""
        # Crear notebook para pestañas
        notebook = ttk.Notebook(parent)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Pestaña de cola actual
        cola_frame = ttk.Frame(notebook)
        notebook.add(cola_frame, text="Cola de Turnos")
        
        # Área de texto para mostrar cola
        self.cola_text = scrolledtext.ScrolledText(cola_frame, 
                                                  font=FUENTE_NORMAL,
                                                  state=tk.DISABLED,
                                                  wrap=tk.WORD)
        self.cola_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Pestaña de información del sistema
        info_frame = ttk.Frame(notebook)
        notebook.add(info_frame, text="Información del Sistema")
        
        self.info_text = scrolledtext.ScrolledText(info_frame,
                                                  font=FUENTE_NORMAL,
                                                  state=tk.DISABLED,
                                                  wrap=tk.WORD)
        self.info_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Pestaña de visualización gráfica
        visual_frame = ttk.Frame(notebook)
        notebook.add(visual_frame, text="Visualización Gráfica")
        
        # Label para mostrar imagen
        self.imagen_label = ttk.Label(visual_frame, text="Genere un gráfico para visualizar la cola")
        self.imagen_label.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def _registrar_turno(self):
        """Registra un nuevo turno en la cola."""
        try:
            # Obtener valores del formulario
            nombre = self.nombre_var.get().strip()
            edad_str = self.edad_var.get().strip()
            especialidad = self.especialidad_var.get()
            
            # Validar campos
            if not nombre or not edad_str:
                messagebox.showerror("Error", MENSAJE_ERROR_CAMPOS)
                return
            
            try:
                edad = int(edad_str)
            except ValueError:
                messagebox.showerror("Error", MENSAJE_ERROR_EDAD)
                return
            
            # Registrar turno
            paciente = self.turno_service.registrar_turno(nombre, edad, especialidad)
            
            # Mostrar mensaje de éxito
            messagebox.showinfo("Éxito", 
                               f"Turno registrado correctamente.\n"
                               f"Número de turno: {paciente.numero_turno}")
            
            # Limpiar formulario
            self.nombre_var.set("")
            self.edad_var.set("")
            self.especialidad_var.set(ESPECIALIDADES[0])
            
            # Actualizar display
            self._actualizar_display()
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
    
    def _atender_paciente(self):
        """Atiende al siguiente paciente en la cola."""
        try:
            paciente = self.turno_service.atender_siguiente_paciente()
            
            # Mostrar información del paciente atendido
            tiempo_atencion = self.turno_service.obtener_tiempo_atencion(paciente.especialidad)
            tiempo_espera = paciente.tiempo_espera_actual()
            
            mensaje = (f"{MENSAJE_PACIENTE_ATENDIDO}\n\n"
                      f"Paciente: {paciente.nombre}\n"
                      f"Edad: {paciente.edad} años\n"
                      f"Especialidad: {paciente.especialidad}\n"
                      f"Tiempo de espera: {tiempo_espera} minutos\n"
                      f"Tiempo de atención: {tiempo_atencion} minutos")
            
            messagebox.showinfo("Paciente Atendido", mensaje)
            
            # Actualizar display
            self._actualizar_display()
            
        except IndexError:
            messagebox.showwarning("Advertencia", MENSAJE_COLA_VACIA)
        except Exception as e:
            messagebox.showerror("Error", f"Error al atender paciente: {str(e)}")
    
    def _generar_grafico(self):
        """Genera el gráfico visual de la cola."""
        try:
            if not self.graphviz_service.verificar_graphviz_instalado():
                messagebox.showerror("Error", 
                                   "Graphviz no está instalado o no está disponible.\n"
                                   "Por favor, instale Graphviz para usar esta función.")
                return
            
            # Generar gráfico en un hilo separado para no bloquear la interfaz
            def generar_en_hilo():
                archivo_imagen = self.graphviz_service.generar_grafico_cola(
                    self.turno_service.cola_turnos)
                
                if archivo_imagen and os.path.exists(archivo_imagen):
                    # Actualizar imagen en el hilo principal
                    self.root.after(0, lambda: self._mostrar_imagen(archivo_imagen))
                else:
                    self.root.after(0, lambda: messagebox.showerror("Error", 
                                                                   "No se pudo generar el gráfico"))
            
            # Ejecutar en hilo separado
            threading.Thread(target=generar_en_hilo, daemon=True).start()
            
            # Mostrar mensaje de progreso
            messagebox.showinfo("Información", "Generando gráfico, por favor espere...")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar gráfico: {str(e)}")
    
    def _mostrar_imagen(self, archivo_imagen):
        """Muestra la imagen generada en la interfaz."""
        try:
            # Abrir y redimensionar imagen
            imagen = Image.open(archivo_imagen)
            
            # Calcular tamaño apropiado
            ancho_max, alto_max = 600, 400
            imagen.thumbnail((ancho_max, alto_max), Image.Resampling.LANCZOS)
            
            # Convertir para Tkinter
            foto = ImageTk.PhotoImage(imagen)
            
            # Actualizar label
            self.imagen_label.configure(image=foto, text="")
            self.imagen_label.image = foto  # Mantener referencia
            
            messagebox.showinfo("Éxito", "Gráfico generado correctamente")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar imagen: {str(e)}")
    
    def _mostrar_estadisticas(self):
        """Muestra estadísticas detalladas del sistema."""
        try:
            estadisticas = self.turno_service.obtener_estadisticas()
            
            # Generar gráfico de estadísticas
            if self.graphviz_service.verificar_graphviz_instalado():
                archivo_stats = self.graphviz_service.generar_grafico_estadisticas(estadisticas)
                
                if archivo_stats and os.path.exists(archivo_stats):
                    # Mostrar ventana con estadísticas
                    self._ventana_estadisticas(estadisticas, archivo_stats)
                else:
                    self._ventana_estadisticas(estadisticas)
            else:
                self._ventana_estadisticas(estadisticas)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar estadísticas: {str(e)}")
    
    def _ventana_estadisticas(self, estadisticas, archivo_imagen=None):
        """Crea una ventana separada para mostrar estadísticas."""
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Estadísticas del Sistema")
        stats_window.geometry("500x600")
        stats_window.resizable(True, True)
        
        # Frame principal
        main_frame = ttk.Frame(stats_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        ttk.Label(main_frame, text="Estadísticas del Sistema", 
                 font=FUENTE_TITULO).pack(pady=(0, 10))
        
        # Información general
        info_frame = ttk.LabelFrame(main_frame, text="Información General", padding=10)
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        total_pacientes = estadisticas.get('total_pacientes', 0)
        tiempo_total = estadisticas.get('tiempo_total_estimado', 0)
        
        ttk.Label(info_frame, text=f"Total de pacientes en cola: {total_pacientes}",
                 font=FUENTE_NORMAL).pack(anchor=tk.W)
        ttk.Label(info_frame, text=f"Tiempo total estimado: {tiempo_total} minutos",
                 font=FUENTE_NORMAL).pack(anchor=tk.W)
        
        # Especialidades
        esp_frame = ttk.LabelFrame(main_frame, text="Distribución por Especialidades", 
                                  padding=10)
        esp_frame.pack(fill=tk.X, pady=(0, 10))
        
        especialidades = estadisticas.get('especialidades', {})
        if especialidades:
            for especialidad, cantidad in especialidades.items():
                tiempo_esp = self.turno_service.obtener_tiempo_atencion(especialidad)
                texto = f"{especialidad}: {cantidad} paciente(s) ({tiempo_esp} min c/u)"
                ttk.Label(esp_frame, text=texto, font=FUENTE_NORMAL).pack(anchor=tk.W)
        else:
            ttk.Label(esp_frame, text="No hay pacientes en cola", 
                     font=FUENTE_NORMAL).pack(anchor=tk.W)
        
        # Imagen de estadísticas
        if archivo_imagen:
            try:
                imagen = Image.open(archivo_imagen)
                imagen.thumbnail((400, 300), Image.Resampling.LANCZOS)
                foto = ImageTk.PhotoImage(imagen)
                
                imagen_label = ttk.Label(main_frame, image=foto)
                imagen_label.pack(pady=10)
                imagen_label.image = foto  # Mantener referencia
            except Exception as e:
                print(f"Error al cargar imagen de estadísticas: {e}")
    
    def _limpiar_cola(self):
        """Limpia completamente la cola de turnos."""
        if self.turno_service.hay_turnos_pendientes():
            respuesta = messagebox.askyesno("Confirmar", 
                                          "¿Está seguro de que desea limpiar toda la cola?\n"
                                          "Esta acción no se puede deshacer.")
            if respuesta:
                self.turno_service.limpiar_turnos()
                messagebox.showinfo("Información", "Cola limpiada correctamente")
                self._actualizar_display()
        else:
            messagebox.showinfo("Información", "La cola ya está vacía")
    
    def _actualizar_display(self):
        """Actualiza la información mostrada en la interfaz."""
        # Actualizar cola de turnos
        self._actualizar_cola_display()
        
        # Actualizar información del sistema
        self._actualizar_info_display()
    
    def _actualizar_cola_display(self):
        """Actualiza la visualización de la cola de turnos."""
        self.cola_text.configure(state=tk.NORMAL)
        self.cola_text.delete(1.0, tk.END)
        
        if not self.turno_service.hay_turnos_pendientes():
            self.cola_text.insert(tk.END, MENSAJE_COLA_VACIA)
        else:
            pacientes = self.turno_service.obtener_todos_turnos()
            self.cola_text.insert(tk.END, "COLA DE TURNOS ACTUAL\n")
            self.cola_text.insert(tk.END, "=" * 50 + "\n\n")
            
            for i, paciente in enumerate(pacientes):
                tiempo_espera = self.turno_service.calcular_tiempo_espera_paciente(i)
                tiempo_atencion = self.turno_service.obtener_tiempo_atencion(paciente.especialidad)
                tiempo_total = tiempo_espera + tiempo_atencion
                
                posicion_texto = "SIGUIENTE" if i == 0 else f"Posición {i + 1}"
                
                info_paciente = (
                    f"[{posicion_texto}] {paciente}\n"
                    f"   Tiempo de espera estimado: {tiempo_espera} min\n"
                    f"   Tiempo de atención: {tiempo_atencion} min\n"
                    f"   Tiempo total estimado: {tiempo_total} min\n\n"
                )
                
                self.cola_text.insert(tk.END, info_paciente)
        
        self.cola_text.configure(state=tk.DISABLED)
    
    def _actualizar_info_display(self):
        """Actualiza la información general del sistema."""
        self.info_text.configure(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        
        # Información general
        self.info_text.insert(tk.END, "INFORMACIÓN DEL SISTEMA DE TURNOS\n")
        self.info_text.insert(tk.END, "=" * 50 + "\n\n")
        
        # Estadísticas actuales
        estadisticas = self.turno_service.obtener_estadisticas()
        
        self.info_text.insert(tk.END, f"Total de turnos pendientes: {estadisticas['total_pacientes']}\n")
        self.info_text.insert(tk.END, f"Tiempo total estimado: {estadisticas['tiempo_total_estimado']} minutos\n\n")
        
        # Información de especialidades
        self.info_text.insert(tk.END, "ESPECIALIDADES DISPONIBLES:\n")
        self.info_text.insert(tk.END, "-" * 30 + "\n")
        
        for especialidad in ESPECIALIDADES:
            tiempo = self.turno_service.obtener_tiempo_atencion(especialidad)
            cantidad = estadisticas['especialidades'].get(especialidad, 0)
            
            self.info_text.insert(tk.END, 
                                 f"{especialidad}: {tiempo} min (Actual: {cantidad} pacientes)\n")
        
        # Próximo paciente
        self.info_text.insert(tk.END, f"\n{'=' * 50}\n")
        siguiente = self.turno_service.ver_siguiente_paciente()
        
        if siguiente:
            self.info_text.insert(tk.END, f"PRÓXIMO PACIENTE:\n{siguiente}\n")
            tiempo_espera_actual = siguiente.tiempo_espera_actual()
            self.info_text.insert(tk.END, f"Tiempo esperando: {tiempo_espera_actual} minutos\n")
        else:
            self.info_text.insert(tk.END, "PRÓXIMO PACIENTE: Ninguno\n")
        
        self.info_text.configure(state=tk.DISABLED)
    
    def ejecutar(self):
        """Ejecuta la aplicación."""
        try:
            # Verificar si Graphviz está disponible
            if not self.graphviz_service.verificar_graphviz_instalado():
                messagebox.showwarning("Advertencia", 
                                     "Graphviz no está instalado.\n"
                                     "Las funciones de visualización gráfica no estarán disponibles.\n"
                                     "Para instalar: pip install graphviz")
            
            # Iniciar bucle principal
            self.root.mainloop()
            
        except Exception as e:
            messagebox.showerror("Error Fatal", f"Error al ejecutar la aplicación: {str(e)}")
        finally:
            # Limpiar archivos temporales
            self.graphviz_service.limpiar_archivos_generados()