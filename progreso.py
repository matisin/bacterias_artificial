import threading
import time
from curses import wrapper
import curses
import algoritmo

i = 0
np = 0
mejor_peor = []
mejor_bacteria = []
var_genetica = 0
def imprimir():
    wrapper(main)
    return

def main(stdscr):
    stdscr.nodelay(True)
    while True:
        stdscr.clear()
        if i >= np :
            stdscr.addstr(0,0,"Iteracion numero\t\t{0}".format(i))
            stdscr.addstr(2,0,"Cantidad variacion libre\t{0}".format(var_genetica))
            stdscr.addstr(4,0,"Mejor fitness global\t\t{0}".format(mejor_bacteria.fitness_real))
            stdscr.addstr(5,0,"Mejor fitness local\t\t{0}".format(mejor_peor[0].fitness_real))
            stdscr.addstr(6,0,"Cantidad de vehiculos \t\t{0}".format(mejor_peor[0].cv))
            stdscr.addstr(7,0,"Peor fitness local\t\t{0}".format(mejor_peor[1].fitness_real))
            stdscr.addstr(8,0,"Cantidad de vehiculos \t\t{0}".format(mejor_peor[1].cv))
            stdscr.addstr(9,0,"")
            stdscr.refresh()
            break
        stdscr.addstr(0,0,"Iteracion numero\t\t{0}".format(i))
        stdscr.addstr(2,0,"Cantidad variacion libre\t{0}".format(var_genetica))
        stdscr.addstr(4,0,"Mejor fitness global\t\t{0}".format(mejor_bacteria.fitness_real))
        stdscr.addstr(5,0,"Mejor fitness local\t\t{0}".format(mejor_peor[0].fitness_real))
        stdscr.addstr(6,0,"Cantidad de vehiculos \t\t{0}".format(mejor_peor[0].cv))
        stdscr.addstr(7,0,"Peor fitness local\t\t{0}".format(mejor_peor[1].fitness_real))
        stdscr.addstr(8,0,"Cantidad de vehiculos \t\t{0}".format(mejor_peor[1].cv))
        stdscr.addstr(9,0,"")
        stdscr.refresh()
        try:
            key = stdscr.getkey()
            if ord(key[0]) == 27:
                break
        except:
            continue
    stdscr.nodelay(False)
    stdscr.addstr(10,0,"Mejor fitness\t\t{0}".format(mejor_bacteria.fitness_real))
    stdscr.addstr(11,0,"Cantidad de vehiculos \t\t{0}".format(mejor_bacteria.cv))
    stdscr.addstr(12,0,"cromosoma\t\t{0}".format(mejor_bacteria.cromosoma))
    stdscr.addstr(15,0,"Presione cualquier tecla para salir")
    stdscr.refresh()
    stdscr.getkey()
    algoritmo.exit()
