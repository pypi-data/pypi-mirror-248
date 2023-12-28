import typer
from pathlib import Path

from chaparral.mapa.map_objects import Mapa


IMAGEN_PAVIMENTADA = Path('data/mapas_anotados/pavimentada_prv.png')
IMAGEN_ANGOSTA = Path('data/mapas_anotados/pavimentada_angosta_prv.png')
IMAGEN_CLUSTERS = Path('data/mapas_anotados/clusters_prv.png')
IMAGEN_SIN_PAVIMENTAR = Path('data/mapas_anotados/sin_pavimentar_prv.png')
IMAGEN_BODEGA = Path('data/mapas_anotados/bodega_prv.png')

ARCHIVO_SALIDA = 'data/objetos_mapa/objetos.ndjson'


def main(nombre_archivo: str = ARCHIVO_SALIDA):
    mapa = Mapa()
    mapa.cargar_objetos_en_imagen(IMAGEN_PAVIMENTADA, 'pavimentada')
    mapa.cargar_objetos_en_imagen(IMAGEN_ANGOSTA, 'angosta')
    mapa.cargar_objetos_en_imagen(IMAGEN_CLUSTERS, 'cluster')
    mapa.cargar_objetos_en_imagen(IMAGEN_SIN_PAVIMENTAR, 'sin_pavimentar')
    mapa.cargar_objetos_en_imagen(IMAGEN_BODEGA, 'bodega')
    for i, objeto in enumerate(mapa.objetos):
        if objeto.nombre == 'VIA_PAVIMENTADA_03':
            mapa.objetos.pop(i)
    mapa.encontrar_vecinos()
    mapa.to_json(nombre_archivo)


if __name__ == "__main__":
    typer.run(main)
