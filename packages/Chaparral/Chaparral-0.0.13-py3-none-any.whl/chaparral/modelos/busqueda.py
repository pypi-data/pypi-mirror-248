import numpy as np
from collections import namedtuple
from typing import Optional

Tupla = namedtuple('Tupla', ['elemento', 'valor'])

class ListaPrioritaria:
	"""
	Estructura de datos para mantener una pila
	ordenada con base en un valor que tiene cada
	elemento.
	"""
   
	def __init__(self, max_size:Optional[int]=np.inf):
		self.pila = []
		self._index = 0
		self.max_size = max_size
				
	def __len__(self):
		return len(self.pila)

	def __iter__(self):
		return self

	def __next__(self):
		if self._index < len(self.pila):
			item = self.pila[self._index]
			self._index += 1
			return item[0]
		else:
			raise StopIteration
			
	def push(self, elemento, valor):
		tupla = Tupla(elemento, valor)
		self.pila.append(tupla)
		self.pila.sort(key=lambda x: x[1])
		if len(self.pila) > self.max_size:
			self.pila = self.pila[:self.max_size]
			
	def pop(self, with_value=False):
		if with_value:
			return self.pila.pop(0)
		else:
			return self.pila.pop(0)[0]

	def is_empty(self):
		return len(self.pila) == 0

	def __len__(self):
		return len(self.pila)

	def __str__(self):
		cadena = '['
		inicial = True
		for elemento, valor in self.pila:
			if inicial:
				cadena += '(' + str(elemento) + ',' + str(valor) + ')'
				inicial = False
			else:
				cadena += ', (' + str(elemento) + ',' + str(valor) + ')'
		return cadena + ']'
	

class Nodo:
	"""Clase para crear los nodos del árbol de búsqueda"""

	def __init__(self, estado, madre, accion, costo_camino, codigo):
		self.estado = estado
		self.madre = madre
		self.accion = accion
		self.costo_camino = costo_camino
		self.codigo = codigo

	def solucion(self):
		if self.madre == None:
			return []
		else:
			return self.solucion(self.madre) + [self.accion]

	def depth(self):
		if self.madre == None:
			return 0
		else:
			return self.depth(self.madre) + 1

	def camino_codigos(self):
		if self.madre == None:
			return [self.codigo]
		else:
			return self.camino_codigos(self.madre) + [self.codigo]

	def is_cycle(self):
		codigos = self.camino_codigos(self)
		return len(set(codigos)) != len(codigos)

