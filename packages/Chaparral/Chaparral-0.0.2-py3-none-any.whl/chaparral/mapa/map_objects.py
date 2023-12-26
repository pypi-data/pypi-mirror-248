# copyright ardillabyte.com 2023

import itertools
from tqdm import tqdm
from dataclasses import dataclass
from typing import Tuple, List, Optional, Sequence, Dict
from enum import Enum
from pathlib import Path
import jsonlines

import numpy as np
from numpy import ndarray
import cv2 as cv
from cv2 import Mat

GREEN_LOW = np.array((42, 193, 243))
GREEN_HIGH = np.array((49, 199, 253))

ERODE_SIZE = 5
DILATE_SIZE = 10
SHAPE = cv.MORPH_ELLIPSE


def get_structuring_element(size: int, shape=SHAPE):
    return cv.getStructuringElement(shape,
                                    (2 * size + 1, 2 * size + 1),
                                    (size, size))


ERODE_ELEMENT = get_structuring_element(ERODE_SIZE)
DILATE_ELEMENT = get_structuring_element(DILATE_SIZE)


class ObjetoTipo(Enum):
    CLUSTER = 'cluster'
    VIA_PAVIMENTADA = 'pavimentada'
    VIA_PAVIMENTADA_ANGOSTA = 'angosta'
    VIA_SIN_PAVIMENTAR = 'sin_pavimentar'
    BODEGA = 'bodega'

    def __repr__(self):
        return self.name


@dataclass
class ObjetoMapa:
    """Objeto en el mapa."""
    nombre: str
    tipo: str
    contorno: List[Tuple[int, int]]
    vecinos: list = None

    def __repr__(self):
        return self.nombre


@dataclass
class Arista:
    nombre: str
    dist: float

    def __repr__(self):
        return f'{self.nombre} {self.dist}'


class Mapa:
    def __init__(self):
        self.objetos: Optional[List[ObjetoMapa]] = None
        self.mapa = None

    def cargar_objetos_en_imagen(self, img_path: Path, tipo: str, factor=4):
        tipo = [o for o in ObjetoTipo if tipo == o.value]
        if tipo:
            tipo = tipo[0]
        else:
            raise ValueError(f'Tipo {tipo} not recognized.')
        objetos = self._encontrar_objetos(img_path, factor)
        objetos_mapa = []
        for i, objeto in enumerate(objetos):
            objetos_mapa.append(
                ObjetoMapa(
                    nombre=f'{tipo.value}_{i:02d}',
                    tipo=tipo.name,
                    contorno=[self._encontrar_centro(objeto)]
                    if tipo.value in ['cluster', 'bodega']
                    else objeto.tolist(),
                )
            )
        if self.objetos is None:
            self.objetos = objetos_mapa
        else:
            self.objetos.extend(objetos_mapa)

    def encontrar_vecinos(self, limite: int = 30):
        for a in tqdm(self.objetos, desc='Encontrando Vecinos'):
            if a.vecinos is None:
                a.vecinos = []
            for b in tqdm(self.objetos, desc=f'encontrando vecinos de {a.nombre}'):
                if a != b:
                    arista_minima = self._encontrar_distancia_minima(a, b)
                    if arista_minima.dist < limite:
                        a.vecinos.append(arista_minima.nombre)

    def to_json(self, nombre_archivo: str):
        with jsonlines.open(nombre_archivo, 'w') as writer:
            for objeto in self.objetos:
                writer.write([objeto.__dict__])

    def _encontrar_objetos(self, img_path: Path, factor: int) -> Sequence[Mat]:
        if not img_path.exists():
            raise ValueError(f'No se encuentra el archivo {img_path}')
        img = cv.imread(str(img_path))
        if img is not None:
            hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
            mask = cv.inRange(hsv, GREEN_LOW, GREEN_HIGH)
            mask = cv.erode(mask, ERODE_ELEMENT)
            mask = cv.dilate(mask, DILATE_ELEMENT)
            mask = cv.resize(mask, (int(mask.shape[0] / factor), int(mask.shape[1] / factor)))
            if self.mapa is None:
                self.mapa = mask
            else:
                self.mapa += mask
            contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
            return contours

    def _encontrar_distancia_minima(self, c1: ObjetoMapa, c2: ObjetoMapa) -> Arista:
        puntos = list(itertools.product(c1.contorno, c2.contorno))
        distancias = [
            Arista(
                nombre=c2.nombre,
                dist=self._medir_distancia(a, b)
            )
            for a, b in puntos]
        return min(distancias, key=lambda x: x.dist)

    @staticmethod
    def _medir_distancia(a: Tuple[int, int], b: Tuple[int, int]) -> float:
        if not isinstance(a, ndarray):
            a = np.array(a)
        if not isinstance(b, ndarray):
            b = np.array(b)
        return np.sqrt(np.sum((a - b) ** 2))

    @staticmethod
    def _encontrar_centro(objeto) -> Tuple[int, int]:
        x, y = objeto.mean(axis=0)[0]
        return int(x), int(y)
