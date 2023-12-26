'''
© Copyright ArdillaByte Inc. 2023

-----------------------------------------------
Clase con el espacio de estados de rutas.
-----------------------------------------------
'''
import numpy as np
from collections import namedtuple
import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.patches as patches
import copy
from tqdm.auto import tqdm
from typing import List, Dict, Optional, Tuple, Union

from chaparral.modelos.busqueda import ListaPrioritaria, Nodo
from chaparral.modelos.constantes import TIEMPO_DESCARGA


class RutasClusters:
	'''
	Espacio de estados para planear el camino más corto
	de un cluster a otro.
	'''
	def __init__(
				self, 
				cluster_inicial: str,
				cluster_objetivo: str,
				rutas: Dict[str,List],
				coordenadas: Dict[str, Tuple[float,float]],
				tiempo_desplazamiento: Dict[str, float]
			) -> None:
		self.cluster_inicial = cluster_inicial
		self.cluster_objetivo = cluster_objetivo
		self.rutas = rutas
		self.coordenadas = coordenadas
		self.tiempo_desplazamiento = tiempo_desplazamiento
		# Maximum size of frontera
		self.max_size = 1000	
		# Render mode
		self.render_mode = 'rgb_array'

	def _hallar_distancia(self, x, y):
		return np.sqrt((x[0] - y[0])**2 + (x[1] - y[1])**2)
        
	def render(self):
		G = nx.Graph()
		G.add_nodes_from(self.coordenadas.keys())
		list_edges = [[(cluster, x, {'distancia':self.tiempo_desplazamiento[cluster][x]}) for x in self.rutas[cluster]] for cluster in self.rutas.keys()]
		list_edges = [item for sublist in list_edges for item in sublist]
		G.add_edges_from(list_edges, color='red')
		order = {cluster:self.coordenadas[cluster] for cluster in self.coordenadas.keys()}
		options = {
			'node_color': 'green',
			'node_size': 10,
			'verticalalignment':'bottom',
			'edge_color': 'red',
			'width': 0.25,
			'font_size': 10
		}
		fig = plt.figure(figsize=(15,15))
		ax = fig.add_subplot()
		nx.draw_networkx(G, pos=order, font_weight='bold', **options)
		edge_labels = nx.get_edge_attributes(G, 'distancia')
		nx.draw_networkx_edge_labels(G, order, edge_labels)
		ax.axis('off')
		fig.canvas.draw()
		string = fig.canvas.renderer.buffer_rgba()
		array = np.array(string)
		if self.render_mode == 'rgb_array':
			return array
		else:
			plt.show()

	def acciones_aplicables(self, estado):
		# Devuelve una lista de ciudades a las que se puede llegar
		# desde la ciudad descrita en estado
		# Input: estado, nombre de una ciudad
		# Output: lista de ciudades
		return self.rutas[estado]

	def transicion(self, estado, accion):
		# Devuelve la ciudad a la que se va
		# Input: estado, que es una ciudad
		#        accion, que es una ciudad
		# Output: accion, que es una ciudad
		return accion

	def test_objetivo(self, estado):
		# Devuelve True/False dependiendo si el estado
		# resuelve el problema
		# Input: estado, que es una ciudad
		# Output: True/False
		return estado == self.cluster_objetivo

	def costo(self, estado, accion):
		# Devuelve la distancia desde estado hasta accion (que es una ciudad)
		# Input: 
		#        estado, que es una ciudad
		#        accion, que es una ciudad
		# Output: distancia de acuerdo al diccionario rutas más tiempo de descarga
		return self.tiempo_desplazamiento[estado][accion] + TIEMPO_DESCARGA

	def codigo(self, estado):
		return estado

	def nodo_hijo(self, madre, accion):
		# Método para crear un nuevo nodo
		# Input: problema, que es un objeto de clase ocho_reinas
		#        madre, que es un nodo,
		#        accion, que es una acción que da lugar al estado del nuevo nodo
		# Output: nodo
		estado = self.transicion(madre.estado, accion)
		costo_camino = madre.costo_camino + self.costo(madre.estado, accion)
		codigo = self.codigo(estado)
		return Nodo(estado, madre, accion, costo_camino, codigo)

	def dijkstra(self):
		s = self.cluster_inicial
		cod = self.codigo(s)
		nodo = Nodo(s, None, None, 0, cod)
		frontera = ListaPrioritaria()
		frontera.push(nodo, 0)
		explorados = {}
		explorados[cod] = 0
		while not frontera.is_empty():
			nodo = frontera.pop()
			if self.test_objetivo(nodo):
				return nodo
			for a in self.acciones_aplicables(nodo.estado):
				hijo = self.nodo_hijo(nodo, a)
				s = hijo.estado
				cod = hijo.codigo
				c = hijo.costo_camino
				if (cod not in explorados.keys()) or (c < explorados[cod]):
					frontera.push(hijo, c)
					assert(len(frontera) < self.max_size), 'MAX_SIZE superado'
					explorados[cod] = c
		return None

	def A_star(
				self, 
				W:float, 
				verbose:bool=False
			) -> Nodo:
		s = self.cluster_inicial
		v = self.heuristica(s)
		cod = self.codigo(s)
		nodo = Nodo(s, None, None, 0, cod)
		frontera = ListaPrioritaria()
		frontera.push(nodo, v)
		explorados = {}
		explorados[cod] = W * v
		while not frontera.is_empty():
			if verbose:
				print(f'Tamaño frontera:{len(frontera)} --- min:{frontera.pila[0][1]}')
			nodo = frontera.pop()
			if self.test_objetivo(nodo.estado):
				return nodo
			for a in self.acciones_aplicables(nodo.estado):
				hijo = self.nodo_hijo(nodo, a)
				s = hijo.estado
				v = self.heuristica(s)
				cod = hijo.codigo
				c = hijo.costo_camino
				h = W * v + c
				if (cod not in explorados.keys()) or (h < explorados[cod]):
					frontera.push(hijo, h)
					explorados[cod] = h
		return None
	
	def heuristica(self, cluster:str) -> float:
		return self._hallar_distancia(
			self.coordenadas[self.cluster_objetivo], 
			self.coordenadas[cluster]
		)



