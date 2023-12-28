from pathlib import Path
import pandas as pd
from typing import List, Dict, Optional, Tuple, Union
import warnings
import numpy as np
import json
import pickle
from copy import deepcopy

from chaparral.modelos.clases import (
	Cluster, 
	Camion, 
	QuimicoEn, 
	Pozo
)
from chaparral.modelos.entorno import CampoPozos
from chaparral.main.cargar_inventario import estandarizar_nombre
# from chaparral.mapa.convenciones import POZO2CLUSTER 
from chaparral.modelos.constantes import (
	ESCALA_VELOCIDAD_CONSUMO, 
	ESCALA_VELOCIDAD_CAMION,
	VALOR_CRITICO_CARGA
)


class Auditor :
	"""Clase que revisa si el CampoPozos tiene los requerimientos necesarios"""

	def __init__(self) -> None:
		self.errores_log = list()
		self.directorio_log = Path.cwd() / Path('..').resolve() / Path('data', 'logs')
		self.directorio_log.mkdir(parents=False, exist_ok=True)

	def auditar_quimicos(
				self,
				pozos:List[Pozo]
			) -> List[Pozo]:
		pozos_a_eliminar = list()
		for pozo in pozos:
			if len(pozo.quimicos) == 0:
				mensaje_error = f'Pozo {pozo.nombre} no tiene quimicos'
				warnings.warn('Advertencia de error en lectura de datos cluster.') 
				self.errores_log.append(mensaje_error)
				pozos_a_eliminar.append(pozo.nombre)
		return [pozo for pozo in pozos if pozo.nombre not in pozos_a_eliminar]

	def auditar_integridad_clusters(
				self,
				clusters:List[Cluster]
			) -> Tuple[List[Cluster], bool]:
		assert(clusters[0].nombre == 'bodega_00'), f'Cluster 0 debe ser bodega_00, no {clusters[0].nombre}'
		clusters_a_eliminar = list()
		for cluster in clusters:
			# Verifica los químicos de los pozos en el cluster
			cluster.pozos = self.auditar_quimicos(cluster.pozos)
			# Verifica el nombre del cluster
			if not isinstance(cluster.nombre, str):
				mensaje_error = f'Cluster {cluster.nombre} sin nombre de tipo adecuado'
				warnings.warn('Advertencia de error en químicos asociados a cluster.') 
				self.errores_log.append(mensaje_error)
				clusters_a_eliminar.append(cluster.nombre)
			# Verifica las coordenadas del cluster
			if not isinstance(cluster.coordenadas, list) and len(cluster.coordenadas) == 2:
				mensaje_error = f'Cluster {cluster.nombre} sin coordenadas de tipo adecuado'
				warnings.warn('Advertencia de error en químicos asociados a cluster.') 
				self.errores_log.append(mensaje_error)
				clusters_a_eliminar.append(cluster.nombre)
			else:
				x, y = cluster.coordenadas[0], cluster.coordenadas[1]	
				if not (isinstance(x, float) and isinstance(y, float)):
					mensaje_error = f'Cluster {cluster.nombre} sin coordenadas de tipo adecuado'
					warnings.warn('Advertencia de error en químicos asociados a cluster.') 
					self.errores_log.append(mensaje_error)
					clusters_a_eliminar.append(cluster.nombre)		
			# Verifica que haya pozos en el cluster	
			if not len(cluster.pozos) > 0 and cluster.nombre != 'bodega_00':
				mensaje_error =  f'Cluster {cluster.nombre} sin pozos'
				warnings.warn('Advertencia de error en químicos asociados a cluster.') 
				self.errores_log.append(mensaje_error)
				clusters_a_eliminar.append(cluster.nombre)
			# if not len(cluster.vecinos) > 0:
			# 	mensaje_error = f'Cluster {cluster.nombre} sin vecinos'
			# 	warnings.warn('Advertencia de error en químicos asociados a cluster.') 
			# 	self.errores_log['clusters & quimicos'].append(mensaje_error)
			# 	clusters_a_eliminar.append(cluster.nombre)			
		if len(clusters_a_eliminar) > 0:
			flag = True
		else:
			flag = False
		clusters = [cluster for cluster in clusters if cluster.nombre not in clusters_a_eliminar]
		return clusters, flag
	
	def auditar_clusters(
				self,
				clusters:List[Cluster]
		) -> List[Cluster]:
		flag = True
		while flag:
			clusters, flag1 = self.auditar_vecinos_en_clusters(clusters)
			clusters, flag2 = self.auditar_integridad_clusters(clusters)
			flag = flag1 or flag2
		return clusters
	
	def auditar_vecinos_en_clusters(
				self,
				clusters:List[Cluster]
			) -> Tuple[List[Cluster], bool]:
		"""Revisa que los vecinos de cada cluster estén incluidos"""
		nombres_clusters = [cluster.nombre for cluster in clusters]
		flags = list()
		for cluster in clusters:
			cluster.vecinos = [vecino for vecino in cluster.vecinos if vecino in nombres_clusters]
			if len(cluster.vecinos) == 0:
				flags.append(True)
			else:
				flags.append(False)
		return clusters, np.any(flags)

	def auditar_cluster_a_pozos(self) -> None:
		"""
		Revisa que la información de cluster a puntos coincida
		con los clusters dados como argumento.
		"""		
		# Creamos ambas listas de clusters
		clusters_desde_argumento = set([cluster.nombre for cluster in self.clusters])
		clusters_desde_argumento.add('bodega_00')
		clusters_en_cluster_a_puntos = set(self.cluster_a_pozos.keys())
		clusters_en_cluster_a_puntos.add('bodega_00')
		# Encontramos diferencias
		errores1 = clusters_desde_argumento.difference(clusters_en_cluster_a_puntos)
		errores2 = clusters_en_cluster_a_puntos.difference(clusters_desde_argumento)
		# Actualizamos el log de errores
		if len(errores1) > 0:
			warnings.warn('Advertencia de error en lectura de datos cluster.') 
			self.errores_log.append(f'clusters sin datos de puntos:\n{errores1}')
		if len(errores2) > 0:
			warnings.warn('Advertencia de error en lectura de datos cluster.') 
			self.errores_log.append(f'clusters con puntos sin datos de rutas:\n{errores2}')
		# Dejamos solo los clusters con toda la información
		clusters_a_usar = clusters_desde_argumento.intersection(clusters_en_cluster_a_puntos)
		self.clusters = [cluster for cluster in self.clusters if cluster.nombre in clusters_a_usar]

	def guardar(self) -> None:
		# Guardamos el registro de errores
		json_object = json.dumps(self.errores_log, indent=4)
		nombre_archivo_log = self.directorio_log / Path('auditor_log.json')
		with open(nombre_archivo_log, "w") as outfile:
			outfile.write(json_object)


