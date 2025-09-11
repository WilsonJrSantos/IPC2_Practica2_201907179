# src/gui/interfaz.py
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
from models.reporte import ReporteEstadisticas
from utils.constantes import (
    VENTANA_TITULO, VENTANA_ANCHO, VENTANA_ALTO,
    ESPECIALIDAD_1, ESPECIALIDAD_2, ESPECIALIDAD_3, ESPECIALIDAD_4,
    COLOR_FONDO, COLOR_PRIMARIO, COLOR_SECUNDARIO,
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
        
        self.root = tk.Tk()
        self.root.title(VENTANA_TITULO)
        self.root.geometry(f"{VENTANA_ANCHO}x{VENTANA_ALTO}")
        self.root.configure(bg=COLOR_FONDO)
        self.root.resizable(True, True)
        
        self._configurar_estilos()
        
        self.nombre_var = tk.StringVar()
        self.edad_var = tk.StringVar()
        self.especialidad_var = tk.StringVar(value=ESPECIALIDAD_1)
        
        self._crear_widgets()
        self._actualizar_display()

    def _configurar_estilos(self):
        """Configura los estilos para los widgets de ttk."""
        self.style = ttk.Style(self.root)
        self.style.theme_use('clam')

        # --- Estilos Generales (sin cambios) ---
        self.style.configure('TFrame', background=COLOR_FONDO)
        self.style.configure('TLabel', background=COLOR_FONDO, foreground="#333", font=FUENTE_NORMAL)
        self.style.configure('Titulo.TLabel', background=COLOR_FONDO, foreground=COLOR_PRIMARIO, font=FUENTE_TITULO)
        self.style.configure('TLabelFrame', background=COLOR_FONDO, bordercolor=COLOR_PRIMARIO, font=FUENTE_NORMAL)
        self.style.configure('TLabelFrame.Label', background=COLOR_FONDO, foreground=COLOR_PRIMARIO, font=FUENTE_NORMAL)

        # --- Jerarquía de Estilos para Botones MEJORADA ---

        # 1. Base para todos los botones: define dimensiones y el EFECTO HOVER UNIFICADO.
        self.style.configure('TButton', font=FUENTE_NORMAL, padding=6, borderwidth=1, focusthickness=0)
        self.style.map('TButton',
                    background=[('active', COLOR_SECUNDARIO)],  # Gris oscuro al pasar el mouse
                    foreground=[('active', 'white')])           # Texto blanco al pasar el mouse

        # 2. Botón Primario (Registrar): Sólido y llamativo.
        self.style.configure('Primary.TButton', background=COLOR_PRIMARIO, foreground='white', borderwidth=0)
        
        # 3. Botón de Éxito (Atender): Verde sólido para la acción principal positiva.
        self.style.configure('Success.TButton', background=COLOR_EXITO, foreground='white', borderwidth=0)

        # 4. Botón Secundario (Estadísticas): Contorno azul, más discreto.
        self.style.configure('Secondary.TButton', 
                            foreground=COLOR_PRIMARIO, 
                            background=COLOR_FONDO, 
                            bordercolor=COLOR_PRIMARIO)

        # 5. Botón de Peligro (Limpiar, Salir): Contorno rojo para acciones finales.
        self.style.configure('Danger.TButton', 
                            foreground=COLOR_ERROR, 
                            background=COLOR_FONDO, 
                            bordercolor=COLOR_ERROR)

        # --- Estilos para otros widgets (sin cambios) ---
        self.style.map('TCombobox', fieldbackground=[('readonly', 'white')], selectbackground=[('readonly', COLOR_PRIMARIO)])
        self.style.configure('TNotebook', background=COLOR_FONDO, borderwidth=0)
        self.style.configure('TNotebook.Tab', background=COLOR_FONDO, foreground=COLOR_SECUNDARIO, font=FUENTE_NORMAL, padding=[10, 5])
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
                                          values=(ESPECIALIDAD_1, ESPECIALIDAD_2, ESPECIALIDAD_3, ESPECIALIDAD_4),
                                          state="readonly", font=FUENTE_NORMAL, width=25)
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
        
        # Botón ver estadísticas
        stats_btn = ttk.Button(parent, text="Ver Estadísticas",
                            command=self._mostrar_estadisticas, style='TButton')
        stats_btn.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)

        #Botón para salir, alineado a la derecha.
        salir_btn = ttk.Button(parent, text="Salir del Programa",
                                command=self.root.destroy, style='Exit.TButton')
        salir_btn.pack(side=tk.RIGHT, fill=tk.X, expand=True)
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
        
    def _dialogo_confirmacion_atencion(self, paciente):
        """
        Crea un diálogo de confirmación modal y personalizado que muestra todos los datos del paciente.
        Devuelve True si se confirma, False si se cancela.
        """
        dialogo = tk.Toplevel(self.root)
        dialogo.title("Confirmar Atención")
        dialogo.configure(bg=COLOR_FONDO)
        dialogo.resizable(False, False)
        
        dialogo.transient(self.root)
        dialogo.grab_set()

        main_frame = ttk.Frame(dialogo, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="¿Desea atender al siguiente paciente?", 
                font=(FUENTE_NORMAL[0], FUENTE_NORMAL[1], 'bold')).pack(pady=(0, 15))
        
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill=tk.X)

        tiempo_espera = self.turno_service.calcular_tiempo_espera_paciente(0)
        tiempo_atencion = self.turno_service.obtener_tiempo_atencion(paciente.especialidad)
        tiempo_total = tiempo_espera + tiempo_atencion

        # Se añade la Especialidad a la lista de datos a mostrar
        labels_info = {
            "Paciente:": paciente.nombre,
            "Especialidad:": paciente.especialidad,
            "Tiempo en Cola:": f"{tiempo_espera} minutos",
            "Tiempo de Atención:": f"{tiempo_atencion} minutos",
            "Tiempo Total:": f"{tiempo_total} minutos"
        }

        row_index = 0
        for key, value in labels_info.items():
            ttk.Label(info_frame, text=key, font=(FUENTE_NORMAL[0], FUENTE_NORMAL[1], 'bold')).grid(row=row_index, column=0, sticky=tk.W, pady=2)
            ttk.Label(info_frame, text=value).grid(row=row_index, column=1, sticky=tk.W, padx=10, pady=2)
            row_index += 1

        resultado = tk.BooleanVar(value=False)

        def confirmar():
            resultado.set(True)
            dialogo.destroy()

        def cancelar():
            resultado.set(False)
            dialogo.destroy()
        
        button_frame = ttk.Frame(main_frame, padding=(0, 20, 0, 0))
        button_frame.pack(fill=tk.X)
        button_frame.columnconfigure((0, 1), weight=1)

        btn_confirmar = ttk.Button(button_frame, text="Confirmar Atención", command=confirmar, style="Success.TButton")
        btn_confirmar.grid(row=0, column=0, sticky=tk.EW, padx=(0, 5))

        btn_cancelar = ttk.Button(button_frame, text="Cancelar", command=cancelar, style="Danger.TButton")
        btn_cancelar.grid(row=0, column=1, sticky=tk.EW, padx=(5, 0))

        self.root.wait_window(dialogo)
        
        return resultado.get()

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
            self.especialidad_var.set(ESPECIALIDAD_1)
            
            # Actualiza los paneles de texto
            self._actualizar_display()
            # (NUEVO) Actualiza el gráfico de forma automática y silenciosa
            self._generar_grafico(silencioso=True)
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")

    def _atender_paciente(self):
        """Verifica si hay pacientes y abre el diálogo de confirmación para atender."""
        if not self.turno_service.hay_turnos_pendientes():
            messagebox.showinfo("Cola Vacía", MENSAJE_COLA_VACIA)
            return
            
        try:
            siguiente_paciente = self.turno_service.ver_siguiente_paciente()
            
            # Llama al nuevo diálogo personalizado y espera una respuesta (True o False)
            if self._dialogo_confirmacion_atencion(siguiente_paciente):
                # Si la respuesta es True, se procede a atender
                paciente_atendido = self.turno_service.atender_siguiente_paciente()
                tiempo_espera = paciente_atendido.tiempo_espera_actual()
                tiempo_atencion = self.turno_service.obtener_tiempo_atencion(paciente_atendido.especialidad)
                
                if self.graphviz_service.verificar_graphviz_instalado():
                    threading.Thread(
                        target=self._generar_y_mostrar_ficha, 
                        args=(paciente_atendido, tiempo_espera, tiempo_atencion),
                        daemon=True
                    ).start()
                
                self._actualizar_display()
                self._generar_grafico(silencioso=True)
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo atender al paciente: {str(e)}")

    def _generar_grafico(self, silencioso=False):
        """
        (MODIFICADO) Genera el gráfico. Acepta un modo 'silencioso' para evitar pop-ups.
        """
        try:
            if not self.graphviz_service.verificar_graphviz_instalado():
                # Solo muestra error si se presiona el botón manualmente
                if not silencioso:
                    messagebox.showerror("Error", 
                                         "Graphviz no está instalado o no está en el PATH.\n"
                                         "Por favor, instale Graphviz para usar esta función.")
                return
            
            def generar_en_hilo():
                archivo_imagen = self.graphviz_service.generar_grafico_cola(self.turno_service)
                
                if archivo_imagen and os.path.exists(archivo_imagen):
                    # Pasa el modo silencioso a la función que muestra la imagen
                    self.root.after(0, self._mostrar_imagen, archivo_imagen, silencioso)
                elif not silencioso:
                    self.root.after(0, lambda: messagebox.showerror("Error", 
                                      "No se pudo generar el gráfico. Verifique la consola."))
            
            threading.Thread(target=generar_en_hilo, daemon=True).start()
            
            # Muestra este mensaje solo si el usuario hizo clic en el botón
            if not silencioso:
                messagebox.showinfo("Información", "Generando gráfico, por favor espere...")
            
        except Exception as e:
            if not silencioso:
                messagebox.showerror("Error", f"Error al generar gráfico: {str(e)}")

    def _mostrar_imagen(self, archivo_imagen, silencioso=False):
        """
        (MODIFICADO) Muestra la imagen. Evita el pop-up de 'éxito' en modo silencioso.
        """
        try:
            imagen = Image.open(archivo_imagen)
            
            ancho_max, alto_max = self.imagen_label.winfo_width(), self.imagen_label.winfo_height()
            if ancho_max < 50 or alto_max < 50:
                ancho_max, alto_max = 600, 400

            imagen.thumbnail((ancho_max - 20, alto_max - 20), Image.Resampling.LANCZOS)
            
            foto = ImageTk.PhotoImage(imagen)
            
            self.imagen_label.configure(image=foto, text="")
            self.imagen_label.image = foto
            
            # Muestra 'éxito' solo si el usuario hizo clic en el botón
            if not silencioso:
                messagebox.showinfo("Éxito", "Gráfico generado correctamente")
            
        except Exception as e:
            if not silencioso:
                messagebox.showerror("Error", f"Error al mostrar imagen: {str(e)}")

    def _generar_y_mostrar_ficha(self, paciente, tiempo_espera, tiempo_atencion):
        """Función para correr en un hilo que genera la ficha y la muestra."""
        # Esta función será llamada por _atender_paciente
        archivo_ficha = self.graphviz_service.generar_ficha_paciente(
            paciente, tiempo_espera, tiempo_atencion
        )
        if archivo_ficha and os.path.exists(archivo_ficha):
            # Usamos self.root.after para asegurar que la ventana se cree en el hilo principal
            self.root.after(0, self._ventana_paciente_atendido, archivo_ficha)

    def _ventana_paciente_atendido(self, archivo_imagen):
        """(NUEVO) Crea una ventana emergente para mostrar la ficha del paciente."""
        ficha_window = tk.Toplevel(self.root)
        ficha_window.title("Ficha de Paciente Atendido")
        ficha_window.configure(bg=COLOR_FONDO)
        ficha_window.resizable(False, False)

        try:
            imagen = Image.open(archivo_imagen)
            foto = ImageTk.PhotoImage(imagen)
            
            # Ajustar tamaño de ventana a la imagen
            ficha_window.geometry(f"{foto.width()+20}x{foto.height()+20}")

            img_label = ttk.Label(ficha_window, image=foto, style="TLabel")
            img_label.pack(padx=10, pady=10)
            img_label.image = foto  # Mantener referencia
        except Exception as e:
            ficha_window.destroy()
            print(f"Error al mostrar ficha de paciente: {e}")

    def _limpiar_cola(self):
        """Limpia la cola y actualiza el gráfico para mostrar que está vacía."""
        if self.turno_service.hay_turnos_pendientes():
            respuesta = messagebox.askyesno("Confirmar Limpieza", 
                                              "¿Está seguro de que desea limpiar toda la cola?\n"
                                              "Esta acción no se puede deshacer.")
            if respuesta:
                self.turno_service.limpiar_turnos()
                messagebox.showinfo("Información", "La cola ha sido limpiada.")
                self._actualizar_display()
                # (MODIFICADO) Llama a generar gráfico en modo silencioso
                self._generar_grafico(silencioso=True) 
        else:
            messagebox.showinfo("Información", "La cola ya está vacía.")

    def _generar_grafico(self, silencioso=False):
        """
        () Genera el gráfico. Ya no se detiene si la cola está vacía
        y maneja el modo silencioso para evitar pop-ups.
        """
        # () El chequeo de cola vacía se eliminó de aquí
        # para permitir que se genere el gráfico de "Cola Vacía".
        try:
            if not self.graphviz_service.verificar_graphviz_instalado():
                if not silencioso:
                    messagebox.showerror("Error", 
                                         "Graphviz no está instalado o no está en el PATH.\n"
                                         "Por favor, instale Graphviz para usar esta función.")
                return
            
            def generar_en_hilo():
                
                archivo_imagen = self.graphviz_service.generar_grafico_cola(self.turno_service)
                
                if archivo_imagen and os.path.exists(archivo_imagen):
                    self.root.after(0, self._mostrar_imagen, archivo_imagen, silencioso)
                elif not silencioso:
                    self.root.after(0, lambda: messagebox.showerror("Error", 
                                      "No se pudo generar el gráfico. Verifique la consola."))
            
            # Muestra este mensaje solo si el usuario hizo clic en el botón
            if not silencioso:
                messagebox.showinfo("Información", "Generando gráfico, por favor espere...")

            # Ejecuta la generación en un hilo para no congelar la interfaz
            threading.Thread(target=generar_en_hilo, daemon=True).start()
            
        except Exception as e:
            if not silencioso:
                messagebox.showerror("Error", f"Error al generar gráfico: {str(e)}")

    def _mostrar_estadisticas(self):
        """
        Crea una ventana separada para mostrar estadísticas y su gráfico.

        Args:
            estadisticas (ReporteEstadisticas): El objeto con los datos a mostrar.
            archivo_imagen (str, optional): La ruta a la imagen del gráfico. Defaults to None.
        """
        try:
            estadisticas = self.turno_service.obtener_estadisticas()
            
            # Genera el gráfico primero
            archivo_stats = None
            if self.graphviz_service.verificar_graphviz_instalado() and self.turno_service.hay_turnos_pendientes():
                archivo_stats = self.graphviz_service.generar_grafico_estadisticas(estadisticas)

            # Llama a la ventana una sola vez, pasándole los datos y el gráfico (si existe)
            self._ventana_estadisticas(estadisticas, archivo_stats)
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar estadísticas: {str(e)}")


    def _ventana_estadisticas(self, estadisticas, archivo_imagen=None):
        """Crea una ventana separada para mostrar estadísticas y su gráfico."""
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Estadísticas del Sistema")
        stats_window.geometry("500x600")
        stats_window.resizable(True, True)
        stats_window.configure(bg=COLOR_FONDO)
        
        main_frame = ttk.Frame(stats_window, style='TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(main_frame, text="Estadísticas del Sistema", style='Titulo.TLabel').pack(pady=(0, 15))
        
        info_frame = ttk.LabelFrame(main_frame, text="Resumen General", padding=10)
        info_frame.pack(fill=tk.X, pady=(0, 10), anchor='n')
        
        ttk.Label(info_frame, text=f"Total de pacientes en cola: {estadisticas.total_pacientes}").pack(anchor=tk.W)
        ttk.Label(info_frame, text=f"Tiempo total de espera estimado: {estadisticas.tiempo_total_estimado} minutos").pack(anchor=tk.W)
        
        esp_frame = ttk.LabelFrame(main_frame, text="Distribución por Especialidad", padding=10)
        esp_frame.pack(fill=tk.X, pady=(0, 10), anchor='n')
        
        nodo_actual = estadisticas.conteo_especialidades
        if nodo_actual is None:
            ttk.Label(esp_frame, text="No hay pacientes en cola.").pack(anchor=tk.W)
        else:
            while nodo_actual is not None:
                texto = f"{nodo_actual.especialidad}: {nodo_actual.cantidad} paciente(s)"
                ttk.Label(esp_frame, text=texto).pack(anchor=tk.W)
                nodo_actual = nodo_actual.siguiente

        # --- CÓDIGO PARA MOSTRAR LA IMAGEN ---
        if archivo_imagen and os.path.exists(archivo_imagen):
            try:
                img_frame = ttk.LabelFrame(main_frame, text="Gráfico de Distribución", padding=10)
                img_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

                imagen = Image.open(archivo_imagen)
                imagen.thumbnail((450, 400), Image.Resampling.LANCZOS)
                foto = ImageTk.PhotoImage(imagen)
                
                imagen_label = ttk.Label(img_frame, image=foto, style="TLabel")
                imagen_label.pack(pady=5)
                
                imagen_label.image = foto
                
            except Exception as e:
                print(f"Error al cargar imagen de estadísticas: {e}")
                error_label = ttk.Label(main_frame, text="No se pudo cargar el gráfico.", style="TLabel")
                error_label.pack(pady=10)

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
        """Actualiza la visualización de la cola de turnos en el área de texto."""
        self.cola_text.configure(state=tk.NORMAL)
        self.cola_text.delete(1.0, tk.END)
        
        if not self.turno_service.hay_turnos_pendientes():
            self.cola_text.insert(tk.END, MENSAJE_COLA_VACIA)
        else:
            pacientes_en_cola = self.turno_service.obtener_todos_turnos()
            self.cola_text.insert(tk.END, "COLA DE TURNOS ACTUAL\n\n", ('titulo',))
            
            posicion = 0
            for paciente in pacientes_en_cola:
                tiempo_espera = self.turno_service.calcular_tiempo_espera_paciente(posicion)
                tiempo_atencion = self.turno_service.obtener_tiempo_atencion(paciente.especialidad)
                
                # --- CÁLCULO DEL TIEMPO TOTAL ESTIMADO ---
                tiempo_total_estimado = tiempo_espera + tiempo_atencion
                
                posicion_texto = "SIGUIENTE" if posicion == 0 else f"Posición {posicion + 1}"
                tag = 'siguiente' if posicion == 0 else 'normal'

                # --- SE AÑADEN TODOS LOS DATOS REQUERIDOS ---
                # Se muestra el nombre, edad y especialidad
                self.cola_text.insert(tk.END, f"[{posicion_texto}] ", (tag, 'bold'))
                self.cola_text.insert(tk.END, f"{paciente.nombre} ({paciente.edad} años) - {paciente.especialidad}\n", (tag,))
                
                # Se muestra el desglose de tiempos
                self.cola_text.insert(tk.END, f"   ├─ Tiempo en cola: {tiempo_espera} min\n", (tag, 'detalle'))
                self.cola_text.insert(tk.END, f"   ├─ Tiempo de atención: {tiempo_atencion} min\n", (tag, 'detalle'))
                self.cola_text.insert(tk.END, f"   └─ Tiempo Total Estimado: {tiempo_total_estimado} min\n\n", (tag, 'detalle', 'bold'))
                
                posicion += 1
        
        # Configuración de estilos para el texto
        self.cola_text.tag_config('titulo', font=FUENTE_TITULO, foreground=COLOR_PRIMARIO)
        self.cola_text.tag_config('siguiente', font=FUENTE_NORMAL, foreground=COLOR_EXITO)
        self.cola_text.tag_config('bold', font=(FUENTE_NORMAL[0], FUENTE_NORMAL[1], 'bold'))
        self.cola_text.tag_config('normal', font=FUENTE_NORMAL, foreground="#333333")
        self.cola_text.tag_config('detalle', font=FUENTE_NORMAL, foreground="#555555")
        self.cola_text.configure(state=tk.DISABLED)


    def _actualizar_info_display(self):
        """Actualiza la información general del sistema."""
        self.info_text.configure(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        

        # 1. `obtener_estadisticas` ahora devuelve un objeto `ReporteEstadisticas`.
        estadisticas = self.turno_service.obtener_estadisticas()
        
        self.info_text.insert(tk.END, "INFORMACIÓN GENERAL\n", ('titulo',))
        self.info_text.insert(tk.END, "=" * 50 + "\n\n")
        # 2. Se accede a los datos como atributos, no como claves de diccionario.
        self.info_text.insert(tk.END, f"› Total de turnos pendientes: {estadisticas.total_pacientes}\n")
        self.info_text.insert(tk.END, f"› Tiempo total estimado: {estadisticas.tiempo_total_estimado} minutos\n\n")
        
        self.info_text.insert(tk.END, "PACIENTES POR ESPECIALIDAD\n", ('subtitulo',))
        self.info_text.insert(tk.END, "-" * 30 + "\n")
        
        # 3. Se itera sobre la lista enlazada de Nodos de estadística.
        nodo_actual = estadisticas.conteo_especialidades
        while nodo_actual is not None:
            especialidad = nodo_actual.especialidad
            cantidad = nodo_actual.cantidad
            tiempo = self.turno_service.obtener_tiempo_atencion(especialidad)
            self.info_text.insert(tk.END, f"› {especialidad}: {cantidad} paciente(s) ({tiempo} min c/u)\n")
            nodo_actual = nodo_actual.siguiente
        
        self.info_text.insert(tk.END, f"\n{'=' * 50}\n\n")
        siguiente = self.turno_service.ver_siguiente_paciente()
        
        self.info_text.insert(tk.END, "PRÓXIMO PACIENTE A ATENDER\n", ('subtitulo',))
        self.info_text.insert(tk.END, "-" * 30 + "\n")

        if siguiente:
            self.info_text.insert(tk.END, f"› {siguiente}\n", ('siguiente',))
            tiempo_espera_actual = siguiente.tiempo_espera_actual()
            self.info_text.insert(tk.END, f"   Tiempo esperando: {tiempo_espera_actual} minutos\n")
        else:
            self.info_text.insert(tk.END, "› Ninguno. La cola está vacía.\n")
        
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