import pydot
import os

from PIL import Image
from Nodos import NodoSerpiente, NodoPila, NodoCola, NodoUsuario

class ListaDoble(object):
    def __init__(self):
        self.primero = None # Hasta la izq
        self.ultimo = None # Hasta la der
    
    # Ingresar
    def add(self,x,y):
        nuevo = NodoSerpiente(x=x,y=y)

        if self.primero is None:
            self.primero = nuevo
            self.ultimo = nuevo
        else:
            #insertar al final
            nuevo.ant = self.ultimo
            self.ultimo.sig = nuevo
            self.ultimo = nuevo
            
            #insertar al inicio
            '''
                nuevo.sig = self.primero
                self.primero.ant = nuevo
                self.primero = nuevo
            '''
            
    # Sacar
    def remove(self):
        if self.primero is None:
            print ("Snake Vacio")
        else:
            aux = self.primero
            if self.primero is self.ultimo:
                self.primero = None
                self.ultimo = None
            else:
                #eliminar inicio
                self.primero = self.primero.sig
                # aux.ant.sig = None
                self.primero.ant = None
                
                #eliminar final
                '''
                self.ultimo = self.ultimo.ant
                #self.ultimo.sig.ant = None
                self.ultimo.sig = None
                '''

    def recorrer(self):
        aux = self.primero
        string = "Primero -> "
        if aux is None:
            print('Snake Vacio')
        else:
            while aux is not None:
                if self.primero is self.ultimo:
                    string += str("null <- (" + aux.x + "," + aux.y +") -> null")
                else:
                    string += str("(" + aux.x + "," + aux.y +") -> ")
                aux = aux.sig

        string += str(" <- Ultimo")
        print(string)

    def graficar(self):
        grafo = "digraph Lista_Doble{\n"
        grafo += str("node[shape=record];\n")
        grafo += str("graph[pencolor=transparent];\n")
        grafo += str("rankdir=LR;\n")
        
        aux = self.primero
        if aux is None:
            grafo += str("\"Lista Vacia\"\n")
        else:
            grafo += str("nI[label=\"//\"];\n")
            grafo += str("nF[label=\"//\"];\n")
            while aux is not None:
                grafo += str(hex(id(aux)) + "[label=\"(" + aux.x + "," + aux.y + ")\"];\n")
                aux = aux.sig

            aux = self.primero
            while aux is not None:
                if self.primero is self.ultimo:
                    grafo += str(hex(id(aux)) + "-> nI")
                    grafo += str(hex(id(aux)) + "-> nF")
                elif aux.sig is None:
                    grafo += str(hex(id(aux)) + "-> nF")
                    grafo += str(hex(id(aux)) + "->" + hex(id(aux.ant)))
                else:
                    if aux.ant is None:
                        grafo += str(hex(id(aux)) + "->" + hex(id(aux.sig)))
                        grafo += str(hex(id(aux)) + "-> nI")
                    else:
                        grafo += str(hex(id(aux)) + "->" + hex(id(aux.sig)))
                        grafo += str(hex(id(aux)) + "->" + hex(id(aux.ant)))
                aux = aux.sig
        
        grafo += str("label = \"Snake\"\n")
        grafo += str("}")

        f = open("ListaSnake.dot","w+")
        f.write(grafo)
        f.close()

        os.system("dot -Tjpg ListaSnake.dot -o Lista_Snake.jpg")
        im = Image.open('Lista_Snake.jpg')
        im.show()


class Pila(object):
    def __init__(self):
        self.tope = None # Arriba
        self.fondo = None # Abajo

    # Ingresar
    def push(self, x, y):
        nuevo = NodoPila(x=x,y=y)
        if self.tope is None:
            self.tope = nuevo
            self.fondo = nuevo
        else:
            nuevo.sig = self.tope
            self.tope = nuevo

    # Sacar
    def pop(self):
        if self.tope is None:
             return None
        else:
            aux = self.tope
            self.tope = self.tope.sig
            # return aux
    
    def recorrer(self):
        if self.tope is None:
            print ('Pila Vacia')
        else:
            aux = self.tope
            string = 'Tope -> '
            while aux is not None:
                string += str('(' + aux.x + ',' + aux.y + ') -> ')
                aux = aux.sig
            string += str(' <- Fondo')
            print (string)

    def graficar(self):
        grafo = "digraph Pila{\n"
        grafo += str("node[shape=record];\n")
        grafo += str("graph[pencolor=transparent];\n")
        grafo += str("rankdir=TB;\n")
        
        aux = self.tope
        if aux is None:
            grafo += str("\"Pila Vacia\"\n")
        else:
            grafo += str("n0[label=\" \"];\n")
            while aux is not None:
                grafo += str(hex(id(aux)) + "[label=\"(" + aux.x + "," + aux.y + ")\"];\n")
                aux = aux.sig
            aux = self.tope
            grafo += str("n0->" + hex(id(aux.sig)) + ";\n")
            while aux is not None:
                if aux.sig is not None:
                    grafo += str(hex(id(aux)) + "->" + hex(id(aux.sig)) + ";\n")
                aux = aux.sig
        
        grafo += str("label = \"Puntos\"\n")
        grafo += str("}")

        f = open("PilaPunteo.dot","w+")
        f.write(grafo)
        f.close()

        os.system("dot -Tjpg PilaPunteo.dot -o Pila_Punteo.jpg")
        im = Image.open('Pila_Punteo.jpg')
        im.show()


