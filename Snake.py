import curses
import csv

from Estructuras import ListaDoble, ListaCircularDoble, Pila, Cola
from Nodos import NodoSerpiente, NodoPila, NodoCola, NodoUsuario
from curses import KEY_RIGHT, KEY_LEFT, KEY_DOWN, KEY_UP, KEY_ENTER
from random import randint

ALTO = 20
ANCHO = 45
MAX_X = ANCHO - 2
MAX_Y = ALTO - 2
SNAKE_TAM = 2
SNAKE_X = SNAKE_TAM + 1
SNAKE_Y = 3
TIMEOUT = 200

class Snake(object):
    REV_DIR_MAP = {
        KEY_UP: KEY_DOWN, KEY_DOWN: KEY_UP,
        KEY_LEFT: KEY_RIGHT, KEY_RIGHT: KEY_LEFT,
    }

    def __init__(self, x, y, window, lc, us):
        self.body_list = []
        self.hit_score = 0
        self.timeout = TIMEOUT
        self.nivel = 1
        self.win = False
        self.lose = False
        self.usuarioactual = us
        self.listacuerpo = lc
        self.tam = 3

        for i in range(SNAKE_TAM, 0, -1):
            self.body_list.append(Body(x - i, y))

        self.body_list.append(Body(x, y, '#'))
        self.window = window
        self.direction = KEY_RIGHT
        self.last_head_coor = (x, y)
        self.direction_map = {
            KEY_UP: self.move_up,
            KEY_DOWN: self.move_down,
            KEY_LEFT: self.move_left,
            KEY_RIGHT: self.move_right
        }

    def add_body(self, body_list):
        self.body_list.extend(body_list)

    def eat_food(self, food):
        if food.tipo is 1:
            body = Body(self.last_head_coor[0], self.last_head_coor[1])
            self.body_list.insert(-1, body)
            self.tam += 1
            self.hit_score += 1
        elif food.tipo is 2:
            self.body_list.pop(0)
            self.tam -= 1
            self.hit_score -= 1

        if self.hit_score is 15:
            if self.nivel is 3:
                #self.estado = "Puntos iguales a 5, Nivel es 3 y Win"
                self.win = True
            else:
                #self.estado = "Puntos iguales a 5 y Nivel no es 3"
                self.nivel += 1
                self.hit_score = 0
                if self.nivel is 2:
                    self.timeout = 170

                    self.body_list = []
                    self.tam = 3
                    for i in range(SNAKE_TAM, 0, -1):
                        self.body_list.append(Body(20 - i, 10))
                    self.body_list.append(Body(20, 10, '#'))
                    self.direction = KEY_RIGHT

                elif self.nivel is 3:
                    self.timeout = 125 

                    self.body_list = []
                    self.tam = 3
                    for i in range(SNAKE_TAM, 0, -1):
                        self.body_list.append(Body(20 - i, 10))
                    self.body_list.append(Body(20, 10, '#'))
                    self.direction = KEY_RIGHT
        else:
            #self.estado = "Puntos menores a 5 => Actual: " + str(self.hit_score)
            if self.nivel is 1:
                if food.tipo is 1:
                    self.timeout -= 2
                elif food.tipo is 2:
                    self.timeout += 2
                self.window.timeout(self.timeout)
            elif self.nivel is 2:
                if food.tipo is 1:
                    self.timeout -= 3
                elif food.tipo is 2:
                    self.timeout += 3
                self.window.timeout(self.timeout)
            elif self.nivel is 3:
                if food.tipo is 1:
                    self.timeout -= 4
                elif food.tipo is 2:
                    self.timeout += 4
                self.window.timeout(self.timeout)
        food.reset(self.tam)

    def update(self):
        last_body = self.body_list.pop(0)
        last_body.x = self.body_list[-1].x
        last_body.y = self.body_list[-1].y
        self.body_list.insert(-1, last_body)
        self.last_head_coor = (self.head.x, self.head.y)
        self.direction_map[self.direction]()

    def change_direction(self, direction):
        if direction != Snake.REV_DIR_MAP[self.direction]:
            self.direction = direction

    def render(self):
        self.listacuerpo.clean()
        for body in self.body_list:
            self.listacuerpo.add(body.y,body.x,str(body.char))
            self.window.addstr(body.y, body.x, body.char)

    def move_up(self):
        self.head.y -= 1
        if self.nivel is not 3:
            if self.head.y < 1:
                self.head.y = MAX_Y
        else:
            if self.head.y < 1:
                self.lose = True

    def move_down(self):
        self.head.y += 1
        if self.nivel is not 3:
            if self.head.y > MAX_Y:
                self.head.y = 1
        else:
            if self.head.y > MAX_Y:
                self.lose = True

    def move_left(self):
        self.head.x -= 1
        if self.nivel is not 3:
            if self.head.x < 1:
                self.head.x = MAX_X
        else:
            if self.head.x < 1:
                self.lose = True

    def move_right(self):
        self.head.x += 1
        if self.nivel is not 3:
            if self.head.x > MAX_X:
                self.head.x = 1
        else:
            if self.head.x > MAX_X:
                self.lose = True

        
    @property
    def score(self):
        return 'Pts: {} Level: {} ----- User: {}'.format(self.hit_score,self.nivel,self.usuarioactual)

    @property
    def collided(self):
        return any([body.coor == self.head.coor
            for body in self.body_list[:-1]])

    @property
    def head(self):
        return self.body_list[-1]

    @property
    def coor(self):
        return self.head.x, self.head.y
    