class TrazadorRuta:
    """Trazador de rutas"""
    def __init__(self, campo):
        self.cluster_inicial = ['bodega_00']
        self.rutas = campo.datos_rutas
        self.coords = campo.coordenadas
        self.clusters = sorted([cluster.nombre for cluster in campo.clusters])
        self.G = None
        self.max_size = 1000

    def render(self, estado):
        """ Creacion y plot del grafo como vertices las localidades y pesos el valor de la distancia entre cada para de localidades """
        self.G = nx.Graph()
        n = len(estado)
        for i in range(n):
            x, y = self.coords[estado[i]]
            self.G.add_node(estado[i], pos = (x,y))
        for i in range(n-1):
            self.G.add_edge(estado[i], estado[i+1], weight = round(self.rutas[estado[i]][estado[i+1]], 2))
        pos = nx.get_node_attributes(self.G, 'pos')
        pesos = nx.get_edge_attributes(self.G,'weight')
        plt.figure(figsize=(12,12))
        nx.draw_networkx(self.G, pos)
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels = pesos)
        plt.show()

    def pintar_camino(self, camino):
        # Input: lista con el camino de los estados
        # Output: plot con la forma de resolver las torres
        for estado in camino:
            clear_output(wait=True)
            self.pintar_estado(estado)
            plt.show()
            sleep(.5)

    def acciones_aplicables(self, estado):
        """ Retorna las posibles acciones dado el estado
            Input: estado (localidad)
            Output: Lista con las localidades no visitadas
        """
        return [x for x in self.clusters if x not in estado]

    def transicion(self, estado, accion):
        """ Retorna la lista actualizada con la accion realizada
            Input: estado (lista con el camino en el momento)
                   accion (desplazamiento)
            Output: Copia de la lista estado actualizada """
        lista = copy.deepcopy(estado)
        lista.append(accion)
        return lista

    def test_objetivo(self, estado):
        """ Verifica si ya fueron visitadas todas las localidades
            Input: estado (lista con el camino)
            Output: Boolean """
        return set(self.clusters) == set(estado)

    def codigo(self, estado):
        """ Actualiza el codigo
            Input: estado (lista con el camino)
            Output: cadena """
        cad = ""
        for i in estado:
            cad = cad + " - " + i
        return cad

    def costo(self, estado1, estado2):
        """ Peso entre el estado y la accion
            Input: estado (camino actual)
                   accion (desplazamiento)
            Output: Int """
        loc = self.rutas[estado1[-1]]
        try:
            costo_ = loc[estado2]
            return costo_
        except Exception as e:
            print(f'Error al buscar costo ({e})')
            print(f'{estado1[-1]} --> {estado2}')
            raise Exception()

    def dijkstra(self):
        s = self.cluster_inicial
        cod = self.codigo(s)
        nodo = Nodo(s, None, None, 0, cod)
        frontera = ListaPrioritaria(max_size=self.max_size)
        frontera.push(nodo, 0)
        explorados = {}
        explorados[cod] = 0
        pbar = tqdm(total=len(self.clusters))
        contador_estados_recorridos = 1
        while not frontera.is_empty():
            nodo = frontera.pop()
            diferencia = len(set(nodo.estado)) - contador_estados_recorridos
            if  diferencia > 0:
                pbar.update(diferencia)
                contador_estados_recorridos += diferencia 
            elif diferencia < 0:
                pbar.close()
                pbar = tqdm(total=len(self.clusters))
                pbar.update(len(set(nodo.estado)))
                contador_estados_recorridos = len(set(nodo.estado))
            if self.test_objetivo(nodo.estado):
                pbar.close()
                return nodo
            for a in self.acciones_aplicables(nodo.estado):
                hijo = self.nodo_hijo(nodo, a)
                s = hijo.estado
                cod = hijo.codigo
                c = hijo.costo_camino
                if (cod not in explorados.keys()) or (c < explorados[cod]):
                    frontera.push(hijo, c)
                    assert(len(frontera) < self.max_size + 1), 'MAX_SIZE superado'
                    explorados[cod] = c
        pbar.close()
        return None

    def A_star(
                self, 
                W:float, 
                verbose:bool=False
            ) -> Nodo:
        s = self.cluster_inicial
        v = self.heuristica(s)
        cod = self.codigo(s)
        nodo = Nodo(s, None, None, 0, cod)
        frontera = ListaPrioritaria(max_size=self.max_size)
        frontera.push(nodo, v)
        explorados = {}
        explorados[cod] = W * v
        pbar = tqdm(
            total=len(self.clusters), 
            desc='%clusters visitados',
            leave=False
        )
        contador_estados_recorridos = 1
        pbar.update(contador_estados_recorridos)
        while not frontera.is_empty():
            nodo = frontera.pop()
            diferencia = len(set(nodo.estado)) - contador_estados_recorridos
            if  diferencia > 0:
                pbar.update(diferencia)
                contador_estados_recorridos += diferencia 
            if self.test_objetivo(nodo.estado):
                return nodo
            for a in self.acciones_aplicables(nodo.estado):
                hijo = self.nodo_hijo(nodo, a)
                s = hijo.estado
                v = self.heuristica(s)
                cod = hijo.codigo
                c = hijo.costo_camino
                h = W * v + c
                if (cod not in explorados.keys()) or (h < explorados[cod]):
                    frontera.push(hijo, h)
                    explorados[cod] = h
        return None
	
    def heuristica(self, clusters:str) -> float:
        if len(clusters) < 2:
            return 0
        objetivo = clusters[-1]
        anterior = clusters[-2]
        return self._hallar_distancia(
			self.coords[objetivo], 
			self.coords[anterior]
        )

    def _hallar_distancia(self, x, y):
        return np.sqrt((x[0] - y[0])**2 + (x[1] - y[1])**2)

    def nodo_hijo(self, madre, accion):
        # Método para crear un nuevo nodo
        # Input: problema, que es un objeto de clase ocho_reinas
        #        madre, que es un nodo,
        #        accion, que es una acción que da lugar al estado del nuevo nodo
        # Output: nodo
        estado = self.transicion(madre.estado, accion)
        costo_camino = madre.costo_camino + self.costo(madre.estado, accion)
        codigo = self.codigo(estado)
        return Nodo(estado, madre, accion, costo_camino, codigo)