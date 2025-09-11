# src/services/graphviz_service.py (VERSIÓN CORREGIDA)
"""
Módulo que maneja la visualización gráfica de la cola de turnos usando Graphviz.
"""
import os
import shutil
from typing import TYPE_CHECKING

# --- --- Se importan las clases y constantes necesarias
if TYPE_CHECKING:
    from services.turno_service import TurnoService
from models.reporte import ReporteEstadisticas
from utils.constantes import (
    GRAPHVIZ_ENGINE, GRAPHVIZ_ARCHIVO,
    ESPECIALIDAD_1, ESPECIALIDAD_2, ESPECIALIDAD_3, ESPECIALIDAD_4
)


class GraphvizService:
    """
    Servicio que genera visualizaciones gráficas de la cola de turnos.
    """
    
    def __init__(self):
        """Inicializa el servicio de Graphviz."""
        self.archivo_salida = GRAPHVIZ_ARCHIVO
        self.reportes_dir = "reportes"
        self._preparar_directorio()

    def _preparar_directorio(self):
        """Se asegura de que la carpeta de reportes exista."""
        os.makedirs(self.reportes_dir, exist_ok=True)

    def _renderizar_grafico(self, dot, base_filename):
        """Helper para renderizar un gráfico y guardar el archivo."""
        from graphviz import Digraph # Importación local
        
        filepath = os.path.join(self.reportes_dir, base_filename)
        try:
            dot.render(filepath, format='png', cleanup=True, engine=GRAPHVIZ_ENGINE)
            return f"{filepath}.png"
        except Exception as e:
            print(f"Error al renderizar el gráfico {base_filename}: {e}")
            return None
        
    def generar_grafico_cola(self, turno_service: 'TurnoService'):
        """Genera un gráfico visual MEJORADO de la cola de turnos."""
        from graphviz import Digraph

        dot = Digraph('TURNOS', comment='Cola de Turnos Médicos')
        
        # --- ATRIBUTOS DE ESTILO MEJORADOS ---
        dot.attr('graph', 
                label="Cola de Turnos Médicos", 
                labelloc="t", 
                fontname="Helvetica", 
                fontsize='20',
                rankdir='LR',  # De izquierda a derecha, como una fila
                bgcolor="#f4f4f4",
                splines='ortho') # Líneas de conexión rectas

        dot.attr('node', shape='none', margin='0') # El nodo no tiene forma, la tabla la define
        dot.attr('edge', color="#404040")

        cola_pacientes = turno_service.obtener_todos_turnos()

        if not turno_service.hay_turnos_pendientes():
            dot.node('cola_vacia', 'La cola de turnos está vacía.', shape='box', style='rounded,filled', fillcolor='#e0e0e0')
        else:
            posicion = 0
            nodo_anterior_id = None
            for paciente in cola_pacientes:
                tiempo_espera = turno_service.calcular_tiempo_espera_paciente(posicion)
                tiempo_atencion = turno_service.obtener_tiempo_atencion(paciente.especialidad)
                
                # --- NUEVO LABEL CON TABLA HTML PARA MEJOR ESTILO ---
                label_html = f'''<
    <TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0" CELLPADDING="5" BGCOLOR="white" >
    <TR>
        <TD COLSPAN="2" BGCOLOR="#4e79a7" ALIGN="CENTER"><FONT COLOR="white"><B>Turno #{paciente.numero_turno}</B></FONT></TD>
    </TR>
    <TR>
        <TD ALIGN="LEFT" VALIGN="TOP"><B>Paciente:</B></TD>
        <TD ALIGN="LEFT">{paciente.nombre} ({paciente.edad} años)</TD>
    </TR>
    <TR>
        <TD ALIGN="LEFT"><B>Especialidad:</B></TD>
        <TD ALIGN="LEFT">{paciente.especialidad}</TD>
    </TR>
    <TR>
        <TD ALIGN="LEFT"><B>T. en Cola:</B></TD>
        <TD ALIGN="LEFT">{tiempo_espera} min</TD>
    </TR>
    <TR>
        <TD ALIGN="LEFT"><B>T. Atención:</B></TD>
        <TD ALIGN="LEFT">{tiempo_atencion} min</TD>
    </TR>
    </TABLE>>'''
                
                nodo_actual_id = f'posicion{posicion + 1}'
                dot.node(nodo_actual_id, label_html)
                
                if nodo_anterior_id is not None:
                    dot.edge(nodo_anterior_id, nodo_actual_id)
                
                nodo_anterior_id = nodo_actual_id
                posicion += 1
        
        return self._renderizar_grafico(dot, self.archivo_salida)

    def generar_ficha_paciente(self, paciente, tiempo_espera, tiempo_atencion):
        """Genera una ficha gráfica MEJORADA para un paciente atendido."""
        from graphviz import Digraph

        dot = Digraph('TURNO_ATENDIDO', comment='Ficha de Paciente Atendido')
        dot.attr('graph', bgcolor="#f4f4f4")
        dot.attr('node', shape='none', margin='0')

        # --- NUEVO LABEL CON TABLA HTML PARA MEJOR ESTILO ---
        label_html = f'''<
    <TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0" CELLPADDING="8" BGCOLOR="white">
    <TR>
        <TD COLSPAN="2" BGCOLOR="#59a14f" ALIGN="CENTER"><FONT COLOR="white"><B>Turno #{paciente.numero_turno} - Atendido</B></FONT></TD>
    </TR>
    <TR>
        <TD ALIGN="LEFT"><B>Paciente:</B></TD>
        <TD ALIGN="LEFT">{paciente.nombre}</TD>
    </TR>
    <TR>
        <TD ALIGN="LEFT"><B>Edad:</B></TD>
        <TD ALIGN="LEFT">{paciente.edad} años</TD>
    </TR>
    <TR>
        <TD ALIGN="LEFT"><B>Especialidad:</B></TD>
        <TD ALIGN="LEFT">{paciente.especialidad}</TD>
    </TR>
    <TR>
        <TD ALIGN="LEFT" BGCOLOR="#e9f5e9"><B>Tiempo en cola:</B></TD>
        <TD ALIGN="LEFT" BGCOLOR="#e9f5e9">{tiempo_espera} min</TD>
    </TR>
    <TR>
        <TD ALIGN="LEFT" BGCOLOR="#e9f5e9"><B>Tiempo de atención:</B></TD>
        <TD ALIGN="LEFT" BGCOLOR="#e9f5e9">{tiempo_atencion} min</TD>
    </TR>
    </TABLE>>'''
        
        dot.node('turno_atendido', label_html)

        nombre_limpio = ""
        for char in paciente.nombre:
            if char.isalnum() or char == ' ' or char == '_':
                nombre_limpio += char
        nombre_limpio = nombre_limpio.strip().replace(' ', '_')
        
        base_filename = f"ficha_T{paciente.numero_turno}_{nombre_limpio}"
        return self._renderizar_grafico(dot, base_filename)
        

    def generar_grafico_estadisticas(self, reporte: ReporteEstadisticas):
        """Genera un gráfico de estadísticas usando el objeto ReporteEstadisticas."""
        from graphviz import Digraph # Importación local

        dot = Digraph(comment='Estadísticas de Especialidades')
        dot.attr('node', shape='box', style='rounded,filled')
        dot.attr('graph', bgcolor='white', rankdir='TB')
        
        dot.node('titulo', 'ESTADÍSTICAS POR ESPECIALIDAD', fillcolor='darkblue', fontcolor='white', fontsize='16')
        
        total = reporte.total_pacientes
        tiempo_total = reporte.tiempo_total_estimado
        
        dot.node('total', f'Total Pacientes: {total}\\nTiempo Estimado: {tiempo_total} min', fillcolor='lightgreen', fontcolor='black')
        dot.edge('titulo', 'total')
        
        nodo_actual = reporte.conteo_especialidades
        
        if nodo_actual is None or total == 0:
             dot.node('vacio', 'No hay datos que mostrar', fillcolor='lightgray')
             dot.edge('total', 'vacio')
        else:
            # Itera sobre la lista enlazada
            while nodo_actual is not None:
                especialidad = nodo_actual.especialidad
                cantidad = nodo_actual.cantidad
                if cantidad > 0:
                    node_id = especialidad.replace(" ", "")
                    color = self._obtener_color_especialidad(especialidad)
                    dot.node(node_id, f'{especialidad}\\n{cantidad} paciente(s)', fillcolor=color, fontcolor='black')
                    dot.edge('total', node_id)
                nodo_actual = nodo_actual.siguiente
        
        return self._renderizar_grafico(dot, f"{self.archivo_salida}_stats")
    
    # --- --- Se reemplaza el diccionario por condicionales if/elif
    def _obtener_color_especialidad(self, especialidad):
        """Devuelve una paleta de colores moderna para cada especialidad."""
        if especialidad == ESPECIALIDAD_1:
            return "#4e79a7"  # Azul
        elif especialidad == ESPECIALIDAD_2:
            return "#59a14f"  # Verde
        elif especialidad == ESPECIALIDAD_3:
            return "#edc948"  # Amarillo
        elif especialidad == ESPECIALIDAD_4:
            return "#e15759"  # Rojo
        else:
            return "#bab0ac"  # Gris

    def limpiar_archivos_generados(self):
        """Borra la carpeta de reportes al cerrar la aplicación."""
        if os.path.exists(self.reportes_dir):
            try:
                shutil.rmtree(self.reportes_dir)
                print(f"Carpeta de reportes '{self.reportes_dir}' eliminada.")
            except Exception as e:
                print(f"No se pudo eliminar la carpeta de reportes: {e}")
    
    def verificar_graphviz_instalado(self):
        """Verifica si Graphviz está instalado y disponible."""
        from graphviz import Digraph # Importación local
        try:
            Digraph().pipe(format='png')
            return True
        except Exception:
            return False