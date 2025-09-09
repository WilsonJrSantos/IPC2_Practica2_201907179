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
    ESPECIALIDADES, COLOR_FONDO, COLOR_PRIMARIO, COLOR_SECUNDARIO,
    COLOR_EXITO, COLOR_ERROR, FUENTE_TITULO, FUENTE_NORMAL,
    MENSAJE_COLA_VACIA, MENSAJE_PACIENTE_ATENDIDO,
    MENSAJE_ERROR_CAMPOS, MENSAJE_ERROR_EDAD
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
        
        # Configurar estilos de la aplicación
        self._configurar_estilos()
        
        # Variables de la interfaz
        self.nombre_var = tk.StringVar()
        self.edad_var = tk.StringVar()
        self.especialidad_var = tk.StringVar(value=ESPECIALIDADES[0])
        
        self._crear_widgets()
        self._actualizar_display()

    def _configurar_estilos(self):
        """Configura los estilos para los widgets de ttk."""
        self.style = ttk.Style(self.root)
        self.style.theme_use('clam') # Usar un tema que permita personalización

        # Estilo general para Frames y Labels
        self.style.configure('TFrame', background=COLOR_FONDO)
        self.style.configure('TLabel', background=COLOR_FONDO, foreground="#333", font=FUENTE_NORMAL)
        self.style.configure('Titulo.TLabel', background=COLOR_FONDO, foreground=COLOR_PRIMARIO, font=FUENTE_TITULO)
        
        # Estilo para LabelFrame (marcos con título)
        self.style.configure('TLabelFrame', background=COLOR_FONDO, bordercolor=COLOR_PRIMARIO, font=FUENTE_NORMAL)
        self.style.configure('TLabelFrame.Label', background=COLOR_FONDO, foreground=COLOR_PRIMARIO, font=FUENTE_NORMAL)

        # Estilo para Botones
        self.style.configure('TButton', font=FUENTE_NORMAL, padding=5, borderwidth=0)
        self.style.map('TButton',
                       foreground=[('pressed', 'white'), ('active', 'white')],
                       background=[('pressed', '!disabled', COLOR_SECUNDARIO), ('active', COLOR_SECUNDARIO)])

        self.style.configure('Primary.TButton', background=COLOR_PRIMARIO, foreground='white')
        self.style.configure('Success.TButton', background=COLOR_EXITO, foreground='white')
        self.style.configure('Danger.TButton', background=COLOR_ERROR, foreground='white')
        
        # Estilo para Combobox
        self.style.map('TCombobox', fieldbackground=[('readonly', 'white')])
        self.style.map('TCombobox', selectbackground=[('readonly', COLOR_PRIMARIO)])
        self.style.map('TCombobox', selectforeground=[('readonly', 'white')])

        # Estilo para Notebook (pestañas)
        self.style.configure('TNotebook', background=COLOR_FONDO, borderwidth=0)
        self.style.configure('TNotebook.Tab', background=COLOR_FONDO, foreground=COLOR_SECUNDARIO,
                             font=FUENTE_NORMAL, padding=[10, 5], borderwidth=0)
        self.style.map('TNotebook.Tab',
                       background=[('selected', COLOR_PRIMARIO)],
                       foreground=[('selected', 'white')])

    def _crear_widgets(self):
        """Crea todos los widgets de la interfaz."""
        # Frame principal
        main_frame = ttk.Frame(self.root, style='TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        titulo_label = ttk.Label(main_frame, text=VENTANA_TITULO, style='Titulo.TLabel')
        titulo_label.pack(pady=(0, 20))
        
        # Frame superior para formulario
        form_frame = ttk.LabelFrame(main_frame, text="Registrar Nuevo Turno", padding=20)
        form_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Campos del formulario
        self._crear_formulario(form_frame)
        
        # Frame para botones principales
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 20))
        
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
        campos_frame.columnconfigure(1, weight=1) # Hacer la columna del entry expandible
        campos_frame.columnconfigure(3, weight=1)
        
        # Nombre
        ttk.Label(campos_frame, text="Nombre:").grid(
            row=0, column=0, sticky=tk.W, padx=(0, 10), pady=5)
        
        nombre_entry = ttk.Entry(campos_frame, textvariable=self.nombre_var, 
                                font=FUENTE_NORMAL, width=25)
        nombre_entry.grid(row=0, column=1, sticky="ew", pady=5)
        
        # Edad
        ttk.Label(campos_frame, text="Edad:").grid(
            row=0, column=2, sticky=tk.W, padx=(20, 10), pady=5)
        
        edad_entry = ttk.Entry(campos_frame, textvariable=self.edad_var, 
                              font=FUENTE_NORMAL, width=10)
        edad_entry.grid(row=0, column=3, sticky=tk.W, pady=5)
        
        # Especialidad
        ttk.Label(campos_frame, text="Especialidad:").grid(
            row=1, column=0, sticky=tk.W, padx=(0, 10), pady=5)
        
        especialidad_combo = ttk.Combobox(campos_frame, textvariable=self.especialidad_var,
                                          values=ESPECIALIDADES, state="readonly",
                                          font=FUENTE_NORMAL, width=25)
        especialidad_combo.grid(row=1, column=1, sticky="ew", pady=5)
        
        # Botón registrar
        registrar_btn = ttk.Button(campos_frame, text="Registrar Turno",
                                   command=self._registrar_turno, style='Primary.TButton')
        registrar_btn.grid(row=1, column=2, columnspan=2, sticky=tk.E, padx=(10, 0), pady=5)
    
    def _crear_botones_principales(self, parent):
        """Crea los botones principales de acción."""
        # Botón atender paciente
        atender_btn = ttk.Button(parent, text="Atender Siguiente Paciente",
                                 command=self._atender_paciente, style='Success.TButton')
        atender_btn.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
        
        # Botón generar gráfico
        grafico_btn = ttk.Button(parent, text="Generar Gráfico",
                                 command=self._generar_grafico, style='TButton')
        grafico_btn.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
        
        # Botón ver estadísticas
        stats_btn = ttk.Button(parent, text="Ver Estadísticas",
                               command=self._mostrar_estadisticas, style='TButton')
        stats_btn.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
        
        # Botón limpiar cola
        limpiar_btn = ttk.Button(parent, text="Limpiar Cola",
                                 command=self._limpiar_cola, style='Danger.TButton')
        limpiar_btn.pack(side=tk.RIGHT, fill=tk.X, expand=True)
    
    def _crear_area_visualizacion(self, parent):
        """Crea el área de visualización de turnos."""
        # Crear notebook para pestañas
        notebook = ttk.Notebook(parent, style='TNotebook')
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Pestaña de cola actual
        cola_frame = ttk.Frame(notebook, padding=10)
        notebook.add(cola_frame, text="Cola de Turnos")
        
        # Área de texto para mostrar cola
        self.cola_text = scrolledtext.ScrolledText(cola_frame, 
                                                   font=FUENTE_NORMAL,
                                                   state=tk.DISABLED,
                                                   wrap=tk.WORD,
                                                   bg="white", fg="#333",
                                                   relief=tk.FLAT)
        self.cola_text.pack(fill=tk.BOTH, expand=True)
        
        # Pestaña de información del sistema
        info_frame = ttk.Frame(notebook, padding=10)
        notebook.add(info_frame, text="Información del Sistema")
        
        self.info_text = scrolledtext.ScrolledText(info_frame,
                                                   font=FUENTE_NORMAL,
                                                   state=tk.DISABLED,
                                                   wrap=tk.WORD,
                                                   bg="white", fg="#333",
                                                   relief=tk.FLAT)
        self.info_text.pack(fill=tk.BOTH, expand=True)
        
        # Pestaña de visualización gráfica
        visual_frame = ttk.Frame(notebook)
        notebook.add(visual_frame, text="Visualización Gráfica")
        
        # Label para mostrar imagen
        self.imagen_label = ttk.Label(visual_frame, text="\nGenere un gráfico para visualizar la cola\n", 
                                      style='TLabel', anchor="center")
        self.imagen_label.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    # --- El resto de los métodos (_registrar_turno, _atender_paciente, etc.) permanecen iguales ---
    # (Se omiten por brevedad, no necesitan cambios para la implementación de estilos)

    def _registrar_turno(self):
        """Registra un nuevo turno en la cola."""
        try:
            nombre = self.nombre_var.get().strip()
            edad_str = self.edad_var.get().strip()
            especialidad = self.especialidad_var.get()
            
            if not nombre or not edad_str:
                messagebox.showerror("Error", MENSAJE_ERROR_CAMPOS)
                return
            
            try:
                edad = int(edad_str)
            except ValueError:
                messagebox.showerror("Error", MENSAJE_ERROR_EDAD)
                return
            
            paciente = self.turno_service.registrar_turno(nombre, edad, especialidad)
            
            messagebox.showinfo("Éxito", 
                              f"Turno registrado correctamente.\n"
                              f"Número de turno: {paciente.numero_turno}")
            
            self.nombre_var.set("")
            self.edad_var.set("")
            self.especialidad_var.set(ESPECIALIDADES[0])
            
            self._actualizar_display()
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")

    def _atender_paciente(self):
        """Atiende al siguiente paciente en la cola."""
        try:
            paciente = self.turno_service.atender_siguiente_paciente()
            
            tiempo_atencion = self.turno_service.obtener_tiempo_atencion(paciente.especialidad)
            tiempo_espera = paciente.tiempo_espera_actual()
            
            mensaje = (f"{MENSAJE_PACIENTE_ATENDIDO}\n\n"
                       f"Paciente: {paciente.nombre}\n"
                       f"Edad: {paciente.edad} años\n"
                       f"Especialidad: {paciente.especialidad}\n"
                       f"Tiempo de espera: {tiempo_espera} minutos\n"
                       f"Tiempo de atención: {tiempo_atencion} minutos")
            
            messagebox.showinfo("Paciente Atendido", mensaje)
            
            self._actualizar_display()
            
        except IndexError:
            messagebox.showwarning("Advertencia", MENSAJE_COLA_VACIA)
        except Exception as e:
            messagebox.showerror("Error", f"Error al atender paciente: {str(e)}")

    def _generar_grafico(self):
        """Genera el gráfico visual de la cola."""
        try:
            if not self.turno_service.hay_turnos_pendientes():
                messagebox.showwarning("Advertencia", MENSAJE_COLA_VACIA)
                return
                
            if not self.graphviz_service.verificar_graphviz_instalado():
                messagebox.showerror("Error", 
                                     "Graphviz no está instalado o no está en el PATH.\n"
                                     "Por favor, instale Graphviz para usar esta función.")
                return
            
            def generar_en_hilo():
                archivo_imagen = self.graphviz_service.generar_grafico_cola(
                    self.turno_service.cola_turnos)
                
                if archivo_imagen and os.path.exists(archivo_imagen):
                    self.root.after(0, lambda: self._mostrar_imagen(archivo_imagen))
                else:
                    self.root.after(0, lambda: messagebox.showerror("Error", 
                                      "No se pudo generar el gráfico. Verifique la consola."))
            
            threading.Thread(target=generar_en_hilo, daemon=True).start()
            messagebox.showinfo("Información", "Generando gráfico, por favor espere...")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar gráfico: {str(e)}")

    def _mostrar_imagen(self, archivo_imagen):
        """Muestra la imagen generada en la interfaz."""
        try:
            imagen = Image.open(archivo_imagen)
            
            ancho_max, alto_max = self.imagen_label.winfo_width(), self.imagen_label.winfo_height()
            if ancho_max < 50 or alto_max < 50:
                ancho_max, alto_max = 600, 400

            imagen.thumbnail((ancho_max - 20, alto_max - 20), Image.Resampling.LANCZOS)
            
            foto = ImageTk.PhotoImage(imagen)
            
            self.imagen_label.configure(image=foto, text="")
            self.imagen_label.image = foto
            
            messagebox.showinfo("Éxito", "Gráfico generado correctamente")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar imagen: {str(e)}")

    def _mostrar_estadisticas(self):
        """Muestra estadísticas detalladas del sistema."""
        try:
            estadisticas = self.turno_service.obtener_estadisticas()
            self._ventana_estadisticas(estadisticas)
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar estadísticas: {str(e)}")

    def _ventana_estadisticas(self, estadisticas):
        """Crea una ventana separada para mostrar estadísticas."""
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Estadísticas del Sistema")
        stats_window.geometry("450x300")
        stats_window.resizable(False, False)
        stats_window.configure(bg=COLOR_FONDO)
        
        main_frame = ttk.Frame(stats_window, style='TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(main_frame, text="Estadísticas del Sistema", 
                  style='Titulo.TLabel').pack(pady=(0, 15))
        
        info_frame = ttk.LabelFrame(main_frame, text="Resumen General", padding=10)
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        total_pacientes = estadisticas.get('total_pacientes', 0)
        tiempo_total = estadisticas.get('tiempo_total_estimado', 0)
        
        ttk.Label(info_frame, text=f"Total de pacientes en cola: {total_pacientes}").pack(anchor=tk.W)
        ttk.Label(info_frame, text=f"Tiempo total de espera estimado: {tiempo_total} minutos").pack(anchor=tk.W)
        
        esp_frame = ttk.LabelFrame(main_frame, text="Distribución por Especialidad", padding=10)
        esp_frame.pack(fill=tk.X)
        
        especialidades_stats = estadisticas.get('especialidades', {})
        if especialidades_stats:
            for especialidad, cantidad in especialidades_stats.items():
                texto = f"{especialidad}: {cantidad} paciente(s)"
                ttk.Label(esp_frame, text=texto).pack(anchor=tk.W)
        else:
            ttk.Label(esp_frame, text="No hay pacientes en cola.").pack(anchor=tk.W)

    def _limpiar_cola(self):
        """Limpia completamente la cola de turnos."""
        if self.turno_service.hay_turnos_pendientes():
            respuesta = messagebox.askyesno("Confirmar Limpieza", 
                                              "¿Está seguro de que desea limpiar toda la cola?\n"
                                              "Esta acción no se puede deshacer.")
            if respuesta:
                self.turno_service.limpiar_turnos()
                messagebox.showinfo("Información", "La cola ha sido limpiada.")
                self._actualizar_display()
                self.imagen_label.configure(image=None, text="\nGenere un gráfico para visualizar la cola\n")
                self.imagen_label.image = None
        else:
            messagebox.showinfo("Información", "La cola ya está vacía.")
    
    def _actualizar_display(self):
        """Actualiza la información mostrada en la interfaz."""
        self._actualizar_cola_display()
        self._actualizar_info_display()

    def _actualizar_cola_display(self):
        """Actualiza la visualización de la cola de turnos."""
        self.cola_text.configure(state=tk.NORMAL)
        self.cola_text.delete(1.0, tk.END)
        
        if not self.turno_service.hay_turnos_pendientes():
            self.cola_text.insert(tk.END, MENSAJE_COLA_VACIA)
        else:
            pacientes = self.turno_service.obtener_todos_turnos()
            self.cola_text.insert(tk.END, "COLA DE TURNOS ACTUAL\n", ('titulo',))
            self.cola_text.insert(tk.END, "=" * 50 + "\n\n")
            
            for i, paciente in enumerate(pacientes):
                tiempo_espera = self.turno_service.calcular_tiempo_espera_paciente(i)
                
                posicion_texto = "SIGUIENTE" if i == 0 else f"Posición {i + 1}"
                tag = 'siguiente' if i == 0 else 'normal'

                info_paciente = (
                    f"[{posicion_texto}] {paciente.nombre} ({paciente.edad} años) - {paciente.especialidad}\n"
                    f"   └─ Tiempo de espera estimado: {tiempo_espera} min\n\n"
                )
                self.cola_text.insert(tk.END, info_paciente, (tag,))
        
        # Aplicar tags de formato
        self.cola_text.tag_config('titulo', font=FUENTE_TITULO, foreground=COLOR_PRIMARIO)
        self.cola_text.tag_config('siguiente', font=(FUENTE_NORMAL[0], FUENTE_NORMAL[1], 'bold'), foreground=COLOR_EXITO)
        self.cola_text.tag_config('normal', font=FUENTE_NORMAL)

        self.cola_text.configure(state=tk.DISABLED)

    def _actualizar_info_display(self):
        """Actualiza la información general del sistema."""
        self.info_text.configure(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        
        estadisticas = self.turno_service.obtener_estadisticas()
        
        self.info_text.insert(tk.END, "INFORMACIÓN GENERAL\n", ('titulo',))
        self.info_text.insert(tk.END, "=" * 50 + "\n\n")
        self.info_text.insert(tk.END, f"› Total de turnos pendientes: {estadisticas['total_pacientes']}\n")
        self.info_text.insert(tk.END, f"› Tiempo total estimado: {estadisticas['tiempo_total_estimado']} minutos\n\n")
        
        self.info_text.insert(tk.END, "PACIENTES POR ESPECIALIDAD\n", ('subtitulo',))
        self.info_text.insert(tk.END, "-" * 30 + "\n")
        
        for especialidad in ESPECIALIDADES:
            tiempo = self.turno_service.obtener_tiempo_atencion(especialidad)
            cantidad = estadisticas['especialidades'].get(especialidad, 0)
            self.info_text.insert(tk.END, 
                f"› {especialidad}: {cantidad} paciente(s) ({tiempo} min c/u)\n")
        
        self.info_text.insert(tk.END, f"\n{'=' * 50}\n\n")
        siguiente = self.turno_service.ver_siguiente_paciente()
        
        self.info_text.insert(tk.END, "PRÓXIMO PACIENTE A ATENDER\n", ('subtitulo',))
        self.info_text.insert(tk.END, "-" * 30 + "\n")

        if siguiente:
            self.info_text.insert(tk.END, f"› {siguiente}\n", ('siguiente',))
            tiempo_espera_actual = siguiente.tiempo_espera_actual()
            self.info_text.insert(tk.END, f"  Tiempo esperando: {tiempo_espera_actual} minutos\n")
        else:
            self.info_text.insert(tk.END, "› Ninguno. La cola está vacía.\n")
        
        # Aplicar tags
        self.info_text.tag_config('titulo', font=FUENTE_TITULO, foreground=COLOR_PRIMARIO)
        self.info_text.tag_config('subtitulo', font=(FUENTE_NORMAL[0], FUENTE_NORMAL[1], 'bold'), foreground=COLOR_PRIMARIO)
        self.info_text.tag_config('siguiente', font=(FUENTE_NORMAL[0], FUENTE_NORMAL[1], 'bold'), foreground=COLOR_EXITO)

        self.info_text.configure(state=tk.DISABLED)

    def ejecutar(self):
        """Ejecuta la aplicación."""
        try:
            self.root.mainloop()
        except Exception as e:
            messagebox.showerror("Error Fatal", f"Error al ejecutar la aplicación: {str(e)}")
        finally:
            self.graphviz_service.limpiar_archivos_generados()