class Cola(object):
    def __init__(self):
        self.frente = None # Izquierda
        self.cola = None # Derecha

    # Ingresar
    def enqueue(self, n, pt):
        nuevo = NodoCola(n=n, p=pt)
        if self.cola is None:
            self.frente = nuevo
            self.cola = nuevo
        else:
            self.cola.sig = nuevo
            self.cola = nuevo

    # Sacar
    def dequeue(self):
        if self.frente is None:
            return None
        else:
            # temp = self.frente
            if self.frente is self.cola and self.frente is not None:
                self.frente = colaNone
                self.cola = None
                # return temp
            else:
                self.frente = self.frente.sig
                # return temp

    def recorrer(self):
        if self.cola is None:
            print ('Cola Vacia')
        else:
            aux = self.frente
            string = 'Frente-> '
            while aux is not None:
                string += str('(Nombre: ' + aux.name + ' | Pts: ' + aux.pts + ') -> ')
                aux = aux.sig
            print (string + " <- Cola")

    def graficar(self):
        grafo = "digraph Cola{\n"
        grafo += str("node[shape=record];\n")
        grafo += str("graph[pencolor=transparent];\n")
        grafo += str("rankdir=LR;\n")
        
        aux = self.frente
        if aux is None:
            grafo += str("\"Cola Vacia\"\n")
        else:
            while aux is not None:
                grafo += str(hex(id(aux)) + "[label=Usuario:" + aux.name + "\nPts: " + aux.pts + "];\n")
                aux = aux.sig
            aux = self.frente
            while aux is not None:
                if aux.sig is not None:
                    grafo += str(hex(id(aux)) + "->" + hex(id(aux.sig)) + ";\n")
                aux = aux.sig
        
        grafo += str("label = \"Scoreboard\"\n")
        grafo += str("}")

        f = open("ColaScoreboard.dot","w+")
        f.write(grafo)
        f.close()

        os.system("dot -Tjpg ColaScoreboard.dot -o Cola_Scoreboard.jpg")
        im = Image.open('Cola_Scoreboard.jpg')
        im.show()


class ListaCircularDoble(object):
    def __init__(self):
        self.primero = None # Izquierda
        self.ultimo = None # Derecha

    # Ingresar
    def add(self, nam):
        nuevo = NodoUsuario(n=nam)
        
        if self.primero is None:
            self.primero = nuevo
            self.ultimo = nuevo
            nuevo.sig = self.primero
            nuevo.ant = self.ultimo
        else:
            #inserta al final
            nuevo.sig = self.primero
            nuevo.ant = self.ultimo
            self.ultimo.sig = nuevo
            self.primero.ant = nuevo
            self.ultimo = nuevo

    def recorrer(self):
        if self.primero is None:
            print("No hay usuarios")
        else:
            aux = self.primero
            while True:
                print ("|Usuario: " + aux.name + "| ")
                aux = aux.sig
                if aux is self.primero:
                    break

    def graficar(self):
        grafo = "digraph Lista_Circular_Doble{\n"
        grafo += str("node[shape=record];\n")
        grafo += str("graph[pencolor=transparent];\n")
        grafo += str("rankdir=LR;\n")
        
        aux = self.primero

        if aux is None:
            grafo += str("\"No hay Usuarios\"\n")
        else:
            if self.primero is self.ultimo and self.primero is not None:
                grafo += str(hex(id(aux)) + "[label=\"Usuario: " + aux.name + "\"];\n")
                grafo += str(hex(id(aux)) + "->" + hex(id(aux.sig)))
                grafo += str(hex(id(aux)) + "->" + hex(id(aux.ant)))
            else:
                while True:
                    grafo += str(hex(id(aux)) + "[label=\"Usuario: " + aux.name + "\"];\n")
                    
                    aux = aux.sig
                    if aux is self.primero:
                        break
                
                aux = self.primero

                while True:
                    grafo += str(hex(id(aux)) + "->" + hex(id(aux.ant)))
                    grafo += str(hex(id(aux)) + "->" + hex(id(aux.sig)))
                    
                    aux = aux.sig
                    if aux is self.primero:
                        break
        
        grafo += str("label = \"Users\"\n")
        grafo += str("}")

        f = open("ListaUsuarios.dot","w+")
        f.write(grafo)
        f.close()

        os.system("dot -Tjpg ListaUsuarios.dot -o Lista_Usuarios.jpg")
        im = Image.open('Lista_Usuarios.jpg')
        im.show()

lel = ListaCircularDoble().graficar()