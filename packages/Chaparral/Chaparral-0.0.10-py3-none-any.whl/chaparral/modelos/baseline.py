import pandas as pd
from pathlib import Path
import json
import numpy as np
import datetime
from typing import List, Optional, Tuple, Union

from chaparral.mapa.convenciones import POZO2CLUSTER
from chaparral.mapa.espacio_rutas import TrazadorRuta
from chaparral.modelos.constantes import (
	VALOR_CRITICO_CARGA, 
	NUM_BULKDRUMS,
	TIEMPO_DESCARGA,
)
from chaparral.modelos.modelo_utils import CampoUtils, CreadorCampoPozos
from chaparral.modelos.clases import Camion2
from chaparral.modelos.busqueda import Nodo



class Baseline :
	"""Encuentra requerimiento de químicos y una ruta de acuerdo a heurística"""

	def __init__(self, dataframe:pd.DataFrame) -> None:
		self.dataframe = dataframe
		self.heuristicas = list()
		self.errors_log = list()
		self.max_size = 200
		self.requerimientos = None
		self.campo = None
		self.trazador = None
		self.solucion = None
		self.datos = None
		self.debug = False

	def crear_quimicos_a_camion(self) -> Tuple[List[str], pd.DataFrame]:
		"""Crea la lista de carga de químicos"""
		# Encuentra los requerimientos de químicos
		data = self.encontrar_requerimientos()
		# Inicializa el camión
		nombres_clusters = list(data.cluster.unique())
		nombres_quimicos = list(data.quimico.unique())
		camion = Camion2(
			nombre='CM1',
			num_bulkdrums=NUM_BULKDRUMS,
			ubicacion=0,
			ruta=None,
			nombres_clusters=nombres_clusters,
			nombres_quimicos=nombres_quimicos
		)
		if self.debug:
			camion.debug = True
		# Recorre los datos y va cargando los químicos en el camión
		# de acuerdo a la prioridad dias_con_stock, total_cluster, requerimiento
		clusters = ['bodega_00']
		saltar = False
		for index_, line_ in data.iterrows():
			if saltar:
				break
			cluster = line_.cluster
			if cluster in clusters:
				continue
			if self.debug:
				print(f'Tomado datos de cluster {cluster}')
			grp = data.groupby('cluster').get_group(cluster)
			for index, line in grp.iterrows():
				quimico = line.quimico
				cantidad = line.requerimiento
				if self.debug:
					print(f'Cargando {cantidad} de {quimico} para pozo {line.punto} en cluster {cluster}')
				try:
					camion.cargar(quimico, cantidad)
					clusters.append(cluster)
				except:
					# Camión lleno
					if self.debug:
						print('Camión lleno!', quimico, cluster, list(set(clusters)), len(list(set(clusters))))
					clusters = [c for c in clusters if c != cluster]
					saltar = True
					break
		# Lista de clusters a visitar
		clusters_a_visitar = list(set(clusters))
		# Guarda los requerimientos
		df = data.copy().sort_values(by=['cluster', 'punto'], inplace=False)
		df = df.drop(columns=['dias_con_stock', 'total_cluster'])
		df = pd.DataFrame(df[df['cluster'].isin(clusters_a_visitar)])
		self.requerimientos = df
		# Se toma la info del camión
		if self.debug:
			print(camion)
		df_quimicos = camion.a_pandas().sort_values(by=['quimico', 'cantidades']).reset_index().drop(columns=['index'])
		return clusters_a_visitar, df_quimicos
	
	def encontrar_ruta(
				self,
				clusters_a_visitar:List[str]
			) -> pd.DataFrame:
		"""Encuentra la mejor ruta por los clusters"""
		# Crea el trazador de rutas
		creador = CreadorCampoPozos(
			nombre_archivo_clusters='objetos_mapa_objetos_api_v1.ndjson',
			df_quimicos=self.dataframe,
			nombre_archivo_rutas='rutas.json'
		)
		campo = creador.crear_campo()
		trazador = self.crear_trazador(
			campo,
			filtro_clusters=clusters_a_visitar,
			max_size=self.max_size
		)
		self.trazador = trazador
		# Encuentra la mejor ruta
		solucion = trazador.A_star(W=1)
		# Convierte en dataframe con las columnas
		#	- hora
		#	- cluster
		if solucion is not None:
			self.solucion = solucion
			clusters_ordenados = solucion.estado + ['bodega_00']
			hora = datetime.timedelta(hours=9)
			hora_en_cluster = [hora]
			inicial = True
			for i, cluster in enumerate(clusters_ordenados[:-1]):
				siguiente_cluster = clusters_ordenados[i+1]
				if inicial:
					hora += datetime.timedelta(hours=self.campo.datos_rutas[cluster][siguiente_cluster] - TIEMPO_DESCARGA)
					inicial = False
				else:
					hora += datetime.timedelta(hours=self.campo.datos_rutas[cluster][siguiente_cluster])
				hora_en_cluster.append(hora)
			df_hora_cluster = pd.DataFrame({'Hora':hora_en_cluster, 'Cluster':clusters_ordenados})
			return df_hora_cluster
		return None

	def encuentra_hora_cluster(self, nodo:Nodo) -> Tuple[float, str]:
		return 

	def encontrar_requerimientos(self) -> pd.DataFrame:
		"""
		Retorna un dataframe de requerimientos de químicos por cluster así:
			- cluster
			- punto
			- quimico
			- requerimiento
			- días con stock
			- total cluster

		La prioridad en el orden de las filas es:
			- dias con stock
			- requerimiento total del cluster
			- requerimiento individual del punto
		"""
		# Carga datos
		data = self.dataframe.copy()
		# Deja solo los puntos activos (velocidad de consumo positiva)
		data = pd.DataFrame(data[data.velocidad_consumo > 0])
		# Prioriza por cantidad de días con stock
		data.sort_values(by='dias_con_stock', inplace=True)
		# Encuentra el cluster de cada punto
		data['cluster'] = data['punto'].apply(lambda x: self.encontrar_cluster(x))
		errores = pd.DataFrame(data[data.cluster.isna()])
		if errores.shape[0] > 0:
			self.errors_log.append(errores)
		data = pd.DataFrame(data[data.cluster.notna()])
		# Determina el requerimiento de químico de acuerdo a valor critico
		data['requerimiento'] = data['velocidad_consumo'] * VALOR_CRITICO_CARGA - data['nivel_actual']
		data['requerimiento'] = data['requerimiento'].apply(lambda x: x if x <= 250 else 250)
		# Deja solo los puntos cuyo requerimiento es positivo
		data = data[data['requerimiento'] > 0].reset_index()
		# Deja solo aquellos puntos cuya existencia sea menor al valor crítico
		data = data[data['dias_con_stock'] < VALOR_CRITICO_CARGA].reset_index()
		# Deja solo las columnas que nos interesan
		columnas_a_quitar = [columna for columna in data.columns if columna not in ['quimico','requerimiento', 'dias_con_stock', 'punto','cluster']]
		data.drop(columns=columnas_a_quitar, inplace=True)
		data = data[['cluster', 'punto', 'quimico', 'requerimiento', 'dias_con_stock']]
		# Encuentra el requerimiento total por cluster
		data['total_cluster'] = data.groupby('cluster')['dias_con_stock'].transform('mean')
		data.sort_values(
			by=[
				'total_cluster', 
				'cluster', 
				'dias_con_stock', 
				'requerimiento'
			], 
			ascending=[True, True, True, False],
			inplace=True
		)
		return data
	
	def cargar_datos(self):
		# Carga datos desde archivo
		archivo_path = self.path_archivo / Path(self.archivo)
		data = pd.read_json(archivo_path, lines=True)
		self.datos = data.copy()
		return data

	def encontrar_cluster(self, punto:str):
		try:
			return POZO2CLUSTER[punto]
		except:
			return np.nan
	
	def crear_trazador(
				self,
				campo,
				filtro_clusters:List[str],
				max_size:Optional[int]=200
			) -> TrazadorRuta:
		"""Crea el trazador de rutas"""
		cutil = CampoUtils()
		campo = cutil.cargar_campo(
			campo,
			filtro_clusters=filtro_clusters
		)
		trazador = TrazadorRuta(campo)
		trazador.max_size = max_size
		self.campo = campo
		return trazador
		
	def aplicar_heuristicas(self, df):
			"""Aplica las heurísticas sobre el dataframe"""
			for heuristica in self.heuristicas:
				df, resultado = heuristica(df)
				if resultado['responder']:
					return df
			
	def heuristica_viaje_simple(self, df):
		"""Verifica si todo cabe en un solo camion"""
		resultado = dict()
		num_quimicos = df.quimico.unique().shape
		print('->', num_quimicos)
		num_quimicos = num_quimicos[0]
		requerimientos_sobre_250 = df.requerimiento.apply(
			lambda x: x > 250
		)
		print('-->', requerimientos_sobre_250)
		requerimientos_sobre_250 = np.any(requerimientos_sobre_250)
		if num_quimicos <= 8 and not requerimientos_sobre_250:
			resultado['responder'] = True
		return df, resultado
	
	def heuristica_prioritarios(self, data):
		"""Atiende primero los pozos con menor días con stock"""
		# Ordenamos los datos por prioridad
		#	- menor cantidad de días con stock
		#	- mayor cantidad de químicos requeridos en el cluster
		#	- requerimiento individual por químico
		data.sort_values(
			by=['dias_con_stock', 'total_cluster', 'requerimiento'], 
			ascending=[True, False, False],
			inplace=True
		)
		for index, line in data.iterrows():
			cluster = line.cluster
			quimicos_cluster = data[data['cluster'] == cluster].tolist()
			print(cluster)
			print(quimicos_cluster)
