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
import pandas as pd

from chaparral.modelos.constantes import NIVEL_MAXIMO_BULKDRUM


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
	
	def a_tensor(self, en_camion=False) -> torch.tensor:
		if en_camion or self.velocidad_consumo is None:
			return torch.tensor([self.nivel_actual], dtype=torch.float32)			
		else:
			return torch.tensor([self.nivel_actual, self.velocidad_consumo], dtype=torch.float32)
	

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
	'''
	def __init__(
				self, 
				nombre:str, 
				pozos:List[str],
				coordenadas:Tuple, 
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
		- tiempo de tránsito de un camión en kilómetros por unidad temporal
	'''
	def __init__(
				self, 
				inicial:Cluster, 
				objetivo:Cluster,
				tiempo:float,
			) -> None:
		self.inicial = inicial
		self.objetivo = objetivo
		self.nombre = f'{self.inicial.nombre} <-> {self.objetivo.nombre}'
		self.tiempo = tiempo
		self.porcentaje_recorrido = 0

	def __str__(self) -> str:
		cadena = f'Ruta {self.nombre} por {round(self.longitud,2)}km a {self.velocidad_promedio}km/hora'
		cadena += '\n\t' + f'El camion ha recorrido el {round(self.porcentaje_recorrido, 2)}%'
		return cadena

	def actualizar(self, unidades_temporales:float) -> None:
		'''
		Mueve el camión por la ruta de acuerdo a la
		cantidad de unidades_temporales dada 
		'''
		tiempo_faltante = self.obtener_unidades_temporales_faltantes()
		if  unidades_temporales >= tiempo_faltante:
			# El camión llega al final de la ruta
			self.porcentaje_recorrido = 100
		else:
			tiempo_recorrido = self.tiempo - tiempo_faltante
			self.porcentaje_recorrido = (tiempo_recorrido + unidades_temporales) / self.tiempo * 100

	def fin_recorrido(self) -> bool:
		# Determina si el camino fue recorrido
		return self.porcentaje_recorrido == 100
	
	def obtener_unidades_temporales_faltantes(self) -> float:
		'''
		Determina cuántas unidades temporales faltan para terminar la ruta
		'''
		tiempo_faltante = (100 - self.porcentaje_recorrido) / 100 * self.tiempo
		return tiempo_faltante


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
				tiempo: float
			) -> None:
		super().__init__(inicial, objetivo, tiempo)

	def __str__(self) -> str:
		return f'Camión estacionado en {self.inicial.nombre}'
	
	def actualizar(self, unidades_temporales: float) -> None:
		return None
	
	def fin_recorrido(self) -> bool:
		return True
	
	def obtener_unidades_temporales_faltantes(self) -> float:
		return np.Inf
	

class BulkDrum:
	'''
	Objeto bulkdrum --- contenedor de químico en el camión
	'''
	def __init__(
				self, 
				nombre:str,
				nombre_quimico:str,
				nivel_actual:float,
			) -> None:
		self.nombre = nombre
		self.quimico = Quimico(
			nombre=nombre_quimico,
			unidades='Gl'
		)
		self.nivel_actual = nivel_actual
		self.nivel_inicial = nivel_actual
		self.nivel_maximo = NIVEL_MAXIMO_BULKDRUM
	
	def __str__(self) -> str:
		''' Genera una cadena en formato html con el nombre del químico, su nivel y velocidad'''
		cadena = f'<td> {self.quimico.nombre} </td> '
		cadena += f'<td> {round(self.nivel_actual, 2)} </td> '
		return cadena

	def llenar(self, cantidad_a_cargar:float) -> None:
		"""Intenta llenar el blulkdrum con la cantidad dada"""
		if self.nivel_actual + cantidad_a_cargar <= self.nivel_maximo:
			self.nivel_actual += cantidad_a_cargar
		else:
			raise Exception(f'Error de llenado bulkdrum {self.nombre} a nivel {round(self.nivel_actual, 2)}. Cantidad {round(cantidad_a_cargar, 2)} supera límite máximo')

	def llenar_suavemente(
				self, 
				cantidad_a_cargar:float
			) -> float:
		"""Llena el bulkdrum y devuelve la cantidad que sobra"""
		if self.nivel_actual + cantidad_a_cargar <= self.nivel_maximo:
			self.nivel_actual += cantidad_a_cargar
			return 0
		else:
			cantidad_faltante = self.nivel_actual + cantidad_a_cargar - self.nivel_maximo
			self.nivel_actual = self.nivel_maximo
			return cantidad_faltante

	def descargar(
				self, 
				cantidad_a_descargar:float
			) -> float:
		"""Descarga el bulkdrum y devuelve la cantidad que falta por descargar"""
		if self.nivel_actual > cantidad_a_descargar:
			self.nivel_actual -= cantidad_a_descargar
			return 0
		else:
			aux = self.nivel_actual
			self.nivel_actual = 0
			return cantidad_a_descargar - aux

	def con_capacidad(self) -> bool:
		return self.nivel_actual < self.nivel_maximo

	def a_tensor(self) -> torch.tensor:
		return torch.tensor([self.nivel_actual], dtype=torch.float32)			


