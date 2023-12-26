'''
© Copyright ArdillaByte Inc. 2023

-----------------------------------------------
Clase para correr el campo de pozos con sus
clusters y camiones como un espacio de estados.
-----------------------------------------------
'''
from chaparral.modelos.entorno import CampoPozos
from chaparral.modelos.clases import Cluster, Camion, Ruta, PseudoRutaCamionEstacionario, Quimico
from chaparral.modelos.constantes import DATOS_RUTAS
from chaparral.modelos.busqueda import Nodo, solucion
from typing import List, Dict, Optional, Tuple, Union
import torch
import warnings 
import numpy as np
from itertools import product
from copy import deepcopy

class EspacioEstados :
	"""Crea el campo de pozos como un espacio de estados"""
	def __init__(self, campo:CampoPozos):
		self.campo = campo
		self.estado_inicial = deepcopy(campo.obtener_estado())

	def acciones_aplicables(
				self, 
				estado:torch.tensor
			) -> List[str]:
		'''
		Devuelve la lista de clusters accessibles
		desde el cluster en que está el camión.
		Input: estado ///// NO SE USA, PERO LO REQUIERE EL METODO DE BUSQUEDA
		Output: lista de acciones correspondientes a las
				combinaciones de clusters accesibles desde 
		 		el lugar donde está cada camión.
		'''
		# Actualiza atributos de acuerdo al estado recibido
		info_estado = self._tensor_a_atributos(estado)
		self._actualiza_desde_info(info_estado)
		# Encontramos los índices de los clusters donde están los camiones
		lista_indices_clusters = [self.campo.dict_clusters[l] for l in self.campo.loc_camiones]
		# Encontramos los clusters veciones de cada locación
		lista_clusters_vecinos = [self.campo.clusters[indice_cluster].vecinos for indice_cluster in lista_indices_clusters]
		lista_clusters_vecinos = [[self.campo.dict_clusters[cluster] for cluster in vecinos] for vecinos in lista_clusters_vecinos]
		# Encontramos las combinaciones posibles
		combinaciones_movimientos = product(*lista_clusters_vecinos)
		combinaciones_movimientos = [list(comb) for comb in combinaciones_movimientos]
		# Encontramos el índice de cada combinación
		lista_acciones = [self.campo.movimientos_a_accion(lista_movimientos) for lista_movimientos in combinaciones_movimientos]
		return lista_acciones

	def transicion(
				self, 
				estado:torch.tensor, 
				accion:int
			) -> torch.tensor:
		'''
		Devuelve el estado resultado de realizar la acción
		en el estado dado
		Input: estado, tensor
		       accion, que es una ciudad
		Output: estado, tensor
		'''
		# Actualiza atributos de acuerdo al estado recibido
		info_estado = self._tensor_a_atributos(estado)
		self._actualiza_desde_info(info_estado)
		# Actualiza bookkeeping de localización de camiones
		locaciones_antes = self.campo.loc_camiones.copy()
		# Hace el step de acuerdo a la acción
		nuevo_estado, recompensa, done = self.campo.step(accion)
		info_nuevo_estado = self._tensor_a_atributos(nuevo_estado)
		# Actualiza bookkeeping de localización de camiones
		locaciones_despues = self.campo.loc_camiones.copy()
		distancias = self._obtiene_distancias_recorridas(
			locaciones_antes=locaciones_antes, 
			locaciones_despues=locaciones_despues,
			unidades_temporales=self.campo._unidades_temporales
		)
		# Actualizamos bookkeeping
		self._check_estado = str(estado)
		self._fake_costo = sum(distancias)
		self._fake_test_objetivo = done
		return nuevo_estado
	
	def _tensor_a_atributos(
				self, 
				estado:torch.tensor
			) -> Dict[str, Dict[str,any]]:
		'''
		Devuelve una lista con los atributos del entorno
		a partir de su representación tensorial.
		'''
		# Vemos el tensor como lista
		estado_como_lista = estado.tolist()
		# Inicializamos registros
		valores_clusters = {cluster.nombre:list() for cluster in self.campo.clusters}
		valores_camiones = {camion.nombre:list() for camion in self.campo.camiones}
		indice_inicial = 0
		#-----------------------------------------------
		# 1. Encontramos la información de cada cluster
		#-----------------------------------------------
		for i, cluster in enumerate(self.campo.clusters):
			# Recorre cada cluster
			# Cada cluster está representado por dos valores para cada químico (cantidad, velocidad)
			# y un valor booleano de si está activo o no
			indice_final = (i + 1) * (2 * len(cluster.quimicos) + 1) 
			lista_estado_cluster = estado_como_lista[indice_inicial:indice_final]
			cantidades, velocidades, activo = self._encuentra_info_cluster(
				lista_estado_cluster,
				cluster.quimicos
			)
			# Guardamos toda la información del cluster
			valores_clusters[cluster.nombre] = {
				'cantidades':cantidades,
				'velocidades':velocidades,
				'activo':activo 
			}
			indice_inicial = indice_final
		#-----------------------------------------------
		# 2. Encontramos la información de los camiones
		#-----------------------------------------------
		for i, camion in enumerate(self.campo.camiones):
			# Recorre cada camion
			# Cada camión está representado por la carga de cada químico y un one-hot de los clusters
			indice_final += camion.num_quimicos + self.campo.num_clusters
			lista_estado_camion = estado_como_lista[indice_inicial:indice_final]
			carga, nombre_cluster = self._encuentra_info_camion(
				lista_estado_camion,
				camion.num_quimicos
			)
			# Guardamos la información del camion
			valores_camiones[camion.nombre] = {
				'carga':carga,
				'ubicacion':nombre_cluster
			}
			indice_inicial = indice_final
		return {'clusters':valores_clusters, 'camiones':valores_camiones}

	def _encuentra_info_cluster(
			self,
			lista_estado_cluster:List[float],
			quimicos:List[Quimico]
		) -> Tuple[List[float], List[float], bool]:
		'''Encuentra la información del cluster en la lista proveniente del tensor'''
		cantidades = list()
		velocidades = list()
		for j, quimico in enumerate(quimicos):
			# Recorremos cada químico en el cluster
			# El primer argumento del químico es su cantidad
			cantidades.append(lista_estado_cluster[j])
			# El segundo argumento es su velocidad de consumo
			velocidades.append(lista_estado_cluster[j + 1])
		# El argumento final es si el pozo está activo o no
		activo = lista_estado_cluster[-1]
		return cantidades, velocidades, activo
	
	def _encuentra_info_camion(
			self,
			lista_estado_camion:List[float],
			num_quimicos:int
		) -> Tuple[float, str]:
		'''Encuentra la información del camión en la lista proveniente del tensor'''
		carga = lista_estado_camion[:num_quimicos]
		indice_cluster = np.argmax(lista_estado_camion[num_quimicos:])
		nombre_cluster = self.campo.clusters[indice_cluster].nombre
		return carga, nombre_cluster
	
	def _actualiza_desde_info(
			self,
			info_estado:Tuple[Dict, Dict]
		) -> None:
		"""Actualiza los atributos del entorno de acuerdo a info"""
		for cluster in self.campo.clusters:
			cluster.niveles_actuales = info_estado['clusters'][cluster.nombre]['cantidades']
		loc_camiones = list()
		for camion in self.campo.camiones:
			camion.carga_cantidades = info_estado['camiones'][camion.nombre]['carga']
			loc_camiones.append(info_estado['camiones'][camion.nombre]['ubicacion'])
		self.campo.loc_camiones = loc_camiones

	def _obtiene_distancias_recorridas(
				self,
				locaciones_antes:List[int], 
				locaciones_despues:List[int],
				unidades_temporales:float
			) -> List[float]:
		"""Encuentra las distancias recorridas por los camiones"""
		nombres_rutas = zip(locaciones_antes, locaciones_despues)
		nombres_rutas = [f'{par[0]} <-> {par[1]}' for par in nombres_rutas]
		velocidades = [DATOS_RUTAS[ruta]['velocidad_promedio'] for ruta in nombres_rutas]
		distancias = [velocidad * unidades_temporales for velocidad in velocidades]
		return distancias

	def test_objetivo(self, nodo:Nodo):
		# Devuelve True/False dependiendo si el estado
		# resuelve el problema
		# Input: estado, que es una ciudad
		# Output: True/False
		# Actualiza atributos de acuerdo al estado recibido
		estado = nodo.estado
		info_estado = self._tensor_a_atributos(estado)
		self._actualiza_desde_info(info_estado)
		primer_check = not self.campo.comienzo
		segundo_check = np.all([l == 'bodega_00' for l in self.campo.loc_camiones])
		camino = solucion(nodo)
		tercer_check = np.all([cluster in camino for cluster in list(range(self.campo.num_clusters))])
		if np.all([primer_check, segundo_check, tercer_check]):
			return True
		return False

	def costo(self, estado, accion):
		# Devuelve la distancia desde estado hasta accion (que es una ciudad)
		# Input: 
		#        estado, que es una ciudad
		#        accion, que es una ciudad
		# Output: distancia de acuerdo al diccionario rutas
		try:
			if str(estado) == self._check_estado:
				return self._fake_costo
		except:
			warnings.warn(f'costo() requiere haber corrido transicion() antes.') 
			return 0

	def codigo(self, estado):
		return str(estado)

	def render(self):
		return