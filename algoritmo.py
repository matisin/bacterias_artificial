import sys
from datetime import datetime
from bacterias import Bacteria
import funciones
import random
import curses
import time
import progreso
import threading

random.seed(datetime.now())


if __name__ == "__main__":
    #se inicializan los nodos con el archivo

    sp = int(sys.argv[1])#cantidad de bacterias
    pc = int(sys.argv[2])#probabilidad de conjugacion
    pt = int(sys.argv[3])#probabilidad de transformacion
    pm = int(sys.argv[4])#probabilidad de mutacion
    pl = int(sys.argv[5])#probabilidad de liberacion
    pcl = int(sys.argv[6])#probabilidad de conjugacion libre
    ptl = int(sys.argv[7])#probabilidad de transformacion libre
    pml = int(sys.argv[8])#probabilidad de mutacion libre
    progreso.np = int(sys.argv[9])#cantidad de iteraciones
    Bacteria.ciudades.nodos_archivo(sys.argv[10])
    size = Bacteria.ciudades.dimension -1
    bacterias = []         #arreglo de bacterias
    resistentes = []       #bacterias resistentes
    no_resistentes = []    #bacterias no resistentes
    material_genetico = [] #material genetico liberado
    progreso.mejor_peor = [0,0] #arreglo con el mejor y peor bacterias encontrados en cada iteracion
    #se inicializan sp bacterias
    funciones.inicializacion_poblacion(bacterias,sp,size)
    progreso.mejor_bacteria = Bacteria(size)
    progreso.mejor_bacteria.cromosoma = bacterias[0].cromosoma
    progreso.mejor_bacteria.calcular_fitness()
    progreso.var_genetica = 0
    t = threading.Thread(target=progreso.imprimir)
    for i in range(0,progreso.np):
        if stop == 1:
            break
        progreso.i = i + 1
        #se formula el antibiotico
        antibiotico = funciones.formular_antibiotico(bacterias)
        #se clasifican las bacterias
        funciones.clasificacion(bacterias,resistentes,no_resistentes,antibiotico)
        #se aplica conjugacion entre bacterias
        funciones.conjugacion_bacterias(resistentes,no_resistentes,pc)
        #se aplica transformacion a las bacterias no resistentes
        funciones.transformacion_bacterias(no_resistentes,material_genetico,pt)
        #se mutan las bacterias con probabilidad pm de mutar
        funciones.mutacion(bacterias,pm)
        #se vuelven a clasificar las bacterias
        funciones.clasificacion(bacterias,resistentes,no_resistentes,antibiotico)
        #se aplica el antibiotico a las bacterias
        funciones.aplicar_antibiotico(no_resistentes,bacterias,material_genetico,pl)
        #se regenera la poblacion para llegar a la cantidad de bacterias inicial
        funciones.regeneracion_poblacion(bacterias,sp,size)
        #se busca el mejor y peor fitness
        funciones.mejor_peor_fitness(bacterias,progreso.mejor_peor)
        if i == 0:
            t.start()

        if progreso.mejor_peor[0].fitness < progreso.mejor_bacteria.fitness:
            progreso.mejor_bacteria.cromosoma = progreso.mejor_peor[0].cromosoma[:]
            progreso.mejor_bacteria.calcular_fitness()
        #comienza el proceso de variacion genetica libre hasta que se detenga el estancamiento
        while progreso.mejor_peor[0].fitness == progreso.mejor_peor[1].fitness:
            progreso.var_genetica = progreso.var_genetica + 1
            funciones.conjugacion_libre_bacterias(bacterias,pcl)
            funciones.transformacion_bacterias(bacterias,material_genetico,ptl)
            funciones.mutacion_libre(bacterias,pml)
            funciones.mejor_peor_fitness(bacterias,progreso.mejor_peor)
            if progreso.mejor_peor[0].fitness < progreso.mejor_bacteria.fitness:
                progreso.mejor_bacteria.cromosoma= progreso.mejor_peor[0].cromosoma[:]
                progreso.mejor_bacteria.calcular_fitness()
