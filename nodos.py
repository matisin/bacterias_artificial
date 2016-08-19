from nodo import Nodo

class Nodos:
    def __init__(self):
        self.nodos = []
        self.dimension = 0
        self.capacidad = 0
    def nodos_archivo(self,Archivo):
        'Retorna los nodos en el archivo'
        f = open(Archivo,'r')
        for line in f:
            line=line.strip()
            columns = line.split()
            if columns[0] == "DIMENSION" :
                self.dimension = int(columns[2])
            if columns[0] == "CAPACITY" :
                self.capacidad = int(columns[2])
            if (line == 'NODE_COORD_SECTION'):
                for line in f:
                    line = line.strip()
                    if (line == 'DEMAND_SECTION'):
                        break
                    columns = line.split()
                    x = int(columns[1])
                    y = int(columns[2])
                    nodo = Nodo(x,y)
                    self.nodos.append(nodo)
            if (line == 'DEMAND_SECTION'):
                for line in f:
                    line = line.strip()
                    if (line == 'DEPOT_SECTION'):
                        break
                    columns = line.split()
                    n = int(columns[0])
                    demanda = int(columns[1])
                    self.nodos[n-1].demanda=demanda
            if (line == 'DEPOT_SECTION'):
                break
        f.close()
