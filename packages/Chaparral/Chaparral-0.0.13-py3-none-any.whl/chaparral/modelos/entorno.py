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
from collections import defaultdict

from chaparral.modelos.clases import (
	Cluster, 
	Camion, 
	Ruta, 
	PseudoRutaCamionEstacionario
)
from chaparral.modelos.constantes import (
	FACTOR_RECOMPENSA,
	RECOMPENSA_MOVIMIENTO_NO_PERMITIDO,
	HORAS_HABILES,
	PENALIZACION_PASADAS_HORAS_HABILES,
	RUIDO,
	VALOR_CRITICO_TOLERANCIA,
	VALOR_CRITICO_CARGA,
	MEDIA_X,
	DESVEST_X,
	MEDIA_Y,
	DESVEST_Y,
	FACTOR_RENDER_X,
	FACTOR_RENDER_Y
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
				datos_rutas:Dict[str, Dict[str,float]],
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
		# Datos referentes al turno
		# -------------------------------
		self.tiempo_transcurrido = 0
		# -------------------------------
		# Datos provenientes de camiones
		# -------------------------------
		self.camiones = camiones
		self.actualizar_camiones()
		self.backup_camiones = deepcopy(camiones)
		self.num_camiones = len(self.camiones)
		# -------------------------------
		# Para usar en entrenamiento
		# -------------------------------
		self.usar_ruido = False
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
		self.tiempo_transcurrido = 0
		if self.usar_ruido:
			self.incluir_ruido()
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
			return self.estado, RECOMPENSA_MOVIMIENTO_NO_PERMITIDO, True
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
		if unidades_temporales == np.inf:
			# Si el mínimo es inf, significa que ningún camión se mueve
			# Esto solo debe ocurrir cuando el entorno termina
			return self.estado, RECOMPENSA_MOVIMIENTO_NO_PERMITIDO, True
		# para bookkeeping de espacio de estados
		self._unidades_temporales = unidades_temporales
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
		tensor_tiempo = [torch.tensor([self.tiempo_transcurrido], dtype=torch.float32)]
		tensores_clusters = [cluster.cluster_a_tensor() for cluster in self.clusters[1:]]
		tensores_camiones = [camion.camion_a_tensor(self.num_clusters) for camion in self.camiones]
		tensores = tensor_tiempo + tensores_clusters + tensores_camiones
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
		# para bookkeeping del turno
		self.tiempo_transcurrido += unidades_temporales

	def _encontrar_recompensa_y_done(self, unidades_temporales) -> Tuple[float, bool]:
		'''Encuentra la recompensa en el estado obtenido'''
		# # Chequeamos si la cantidad de algún químico en algún cluster es negativa
		# for cluster in self.clusters[1:]:
		# 	for pozo in cluster.pozos:
		# 		for quimico in pozo.quimicos:
		# 			if quimico.nivel_actual < quimico.velocidad_consumo * VALOR_CRITICO_TOLERANCIA:
		# 				if self.debug:
		# 					print('¡Se infringieron los porcentajes críticos!')
		# 					print(f'\tCluster {cluster.nombre}--{pozo.nombre}--{quimico.nombre} con niveles: {round(quimico.nivel_actual, 2)} (mínimo: {round(quimico.velocidad_consumo * VALOR_CRITICO_TOLERANCIA, 2)})')
		# 				# Por lo menos un químico está por debajo del nivel crítico => penalizar al agente
		# 				return -1000, True
		# Chequeamos si todos los camiones están en bodega
		# y no es el estado incial
		# Si el camión tomó más de las horas hábiles, penalizar
		penalizacion = 0
		if self.tiempo_transcurrido > HORAS_HABILES:
			penalizacion = PENALIZACION_PASADAS_HORAS_HABILES
		if not self.comienzo and np.all([camion.ubicacion == 0 for camion in self.camiones]):
			# Entorno terminado
			# # Encontramos la recompensa como la suma de las diferencias 
			# # entre los niveles actuales y los requeridos (todos estos valores
			# # deben ser negativos)
			# recompensas = [np.subtract(cluster.niveles_actuales, 1) for cluster in self.clusters if cluster.activo]
			# Encontramos la recompensa como la suma de los niveles por encima del 1%
			recompensas = list()
			for cluster in self.clusters:
				for pozo in cluster.pozos:
					for quimico in pozo.quimicos:
						if quimico.velocidad_consumo > 0:
							recompensas.append(quimico.nivel_actual // quimico.velocidad_consumo)
			if self.debug:
				print(f'Las diferencias de químicos son: {recompensas}')
			recompensa = sum(recompensas) * FACTOR_RECOMPENSA
			recompensa += -1 * unidades_temporales + penalizacion
			return recompensa, True
		return -1 * unidades_temporales + penalizacion, False	

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
			# Crea la ruta
			ruta = Ruta(
				inicial=inicial,
				objetivo=objetivo,
				tiempo=self.datos_rutas[inicial.nombre][objetivo.nombre]
			)
		else:
			# Debemos crear una pseudoruta porque el movimiento
			# determina que el camión se queda estacionario
			ruta = PseudoRutaCamionEstacionario(
				inicial=inicial,
				objetivo=objetivo,
				tiempo=np.Inf
			)
		self.camiones[indice_camion].ruta = ruta

	def _check_movimientos(self, movimientos_camiones:List[int]) -> bool:
		'''
		Verifica que todos los movimientos sean válidos
		'''
		for indice_camion, movimiento in enumerate(movimientos_camiones):
			verificacion = self._check_accion(
				indice_camion=indice_camion,
				movimiento=movimiento
			)
			if not verificacion:
				return False
		return True

	def _check_accion(self, indice_camion:int, movimiento:int) -> bool:
		'''
		Verifica que, si el camión está en ruta, el movimiento
		coincide con la dirección de la ruta. También es posible
		que el camión se quede estacionario.
		'''
		# Obtiene el nombre del culster dado por el movimiento
		a_cluster = self.clusters[movimiento].nombre
		# Si camión en transito, accion debe coincidir con destino
		ruta = self.camiones[indice_camion].ruta
		if ruta is None:
			# Camión no está en tránsito
			check = True
		else:
			# Camión en tránsito
			destino = ruta.objetivo.nombre
			check = destino == a_cluster
		if self.debug:
			print(f'Movimiento en ruta: {check}')
		return check
	
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
				# Determina si el quimico está activo (velocidad de consumo mayor a 0)
				if quimico.velocidad_consumo > 0:
					# Determina si el camion tiene el químico
					indice_quimico = quimico.in_carga(camion.carga_quimicos)
					if indice_quimico is not None:
						# Encuentra la cantidad que falta del químico
						# como la diferencia entre el valor requerido y el actual
						falta = max(quimico.velocidad_consumo * VALOR_CRITICO_CARGA - quimico.nivel_actual, 0)
						carga = camion.carga_quimicos[indice_quimico].nivel_actual
						# Calcula la cantidad a descargar del camión
						if 0 <= falta <= carga:
							descarga = falta
						elif falta > carga:
							descarga = carga
						else:
							raise Exception(f'¡Valor de descarga inválido!\n\t carga:{carga} --- falta:{falta}')
						if self.debug:
							print(f'El camión {camion.nombre} descarga {round(descarga, 2)} de {quimico.nombre} (requerimiento: {round(falta, 2)})')
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
	
	def incluir_ruido(self):
		"""Modifica los valores de quimicos para facilitar aprendizaje"""
		for cluster in self.clusters:
			for pozo in cluster.pozos:
				for quimico in pozo.quimicos:
					quimico.nivel_actual = np.random.normal(loc=100, scale=10)
					quimico.velocidad_consumo = max(0.001, np.random.normal(loc=1e-1, scale=1e-2))
		for camion in self.camiones:
			for quimico in camion.carga_quimicos:
				quimico.nivel_actual = np.random.normal(loc=220, scale=10)
		
	def generar_rutas_de_politica(
				self, 
				agente:any, 
				max_steps:Optional[int]=10
			) -> List[Tuple[Dict,PrettyTable,PrettyTable]]:
		"""
		Genera las rutas usando un agente
		
		Input:
			- politica, una función que genera movimientos de los camiones en un estado dado
		
		Output:
			- dict_rutas, un diccionario con la ruta de cada camión
		"""
		# Hace un backup del valor de epsilon
		backup_epsilon = deepcopy(agente.epsilon)
		# Apaga la exploración del agente
		agente.epsilon = 0
		# Inicia los registros
		num_steps = 0
		done = False
		estado = self.reset()
		accion = agente.make_decision(estado)
		movimientos_camiones = self.accion_a_movimientos(accion)
		dict_rutas = {camion.nombre:[movimientos_camiones[indice_camion]] for indice_camion, camion in enumerate(self.camiones)}
		# Usa el agente óptimo para recorrer el campo de pozos
		while not done and num_steps < max_steps:
			num_steps += 1
			estado, recompensa, done = self.step(accion)
			accion = agente.make_decision(estado)
			movimientos_camiones = self.accion_a_movimientos(accion)
			for indice_camion, camion in enumerate(self.camiones):
				dict_rutas[camion.nombre].append(movimientos_camiones[indice_camion])
		table = PrettyTable(['Camión', 'Cluster'])
		table_quimicos = PrettyTable(['Camión', 'Quimico', 'Cantidad'])
		for camion in self.camiones:
			# Crea la tabla de químicos a llevar
			for quimico in camion.carga_quimicos:
				diferencia = quimico.nivel_inicial - quimico.nivel_actual
				if diferencia > 0:
					table_quimicos.add_row([camion.nombre, quimico.nombre, diferencia])
			# Crea la tabla de rutas
			table.add_row([camion.nombre, self.punto_partida])
			for i in range(num_steps):
				indice_cluster = dict_rutas[camion.nombre][i]
				a_cluster = self.clusters[indice_cluster].nombre
				table.add_row([camion.nombre, a_cluster])
		# Reinstaura el valor de epsilon
		agente.epsilon = backup_epsilon
		return (dict_rutas, table, table_quimicos)
	
	def render(self):
		G = nx.Graph()
		G.add_nodes_from(self.coordenadas.keys())
		order = {cluster:self._transformar_coordenadas(self.coordenadas[cluster]) for cluster in self.coordenadas.keys()}
		options = {
			'node_color': 'green',
			'node_size': 10,
			'verticalalignment':'bottom',
			'font_size': 12
		}
		fig = plt.figure(figsize=(15,15))
		ax = fig.add_subplot()
		nx.draw_networkx(G, pos=order, font_weight='bold', **options)
		for c, camion in enumerate(self.camiones):
			camion_en_pozo = camion.ubicacion
			coordenadas = self._transformar_coordenadas(self.clusters[camion_en_pozo].coordenadas)
			circle1 = patches.Circle(coordenadas, radius=0.25, color='green')
			ax.add_patch(circle1)
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
		x = (coordenadas[0] - MEDIA_X) / DESVEST_X * FACTOR_RENDER_X
		y = (coordenadas[1] - MEDIA_Y) / DESVEST_Y * FACTOR_RENDER_Y
		return x, y

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
		# html_table = str(self)
		# table_MN = pd.read_html(html_table)
		# return table_MN
		return str(state.tolist())

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

	def actualizar_camiones(self) -> None:
		"""Actualiza la carga de los camiones"""
		# Actualiza las estimaciones de las velocidades de
		# consumo de los químicos en el campo
		estimaciones = self.estimar_velocidades_consumo_clusters()
		nombres_quimicos = list(estimaciones.keys())
		for cluster in self.clusters:
			for pozo in cluster.pozos:
				for quimico in pozo.quimicos:
					nombres_quimicos.append(quimico.nombre)
		# Actualiza camiones con estimaciones y valor crítico de carga
		for camion in self.camiones:
			camion.ubicacion = 0
			camion.ruta = None
			camion.nombres_clusters = [cluster.nombre for cluster in self.clusters]
			camion.carga_quimicos = [quimico for quimico in camion.carga_quimicos if quimico.nombre in nombres_quimicos]
			for quimico in camion.carga_quimicos:
				quimico.nivel_actual = estimaciones[quimico.nombre] * VALOR_CRITICO_CARGA
				quimico.nivel_inicial = quimico.nivel_actual

	def estimar_velocidades_consumo_clusters(self) -> Dict[str, float]:
		"""
		Estima las velocidades de consumo de los químicos
		en todos los pozos del campo.
		"""
		velocidades = defaultdict(list)
		estimaciones = dict()
		for cluster in self.clusters:
			for pozo in cluster.pozos:
				for quimico in pozo.quimicos:
					velocidades[quimico.nombre].append(quimico.velocidad_consumo)
		nombres_quimicos = list(velocidades.keys())
		for nombre_quimico in nombres_quimicos:
			estimaciones[nombre_quimico] = np.mean(velocidades[nombre_quimico])
		return estimaciones		