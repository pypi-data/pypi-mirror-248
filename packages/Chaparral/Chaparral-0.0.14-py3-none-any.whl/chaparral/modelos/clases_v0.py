'''
© Copyright ArdillaByte Inc. 2023

-----------------------------------------------
Class to XXXX.
-----------------------------------------------
'''
import numpy as np
from typing import List, Dict, Optional, Tuple, Union
from copy import deepcopy
import torch
import torch.nn.functional as F

from chaparral.modelos.constantes import NOMBRES_CLUSTERS


def a_tabla(cadena):
    c = '<table>\n<tbody>\n'
    c += cadena
    c += '</tbody>\n</table>'
    return c

class Quimico:
	'''
	Objeto quimico

	Atributos:
		- nombre
		- unidades de medida
	'''
	def __init__(
				self, 
				nombre:str, 
				unidades:str
			) -> None:
		self.nombre = nombre
		self.unidades = unidades

	def __str__(self) -> str:
		return f'{self.nombre} (unidades:{self.unidades})'

	def in_carga(
				self, 
				carga_quimicos:List[any]
			) -> Union[None, int]:
		'''Determina si self está en una lista y en caso positivo devuelve el índice en la lista'''
		nombres_quimicos = [quimico.nombre for quimico in carga_quimicos]
		if self.nombre in nombres_quimicos:
			return nombres_quimicos.index(self.nombre)
		else:
			return None


class QuimicoEn(Quimico):

	def __init__(
				self, 
				nombre: str, 
				unidades: str,
				nivel_actual: float,
				velocidad_consumo: float
			) -> None:
		super().__init__(nombre, unidades)
		self.nivel_actual = nivel_actual
		self.nivel_inicial = nivel_actual
		self.velocidad_consumo = velocidad_consumo

	def __str__(self) -> str:
		''' Genera una cadena en formato html con el nombre del químico, su nivel y velocidad'''
		cadena = f'<td> {self.nombre} </td> '
		cadena += f'<td> {round(self.nivel_actual, 2)} </td> '
		if self.velocidad_consumo is not None:
			cadena += f'<td> {round(self.velocidad_consumo, 2)} </td>'
		return cadena

	def actualizar(
				self, 
				unidades_temporales:float
			) -> None:
		self.nivel_actual -= self.velocidad_consumo * unidades_temporales
		self.nivel_actual = max(0, self.nivel_actual)
	
	def a_tensor(self) -> torch.tensor:
		if self.velocidad_consumo is not None:
			return torch.tensor([self.nivel_actual, self.velocidad_consumo], dtype=torch.float32)
		else:
			return torch.tensor([self.nivel_actual], dtype=torch.float32)			


class Pozo:
	'''
	Objeto pozo

	Atributos:
		- nombre
		- si está activo o no
		- lista de químicos en pozo
	'''
	def __init__(
				self,
				nombre:str,
				quimicos:List[QuimicoEn]
			) -> None:
		self.nombre = nombre
		self.quimicos = quimicos	
		self.num_quimicos = len(quimicos)

	def __str__(self) -> str:
		cadena = f'\n<tr>\n\t<td> {self.nombre} </td> '
		inicial = True
		for quimico in self.quimicos:
			if inicial:
				cadena += str(quimico) + '\n</tr> '	
				inicial = False
			else:
				cadena += ' \n<tr>\n\t<td>&nbsp;</td> ' + str(quimico) + '\n</tr>'	
		return cadena

	def actualizar(
				self,
				unidades_temporales:float
			) -> None:
		for quimico in self.quimicos:
			quimico.actualizar(unidades_temporales)

	def a_tensor(self) -> torch.tensor:
		tensores = [quimico.a_tensor() for quimico in self.quimicos]
		return torch.cat(tensores)


class Cluster:
	'''
	Objeto cluster

	Atributos:
		- nombre
		- lista de pozos
		- coordenadas del cluster
		# - lista de clusters vecinos
	'''
	def __init__(
				self, 
				nombre:str, 
				pozos:List[str],
				coordenadas:Tuple, 
				# vecinos:List[str]
			) -> None:
		self.nombre = nombre
		# -----------------------------------
		# Los pozos del cluster
		# -----------------------------------
		self.pozos = pozos
		self.num_pozos = len(self.pozos)
		# -----------------------------------
		# Atributos geográficos
		# -----------------------------------
		self.coordenadas = coordenadas # Coordenadas geográficas del cluster
		# self.vecinos = vecinos # Rutas que conectan el cluster con otros clusters/bodega
		
	def actualizar(
			self, 
			unidades_temporales:int
			) -> None:
		'''
		Actualiza el cluster simulando que transcurren las unidades temporales dadas

		Input:
			- unidades_temporales (int), la cantidad de unidades de tiempo que transcurren.
		'''
		for pozo in self.pozos:
			pozo.actualizar(unidades_temporales)
	
	def __str__(self) -> str:
		'''Genera una cadena en formato html con el nombre de cada químico y su cantidad actual'''
		cadena = '<tr>\n\t<td>Cluster</td> \n</tr>'
		cadena += f'\n<tr>\n\t<td> {self.nombre} </td> '
		inicial = True
		for pozo in self.pozos:
			if inicial:
				str_pozo = '<tr>\n\t<td>Pozo</td> <td>Químico</td> <td>Cantidad</td> <td>Vel.Cons</td> \n</tr>' + str(pozo)
				cadena += ' <td> ' + a_tabla(str_pozo) + ' </td> \n</tr> '	
				inicial = False
			else:
				str_pozo = '<tr>\n\t<td>Pozo</td> <td>Químico</td> <td>Cantidad</td> <td>Vel.Cons</td> \n</tr>' + str(pozo)
				cadena += ' <tr>\n\t<td>&nbsp;</td> ' + ' <td> ' + a_tabla(str_pozo) + ' </td> \n</tr> '	
		return a_tabla(cadena)
	
	def cluster_a_tensor(self) -> torch.tensor:
		'''Genera un tensor plano donde, por cada químico, incluye 
			el nivel actual,
			la velocidad de consumo.
		'''
		tensores = [pozo.a_tensor() for pozo in self.pozos]
		assert(len(tensores) > 0), f'¡Error!: ¡Cluster {self.nombre} no tiene pozos!'
		return torch.cat(tensores)


