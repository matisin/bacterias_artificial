from bacterias import Bacteria
import random

'Se comparan los fitness de las bacterias y se guardan la mejor y peor en el arreglo'
def mejor_peor_fitness(bacterias,mejor_peor):
    peor_fitness = 0
    mejor_fitness = 300000
    for bacteria in bacterias:
        fitness = bacteria.fitness
        if fitness < mejor_fitness :
            mejor_fitness = fitness
            mejor_peor[0] = bacteria
        if fitness > peor_fitness :
            peor_fitness = fitness
            mejor_peor[1] = bacteria



def inicializacion_poblacion(bacterias,sp,size):
    bacterias[:] = []
    for i in range(0,sp):
        bacteria = Bacteria(size)
        bacteria.random_cromosoma()
        bacteria.calcular_fitness()
        bacterias.append(bacteria)

def regeneracion_poblacion(bacterias,sp,size):
    sobrevivientes = len(bacterias) #cantidad de bacterias que quedan
    restantes = sp - sobrevivientes #cantidad de bacterias que faltan
    for i in range(0,restantes):
        bacteria = Bacteria(size) #nueva bacteria
        j = random.randrange(0,sobrevivientes) #bacteria randomica
        bacteria.cromosoma = bacterias[j].cromosoma[:] #se copia el cromosoma
        i1 = random.randrange(0,bacteria.size)#2 pares de puntos randomicos
        i2 = random.randrange(0,bacteria.size)
        i3 = random.randrange(0,bacteria.size)
        i4 = random.randrange(0,bacteria.size)
        aux = bacteria.cromosoma[i1]#se intercambian los genes
        bacteria.cromosoma[i1] = bacteria.cromosoma[i2]
        bacteria.cromosoma[i2] = aux
        aux = bacteria.cromosoma[i3]#se intercambian los genes
        bacteria.cromosoma[i3] = bacteria.cromosoma[i4]
        bacteria.cromosoma[i4] = aux
        bacteria.calcular_fitness()
        bacterias.append(bacteria)

def aplicar_antibiotico(no_resistentes,bacterias,material_genetico,pl):
    for bacteria in no_resistentes:
        #para la probabilidad de liberar material genetico
        p = random.randrange(0,100)
        if p <= pl:
            i1 = random.randrange(0,bacteria.size) #indices entre
            i2 = random.randrange(0,bacteria.size) #alelos randomicos
            while(i1 == i2):
                i2 = random.randrange(0,bacteria.size)
            if i1 > i2:
                aux = i1
                i1 = i2
                i2 = aux
            #se corta el cromosoma entre indices randomicos
            bacteria.cromosoma = bacteria.cromosoma[i1:i2]
            bacteria.size = i2 - i1
            material_genetico.append(bacteria)
        bacterias.remove(bacteria)

def clasificacion(bacterias,resistentes,no_resistentes,antibiotico):
    resistentes[:] = []
    no_resistentes[:] = []
    for bacteria in bacterias:
        #se aplica el antibiotico
        bacteria.set_resistencia(antibiotico)
        if bacteria.resistente:
            resistentes.append(bacteria)
        else:
            no_resistentes.append(bacteria)

def mutacion_libre(bacterias,pml):
    for bacteria in bacterias:
        p = random.randrange(0,100)
        if p <= pml:
            i1 = random.randrange(0,bacteria.size)#dos puntos randomicos
            i2 = random.randrange(0,bacteria.size)
            aux = bacteria.cromosoma[i1]#se intercambian los genes
            bacteria.cromosoma[i1] = bacteria.cromosoma[i2]
            bacteria.cromosoma[i2] = aux
            bacteria.calcular_fitness()


def mutacion(bacterias,pm):
    for bacteria in bacterias:
        p = random.randrange(0,100)
        if p <= pm:
            i1 = random.randrange(0,bacteria.size)#dos puntos randomicos
            i2 = random.randrange(0,bacteria.size)
            if bacteria.resistente:#si la bacteria es resistente
                cromosoma = bacteria.cromosoma[:]#se guardan su cromosoma
                fitness = bacteria.fitness       # y su fitness
                cv = bacteria.cv
                aux = bacteria.cromosoma[i1] #se intercambian los genes
                bacteria.cromosoma[i1] = bacteria.cromosoma[i2]
                bacteria.cromosoma[i2] = aux
                bacteria.calcular_fitness()#y se recalcula el fitness
                if(bacteria.fitness > fitness):#si empeora se vuelve como era
                    bacteria.fitness = fitness
                    bacteria.cromosoma = cromosoma
                    bacteria.cv = cv
            else:# si la bacteria no es resistente
                aux = bacteria.cromosoma[i1]#se intercambian los genes
                bacteria.cromosoma[i1] = bacteria.cromosoma[i2]
                bacteria.cromosoma[i2] = aux
                bacteria.calcular_fitness()

def conjugacion_libre_bacterias(bacterias,pcl):
    for bacteria in bacterias:
        p = random.randrange(0,100)
        if p <= pcl:
            i = random.randrange(0,len(bacterias))
            cromosoma1 = bacteria * bacterias[i]
            cromosoma2 = bacterias[i] * bacteria
            bacteria.cromosoma = cromosoma1
            bacterias[i].cromosoma = cromosoma2
            bacteria.calcular_fitness()
            bacterias[i].calcular_fitness()

def conjugacion_bacterias(resistentes,no_resistentes,pc):
    for bacteria in no_resistentes:
        p = random.randrange(0,100)
        if p <= pc:
            i = random.randrange(0,len(resistentes))#se busca una bacteria resistente al azar
            bacteria.cromosoma = bacteria * resistentes[i] # se cruzan OX
            bacteria.calcular_fitness()


'Para este metodo no se necsita un analogo libre, ya que simplemente se le'
'entrega el arreglo de bacterias y la probabilidad de transformacion libre'
def transformacion_bacterias(no_resistentes,material_genetico,pt):
    if len(material_genetico) > 0: #si hay material genetico disponible
        for bacteria in no_resistentes:
            p = random.randrange(0,100)
            if p <= pt:
                i = random.randrange(0,len(material_genetico))#se elige un material genetico al azar
                bacteria.cromosoma = bacteria + material_genetico[i]#se cruza con el material genetico
                bacteria.calcular_fitness()
                material_genetico.remove(material_genetico[i])#se remueve el material genetico
                if len(material_genetico) == 0:
                    break

def formular_antibiotico(bacterias):
    antibioticos = [] #antibioticos para competir
    size = len(bacterias)
    for i in range(0,4):
        antibioticos.append(bacterias[i].fitness)
    for i in range(4,size):
        j = random.randrange(0,i)
        if j < 4 :
            antibioticos[j] = bacterias[i].fitness
    if antibioticos[0] < antibioticos[1]:
        antibiotico1 = antibioticos[0]
    else:
        antibiotico1 = antibioticos[1]
    if antibioticos[2] < antibioticos[3]:
        antibiotico2 = antibioticos[2]
    else:
        antibiotico2 = antibioticos[3]
    if antibiotico1 < antibiotico2:
        return antibiotico2
    else:
        return antibiotico1
