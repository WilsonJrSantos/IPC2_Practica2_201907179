"""
Módulo que implementa la estructura de datos Cola de forma dinámica.
No utiliza estructuras nativas de Python como list, deque, etc.
"""

from models.nodo import Nodo


class Cola:
    """
    Implementación de una cola dinámica usando nodos enlazados.
    Sigue el principio FIFO (First In, First Out).
    
    Attributes:
        frente: Referencia al primer nodo de la cola
        final: Referencia al último nodo de la cola
        tamaño: Cantidad de elementos en la cola
    """
    
    def __init__(self):
        """Inicializa una cola vacía."""
        self.frente = None
        self.final = None
        self.tamaño = 0
    
    def esta_vacia(self):
        """
        Verifica si la cola está vacía.
        
        Returns:
            bool: True si la cola está vacía, False en caso contrario
        """
        return self.frente is None
    
    def encolar(self, dato):
        """
        Agrega un elemento al final de la cola.
        
        Args:
            dato: Elemento a agregar a la cola
        """
        nuevo_nodo = Nodo(dato)
        
        if self.esta_vacia():
            # Si la cola está vacía, el nuevo nodo es tanto frente como final
            self.frente = nuevo_nodo
            self.final = nuevo_nodo
        else:
            # Agregar el nuevo nodo al final y actualizar la referencia
            self.final.siguiente = nuevo_nodo
            self.final = nuevo_nodo
        
        self.tamaño += 1
    
    def desencolar(self):
        """
        Remueve y retorna el elemento del frente de la cola.
        
        Returns:
            object: El elemento removido del frente de la cola
            
        Raises:
            IndexError: Si la cola está vacía
        """
        if self.esta_vacia():
            raise IndexError("No se puede desencolar de una cola vacía")
        
        dato = self.frente.dato
        self.frente = self.frente.siguiente
        
        # Si la cola queda vacía, actualizar también final
        if self.frente is None:
            self.final = None
        
        self.tamaño -= 1
        return dato
    
    def ver_frente(self):
        """
        Retorna el elemento del frente sin removerlo.
        
        Returns:
            object: El elemento del frente de la cola
            
        Raises:
            IndexError: Si la cola está vacía
        """
        if self.esta_vacia():
            raise IndexError("La cola está vacía")
        
        return self.frente.dato
    
    def obtener_tamaño(self):
        """
        Retorna el número de elementos en la cola.
        
        Returns:
            int: Cantidad de elementos en la cola
        """
        return self.tamaño
    
    def obtener_todos_elementos(self):
        """
        Retorna todos los elementos de la cola sin modificarla.
        
        Returns:
            list: Lista con todos los elementos de la cola en orden FIFO
        """
        elementos = []
        nodo_actual = self.frente
        
        while nodo_actual is not None:
            elementos.append(nodo_actual.dato)
            nodo_actual = nodo_actual.siguiente
        
        return elementos
    
    def limpiar(self):
        """Vacía completamente la cola."""
        self.frente = None
        self.final = None
        self.tamaño = 0
    
    def __str__(self):
        """
        Representación en cadena de la cola.
        
        Returns:
            str: Representación de todos los elementos de la cola
        """
        if self.esta_vacia():
            return "Cola vacía"
        
        elementos = []
        nodo_actual = self.frente
        
        while nodo_actual is not None:
            elementos.append(str(nodo_actual.dato))
            nodo_actual = nodo_actual.siguiente
        
        return " <- ".join(elementos)
    
    def __len__(self):
        """
        Retorna la longitud de la cola.
        
        Returns:
            int: Número de elementos en la cola
        """
        return self.tamaño