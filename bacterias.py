import random
from nodos import Nodos
from math import hypot

class Bacteria:
    ciudades = Nodos() # Nodos con la informacion de la posicion
                       # y respectivas demandas
    def __init__(self,size):
        self.size = size #tamano de nodos sin contar el deposito
        self.cromosoma = [] #cromosoma inicialmente vacio
        self.fitness = 0.0 #fitness asociado al cromosoma
        self.fitness_real = 0.0
        self.resistente = False #resistencia al antibiotico
        self.cv = 0  #cantidad de vehiculos utilizados en la solucion

    def random_cromosoma(self):
        self.cromosoma[:] = []
        for i in range(0,self.size):
            self.cromosoma.append(i+1) #se inicializa el arreglo en orden
        for i in range(0,self.size):
            j = random.randrange(0,self.size) #para cada indice del arreglo, se elige
            aux = self.cromosoma[i]      #otro indice al azar para ser intercambiados.
            self.cromosoma[i] = self.cromosoma[j]
            self.cromosoma[j] = aux

    'Calcula el fitness en funcion del coromosoma y el archivo de nodos'
    def calcular_fitness(self):
        if self.ciudades.nodos == [] :
            raise SystemExit("Error: Ciudades no inicializadas")
        else:
            x_d = self.ciudades.nodos[0].x #coordenadas del
            y_d = self.ciudades.nodos[0].y #deposito
            capacidad_max = self.ciudades.capacidad #capacidad maxima del camion
            self.cv = 1 #camiones iniciales
            self.fitness_real = 0.0 #fitness total
            capacidad = 0 #capacidad inicial
            #se recorren los genes
            for i in range(0,self.size-1):
                x_1 = self.ciudades.nodos[self.cromosoma[i]].x #se guardan las coordenadas
                y_1 = self.ciudades.nodos[self.cromosoma[i]].y #del nodo actual y el nodo
                x_2 = self.ciudades.nodos[self.cromosoma[i+1]].x #siguiente a recorrer
                y_2 = self.ciudades.nodos[self.cromosoma[i+1]].y
                demanda = self.ciudades.nodos[self.cromosoma[i+1]].demanda #demanda del nodo siguiente
                if i == 0 :
                    #se calcula la distancia entre el deposito y el
                    #primer nodo en el gen y se suma al fitness
                    self.fitness_real = self.fitness_real + hypot(x_1 - x_d,y_1 - y_d)
                    capacidad = self.ciudades.nodos[self.cromosoma[i]].demanda
                if (capacidad + demanda) > capacidad_max :
                    #si la capacidad actual supera la demanda se
                    #retorna al deposito y se va al nodo siguiente
                    self.fitness_real = self.fitness_real + hypot(x_1 - x_d,y_1 - y_d) + hypot(x_2 - x_d,y_2 - y_d)
                    self.cv = self.cv+1 #se aumenta el numero de vehiculos utilizados
                    capacidad = demanda #se vacia el camion
                else :
                    #si se puede suplir la demanda se calcula la distancia
                    #entre nodos y se suma al fitness
                    self.fitness_real = self.fitness_real + hypot(x_2 - x_1,y_2 - y_1)
                    capacidad = capacidad + demanda
                if i == (self.size - 2) :
                    #se calcula la distancia entre el deposito y el
                    #ultimo nodo en el gen y se suma al fitness
                    self.fitness_real = self.fitness_real + hypot(x_2 - x_d,y_2 - y_d)
                self.fitness = self.fitness_real * self.cv**2


    'Operador de transformacion con material genetico libre en el ambiente'
    def __add__(self,other):
        cromosoma_ox = []
        cromosoma = self.cromosoma[:]
        for i in range(0,self.size):
            cromosoma_ox.append(0)
        i1 = random.randrange(0,self.size - other.size) #alelo randomico
        i2 = i1 + other.size #tamano de material genetico
        #se copia el contenido del material genetico
        for i in range(i1,i2):
            cromosoma_ox[i] = other.cromosoma[i-i1]
            #se marcan los genes del segundo cromosoma
            #que se encuentran entre los alelos del primero
            for j in range(0,self.size):
                if(cromosoma[j] == other.cromosoma[i-i1]):
                    cromosoma[j] = -1
                    break
        i = i2
        j = i2
        #desde el indice i2 se copian circularmente
        #los genes que no estan marcados
        while(i != i1):
            if(j == self.size):
                j = 0
                continue
            if(i == self.size):
                i = 0
                continue
            if(cromosoma[j] == -1):
                j=j+1
                continue
            cromosoma_ox[i] = cromosoma[j]
            i=i+1
            j=j+1
        return cromosoma_ox

    'Operador de conjugacion OX entre cromosomas de las bacterias'
    def __mul__(self,other):
        cromosoma_ox = []
        cromosoma = self.cromosoma[:]
        for i in range(0,self.size):
            cromosoma_ox.append(0)
        i1 = random.randrange(0,self.size) #indices entre
        i2 = random.randrange(0,self.size) #alelos randomicos
        while i1 == i2:
            i2 = random.randrange(0,self.size)
        if i1 > i2:
            aux = i1
            i1 = i2
            i2 = aux
        #se copia el contenido entre los indices del primer
        #cromooma al cromosoma resultante
        for i in range(i1,i2):
            cromosoma_ox[i] = other.cromosoma[i]
            #se marcan los genes del segundo cromosoma
            #que se encuentran entre los alelos del primero
            for j in range(0,self.size):
                if(cromosoma[j] == other.cromosoma[i]):
                    cromosoma[j] = -1
                    break
        i = i2
        j = i2
        #desde el indice i2 se copian circularmente
        #los genes que no estan marcados
        while(i != i1):
            if(j == self.size):
                j = 0
                continue
            if(i == self.size):
                i = 0
                continue
            if(cromosoma[j] == -1):
                j=j+1
                continue
            cromosoma_ox[i] = cromosoma[j]
            i=i+1
            j=j+1
        return cromosoma_ox

    def set_resistencia(self,antibiotico):
        if antibiotico < self.fitness :
            self.resistente = False
        else :
            self.resistente = True
