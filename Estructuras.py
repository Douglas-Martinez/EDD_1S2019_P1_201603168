import pydot
import os

from PIL import Image
from Nodos import NodoSerpiente, NodoPila, NodoCola, NodoUsuario

class ListaDoble(object):
    def __init__(self):
        self.primero = None # Hasta la izq
        self.ultimo = None # Hasta la der
    
    # Ingresar
    def add(self,x,y,c):
        nuevo = NodoSerpiente(x=x,y=y,c=c)

        if self.primero is None:
            self.primero = nuevo
            self.ultimo = nuevo
        else:
            '''
            #insertar al final
            nuevo.ant = self.ultimo
            self.ultimo.sig = nuevo
            self.ultimo = nuevo
            '''
            
            #insertar al inicio
            nuevo.sig = self.primero
            self.primero.ant = nuevo
            self.primero = nuevo
       
    # Sacar
    def remove(self):
        if self.primero is None:
            #print ("Snake Vacio")
            a = 1
        else:
            aux = self.primero
            if self.primero is self.ultimo:
                self.primero = None
                self.ultimo = None
            else:
                '''
                #eliminar inicio
                self.primero = self.primero.sig
                # aux.ant.sig = None
                self.primero.ant = None
                '''

                #eliminar final
                self.ultimo = self.ultimo.ant
                #self.ultimo.sig.ant = None
                self.ultimo.sig = None

    def clean(self):
        self.primero = None
        self.ultimo = None

    def graficar(self):
        grafo = "digraph Lista_Doble{\n"
        grafo += str("node[shape=record];\n")
        grafo += str("graph[pencolor=transparent];\n")
        grafo += str("rankdir=LR;\n")
        
        aux = self.primero
        if aux is None:
            grafo += str("\"Lista Vacia\"\n")
        else:
            grafo += str("nI[label=\"null\"];\n")
            grafo += str("nF[label=\"null\"];\n")
            while aux is not None:
                if aux is self.primero:
                    #grafo += str(str(id(aux)) + "[label=\"(" + str(aux.x) + "," + str(aux.y) '''+ "," + str(aux.ch)''' + ")\",style=\"filled\",color=\"green\"];\n")
                    grafo += str(str(id(aux)) + "[label=\"(" + str(aux.x) + "," + str(aux.y) + ")\",style=\"filled\",color=\"green\"];\n")
                else:
                    #grafo += str(str(id(aux)) + "[label=\"(" + str(aux.x) + "," + str(aux.y) + ''' "," + str(aux.ch) +''' ")\"];\n")
                    grafo += str(str(id(aux)) + "[label=\"(" + str(aux.x) + "," + str(aux.y) + ")\"];\n")
                aux = aux.sig

            aux = self.primero
            while aux is not None:
                if self.primero is self.ultimo:
                    grafo += str(str(id(aux)) + "-> nI\n")
                    grafo += str(str(id(aux)) + "-> nF\n")
                elif aux.sig is None:
                    grafo += str(str(id(aux)) + "-> nF\n")
                    grafo += str(str(id(aux)) + "->" + str(id(aux.ant)) + "\n")
                else:
                    if aux.ant is None:
                        grafo += str(str(id(aux)) + "->" + str(id(aux.sig)) + "\n")
                        grafo += str(str(id(aux)) + "-> nI\n")
                    else:
                        grafo += str(str(id(aux)) + "->" + str(id(aux.sig)) + "\n")
                        grafo += str(str(id(aux)) + "->" + str(id(aux.ant)) + "\n")
                aux = aux.sig
        
        grafo += str("label = \"Snake\"\n")
        grafo += str("}")

        f = open("Graficas/ListaSnake.dot","w+")
        f.write(grafo)
        f.close()

        os.system("dot -Tjpg Graficas/ListaSnake.dot -o Graficas/Lista_Snake.jpg")
        im = Image.open('Graficas/Lista_Snake.jpg')
        im.show()

