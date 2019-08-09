# Lista Doblemente Enlazada (SNAKE)
class NodoSerpiente(object):
    def __init__(self, x=None, y=None, next=None, prev=None):
        self.x = x
        self.y = y
        self.sig = next # Siguiente es Derecha
        self.ant = prev # Anterior es Izquierda
    '''
    PRIMERO ->  null (ant)<- NodoS ->(sig) null <- ULTIMO
    '''

# Pila (PUNTOS)
class NodoPila(object):
    def __init__(self, x=None, y=None, next=None):
        self.x = x
        self.y = y
        self.sig = next # Siguiente es abajo
    '''
    TOPE
      |
      v
    nodoP
      |
      v(sig)
    nodoP
      |
      v(sig)
    FONDO
      |
      v
    null
    '''

# Cola o Fila (PUNTAJES)
class NodoCola(object):
    def __init__(self, n=None, p=None, next=None):
        self.name = n
        self.pts = p
        self.sig = next # Siguiente es el que va atras
        # self.ant = bef # Anterior es el que va adelante
    '''
    FRENTE -> nodoC ->(sig) nodoC ->(sig) null <- COLA
    '''


# Lista Circular Doblemente Enlazada (USUARIOS)
class NodoUsuario(object):
    def __init__(self, n=None, next=None, bef=None):
        self.name = n
        self.sig = next # Siguiente es Derecha
        self.ant = bef # Anterior es Izquierda
    '''
        |-----------------------------------------------
        v                                              |
    PRIMERO -> (ant)<- nodoU ->(sig) (ant)<- nodoU ->(sig) <- ULTIMO
                 |                                             ^
                 |_____________________________________________|
    '''