class Camion2:
	'''
	Objeto camion
	
	Atributos:
		- nombre
		- lista de bulkdrums
		- ubicación
		- ruta
		- nombres clusters
		- nombres quimicos
	'''
	def __init__(
				self, 
				nombre:str, 
				num_bulkdrums:int,
				ubicacion:int,
				ruta:Union[None, Ruta],
				nombres_clusters:List[str],
				nombres_quimicos:List[str]
			) -> None:
		self.nombre = nombre
		self.num_bulkdrums = num_bulkdrums
		self.bulkdrums = [None for _ in range(num_bulkdrums)]
		self.ubicacion = ubicacion
		self.ruta = ruta
		self.nombres_clusters = nombres_clusters
		self.num_clusters = len(nombres_clusters)
		self.nombres_quimicos = nombres_quimicos
		self.num_quimicos = len(self.nombres_quimicos)
		self.primer_bulkdrum_vacio = 0
		self.quimico_a_bulkdrum = {quimico:list() for quimico in self.nombres_quimicos}
		self.nivel_maximo = NIVEL_MAXIMO_BULKDRUM
		self.debug = False

	def __str__(self) -> str:
		cadena = '<tr>\n\t<td>Camion</td> <td>Ubicado en</td> <td>Químico</td> <td>Carga</td>\n</tr>'
		cadena += f'\n<tr>\n\t<td> {self.nombre} </td> <td>{self.nombres_clusters[self.ubicacion]}</td> '
		inicial = True
		for bulkdrum in self.bulkdrums:
			if inicial:
				cadena += str(bulkdrum) + '\n</tr> '	
				inicial = False
			else:
				cadena += ' \n<tr>\n\t<td>&nbsp;</td> <td>&nbsp;</td> ' + str(bulkdrum) + '\n</tr>'	
		return cadena

	def camion_a_tensor(self) -> torch.tensor:
		tensores = [bulkdrum.a_tensor() for bulkdrum in self.bulkdrums]
		tensor_ubicacion = torch.tensor(self.ubicacion)
		tensores += [F.one_hot(tensor_ubicacion, num_classes=self.num_clusters)]
		return torch.cat(tensores)
	
	def cargar(
				self,
				nombre_quimico:str,
				cantidad_a_cargar:float
			) -> None:
		# Determina si hay bulkdrums con el químico a bordo
		indices = self.quimico_a_bulkdrum[nombre_quimico]
		if self.debug:
			print(f'Bulkdrums donde está el químico {nombre_quimico}: {indices}')
		# Si sí, comienza a cargar y llenar los bulkdrums
		if len(indices) > 0:
			for indice in indices:
				if cantidad_a_cargar == 0:
					return None
				bulkdrum = self.bulkdrums[indice]
				if self.debug:
					print(f'\tBulkdrum {bulkdrum.nombre} tiene {bulkdrum.nivel_actual}')
				cantidad_a_cargar = bulkdrum.llenar_suavemente(cantidad_a_cargar)
				if self.debug:
					print(f'\t\tBulkdrum {bulkdrum.nombre} quedó con {bulkdrum.nivel_actual} y faltan {cantidad_a_cargar}')
		while cantidad_a_cargar > 0:
			# Aún hay que cargar químico
			if self.debug:
				print(f'Aún hay que cargar más químico {nombre_quimico}')
			if self.primer_bulkdrum_vacio < self.num_bulkdrums:
				self.quimico_a_bulkdrum[nombre_quimico].append(self.primer_bulkdrum_vacio)
				bulkdrum = BulkDrum(
					nombre=f'bulkdrum{self.primer_bulkdrum_vacio}',
					nombre_quimico=nombre_quimico,
					nivel_actual=0
				)
				cantidad_a_cargar = bulkdrum.llenar_suavemente(cantidad_a_cargar)
				self.bulkdrums[self.primer_bulkdrum_vacio] = bulkdrum
				self.primer_bulkdrum_vacio += 1
				if self.debug:
					print(bulkdrum)
			else:
				raise Exception('Error de capacidad de camion.')
		return None

	def descargar(
				self,
				nombre_quimico:str,
				cantidad_a_descargar:float
			) -> None:
		indices = self.quimico_a_bulkdrum[nombre_quimico]
		if len(indices) == 0:
			raise Exception(f'Error: Camión no lleva el químico {nombre_quimico}')
		cantidad_quimico = sum([
			bulkdrum.nivel_actual for bulkdrum in self.bulkdrums if bulkdrum.nombre_quimico == nombre_quimico
		])
		if cantidad_a_descargar > cantidad_quimico:
			raise Exception(f'Error: cantidad de {nombre_quimico} insuficiente en camión.')
		for indice in indices:
			if cantidad_a_descargar == 0:
				return None
			bulkdrum = self.bulkdrums[indice]
			cantidad_a_descargar = bulkdrum.descargar(cantidad_a_descargar)

	def a_pandas(self):
		quimicos = list()
		cantidades = list()
		for bulkdrum in self.bulkdrums:
			quimicos.append(bulkdrum.quimico.nombre)
			cantidades.append(bulkdrum.nivel_actual)
		return pd.DataFrame({'quimico':quimicos, 'cantidades':cantidades})


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
				ruta:Union[None, Ruta],
				nombres_clusters:List[str]
			) -> None:
		self.nombre = nombre
		self.capacidad = capacidad
		self.carga_quimicos = carga_quimicos
		self.num_quimicos = len(self.carga_quimicos)
		self.ubicacion = ubicacion
		self.ruta = ruta
		self.nombres_clusters = nombres_clusters

	def __str__(self) -> str:
		cadena = '<tr>\n\t<td>Camion</td> <td>Ubicado en</td> <td>Químico</td> <td>Carga</td>\n</tr>'
		cadena += f'\n<tr>\n\t<td> {self.nombre} </td> <td>{self.nombres_clusters[self.ubicacion]}</td> '
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
		tensores = [quimico.a_tensor(en_camion=True) for quimico in self.carga_quimicos]
		tensor_ubicacion = torch.tensor(self.ubicacion)
		tensores += [F.one_hot(tensor_ubicacion, num_classes=num_clusters)]
		return torch.cat(tensores)