class Pila(object):
    def __init__(self):
        self.tope = None # Arriba

    # Ingresar
    def push(self, x, y):
        nuevo = NodoPila(x=x,y=y)
        if self.tope is None:
            self.tope = nuevo
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
    
    def vaciar(self):
        self.tope = None

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
                grafo += str(str(id(aux)) + "[label=\"(" + str(aux.x) + "," + str(aux.y) + ")\"];\n")
                aux = aux.sig
            aux = self.tope
            grafo += str("n0->" + str(id(aux)) + ";\n")
            while aux is not None:
                if aux.sig is not None:
                    grafo += str(str(id(aux)) + "->" + str(id(aux.sig)) + ";\n")
                aux = aux.sig
        
        grafo += str("label = \"Puntos\"\n")
        grafo += str("}")

        f = open("Graficas/PilaPunteo.dot","w+")
        f.write(grafo)
        f.close()

        os.system("dot -Tjpg Graficas/PilaPunteo.dot -o Graficas/Pila_Punteo.jpg")
        im = Image.open('Graficas/Pila_Punteo.jpg')
        im.show()

class Cola(object):
    def __init__(self):
        self.frente = None # Izquierda
        self.cola = None # Derecha
        self.tam = 0

    # Sacar
    def dequeue(self):
        if self.frente is None:
            return None
        else:
            # temp = self.frente
            if self.frente is self.cola and self.frente is not None:
                self.frente = None
                self.cola = None
                # return temp
            else:
                self.frente = self.frente.sig
                # return temp

    # Ingresar
    def enqueue(self, n, pt):
        nuevo = NodoCola(n=n, p=pt)
        if self.tam is 10:
            self.dequeue()
            self.tam -= 1

        if self.cola is None:
            self.frente = nuevo
            self.cola = nuevo
        else:
            self.cola.sig = nuevo
            self.cola = nuevo
        self.tam += 1

    def graficar(self):
        grafo = "digraph Cola{\n"
        grafo += str("node[shape=record];\n")
        grafo += str("graph[pencolor=transparent];\n")
        grafo += str("rankdir=LR;\n")
        
        aux = self.frente
        if aux is None:
            grafo += str("\"Cola Vacia\"\n")
        else:
            grafo += str("n[label=\"null\"];\n")
            while aux is not None:
                grafo += str(str(id(aux)) + "[label=\"Usuario: " + aux.name + "|Pts: " + str(aux.pts) + "\"];\n")
                aux = aux.sig
            aux = self.frente
            while aux.sig is not None:
                grafo += str(str(id(aux)) + "->" + str(id(aux.sig)) + ";\n")
                aux = aux.sig
            grafo += str(str(id(aux)) + "->n;\n")
        
        grafo += str("label = \"Scoreboard\"\n")
        grafo += str("}")

        f = open("Graficas/ColaScoreboard.dot","w+")
        f.write(grafo)
        f.close()
        
        os.system("dot -Tjpg Graficas/ColaScoreboard.dot -o Graficas/Cola_Scoreboard.jpg")
        im = Image.open('Graficas/Cola_Scoreboard.jpg')
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
                grafo += str(str(id(aux)) + "[label=\"Usuario: " + str(aux.name) + "\"];\n")
                grafo += str(str(id(aux)) + "->" + str(id(aux.sig)) + "\n")
                grafo += str(str(id(aux)) + "->" + str(id(aux.ant)) + "\n")
            else:
                while True:
                    grafo += str(str(id(aux)) + "[label=\"Usuario: " + str(aux.name) + "\"];\n")
                    aux = aux.sig

                    if aux is self.primero:
                        break
                
                aux = self.primero
                while True:
                    grafo += str(str(id(aux)) + "->" + str(id(aux.ant)) + "\n")
                    grafo += str(str(id(aux)) + "->" + str(id(aux.sig)) + "\n")
                    aux = aux.sig

                    if aux is self.primero:
                        break
        
        grafo += str("label = \"Users\"\n")
        grafo += str("}")

        f = open("Graficas/ListaUsuarios.dot","w+")
        f.write(grafo)
        f.close()

        os.system("dot -Tjpg Graficas/ListaUsuarios.dot -o Graficas/Lista_Usuarios.jpg")
        im = Image.open('Graficas/Lista_Usuarios.jpg')
        im.show()