'''
© Copyright ArdillaByte Inc. 2023

-----------------------------------------------
Clase para correr el campo de pozos con sus
clusters y camiones.
-----------------------------------------------
'''
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import networkx as nx
import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Tuple, Union
from IPython.display import HTML
from copy import deepcopy
import torch
from prettytable import PrettyTable
import pickle
from pathlib import Path

from chaparral.modelos.clases import (
	Cluster, 
	Camion, 
	Ruta, 
	PseudoRutaCamionEstacionario
)
from chaparral.modelos.constantes import (
	FACTOR_RECOMPENSA,
	RUIDO,
	VALOR_CRITICO,
	FACTOR_RENDER
)


class CampoPozos:
	'''
	El entorno de los clusters unidos por caminos.
 
	Atributos:
		- Lista de clusters
		- Lista de caminos
		- Lista de camiones
		- Datos de las rutas
	'''
	def __init__(
				self, 
				clusters:List[Cluster], 
				datos_rutas:Dict[str,float],
				camiones:List[Camion]
			) -> None:
		# -------------------------------
		# Datos provenientes de clusters
		# -------------------------------
		self.clusters = clusters
		self.backup_clusters = deepcopy(clusters)
		self.num_clusters = len(self.clusters)
		self.punto_partida = clusters[0].nombre
		self.dict_clusters = {cluster.nombre:p for p, cluster in enumerate(self.clusters)}
		self.coordenadas = {cluster.nombre:cluster.coordenadas for cluster in self.clusters}
		# -------------------------------
		# Datos provenientes de rutas
		# -------------------------------
		self.datos_rutas = datos_rutas
		# -------------------------------
		# Datos provenientes de camiones
		# -------------------------------
		self.camiones = camiones
		for camion in self.camiones:
			camion.ubicacion = 0
			camion.ruta = None
		self.backup_camiones = deepcopy(camiones)
		self.num_camiones = len(self.camiones)
		# -------------------------------
		# Inicializa el estado
		# -------------------------------
		self.estado = self.reset()
		self.nS = self.estado.shape[0]
		self.comienzo = True # El entorno recién se inicializa
		# -------------------------------
		# Crea el bookkeeping de las acciones
		# -------------------------------
		# Las acciones posibles es decirle a cada camión
		# a qué cluster ir
		self.nA = self.num_clusters * self.num_camiones
		# -------------------------------
		# Para usar en debugging
		# -------------------------------
		self.debug = False
		# -------------------------------
		# Para usar en render
		# -------------------------------
		self.render_mode = 'rgb_array'

	def reset(self):
		'''
		Reinicia el entorno y devuelve el estado inicial
		'''
		self.clusters = deepcopy(self.backup_clusters)
		self.camiones = deepcopy(self.backup_camiones)
		estado = self.obtener_estado()
		self.comienzo = True # El entorno recién se inicializa
		return estado
	
	def step(self, accion:int) -> Tuple[torch.tensor, float, bool]:
		'''
		Avanza el entorno de acuerdo a la tupla de acciones.

		Input:
			- accion, índice de la lista de qué ruta toma cada camión

		Output:
			- tripla con nuevo estado, recompensa y done
		'''
		# El entorno comenzó
		self.comienzo = False
		# Decodifica la acción como índice de lista de movimientos
		movimientos_camiones = self.accion_a_movimientos(accion)
		# Verifica que todos los movimientos sean válidos
		verificacion_movimientos = self._check_movimientos(movimientos_camiones)
		if not verificacion_movimientos:
			# Alguno de los movimientos no es permitido.
			# El entorno debe seguir en el mismo estado 
			# y devolver castigo mediante la tupla: 
			# (mismo estado, recompensa negativa, entorno sigue activo)
			return self.estado, -1000, False
		# Si un camión debe comenzar una nueva ruta, inicializar en la lista atributo
		self._inicializar_rutas(movimientos_camiones)
		# Obtenemos cuántas unidades temporales se demora cada
		# camión en su respectiva ruta
		unidades = self._obtener_unidades_temporales()
		# Las unidades temporales a transcurrir son
		# el menor tiempo para terminar una ruta
		if self.debug:
			print('Unidades temporales de las rutas:', unidades)
		unidades_temporales = min(unidades)
		# para bookkeeping de espacio de estados
		self._unidades_temporales = unidades_temporales
		if unidades_temporales == np.inf:
			# Si el mínimo es inf, significa que ningún camión se mueve
			# Esto solo debe ocurrir cuando el entorno termina
			return self.estado, -10000, True
		if self.debug:
			print(f'Unidades temporales que transcurren: {unidades_temporales}')
		# Actualiza el estado
		self._actualizar_estado(unidades_temporales)
		nuevo_estado = self.obtener_estado()
		# Encuentra la recompensa y el done
		recompensa, done = self._encontrar_recompensa_y_done(unidades_temporales)
		return nuevo_estado, recompensa, done
	
	def obtener_estado(
				self,
				noise_:Optional[float]=RUIDO
			) -> torch.tensor:
		'''
		Obtiene el estado actual a partir de los atributos del entorno
		'''
		tensores_clusters = [cluster.cluster_a_tensor() for cluster in self.clusters[1:]]
		tensores_camiones = [camion.camion_a_tensor(self.num_clusters) for camion in self.camiones]
		tensores = tensores_clusters + tensores_camiones
		tensores = torch.cat(tensores)
		# Incluimos algo de ruido en el tensor
		shape = tensores.shape
		RUIDO = torch.rand(shape) * noise_
		return torch.add(tensores, RUIDO)

	def _actualizar_estado(
				self, 
				unidades_temporales:float
			) -> None:
		'''
		Actualiza el estado con la lógica siguente:
			1. Actualiza los clusters
			2. Actualiza los camiones en su respectiva ruta
			3. Si un camión llega al final de la ruta, descarga lo que pueda
		'''
		# 1. Pedimos a cada cluster que actualize con la cantidad de unidades temporales
		for cluster in self.clusters:
			cluster.actualizar(unidades_temporales)
		# 2. Pedimos a cada ruta que actualize con la cantidad de unidades temporales
		for camion in self.camiones:
			camion.ruta.actualizar(unidades_temporales)
			# 3. Verificar si el camión que va en la ruta llegó al final
			if camion.ruta.fin_recorrido():
				nombre_cluster_llegada = camion.ruta.objetivo.nombre
				if self.debug:
					print(f'Camión {camion.nombre} llegó a cluster {nombre_cluster_llegada}')
				# Descarga químicos en cluster
				indice_cluster = self.dict_clusters[nombre_cluster_llegada]
				self._descargar_camion_en_cluster(
					nombre_cluster=nombre_cluster_llegada, 
					camion=camion
				)
				# Actualizar la posición del camión
				camion.ubicacion = self.dict_clusters[nombre_cluster_llegada]
				# Dejar en espera de nueva ruta para el camión
				camion.ruta = None

	def _encontrar_recompensa_y_done(self, unidades_temporales) -> Tuple[float, bool]:
		'''Encuentra la recompensa en el estado obtenido'''
		# Chequeamos si la cantidad de algún químico en algún cluster es negativa
		for cluster in self.clusters[1:]:
			for pozo in cluster.pozos:
				for quimico in pozo.quimicos:
					if quimico.nivel_actual < quimico.velocidad_consumo * VALOR_CRITICO:
						if self.debug:
							print('¡Se infringieron los porcentajes críticos!')
							for cluster in self.clusters:
								print(f'\tCluster {cluster.nombre}--{pozo.nombre}--{quimico.nombre} con niveles: {quimico.nivel_actual}')
						# Por lo menos un químico está por debajo del nivel crítico => penalizar al agente
						return -1000, True
		# Chequeamos si todos los camiones están en bodega
		# y no es el estado incial
		if not self.comienzo and np.all([camion.ubicacion == 0 for camion in self.camiones]):
			# Entorno terminado
			# # Encontramos la recompensa como la suma de las diferencias 
			# # entre los niveles actuales y los requeridos (todos estos valores
			# # deben ser negativos)
			# recompensas = [np.subtract(cluster.niveles_actuales, 1) for cluster in self.clusters if cluster.activo]
			# Encontramos la recompensa como la suma de los niveles por encima del 1%
			recompensas = [quimico.nivel_actual // quimico.velocidad_consumo for cluster in self.clusters for pozo in cluster.pozos for quimico in pozo.quimicos]
			if self.debug:
				print(f'Las diferencias de químicos son: {recompensas}')
			recompensa = sum(recompensas) * FACTOR_RECOMPENSA
			return recompensa, True
		return -1 * unidades_temporales, False	

	def _obtener_unidades_temporales(self) -> Union[None, List[int]]:
		'''
		Obtiene la cantidad de unidades temporales requeridas 
		para terminar cada ruta de acuerdo a los movimientos
		de los camiones dado en el argumento

		Input:
			- movimientos_camiones, la lista de qué ruta toma cada camión

		Output:
			- Lista de unidades temporales o None en caso de acción inválida
		'''
		unidades = list()
		for camion in self.camiones:
			unidad = camion.ruta.obtener_unidades_temporales_faltantes()
			unidades.append(unidad)
		return unidades

	def _inicializar_rutas(self, movimientos_camiones:List[int]) -> None:
		'''Verifica si camión está en la ruta o si no inicializa'''
		for indice_camion, movimiento in enumerate(movimientos_camiones):
			ruta = self.camiones[indice_camion].ruta
			if ruta is None:
				self._iniciar_ruta(indice_camion, movimiento)

	def _iniciar_ruta(self, indice_camion, movimiento) -> None:
		'''Obtiene la ruta que debe seguir el camión y modifica la lista atributo'''
		# Obtiene dónde está el camión
		indice_inicial = self.camiones[indice_camion].ubicacion
		inicial = self.clusters[indice_inicial]
		# Obtiene para dónde va el camión de acuerdo al movimiento
		objetivo = self.clusters[movimiento]
		# Verifica si el movimiento estipula que el camión debe quedarse donde está
		if inicial.nombre != objetivo.nombre:
			# Crea el nombre de la ruta
			nombre = f'{inicial.nombre} <-> {objetivo.nombre}'
			# Encuentra longitud y velocidad promedio
			longitud = self.datos_rutas[nombre]['longitud']
			velocidad_promedio = self.datos_rutas[nombre]['velocidad_promedio']
			# Crea la ruta
			ruta = Ruta(
				inicial=inicial,
				objetivo=objetivo,
				longitud=longitud,
				velocidad_promedio=velocidad_promedio
			)
		else:
			# Debemos crear una pseudoruta porque el movimiento
			# determina que el camión se queda estacionario
			ruta = PseudoRutaCamionEstacionario(
				inicial=inicial,
				objetivo=objetivo,
				longitud=np.Inf,
				velocidad_promedio=0
			)
		self.camiones[indice_camion].ruta = ruta

	def _check_movimientos(self, movimientos_camiones:List[int]) -> bool:
		'''
		Verifica que todos los movimientos sean válidos
		'''
		for indice_camion, movimiento in enumerate(movimientos_camiones):
			verificacion = self._check_accion(
				indice_camion=indice_camion,
				movimiento=movimiento,
				indice_cluster=self.camiones[indice_camion].ubicacion
			)
			if not verificacion:
				return False
		return True

	def _check_accion(self, indice_camion:int, movimiento:int, indice_cluster:str) -> bool:
		'''
		Verifica que el movimiento es posible en el cluster dado
		y, si el camión está en ruta, verifica que el movimiento
		coincida con la dirección de la ruta. También es posible
		que el camión se quede estacionario
		'''
		nombre_cluster = self.clusters[indice_cluster]
		# Obtener lista de clusters accesibles desde donde está el camión
		clusters_posibles = self.clusters[indice_cluster].vecinos + [nombre_cluster]
		# Obtiene el nombre del culster dado por el movimiento
		a_cluster = self.clusters[movimiento].nombre
		# El movimiento debe estar en rango de movimientos posibles
		primer_check = a_cluster in clusters_posibles
		# Si camión en transito, accion debe coincidir con destino
		ruta = self.camiones[indice_camion].ruta
		if ruta is None:
			# Camión no está en tránsito
			segundo_check = True
		else:
			# Camión en tránsito
			destino = ruta.objetivo.nombre
			segundo_check = destino == a_cluster
		if self.debug:
			print(f'Movimiento permitido: {primer_check}, Movimiento en ruta: {segundo_check}')
		return np.all([primer_check, segundo_check])
	
	def _descargar_camion_en_cluster(
				self, 
				nombre_cluster:str,
				camion:Camion
			) -> None:
		'''Descarga los químicos en el cluster'''
		# Carga el objeto cluster
		indice_cluster = self.dict_clusters[nombre_cluster]
		cluster = self.clusters[indice_cluster]
		# Itera sobre los pozos del cluster
		for pozo in cluster.pozos:
			# Itera sobre los químicos del pozo
			for quimico in pozo.quimicos:
				# Determina si el camion tiene el químico
				indice_quimico = quimico.in_carga(camion.carga_quimicos)
				if indice_quimico is not None:
					# Encuentra la cantidad que falta del químico
					# como la diferencia entre el valor requerido y el actual
					falta = quimico.velocidad_consumo * VALOR_CRITICO - quimico.nivel_actual
					carga = camion.carga_quimicos[indice_quimico].nivel_actual
					# Calcula la cantidad a descargar del camión
					if 0 <= falta <= carga:
						descarga = falta
					elif falta > carga:
						descarga = carga
					else:
						raise Exception(f'¡Valor de descarga inválido!\n\t carga:{carga} --- falta:{falta}')
					if self.debug:
						print(f'El camión {camion.nombre} descarga {descarga} (faltaba {falta})')
					# Actualiza los niveles de cluster y camión
					quimico.nivel_actual += descarga
					camion.carga_quimicos[indice_quimico].nivel_actual -= descarga
	
	def accion_a_movimientos(self, accion:int) -> List[int]:
		"""Toma una acción y devuelve la lista correspondiente"""
		shape = tuple([self.num_clusters] * self.num_camiones)
		return list(np.unravel_index(accion, shape))
	
	def movimientos_a_accion(self, movimientos:Tuple[int]) -> int:
		"""Toma una lista de movimientos y devuelve la acción como índice"""
		shape = tuple([self.num_clusters] * self.num_camiones)
		return np.ravel_multi_index(movimientos, shape)
		
	def _list_edges(self) -> List[Tuple[str,str,Dict]]:
		if hasattr(self, 'list_edges'):
			return self.list_edges
		else:
			list_edges = [self._obtener_tupla_distancia(c1.nombre, c2) for c1 in self.clusters for c2 in c1.vecinos]
			self.list_edges = list_edges
			return self.list_edges

	def _obtener_tupla_distancia(self, cl1:str, cl2:str) -> float:
		distancia = f"{self.datos_rutas[f'{cl1} <-> {cl2}']['longitud']}km"
		velocidad = f"{self.datos_rutas[f'{cl1} <-> {cl2}']['velocidad_promedio']}km/h"
		rotulo = f'{distancia} a {velocidad}'
		dict_distancia = {'distancia':rotulo}
		return (cl1, cl2, dict_distancia)

	def generar_rutas_de_politica(
				self, 
				agente:any, 
				max_steps:Optional[int]=100
			) -> List[Tuple[Dict,PrettyTable]]:
		"""
		Genera las rutas usando un agente
		
		Input:
			- politica, una función que genera movimientos de los camiones en un estado dado
		
		Output:
			- dict_rutas, un diccionario con la ruta de cada camión
		"""
		# Hacemos un backup del valor de epsilon
		backup_epsilon = deepcopy(agente.epsilon)
		# Apagamos la exploración del agente
		agente.epsilon = 0
		# Iniciamos los registros
		num_steps = 0
		done = False
		estado = self.reset()
		accion = agente.make_decision(estado)
		movimientos_camiones = self.accion_a_movimientos(accion)
		dict_rutas = {camion.nombre:[movimientos_camiones[indice_camion]] for indice_camion, camion in enumerate(self.camiones)}
		while not done:
			num_steps += 1
			estado, recompensa, done = self.step(accion)
			accion = agente.make_decision(estado)
			movimientos_camiones = self.accion_a_movimientos(accion)
			for indice_camion, camion in enumerate(self.camiones):
				dict_rutas[camion.nombre].append(movimientos_camiones[indice_camion])
		table = PrettyTable(['Camión', 'Cluster'])
		for indice_camion in range(self.num_camiones):
			camion = self.camiones[indice_camion].nombre
			a_cluster = self.clusters[0].nombre
			table.add_row([camion, a_cluster])
		for indice_camion in range(self.num_camiones):
			for i in range(num_steps):
				camion = self.camiones[indice_camion].nombre
				indice_cluster = dict_rutas[camion][i]
				a_cluster = self.clusters[indice_cluster].nombre
				table.add_row([camion, a_cluster])
		# Reinstauramos el valor de epsilon
		agente.epsilon = backup_epsilon
		return (dict_rutas, table)
	
	def render(self):
		G = nx.Graph()
		G.add_nodes_from(self.coordenadas.keys())
		list_edges = self._list_edges()
		print(list_edges)
		G.add_edges_from(list_edges, color='red')
		order = {cluster:self._transformar_coordenadas(self.coordenadas[cluster]) for cluster in self.coordenadas.keys()}
		options = {
			'node_color': 'green',
			'node_size': 10,
			'verticalalignment':'bottom',
			'edge_color': 'red',
			'width': 0.5,
			'font_size': 8
		}
		fig = plt.figure(figsize=(15,15))
		ax = fig.add_subplot()
		nx.draw_networkx(G, pos=order, font_weight='bold', **options)
		# edge_labels = nx.get_edge_attributes(G, 'distancia')
		# nx.draw_networkx_edge_labels(G, order, edge_labels)
		# for c, camion in enumerate(self.camiones):
		# 	camion_en_pozo = camion.ubicacion
		# 	coordenadas = self.clusters[camion_en_pozo].coordenadas
		# 	circle1 = patches.Circle(coordenadas, radius=5, color='green')
		# 	ax.add_patch(circle1)
		ax.axis('off')
		fig.canvas.draw()
		string = fig.canvas.renderer.buffer_rgba()
		array = np.array(string)
		if self.render_mode == 'rgb_array':
			return array
		else:
			plt.show()

	def _transformar_coordenadas(
				self,
				coordenadas:List[float]
			) -> List[float]:
		return [coordenadas[0] * FACTOR_RENDER, coordenadas[1] * FACTOR_RENDER]

	def __str__(self) -> str:
		cadena = '<table> <tbody>'
		for cluster in self.clusters:
			cadena += str(cluster)
		cadena += '</tbody> </table>'
		cadena += '<tr> <td>&nbsp;</td> <td>&nbsp;</td> <td>&nbsp;</td> </tr>'
		cadena += '<table> <tbody>'
		for camion in self.camiones:
			cadena += str(camion)
		cadena += '</tbody> </table>'
		return cadena

	def state_visualizer(self, state):
		"""Retorna una representación visual del estado"""
		html_table = str(self)
		table_MN = pd.read_html(html_table)
		return table_MN

	def action_visualizer(self, action):
		"""Retorna una representación visual de la acción"""
		movimientos_camiones = self.accion_a_movimientos(action)
		lista_movimientos = [self.clusters[indice_cluster].nombre for indice_cluster in movimientos_camiones]
		return lista_movimientos
	
	def save(
				self,
				archivo:Optional[Union[None, str]]=None
			) -> None:
		directorio = Path.cwd() / Path('..').resolve() / Path('data', 'entornos')
		directorio.mkdir(parents=False, exist_ok=True)
		if archivo is not None:
			path_archivo = directorio / Path(archivo)
		else:
			path_archivo = directorio / Path('entorno.pkl')
		with open(path_archivo, 'wb') as file:
			pickle.dump(self, file)
			file.close()