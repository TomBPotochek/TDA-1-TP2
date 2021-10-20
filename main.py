
import math
from collections import defaultdict

from dataclasses import dataclass
from typing import DefaultDict, Dict, List, Tuple, Set, Iterable


@dataclass
class Ciudades:
    """el grafo de ciudades por lista de adyacencias 
    y total de ciudades"""
    adyacencias: DefaultDict[str, List[str]]
    lista: Set[str]

    def iterar(self):
        """generador para iterar las ciudades 
        siguiendo las adyacencias"""
        for u in self.adyacencias:
            for v in self.adyacencias[u]:
                yield u, v


INF = math.inf  # '<infinito>'
path = str
costos_t = DefaultDict[Tuple[str, str], int]


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
    return Ciudades(grafo_ciudades, total_ciudades),  matriz_costos


def dijkstra(grafo: Ciudades, costos: costos_t, vertice_fuente: str):
    import heapq
    entries = {}  # sirve para actualizar pesos
    min_queue = []

    # init de pesos desde fuente en heap de minimos
    for v in grafo.lista:
        if v == vertice_fuente:
            # entry = [distancia de vertice a fuente, vertice, predecesor de v]
            entry = [0, v, None]
        else:
            entry = [INF, v, None]
        entries[v] = entry
        min_queue.append(entry)
    heapq.heapify(min_queue)  # heap de minimos

    while min_queue != []:
        costo_actual_u, u, _ = heapq.heappop(min_queue)
        for v in grafo.adyacencias[u]:
            costo_actual_v = entries[v][0]
            costo_nuevo_v = costo_actual_u + costos[u, v]
            if costo_actual_v > costo_nuevo_v:
                entries[v][0] = costo_nuevo_v
                entries[v][2] = u
        heapq.heapify(min_queue)  # mantener la condicion heap

    predecesores = {ciud: entries[ciud][2] for ciud in entries}
    costos_desde_fuente = {ciud: entries[ciud][0] for ciud in entries}
    return predecesores, costos_desde_fuente


def bellmanFord(grafo: Ciudades, costos: costos_t, vertice_fuente: str):

    # init
    pesos_desde_fuente = defaultdict(lambda: INF)
    pesos_desde_fuente[vertice_fuente] = 0

    predecesores = defaultdict(lambda: None)
    predecesores[vertice_fuente] = None  # para explicitarlo

    for i in range(1, len(grafo.lista)):
        for u, v in grafo.iterar():
            costo_viejo = pesos_desde_fuente[v]
            costo_nuevo = pesos_desde_fuente[u] + costos[u, v]
            if costo_viejo > costo_nuevo:
                pesos_desde_fuente[v] = costo_nuevo
                predecesores[v] = u

    for u, v in grafo.iterar():
        peso_u, peso_v = pesos_desde_fuente[u], pesos_desde_fuente[v]
        if peso_v > peso_u + costos[u, v]:
            return False, None, None
    return True, predecesores, pesos_desde_fuente


def johnson(grafo: Ciudades, costos: costos_t):
    from copy import deepcopy
    grafo_con_extra_vertice = deepcopy(grafo)
    costos_con_extra_v = deepcopy(costos)
    # podria no hacer una copia y en su lugar agregar lo que
    # necesito a 'grafo', pero como
    # en python no se puede obligar el pasaje de variables
    # por copia, lo hago asi para no generar efectos
    # secundarios.

    extra_vertice = "0"
    # init del extra vertice
    for ciud in grafo_con_extra_vertice.lista:
        costos_con_extra_v[extra_vertice, ciud] = 0

    grafo_con_extra_vertice.adyacencias[extra_vertice] = [
        c for c in grafo_con_extra_vertice.lista]

    grafo_con_extra_vertice.lista.add(extra_vertice)

    # uso de bellman-ford
    sin_ciclos, _, costos_bellmanFord = bellmanFord(
        grafo_con_extra_vertice, costos_con_extra_v, extra_vertice)
    if not sin_ciclos:
        print("el grafo de ciudades contiene un ciclo negativo")
        return None

    # reponderacion con bellman-ford
    costos_reponderados = {}
    for u, v in grafo_con_extra_vertice.iterar():
        costos_reponderados[u, v] = costos_con_extra_v[u, v] \
            + costos_bellmanFord[u] \
            - costos_bellmanFord[v]

    matriz_costos_finales = {}

    # combinacion con dijkstra por cada ciudad
    costos_dijkstra = {}
    for u in grafo.lista:
        _, costos_dijkstra = dijkstra(grafo, costos_reponderados, u)
        for v in grafo.lista:
            matriz_costos_finales[u, v] = costos_dijkstra[v] \
                + costos_bellmanFord[v] \
                - costos_bellmanFord[u]
    
    print("Matriz de costos mínimos para ir de X a Y:")
    print()
    print("     ", end="")
    for u in grafo.lista:
        print(f" {u}  ", end="")
    print()
    for u in grafo.lista:
        print(f" {u}  ", end="")
        for v in grafo.lista:
            print(f"{str(matriz_costos_finales[u, v])} ".rjust(4, " "), end="")
        print()
    return matriz_costos_finales


 


def elegir_ciudad(matriz_costos: Dict, lista_ciudades: Iterable):
    from itertools import product
    costo_tot_por_ciud = DefaultDict(lambda: 0)

    for u, v in product(lista_ciudades, repeat=2):
        costo_tot_por_ciud[u] += matriz_costos[u, v]

    ciud, _ = min(costo_tot_por_ciud.items(), key=lambda x: x[1])
    return ciud


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

    ciudades, costos = parse_file(args.archivo)

    matriz = johnson(ciudades, costos)
    res = elegir_ciudad(matriz, ciudades.lista)
    print(f"la ciudad dónde conviene colocar la fábrica es {res}")