class LectorQuimicos :
	"""Lee información de quimicos y sus cantidades en los clusters."""

	def __init__(
				self, 
				df_quimicos:pd.DataFrame
			) -> Dict[str, Dict[str, float]]:
		self.data = df_quimicos
		self.verbose = False
		# Inicializa el registro de quimicos
		self.quimicos = list()
		self.nombres_quimicos = list()
		self.dict_quimicos = {quimico.nombre:p for p, quimico in enumerate(self.quimicos)}
		# Inicializa el registro de errores
		self.errores_log = list()
		# # Genera diccionario de cluster a puntos
		# self.cluster_a_pozos = self.crear_cluster_a_pozos()
		# # Compara datos de puntos a cluster con clusters recibidos como argumento
		# self.auditar_cluster_a_pozos()

	def actualizar_clusters(
				self,
				clusters:List[Cluster]
			) -> Tuple[List[Cluster], List[str]]:
		"""Actualiza los clusters dados con la info."""
		# Inicializa listado de clusters sin datos
		clusters_sin_datos = list()
		# Itera sobre clusters
		for cluster in clusters[1:]: # Omitir Bodega
			# Itera sobre pozo en cluster
			for pozo in cluster.pozos:
				lista_pozos = self.data.punto.unique().tolist()
				# if self.verbose:
				# 	print(f'Actualizando químicos de pozo {pozo.nombre}')
				if pozo.nombre in lista_pozos:
					quimicos_en_cluster = self.data.groupby('punto').get_group(pozo.nombre)
					quimicos = list()
					# Itera sobre químico en pozo
					for nombre_quimico, grp in quimicos_en_cluster.groupby('quimico'):
						quimico = self.crear_quimico(
							nombre_quimico=nombre_quimico, 
							datos=grp
						)
						quimicos.append(quimico)
					pozo.quimicos = quimicos
					self.quimicos += quimicos
				else:
					mensaje_error = f'No parece haber datos del pozo {pozo}.'
					self.errores_log.append(mensaje_error)
			# pozos = self.auditar_quimicos(pozos)
		if self.verbose:
			print('Clusters actualizados con datos de los químicos.')
		# Limpia registros clusters
		clusters = [cluster for cluster in clusters if cluster.nombre not in clusters_sin_datos]
		# Limpia registro químicos
		nombres_quimicos = list(set([quimico.nombre for quimico in self.quimicos]))
		self.quimicos = [
			QuimicoEn(
				nombre=nombre,
				unidades='Gl',
				nivel_actual=0,
				velocidad_consumo=0
			) for nombre in nombres_quimicos
		]
		return clusters, self.errores_log
	
	def crear_quimico(
				self,
				nombre_quimico:str,
				datos:pd.DataFrame
			) -> QuimicoEn:
		nivel_actual = datos.nivel_actual.values.tolist()[0]
		velocidad_consumo = datos.velocidad_consumo.values.tolist()[0]
		quimico = QuimicoEn(
			nombre=nombre_quimico,
			unidades='Gl',
			nivel_actual=nivel_actual,
			velocidad_consumo=velocidad_consumo * ESCALA_VELOCIDAD_CONSUMO
		)
		return quimico
	
	# def crear_cluster_a_pozos(self) -> Dict[str, str]:
	# 	"""Crea el diccionario que relaciona un cluster con sus pozos/puntos"""
	# 	df = pd.DataFrame({'pozo':POZO2CLUSTER.keys(), 'cluster':POZO2CLUSTER.values()})
	# 	cluster_a_pozos = dict()
	# 	for cluster, grp in df.groupby('cluster'):
	# 		if cluster != 'bodega_00':
	# 			pozos = grp.pozo.unique().tolist()
	# 			cluster_a_pozos[cluster] = pozos
	# 			if len(pozos) == 0:
	# 				mensaje_error = f'Cluster {cluster} no tiene pozos'
	# 				warnings.warn('Advertencia de error en lectura de datos cluster.') 
	# 				self.errores_log.append(mensaje_error)
	# 	return cluster_a_pozos