class Body(object):
    def __init__(self, x, y, char='#'):
        self.x = x
        self.y = y
        self.char = char

    @property
    def coor(self):
        return self.x, self.y

class Food(object):
    def __init__(self, window):
        self.x = randint(1, MAX_X)
        self.y = randint(1, MAX_Y)
        self.tipo = 1
        self.window = window
        self.char = '+'

    def render(self):
        self.window.addstr(self.y, self.x, self.char)

    def reset(self,t):
        tam = t
        opcion = 0
        if tam > 3:
            opcion = randint(0,10)

        #malos 1, 4, 7
        if opcion is 1 or opcion is 4 or opcion is 7:
            self.tipo = 2
            self.char = '*'
        #buenos 0, 2, 3, 5, 6, 8, 9
        else:
            self.tipo = 1
            self.char = '+'
        self.x = randint(1, MAX_X)
        self.y = randint(1, MAX_Y)


def menu(window,usua):
    window.clear()
    window.border(0)
    window.addstr(1,ANCHO//2-len("MENU"),"MENU")
    if usua is "":
        window.addstr(2,1,"Usuario: Niguno")
    else:
        window.addstr(2,1,"Usuario: " + str(usua))
    window.addstr(7,10,"1. Jugar")
    window.addstr(8,10,"2. Puntuaciones")
    window.addstr(9,10,"3. Seleccion de Usuario")
    window.addstr(10,10,"4. Reportes")
    window.addstr(11,10,"5. Carga Masiva")
    window.addstr(12,10,"6. Limpiar Usuario")
    window.addstr(13,10,"7. Salir")

def play(window,us,lista):
    window.clear()
    window.border(0)
    snake = Snake(SNAKE_X,SNAKE_Y, window, lista, us)
    food = Food(window)
    
    while True:
        window.clear()
        window.border(0)
        
        snake.render()
        food.render()
        window.addstr(0,(MAX_X//2-len(snake.score)//2),snake.score)
        event = window.getch()

        if event == 27:
            break
        elif event == 32:
            snake.listacuerpo.graficar()
            #pila.graficar()
            key = -1
            while key != 32:
                key = window.getch()
        elif event in [KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT]:
            snake.change_direction(event)
        
        if snake.head.x == food.x and snake.head.y == food.y:
            curses.beep()
            if (snake.hit_score + 1) is 15:
                pila.vaciar()
            else:
                if food.tipo is 1:
                    pila.push(food.y,food.x)
                elif food.tipo is 2:
                    pila.pop()
            snake.eat_food(food) 

        snake.update()

        if snake.collided:
            snake.lose = True

        if snake.win is True or snake.lose is True:
            break
    
    if snake.win is True:
        m = "Game Over!"
        m2 = "Ganaste!"
        window.addstr(MAX_Y//2,(MAX_X//2-len(m)//2) + 1, m)
        window.addstr(MAX_Y//2 + 1,(MAX_X//2-len(m2)//2) + 1, m2)
        window.nodelay(0)
        l =-1
        lista.graficar()
        while True:
            l = window.getch()
            if l is 10:
                break
    elif snake.lose is True:
        m = "Game Over!"
        window.addstr(MAX_Y//2,(MAX_X//2-len(m)//2) + 1, m)
        window.nodelay(0)
        ll =-1
        lista.graficar()
        while True:
            ll = window.getch()
            if ll is 10:
                break
    else:
        m = "Saliste!"
        window.addstr(MAX_Y//2,(MAX_X//2-len(m)//2) + 1, m)
        window.nodelay(0)
        lll =-1
        lista.graficar()
        while True:
            lll = window.getch()
            if lll is 10:
                break

    cola.enqueue(us,str(snake.nivel)+"-"+str(snake.hit_score))
    #pila.graficar()

def scoreboard(window,cola):
    window.clear()
    window.border(0)
    window.addstr(1,ANCHO//2-len("PUNTUACIONES")//2,"PUNTUACIONES")
    window.addstr(3,10,"Nombre")
    window.addstr(3,23,"Puntaje")
    window.addstr(4,21,"(Nivel-Pts)")
    lin = 6
    aux = cola.frente
    while aux is not None:
        window.addstr(lin,10,str(aux.name))
        window.addstr(lin,23,str(aux.pts))
        lin += 1
        aux = aux.sig
    while True:
        op = window.getch()

        if op is 10:
            break
        
def userselect(window,lcd):
    window.clear()
    window.border(0)
    nombre = ""
    aux = lcd.primero
    op = -1
    while True:
        window.clear()
        window.border(0)
        window.addstr(1,ANCHO//2-len("USUARIOS")//2,"USUARIOS")
        window.addstr(3,1,"Enter: Aceptar")
        window.addstr(4,1,"Esc: Regresar")
        n = aux.name
        us = "<--   " + str(n) + "   -->"
        window.addstr(ALTO//2,ANCHO//2-len(str(us))//2,us)
        op = window.getch()
        if op == 261:
            aux = aux.sig
        elif op == 260:
            aux = aux.ant
        elif op is 10:
            nombre = aux.name
            break
        elif op is 27:
            break
    return nombre
    
def reports(window,ld,c,p,lc):
    while True:
        window.clear()
        window.border(0)
        window.addstr(1,ANCHO//2-len("REPORTES")//2,"REPORTES")
        window.addstr(7,10,"1. Snake Report")
        window.addstr(8,10,"2. Score Report")
        window.addstr(9,10,"3. Scoreboard Report")
        window.addstr(10,10,"4. Users Report")
        window.addstr(11,10,"5. Salir")
        op = -1
        op = window.getch()
        if op is 49:
            ld.graficar()
        elif op is 50:
            p.graficar()
        elif op is 51:
            c.graficar()
        elif op is 52:
            lc.graficar()
        elif op is 53:
            break

def bulk(window):
    window.clear()
    window.border(0)
    window.addstr(1,ANCHO//2-len("CARGA MASIVA")//2,"CARGA MASIVA")
    window.addstr(3,ANCHO//2-len("Ingresa el archivo .csv")//2,"Ingresa el archivo .csv")
    window.addstr(4,ANCHO//2-len(str("Al terminar presiona ENTER"))//2,"Al terminar presiona ENTER")
    string = ""
    op = -1
    while True:
        window.addstr(ALTO//2+1,ANCHO//2-len(string)//2,string)
        op = window.getch()
        if op is 10:
            break
        elif op is not -1:
            string += str(chr(op))
        op = -1
    return string


if __name__ == '__main__':
    #---------------------
    ld = ListaDoble()
    #---------------------
    lcd = ListaCircularDoble()
    #---------------------
    cola = Cola()
    #---------------------
    pila = Pila()
    #---------------------
    usuario = ""

    curses.initscr()
    curses.beep()
    curses.beep()

    window = curses.newwin(ALTO, ANCHO, 0, 0)
    window.timeout(TIMEOUT)
    window.keypad(1)
    curses.noecho()
    curses.curs_set(0)
    
    window.clear()
    window.border(0)
    
    op = -1
    while True:
        menu(window,str(usuario))
        op = window.getch()

        if op is 49:
            #1. Play
            if usuario is "":
                window.clear()
                window.border(0)
                string = ""
                op = -1
                while True:
                    window.addstr(1,ANCHO//2-len(str("Al terminar presiona ENTER"))//2,"Al terminar presiona ENTER")
                    window.addstr(ALTO//2,ANCHO//2-len(string)//2,string)
                    op = window.getch()
                    if op is 10:
                        break
                    elif op is not -1:
                        string += str(chr(op))
                    op = -1

                usuario = string
                lcd.add(usuario)
            pila.vaciar()
            ld.clean()
            play(window,usuario,ld)
        elif op is 50:
            #2. Scoreboard
            scoreboard(window,cola)
        elif op is 51:
            #3. User Selection
            if lcd.primero is not None:
                usuario = userselect(window,lcd)
            else:
                window.clear()
                window.border(0)
                window.addstr(1,ANCHO//2-len("USUARIOS")//2,"USUARIOS")
                window.addstr(5,ANCHO//2-len("NO HAY USUARIOS")//2,"NO HAY USUARIOS")
                window.addstr(7,ANCHO//2-len("Juega para crear uno")//2,"Juega para crear uno")
                window.addstr(12,ANCHO//2-len("Enter para continuar...")//2,"Enter para continuar...")
                while True:
                    ent = window.getch()
                    if ent is 10:
                        break
        elif op is 52:
            #4. Reports
            reports(window,ld,cola,pila,lcd)
        elif op is 53:
            #5. Bulk Loading
            arch = bulk(window)
            try:
                with open(arch) as csv_f:
                    csv_r = csv.reader(csv_f,delimiter=',')
                    line = 0
                    for row in csv_r:
                        if line == 0:
                            #Header de usuario
                            line += 1
                        else:
                            lcd.add(str(row[0]))
                            line += 1
                sel = -1
                while True:
                    window.clear()
                    window.border(0)
                    window.addstr(1,ANCHO//2-len("Carga Masiva")//2,"Carga Masiva")
                    window.addstr(ALTO//2,ANCHO//2-len("Ususarios cargados")//2,"Ususarios cargados")
                    sel = window.getch()
                    if sel == 10:
                        break
            except:
                window.clear()
                window.border(0)
                sel = -1
                while True:
                    window.addstr(1,ANCHO//2-len("Carga Masiva")//2,"Carga Masiva")
                    window.addstr(ALTO//2-2,ANCHO//2-len("Error con el archivo")//2,"Error con el archivo")
                    window.addstr(ALTO//2,ANCHO//2-len("Verifica su ubicacion y existencia")//2,"Verifica su ubicacion y existencia")
                    window.addstr(ALTO//2+2,ANCHO//2-len("Vuelve a intentar")//2,"Vuelve a intentar")
                    sel = window.getch()
                    if sel == 10:
                        break
        elif op is 54:
            #6. Limpiar usuario
            usuario = ""
        elif op is 55:
            #7. Exit
            break

    curses.endwin()