class Ruta:
	'''
	Objeto que representa la ruta que está siguiendo 
	un camión para ir de un cluster a otro.

	Atributos:
		- nombre del cluster inicial
		- nombre del cluster objetivo
		- longitud del camino en kilómetros
		- velocidad promedio de tránsito de un camión en kilómetros por unidad temporal
	'''
	def __init__(
				self, 
				inicial:Cluster, 
				objetivo:Cluster,
				longitud:float,
				velocidad_promedio:float,
			) -> None:
		self.inicial = inicial
		self.objetivo = objetivo
		self.nombre = f'{self.inicial.nombre} <-> {self.objetivo.nombre}'
		self.longitud = longitud
		self.velocidad_promedio = velocidad_promedio
		self.porcentaje_recorrido = 0

	def __str__(self) -> str:
		cadena = f'Ruta {self.nombre} por {round(self.longitud,2)}km a {self.velocidad_promedio}km/hora'
		cadena += '\n\t' + f'El camion ha recorrido el {round(self.porcentaje_recorrido, 2)}%'
		return cadena

	def actualizar(self, unidades_temporales:float) -> None:
		'''
		Mueve el camión por la ruta de acuerdo a la
		velocidad promedio de la ruta por la cantidad
		de unidades_temporales dada 
		'''
		# Encuentra la distancia recorrida después de unidades temporales
		distancia_recorrida = self.velocidad_promedio * unidades_temporales
		longitud_faltante =  self.longitud * (100 - self.porcentaje_recorrido) / 100
		if  distancia_recorrida >= longitud_faltante:
			# El camión llega al final de la ruta
			self.porcentaje_recorrido = 100
		else:
			self.porcentaje_recorrido = (1 - (longitud_faltante - distancia_recorrida) / self.longitud) * 100

	def fin_recorrido(self) -> bool:
		# Determina si el camino fue recorrido
		return self.porcentaje_recorrido == 100
	
	def obtener_unidades_temporales_faltantes(self) -> float:
		'''
		Determina cuántas unidades temporales faltan para terminar la ruta
		de acuerdo a la velocidad promedio del camino y la longitud faltante
		'''
		longitud_faltante =  self.longitud * (100 - self.porcentaje_recorrido) / 100
		return longitud_faltante / self.velocidad_promedio


class PseudoRutaCamionEstacionario(Ruta):
	'''
	Clase que simula una ruta pero establece
	los métodos de ruta para cuando el camión
	está estacionario.
	'''
	def __init__(
				self, 
				inicial: Cluster, 
				objetivo: Cluster, 
				longitud: float, 
				velocidad_promedio: 
				float
			) -> None:
		super().__init__(inicial, objetivo, longitud, velocidad_promedio)

	def __str__(self) -> str:
		return f'Camión estacionado en {self.inicial.nombre}'
	
	def actualizar(self, unidades_temporales: float) -> None:
		return None
	
	def fin_recorrido(self) -> bool:
		return True
	
	def obtener_unidades_temporales_faltantes(self) -> float:
		return np.Inf
	

class Camion:
	'''
	Objeto camion
	
	Atributos:
		- nombre
		- capacidad de carga
		- lista de químicos que carga
		- ubicación
	'''
	def __init__(
				self, 
				nombre:str, 
				capacidad:float, 
				carga_quimicos:List[QuimicoEn],
				ubicacion:int,
				ruta:Union[None, Ruta]
			) -> None:
		self.nombre = nombre
		self.capacidad = capacidad
		self.carga_quimicos = carga_quimicos
		self.num_quimicos = len(self.carga_quimicos)
		self.ubicacion = ubicacion
		self.ruta = None

	def __str__(self) -> str:
		cadena = '<tr>\n\t<td>Camion</td> <td>Ubicado en</td> <td>Químico</td> <td>Carga</td>\n</tr>'
		cadena += f'\n<tr>\n\t<td> {self.nombre} </td> <td>{NOMBRES_CLUSTERS[self.ubicacion]}</td> '
		inicial = True
		for quimico in self.carga_quimicos:
			if inicial:
				cadena += str(quimico) + '\n</tr> '	
				inicial = False
			else:
				cadena += ' \n<tr>\n\t<td>&nbsp;</td> <td>&nbsp;</td> ' + str(quimico) + '\n</tr>'	
		return cadena

	def camion_a_tensor(
				self, 
				num_clusters:Optional[int]
			) -> torch.tensor:
		tensores = [quimico.a_tensor() for quimico in self.carga_quimicos]
		tensor_ubicacion = torch.tensor(self.ubicacion)
		tensores += [F.one_hot(tensor_ubicacion, num_classes=num_clusters)]
		return torch.cat(tensores)