class CreadorCampoPozos :
	"""
	Crea la clase CampoPozos con todos sus componentes.
	"""

	def __init__(
				self,
				nombre_archivo_clusters:str,
				df_quimicos:pd.DataFrame,
				nombre_archivo_rutas:str
			) -> CampoPozos:
		# -------------------------------
		# Registros de directorios
		# -------------------------------
		self.directorio = Path.cwd() / Path('..').resolve() / Path('data', 'objetos_mapa')
		self.directorio.mkdir(parents=False, exist_ok=True)
		self.directorio_log = Path.cwd() / Path('..').resolve() / Path('data', 'logs')
		self.directorio_log.mkdir(parents=False, exist_ok=True)
		# -------------------------------
		# Registros de archivos
		# -------------------------------
		self.nombre_archivo_clusters = nombre_archivo_clusters
		self.nombre_archivo_rutas = nombre_archivo_rutas
		# -------------------------------
		# Registro de datos
		# -------------------------------
		self.df_quimicos = df_quimicos
		self.data = None
		self.nombres_clusters = list()
		self.verbose = False
		self.errors_log = {
			'clusters':list(),
			'clusters & quimicos':list()
		}

	def crear_campo(self) -> None:
		# -------------------------------
		# Carga los datos desde archivo
		# -------------------------------
		self.cargar_datos()
		# -------------------------------
		# Crea los clusters y los quimicos
		# -------------------------------
		clusters, quimicos = self.generar_clusters_y_quimicos()
		# -------------------------------
		# Auditar clusters
		# -------------------------------
		auditor = Auditor()
		clusters, flag = auditor.auditar_integridad_clusters(clusters)
		nombres_clusters = [cluster.nombre for cluster in clusters]
		auditor.guardar()
		if self.verbose:
			print(f'Log de auditor guardado')
		# -------------------------------
		# Carga las rutas
		# -------------------------------
		datos_rutas = self.cargar_rutas()
		# -------------------------------
		# Crea el camion
		# -------------------------------
		# Inicializa la carga del camión
		print('')
		print('Químicos a camión:')
		for quimico in quimicos:
			quimico.nivel_actual = VALOR_CRITICO_CARGA * quimico.velocidad_consumo
			quimico.nivel_inicial = quimico.nivel_actual
			print(quimico.nombre, quimico.nivel_actual)
		camion1 = Camion(
			nombre='C1',
			capacidad=100,
			carga_quimicos=quimicos,
			ubicacion=0,
			ruta=None,
			nombres_clusters=nombres_clusters
		)
		# -------------------------------
		# Crea el campo de pozos
		# -------------------------------
		campo = CampoPozos(
			clusters=clusters,
			datos_rutas=datos_rutas,
			camiones=[camion1],
		)
		return campo

	def cargar_datos(self) -> None:
		ruta_archivo = self.directorio / Path(self.nombre_archivo_clusters)
		with open(ruta_archivo) as f:
			self.data = pd.read_json(f, lines=True)
		if self.verbose:
			print('')
			print(f'Datos cargados con éxito desde archivo.\n\t({ruta_archivo})')

	def cargar_rutas(self) -> None:
		ruta_archivo = self.directorio / Path(self.nombre_archivo_rutas)
		with open(ruta_archivo) as f:
			data = json.load(f)
		return data

	def generar_clusters_y_quimicos(self) -> List[Cluster]:
		# Creamos los clusters
		if self.verbose:
			print('')
			print('Creando clusters...')
		clusters = self.crear_clusters()
		# Cargamos la información de químicos
		if self.verbose:
			print('')
			print('Actualizando información de químicos en clusters...')
		lector = LectorQuimicos(self.df_quimicos)
		lector.verbose = self.verbose
		clusters, errores = lector.actualizar_clusters(clusters)
		self.errors_log['quimicos'] = errores
		# Guardamos el registro de errores
		json_object = json.dumps(self.errors_log, indent=4)
		nombre_archivo_log = self.directorio_log / Path('creador_log.json')
		with open(nombre_archivo_log, "w") as outfile:
			outfile.write(json_object)
		if self.verbose:
			print(f'Log de errores guardado en {nombre_archivo_log}')
		return clusters, deepcopy(lector.quimicos)

	def crear_clusters(self) -> Tuple[List[Cluster], Dict[str,int]] :
		# Inicializamos la lista de clusters
		clusters = list()
		data_bodega = self.data[self.data.tipo == 'BODEGA']
		bodega = self.crear_cluster(
			data_bodega, 
			bodega=True
		)
		if bodega is not None:
			clusters.append(bodega)
			if self.verbose:
				print('')
				print('\tBodega creada')
		else:
			print('Advertencia: Bodega no se creó. Revisar log.')
		data_clusters = self.data[self.data.tipo == 'CLUSTER']
		if self.verbose:
			print('')
			print(f'\tCreando {data_clusters.shape[0]} clusters...')
		for indice, data_cluster in data_clusters.iterrows():
			cluster = self.crear_cluster(data_cluster)
			clusters.append(cluster)
		return clusters

	def crear_cluster(
			self,
			data_cluster:pd.DataFrame,
			bodega:bool=False,
		) -> Cluster:
		"""Crea el cluster a partir de los datos"""
		# Extraemos el nombre
		if bodega:
			nombre = 'bodega_00'
		else:
			nombre = str(data_cluster.nombre)
		# Incluimos el nombre en la lista
		if nombre not in self.nombres_clusters:
			self.nombres_clusters.append(nombre)
		# Extraemos las coordenadas
		coordenadas = data_cluster.coords
		if isinstance(coordenadas, pd.Series):
			coordenadas = coordenadas.values[0]
		elif isinstance(coordenadas, np.ndarray):
			coordenadas = coordenadas.tolist()
		# Extraer información de pozos
		pozos = list()
		for pozo_ in data_cluster.pozos:
			pozo = Pozo(
				nombre=pozo_,
				quimicos=list()
			)
			pozos.append(pozo)
		# # Extraemos toda la información de los vecinos
		# data_vecinos = list(data_cluster.vecinos)
		# if bodega:
		# 	data_vecinos = data_vecinos[0]
		# 	nombre = 'bodega_00'
		# # Procesamos la información de las rutas a vecinos
		# try:
		# 	self.agregar_rutas(
		# 		nombre_cluster=nombre, 
		# 		data_vecinos=data_vecinos
		# 	)
		# 	if self.verbose:
		# 		print(f'\t\tRutas con vecinos actualizadas para cluster {nombre}...')
		# except Exception as e:
		# 	error_message = f'Error con cluster {nombre}\n{e}'
		# 	warnings.warn('Advertencia de error en lectura de datos cluster.') 
		# 	self.errors_log['clusters'].append(error_message)
		# # Encontramos los nombres de los vecions
		# vecinos = [d['nombre'] for d in data_vecinos]
		# Creamos el cluster
		cluster = Cluster(
			nombre=nombre,
			pozos=pozos,
			coordenadas=coordenadas,
			# vecinos=vecinos,
		)
		return cluster	

	# def agregar_rutas(
	# 			self, 
	# 			nombre_cluster:str,
	# 			data_vecinos:Dict[str, any]
	# 		) -> None:
	# 	"""
	# 	Agrega la informacion de los vecinos a los
	# 	datos de las rutas.
	# 	"""
	# 	for vecino in data_vecinos:
	# 		# Incluimos una dirección
	# 		nombre = f'{nombre_cluster} <-> {vecino["nombre"]}'
	# 		if nombre in self.datos_rutas.keys():
	# 			assert(np.isclose(self.datos_rutas[nombre]['longitud'], vecino["dist"])), f'distancias inconsistentes {nombre}'
	# 			assert(np.isclose(self.datos_rutas[nombre]['velocidad_promedio'], vecino["dist"] / vecino["tiempo"])), f'velocidades inconsistentes {nombre}'
	# 		assert(vecino["tiempo"] > 0), f'tiempo a vecino {vecino["nombre"]} es 0'
	# 		self.datos_rutas[nombre] = {
	# 			'longitud':vecino["dist"],
	# 			'velocidad_promedio':vecino["dist"] / vecino["tiempo"] * ESCALA_VELOCIDAD_CAMION
	# 		}


