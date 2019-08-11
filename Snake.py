import curses

from Estructuras import ListaDoble, ListaCircularDoble, Pila, Cola
from Nodos import NodoSerpiente, NodoPila, NodoCola, NodoUsuario
from curses import KEY_RIGHT, KEY_LEFT, KEY_DOWN, KEY_UP, KEY_ENTER
from random import randint

ALTO = 20
ANCHO = 40
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

    def __init__(self, x, y, window):
        self.body_list = []
        self.hit_score = 0
        self.timeout = TIMEOUT
        self.nivel = 1
        self.win = False
        self.lose = False
        #self.estado = "Estado"

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
        food.reset()
        body = Body(self.last_head_coor[0], self.last_head_coor[1])
        self.body_list.insert(-1, body)
        self.hit_score += 1

        if self.hit_score is 5:
            if self.nivel is 3:
                #self.estado = "Puntos iguales a 5, Nivel es 3 y Win"
                self.win = True
            else:
                #self.estado = "Puntos iguales a 5 y Nivel no es 3"

                self.nivel += 1
                self.hit_score = 0
                if self.nivel is 2:
                    self.timeout = 150
                elif self.nivel is 3:
                    self.timeout = 100
        else:
            #self.estado = "Puntos menores a 5 => Actual: " + str(self.hit_score)
            if self.nivel is 1:
                self.timeout -= 2
                self.window.timeout(self.timeout)
            elif self.nivel is 2:
                #if self.hit_score % 3 == 0:
                self.timeout -= 3
                self.window.timeout(self.timeout)
            elif self.nivel is 3:
                self.timeout -= 4
                self.window.timeout(self.timeout)

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
        for body in self.body_list:
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
        return 'Punteo: {} Nivel: {} Vel: {}'.format(self.hit_score,self.nivel,self.timeout)

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
    def __init__(self, window, char='*'):
        self.x = randint(1, MAX_X)
        self.y = randint(1, MAX_Y)
        self.window = window
        self.char = char

    def render(self):
        self.window.addstr(self.y, self.x, self.char)

    def reset(self):
        self.x = randint(1, MAX_X)
        self.y = randint(1, MAX_Y)


def menu(window):
    window.clear()
    window.border(0)
    window.addstr(7,10,"1. Jugar")
    window.addstr(8,10,"2. Puntuaciones")
    window.addstr(9,10,"3. Seleccion de Usuario")
    window.addstr(10,10,"4. Reportes")
    window.addstr(11,10,"5. carga Masiva")
    window.addstr(12,10,"6. Salir")

def play(window):
    window.clear()
    window.border(0)
    snake = Snake(SNAKE_X,SNAKE_Y, window)
    food = Food(window,'*')
    
    while True:
        window.clear()
        window.border(0)
        
        snake.render()
        food.render()
        window.addstr(0,(MAX_X//2-len(snake.score)//2)+1,snake.score)
        event = window.getch()

        if event == 27:
            break
        
        if event in [KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT]:
            snake.change_direction(event)

        if snake.head.x == food.x and snake.head.y == food.y:
            curses.beep()
            if (snake.hit_score + 1) is 5:
                pila.vaciar()
            else:
                pila.push(food.y,food.x)
            snake.eat_food(food) 

        if event == 32:
            pila.graficar()
            key = -1
            while key != 32:
                key = window.getch()

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
        window.getch()
    elif snake.lose is True:
        m = "Game Over!"
        window.addstr(MAX_Y//2,(MAX_X//2-len(m)//2) + 1, m)
        window.nodelay(0)
        window.getch()
    else:
        m = "Saliste!"
        window.addstr(MAX_Y//2,(MAX_X//2-len(m)//2) + 1, m)
        window.nodelay(0)
        window.getch()
    # pila.graficar()

def scoreboard(window, cola):
    window.clear()
    window.border(0)
    window.addstr(1,ANCHO//2-len("Puntuaciones")//2,"Puntuaciones")
    window.addstr(3,10,"Nombre")
    window.addstr(3,23,"Puntos")
    
    lin = 5
    aux = cola.frente
    while aux is not None:
        if lin is 15:
            break
        else:
            window.addstr(lin,10,str(aux.name))
            window.addstr(lin,23,str(aux.pts))
        lin += 1
        aux = aux.sig
        

if __name__ == '__main__':
    #ld = ListaDoble()
    #lcd = ListaCircularDoble()
    cola = Cola()
    for i in range(11):
        cola.enqueue(str("Juan" + str(i)),i*2)
    
    pila = Pila()

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
    scoreboard(window,cola)
    '''
    while True:
        menu(window)
        op = window.getch()

        if op is 49:
            #1. Play
            play(window)
        elif op is 50:
            #2. Scoreboard

            a = 1
        elif op is 51:
            #3. User Selection
            a = 1
        elif op is 52:
            #4. Reports
            a = 1
        elif op is 53:
            #5. Bulk Loading
            a = 1
        elif op is 54:
            #6. Exit
            a = 1

        if op is 54:
            break
    '''
    curses.endwin()