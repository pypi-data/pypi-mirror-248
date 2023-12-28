'''
© Copyright ArdillaByte Inc. 2023

-----------------------------------------------
Clase para crear el espacio de estados de 
búsqueda de rutas.
-----------------------------------------------
'''
from pathlib import Path
import pandas as pd
from typing import List, Dict, Optional, Tuple, Union
from itertools import product
from collections import defaultdict
import json
from tqdm.auto import tqdm

from chaparral.mapa.espacio_rutas import RutasClusters
from chaparral.modelos.constantes import ESCALA_TIEMPO_RUTA


class CreadorEspacioRutas :
	"""Clase para crear un espacio de estados para las rutas"""
	def __init__(
				self,
				nombre_archivo_clusters:str
			) -> None:
		# -------------------------------
		# Registros de directorios
		# -------------------------------
		self.directorio = Path.cwd() / Path('..').resolve() / Path('data', 'objetos_mapa')
		# self.directorio.mkdir(parents=False, exist_ok=True)
		# -------------------------------
		# Registros de archivos
		# -------------------------------
		self.nombre_archivo_clusters = nombre_archivo_clusters
		# -------------------------------
		# Registro de datos
		# -------------------------------
		self.data = None
		self.verbose = False
	
	def crear(self) -> RutasClusters:
		# Cargar datos desde archivo
		self.cargar_datos()
		# Crea las rutas
		rutas = dict()
		# Crea las coordenadas
		coordenadas = dict()
		# Crea los tiempo_desplazamiento
		tiempo_desplazamiento = dict()
		# Iteramos sobre los registos
		for index, linea in self.data.iterrows():
			rutas[linea.nombre] = self.obtener_vecinos(linea)
			coordenadas[linea.nombre] = linea.coords
			tiempo_desplazamiento[linea.nombre] = self.obtener_tiempos(linea)
		espacio = RutasClusters(
			cluster_inicial='',
			cluster_objetivo='',
			rutas=rutas,
			coordenadas=coordenadas,
			tiempo_desplazamiento=tiempo_desplazamiento
		)
		return espacio 
	
	def cargar_datos(self) -> None:
		ruta_archivo = self.directorio / Path(self.nombre_archivo_clusters)
		self.data = pd.read_json(ruta_archivo, lines=True)
		if self.verbose:
			print('')
			print(f'Datos cargados con éxito desde archivo.\n\t({ruta_archivo})')
	
	def obtener_vecinos(self, datos:pd.Series) -> List[str]:
		vecinos = list()
		vecinos_ = datos.vecinos
		for vecino in vecinos_:
			vecinos.append(vecino['nombre'])
		return vecinos
	
	def obtener_tiempos(self, datos:pd.Series) -> List[str]:
		tiempo_desplazamiento = dict()
		vecinos = datos.vecinos
		for vecino in vecinos:
			tiempo_desplazamiento[vecino['nombre']] = vecino['tiempo'] * ESCALA_TIEMPO_RUTA
		return tiempo_desplazamiento


class CreadorBaseRutas:
	"""
	Clase para crear la base de datos de las rutas
	de cluster a cluster
	"""
	def __init__(
				self,
				nombre_archivo:str
			) -> None:
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
		self.nombre_archivo = nombre_archivo
		# -------------------------------
		# Registros de datos
		# -------------------------------
		self.base_rutas = defaultdict(dict)
		self.verbose = True
		self.errors_log = list()

	def crear_base_rutas(self):
		creador = CreadorEspacioRutas(
			nombre_archivo_clusters='objetos_api.ndjson'
		)
		# Creamos el espacio de estados
		espacio = creador.crear()
		# Creamos las parejas de clusters
		clusters = list(espacio.rutas.keys())
		parejas = product(clusters, repeat=2)
		parejas = [pareja for pareja in parejas if pareja[0] != pareja[1]]
		# Iteramos sobre las parejas para encontrar
		# la ruta más corta
		for pareja in tqdm(parejas):
			cluster_desde, cluster_a = pareja
			espacio.cluster_inicial = cluster_desde
			espacio.cluster_objetivo = cluster_a
			ruta = espacio.A_star(W=1)
			if ruta is not None:
				self.base_rutas[cluster_desde][cluster_a] = ruta.costo_camino
			else:
				mensaje = f'Clusters {cluster_desde} y {cluster_a} no están conectados.'
				self.errors_log.append(mensaje)
		# Guardamos base a archivo
		self.guardar()
		# Guardamos log de errores
		json_object = json.dumps(self.errors_log, indent=4)
		nombre_archivo_log = self.directorio_log / Path('rutas_log.json')
		with open(nombre_archivo_log, "w") as outfile:
			outfile.write(json_object)
		if self.verbose:
			print(f'Log de errores guardado en:\n\t{nombre_archivo_log}')

	def guardar(
				self, 
				file:Optional[Union[None, str]]=None
			) -> None:
		nombre_archivo = self.directorio / Path('rutas.json')
		with open(nombre_archivo, "w") as outfile:
			json.dump(self.base_rutas, outfile)
		if self.verbose:
			print(f'Base de datos de rutas guardadas en:\n\t{nombre_archivo}')