class CampoUtils :

	def __init__(self) -> None:
		self.cluster_de_pozo = dict()
		self.pozos_en_cluster = dict()
		self.debug = False

	def cargar_campo_desde_archivo(
				self,
				archivo_path: Union[str, Path],
				filtro_clusters:Optional[Union[None, List[str]]]=None,
				filtro_pozos:Optional[Union[None, List[str]]]=None
			) -> CampoPozos:
		# Carga el campo desde archivo
		with open(archivo_path, 'rb') as f:
			campo = pickle.load(f)
		# Genera diccionarios
		for cluster in campo.clusters:
			for pozo in cluster.pozos:
				self.cluster_de_pozo[pozo.nombre] = cluster.nombre
			self.pozos_en_cluster[cluster.nombre] = [pozo.nombre for pozo in cluster.pozos]
		if self.debug:
			print('')
			print('Pozos en clusters:')
			pozos = sorted(list(self.cluster_de_pozo.keys()))
			for pozo in pozos:
				print('\t', pozo)
		# Aplicar filtros
		if filtro_clusters is not None or filtro_pozos is not None:
			campo = self.filtrar(
				campo,
				filtro_clusters=filtro_clusters,
				filtro_pozos=filtro_pozos
			)
		return campo		

	def cargar_campo(
			self,
			campo,
			filtro_clusters:Optional[Union[None, List[str]]]=None,
			filtro_pozos:Optional[Union[None, List[str]]]=None
	) -> CampoPozos:
		# Genera diccionarios
		for cluster in campo.clusters:
			for pozo in cluster.pozos:
				self.cluster_de_pozo[pozo.nombre] = cluster.nombre
			self.pozos_en_cluster[cluster.nombre] = [pozo.nombre for pozo in cluster.pozos]
		if self.debug:
			print('')
			print('Pozos en clusters:')
			pozos = sorted(list(self.cluster_de_pozo.keys()))
			for pozo in pozos:
				print('\t', pozo)
		# Aplicar filtros
		if filtro_clusters is not None or filtro_pozos is not None:
			campo = self.filtrar(
				campo,
				filtro_clusters=filtro_clusters,
				filtro_pozos=filtro_pozos
			)
		return campo

	def filtrar(
				self, 
				campo:CampoPozos,
				filtro_clusters:Union[None, List[str]]=None,
				filtro_pozos:Union[None, List[str]]=None
			) -> CampoPozos:
		#-----------------------------
		# Filtrado de pozos
		#-----------------------------
		if filtro_clusters is None:
			filtro_clusters = list()
		if filtro_pozos is not None:
			# Encuentra clusters de los pozos dados
			filtro_pozos = self.auditar_filtro(filtro_pozos)
			pozos = sorted(list(self.cluster_de_pozo.keys()))
			pozos_no_conocidos = [pozo for pozo in filtro_pozos if pozo not in pozos]
			if len(pozos_no_conocidos) > 0:
				print('Atención: los siguientes pozos no están en el campo')
				for pozo in pozos_no_conocidos:
					print('\t', pozo)
				filtro_pozos = [pozo for pozo in filtro_pozos if pozo not in pozos_no_conocidos]
			assert(len(filtro_pozos) > 0)
			if self.debug:
				print('')
				print('Pozos en filtro:')
				for pozo in filtro_pozos:
					print('\t', pozo)
			clusters = [self.cluster_de_pozo[pozo] for pozo in filtro_pozos]
			filtro_clusters += clusters
		#-----------------------------
		# Filtra clusters
		#-----------------------------
		filtro_clusters = self.auditar_filtro(filtro_clusters)
		assert(len(filtro_clusters) > 0)
		if 'bodega_00' not in filtro_clusters: 
			filtro_clusters.insert(0, 'bodega_00')
		clusters = [cluster for cluster in campo.clusters if cluster.nombre in filtro_clusters]
		# Filtra pozos en clusters
		clusters_sin_pozo = list()
		if filtro_pozos is not None:
			for cluster in clusters:
				pozos = [pozo for pozo in cluster.pozos if pozo.nombre in filtro_pozos]
				if len(pozos) == 0 and cluster.nombre != 'bodega_00':
					clusters_sin_pozo.append(cluster.nombre)
				else:
					cluster.pozos = pozos
		clusters = [cluster for cluster in clusters if cluster.nombre not in clusters_sin_pozo]
		#-----------------------------
		# Actualiza registros
		#-----------------------------
		campo.clusters = clusters		
		campo.backup_clusters = deepcopy(clusters)
		campo.num_clusters = len(campo.clusters)
		campo.punto_partida = clusters[0].nombre
		campo.dict_clusters = {cluster.nombre:p for p, cluster in enumerate(campo.clusters)}
		campo.coordenadas = {cluster.nombre:cluster.coordenadas for cluster in campo.clusters}
		campo.actualizar_camiones()
		campo.backup_camiones = deepcopy(campo.camiones)
		campo.estado = campo.reset()
		campo.nS = campo.estado.shape[0]
		campo.comienzo = True # El entorno recién se inicializa
		campo.nA = campo.num_clusters * campo.num_camiones
		campo.debug = False
		campo.render_mode = 'rgb_array'
		return campo
	
	def auditar_filtro(
				self,
				filtro_clusters:List[str]
			) -> List[str]:
		clusters_auditados = list()
		for cluster in filtro_clusters:
			if ':1' in cluster:
				cluster = estandarizar_nombre(cluster)
			clusters_auditados.append(cluster)
		clusters_auditados = list(set(clusters_auditados))
		return sorted(clusters_auditados)