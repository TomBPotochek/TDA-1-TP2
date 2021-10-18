
from collections import defaultdict

from dataclasses import dataclass
from typing import DefaultDict, List, Tuple, Set
@dataclass
class Ciudades:
    """el grafo de ciudades por lista de adyacencias, costos y total de ciudades"""
    adyacencias: DefaultDict[str, List[str]]
    costos: DefaultDict[Tuple[str, str], int]
    lista: Set[str]

    def iterar(self):
        """generador para iterar las ciudades 
        siguiendo las adyacencias"""
        for u in self.adyacencias:
            for v in self.adyacencias[u]:
                yield u,v

import math
INF = math.inf  # '<infinito>'
path = str
def parse_file(depositos: path) -> Ciudades:
    from csv import reader
    from collections import defaultdict

    matriz_costos = defaultdict(lambda: INF)
    grafo_ciudades = defaultdict(list)
    total_ciudades = set()

    with open(depositos, "r") as depositos_csv:
        filas = reader(depositos_csv, delimiter=',')
        for a, b, costo in filas:
            costo = int(costo)
            grafo_ciudades[a].append(b)
            matriz_costos[a, b] = costo
            total_ciudades |= {a, b}
    return Ciudades(grafo_ciudades, matriz_costos, total_ciudades)




# ver si conviene no tomar por parametro
def dijkstra(grafo: Ciudades, vertice_fuente: str):
    import heapq
    entries = {}  # sirve para actualizar pesos
    min_queue = []

    #init de pesos desde fuente en heap de minimos
    for v in grafo.lista: 
        if v == vertice_fuente:
#entry = [distancia de vertice a fuente, vertice, predecesor de v]
            entry = [0, v, None]
        else:
            entry = [INF, v, None]
        entries[v] = entry
        min_queue.append(entry)
    heapq.heapify(min_queue)  # heap de minimos


    while min_queue != []:
        costo_actual_u, u, _ = heapq.heappop(min_queue)
        #camino_minimo.append(u)  # sirve esta lista??
        for v in grafo.adyacencias[u]:
            costo_actual_v = entries[v][0]
            costo_nuevo_v = costo_actual_u + grafo.costos[u, v]
            if costo_actual_v > costo_nuevo_v:
                entries[v][0] = costo_nuevo_v
                entries[v][2] = u
        heapq.heapify(min_queue)  # mantener la condicion heap

    #return {ciud:(entries[ciud][0],entries[ciud][2]) for ciud in entries}
    return {ciud:entries[ciud][2] for ciud in entries}

def bellmanFord(grafo: Ciudades, vertice_fuente: str):

    #init
    pesos_desde_fuente = defaultdict(lambda: INF)
    pesos_desde_fuente[vertice_fuente] = 0

    predecesores = defaultdict(lambda: None)
    predecesores[vertice_fuente] = None #para explicitarlo

    for i in range(1,len(grafo.lista)):
        for u, v in grafo.iterar():
            costo_viejo = pesos_desde_fuente[v]
            costo_nuevo = pesos_desde_fuente[u] + grafo.costos[u,v]
            if costo_viejo > costo_nuevo:
                pesos_desde_fuente[v] = costo_nuevo
                predecesores[v] = u

    for u,v in grafo.iterar():
        peso_u, peso_v = pesos_desde_fuente[u], pesos_desde_fuente[v]
        if peso_v > peso_u + grafo.costos[u, v]:
            return False, None
    return True, predecesores


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser(description=('Toma un archivo de texto con información '
                                         'sobre los depósitos y calcula la ciudad óptima '
                                         'donde ubicar la fábrica mediante el algoritmo '
                                         'de Johnson.'))

    parser.add_argument('archivo', metavar='archivo.txt', type=str,
                        help=('path al archivo que contiene la información '
                              'sobre los contenedores.'))

    args = parser.parse_args()

    ciudades = parse_file(args.archivo)

    #para ir viendo/debuggear
    print(dijkstra(ciudades, "A"), bellmanFord(ciudades, "A"))
