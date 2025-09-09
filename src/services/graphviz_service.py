"""
Módulo que maneja la visualización gráfica de la cola de turnos usando Graphviz.
"""

import os
import shutil  # <-- Importado para borrar la carpeta de reportes
from graphviz import Digraph
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from services.turno_service import TurnoService

from utils.constantes import GRAPHVIZ_FORMATO, GRAPHVIZ_ENGINE, GRAPHVIZ_ARCHIVO


class GraphvizService:
    """
    Servicio que genera visualizaciones gráficas de la cola de turnos.
    """
    
    def __init__(self):
        """Inicializa el servicio de Graphviz."""
        self.archivo_salida = GRAPHVIZ_ARCHIVO
        self.reportes_dir = "reportes"
        # (NUEVO) Se asegura de que la carpeta exista desde el inicio.
        self._preparar_directorio()

    def _preparar_directorio(self):
        """Se asegura de que la carpeta de reportes exista."""
        os.makedirs(self.reportes_dir, exist_ok=True)

    def _renderizar_grafico(self, dot, base_filename):
        """
        Helper para renderizar un gráfico en PNG y PDF y guardar los archivos.
        """
        filepath = os.path.join(self.reportes_dir, base_filename)
        
        try:
            dot.render(filepath, format='png', cleanup=False, engine=GRAPHVIZ_ENGINE)
            dot.render(filepath, format='pdf', cleanup=False, engine=GRAPHVIZ_ENGINE)
            return f"{filepath}.png"
        except Exception as e:
            print(f"Error al renderizar el gráfico {base_filename}: {e}")
            return None

    def generar_grafico_cola(self, turno_service: 'TurnoService'):
        """
        Genera un gráfico visual de la cola de turnos.
        """
        dot = Digraph('TURNOS', comment='Cola de Turnos Médicos')
        dot.attr('graph', 
                 label="COLA DE TURNOS MÉDICOS", 
                 labelloc="t",
                 fontname="Helvetica,Arial,sans-serif",
                 fontsize='16')
        dot.attr('node', 
                 fontname="Helvetica,Arial,sans-serif",
                 shape='record',
                 style='filled',
                 fillcolor='lightblue')
        dot.attr('edge', dir='none')

        pacientes = turno_service.obtener_todos_turnos()

        if not pacientes:
            dot.attr('node', fillcolor='lightgray')
            dot.node('cola_vacia', 
                     label='{<b>COLA VACÍA</b> | No hay pacientes en espera.}')
        else:
            for i, paciente in enumerate(pacientes):
                tiempo_espera = turno_service.calcular_tiempo_espera_paciente(i)
                tiempo_atencion = turno_service.obtener_tiempo_atencion(paciente.especialidad)
                tiempo_total = tiempo_espera + tiempo_atencion
                
                label = (
                    f'<{{<b>Turno #{paciente.numero_turno}</b> |'
                    f'Paciente: {paciente.nombre}<br align="center"/>'
                    f'Edad: {paciente.edad} años<br align="center"/>|'
                    f'Especialidad: {paciente.especialidad}<br align="center"/>'
                    f'Tiempo de atención: {tiempo_atencion} min<br align="center"/>|'
                    f'Tiempo total estimado: {tiempo_total} min<br align="center"/>'
                    f'Tiempo en cola: {tiempo_espera} min<br align="center"/>}}>'
                )
                
                node_id = f'posicion{i+1}'
                dot.node(node_id, label=label)
                
                if i > 0:
                    prev_node_id = f'posicion{i}'
                    dot.edge(prev_node_id, node_id)
        
        return self._renderizar_grafico(dot, self.archivo_salida)

    def generar_ficha_paciente(self, paciente, tiempo_espera, tiempo_atencion):
        """
        Genera una ficha gráfica para un paciente atendido con un nombre de archivo único.
        """
        dot = Digraph('TURNO_ATENDIDO', comment='Ficha de Paciente Atendido')
        dot.attr('graph', 
                 label="TURNO ATENDIDO", 
                 labelloc="t",
                 fontname="Helvetica,Arial,sans-serif",
                 fontsize='16')
        dot.attr('node', 
                 fontname="Helvetica,Arial,sans-serif",
                 shape='record',
                 style='filled',
                 fillcolor='lightgreen')

        tiempo_total = tiempo_espera + tiempo_atencion

        label = (
            f'<{{<b>Turno #{paciente.numero_turno}</b> |'
            f'Paciente: {paciente.nombre}<br align="center"/>'
            f'Edad: {paciente.edad} años<br align="center"/>|'
            f'Especialidad: {paciente.especialidad}<br align="center"/>'
            f'Tiempo de atención: {tiempo_atencion} min<br align="center"/>|'
            f'Tiempo total: {tiempo_total} min<br align="center"/>'
            f'Tiempo en cola: {tiempo_espera} min<br align="center"/>}}>'
        )
        
        dot.node('turno_atendido', label=label)

        # (MODIFICADO) Crear un nombre de archivo único para la ficha
        # Ejemplo: "ficha_T3_Maria_Lopez.png"
        nombre_paciente_limpio = "".join(c for c in paciente.nombre if c.isalnum() or c in (' ', '_')).rstrip()
        base_filename = f"ficha_T{paciente.numero_turno}_{nombre_paciente_limpio.replace(' ', '_')}"

        return self._renderizar_grafico(dot, base_filename)
    
    def generar_grafico_estadisticas(self, estadisticas):
        """
        Genera un gráfico de estadísticas.
        """
        dot = Digraph(comment='Estadísticas de Especialidades')
        dot.attr(rankdir='TB')
        dot.attr('node', shape='box', style='rounded,filled')
        dot.attr('graph', bgcolor='white')
        
        dot.node('titulo', 'ESTADÍSTICAS POR ESPECIALIDAD', 
                 fillcolor='darkblue', fontcolor='white', fontsize='16')
        
        total = estadisticas.get('total_pacientes', 0)
        tiempo_total = estadisticas.get('tiempo_total_estimado', 0)
        
        dot.node('total', f'Total Pacientes: {total}\\nTiempo Estimado: {tiempo_total} min',
                 fillcolor='lightgreen', fontcolor='black')
        
        dot.edge('titulo', 'total')
        
        especialidades = estadisticas.get('especialidades', {})
        
        for i, (especialidad, cantidad) in enumerate(especialidades.items()):
            node_id = f'esp_{i}'
            color = self._obtener_color_especialidad(especialidad)
            
            dot.node(node_id, f'{especialidad}\\n{cantidad} paciente(s)', 
                     fillcolor=color, fontcolor='black')
            
            dot.edge('total', node_id)
        
        return self._renderizar_grafico(dot, f"{self.archivo_salida}_stats")
    
    def _obtener_color_especialidad(self, especialidad):
        colores = {
            "Medicina General": "#a8e6cf",
            "Pediatría": "#dcedc1", 
            "Ginecología": "#ffd3b6",
            "Dermatología": "#ffaaa5"
        }
        return colores.get(especialidad, "#e0e0e0")
    
    def limpiar_archivos_generados(self):
        """
        Borra toda la carpeta de reportes y su contenido.
        Esta función solo se llama cuando se cierra la aplicación.
        """
        if os.path.exists(self.reportes_dir):
            try:
                # shutil.rmtree borra una carpeta y todo lo que contiene
                shutil.rmtree(self.reportes_dir)
                print(f"Carpeta de reportes '{self.reportes_dir}' eliminada.")
            except Exception as e:
                print(f"No se pudo eliminar la carpeta de reportes: {e}")
    
    def verificar_graphviz_instalado(self):
        """Verifica si Graphviz está instalado y disponible."""
        try:
            dot = Digraph()
            dot.pipe(format='png')
            return True
        except Exception:
            return False