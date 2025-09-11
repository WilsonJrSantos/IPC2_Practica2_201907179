# src/models/cola.py
"""
Módulo que implementa la estructura de datos Cola de forma dinámica.
No utiliza estructuras nativas de Python como list, deque, etc.
"""

from models.nodo import Nodo

class Cola:
    """
    Implementación de una cola dinámica usando nodos enlazados.
    Sigue el principio FIFO (First In, First Out).
    """
    
    def __init__(self):
        """Inicializa una cola vacía."""
        self.frente = None
        self.final = None
        self.tamaño = 0
    
    def esta_vacia(self):
        """Verifica si la cola está vacía."""
        return self.frente is None
    
    def encolar(self, dato):
        """Agrega un elemento al final de la cola."""
        nuevo_nodo = Nodo(dato)
        
        if self.esta_vacia():
            self.frente = nuevo_nodo
            self.final = nuevo_nodo
        else:
            self.final.siguiente = nuevo_nodo
            self.final = nuevo_nodo
        
        self.tamaño += 1
    
    def desencolar(self):
        """Remueve y retorna el elemento del frente de la cola."""
        if self.esta_vacia():
            raise IndexError("No se puede desencolar de una cola vacía")
        
        dato = self.frente.dato
        self.frente = self.frente.siguiente
        
        if self.frente is None:
            self.final = None
        
        self.tamaño -= 1
        return dato
    
    def ver_frente(self):
        """Retorna el elemento del frente sin removerlo."""
        if self.esta_vacia():
            raise IndexError("La cola está vacía")
        
        return self.frente.dato
    
    def obtener_tamaño(self):
        """Retorna el número de elementos en la cola."""
        return self.tamaño
    
    def limpiar(self):
        """Vacía completamente la cola."""
        self.frente = None
        self.final = None
        self.tamaño = 0
    
    def __str__(self):
        """
        Representación en cadena de la cola, CONSTRUIDA SIN USAR LISTAS.
        """
        if self.esta_vacia():
            return "Cola vacía"
        
        cadena_resultado = ""
        nodo_actual = self.frente
        
        while nodo_actual is not None:
            cadena_resultado += str(nodo_actual.dato)
            if nodo_actual.siguiente is not None:
                cadena_resultado += " <- "
            nodo_actual = nodo_actual.siguiente
            
        return cadena_resultado
    
    def __len__(self):
        """Retorna la longitud de la cola."""
        return self.tamaño

    #Esto es lo que nos permite recorrer la cola sin usar listas!
    def __iter__(self):
        """Prepara la cola para ser iterada."""
        self.nodo_iterador = self.frente
        return self

    def __next__(self):
        """Retorna el siguiente elemento en la iteración."""
        if self.nodo_iterador is not None:
            dato = self.nodo_iterador.dato
            self.nodo_iterador = self.nodo_iterador.siguiente
            return dato
        else:
            raise StopIteration