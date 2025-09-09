"""
Módulo que define la clase Nodo para la implementación de la cola dinámica.
"""

class Nodo:
    """
    Clase que representa un nodo en la estructura de cola dinámica.
    
    Attributes:
        dato: Información almacenada en el nodo
        siguiente: Referencia al siguiente nodo en la cola
    """
    
    def __init__(self, dato):
        """
        Inicializa un nuevo nodo.
        
        Args:
            dato: Información a almacenar en el nodo
        """
        self.dato = dato
        self.siguiente = None
    
    def __str__(self):
        """
        Representación en cadena del nodo.
        
        Returns:
            str: Representación del dato contenido
        """
        return str(self.dato)