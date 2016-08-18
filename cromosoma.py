import random
from datetime import datetime
from nodos import Nodos
from math import hypot

class Cromosoma:
    'Cromosoma de bacterias donde cada gen representa un nodo'
    random.seed(datetime.now())
    ciudades = Nodos() #Nodos con la informacion de la posicion
                       #y respectivas demandas

    def __init__(self,size):
        self.genes = [] #arreglo de genes que representan las ciudades
        self.size = size #tamano del cromosoma
        self.cv = 1 #cantidad de vehiculos utilizados en la solucion
        for i in range(0,size):
            self.genes.append(i+1) #se inicializa el arreglo en orden
        for i in range(0,size):
            j = random.randrange(0,size) #para cada indice del arreglo, se elige
            aux = self.genes[i]          #otro indice al azar para ser intercambiados.
            self.genes[i] = self.genes[j]
            self.genes[j] = aux

    def set_genes(self,genes):
        self.genes = genes
    #falta terminar
    'Operador de transformacion con material genetico libre en el ambiente, retorna un cromosoma'
    def __add__(self,other):
        genes_ox = []
        genes = self.genes[:]
        for i in range(0,self.size):
            genes_ox.append(0)
        i1 = random.randrange(0,self.size - len(other)) #alelo randomico
        i2 = i1 + len(other) #tamano de material genetico
        #se copia el contenido del material genetico
        for i in range(i1,i2):
            genes_ox[i] = other.genes[i-i1]
            #se marcan los genes del segundo cromosoma
            #que se encuentran entre los alelos del primero
            for j in range(0,self.size):
                if(genes[j] == other.genes[i-i1]):
                    genes[j] = -1
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
            if(genes[j] == -1):
                j=j+1
                continue
            genes_ox[i] = genes[j]
            i=i+1
            j=j+1
        cromosoma_ox = Cromosoma(self.size)
        cromosoma_ox.set_genes(genes_ox)
        #se retorna el cromosoma hijo
        return cromosoma_ox

    'Operador de conjugacion OX entre cromosomas, retorna un cromosoma'
    def __mul__(self,other):
        genes_ox = []
        genes = self.genes[:]
        for i in range(0,self.size):
            genes_ox.append(0)
        i1 = random.randrange(0,self.size) #indices entre
        i2 = random.randrange(0,self.size) #alelos randomicos
        while(i1 == i2 or i1 > i2):
            i2 = random.randrange(0,self.size)
        #se copia el contenido entre los indices del primer
        #cromooma al cromosoma resultante
        for i in range(i1,i2):
            genes_ox[i] = other.genes[i]
            #se marcan los genes del segundo cromosoma
            #que se encuentran entre los alelos del primero
            for j in range(0,self.size):
                if(genes[j] == other.genes[i]):
                    genes[j] = -1
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
            if(genes[j] == -1):
                j=j+1
                continue
            genes_ox[i] = genes[j]
            i=i+1
            j=j+1
        cromosoma_ox = Cromosoma(self.size)
        cromosoma_ox.set_genes(genes_ox)
        #se retorna el cromosoma hijo
        return cromosoma_ox

    'Se decodifica y calcula el fitness asociado a los genes del cromosoma'
    def calcular_fitness(self):
        if self.ciudades.nodos == [] :
            raise SystemExit("Error: Ciudades no inicializadas")
        else:
            x_d = self.ciudades.nodos[0].x #coordenadas del
            y_d = self.ciudades.nodos[0].y #deposito
            capacidad_max = self.ciudades.capacidad #capacidad maxima del camion
            self.cv = 1 #camiones iniciales
            capacidad = 0 #capacidad inicial
            fitness = 0.0 #fitness total
            #se recorren los genes
            for i in range(0,self.size-1):
                x_1 = self.ciudades.nodos[self.genes[i]].x #se guardan las coordenadas
                y_1 = self.ciudades.nodos[self.genes[i]].y #del nodo actual y el nodo
                x_2 = self.ciudades.nodos[self.genes[i+1]].x #siguiente a recorrer
                y_2 = self.ciudades.nodos[self.genes[i+1]].y
                demanda_2 = self.ciudades.nodos[i+1].demanda #demanda del nodo siguiente
                if i == 0 :
                    #se calcula la distancia entre el deposito y el
                    #primer nodo en el gen y se suma al fitness
                    fitness = fitness + hypot(x_1 - x_d,y_1 - y_d)
                    capacidad = capacidad + self.ciudades.nodos[self.genes[i]].demanda
                elif i == (self.size - 2) :
                    #se calcula la distancia entre el deposito y el
                    #ultimo nodo en el gen y se suma al fitness
                    fitness = fitness + hypot(x_2 - x_d,y_2 - y_d)
                if (capacidad + demanda_2) > capacidad_max :
                    #si la capacidad actual supera la demanda se
                    #retorna al deposito y se va al nodo siguiente
                    fitness = fitness + hypot(x_1 - x_d,y_1 - y_d)
                    fitness = fitness + hypot(x_2 - x_d,y_2 - y_d)
                    capacidad = demanda_2
                    self.cv = self.cv+1 #se aumenta el numero de vehiculos utilizados
                else :
                    #si se puede suplir la demanda se calcula la distancia
                    #entre nodos y se suma al fitness
                    fitness = fitness + hypot(x_2 - x_1,y_2 - y_1)
                    capacidad = capacidad + demanda_2
            return fitness
