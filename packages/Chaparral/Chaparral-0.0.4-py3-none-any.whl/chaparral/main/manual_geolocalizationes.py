import os
from tqdm import tqdm

import googlemaps
import polars as pl

from chaparral.mapa.convenciones import CLUSTER2MAPA, POZO2CLUSTER

API_KEY = os.environ['GOOGLE_API_KEY']
gmaps = googlemaps.Client(key=API_KEY)
objetos = pl.read_ndjson('data/objetos_mapa/objetos.ndjson')
obj_coords = pl.read_ndjson('data/objetos_mapa/obj_coords.ndjson')


def get_vecinos(df, cluster, iter=0) -> set:
    """Encuentra los clusteres vecinos al target cluster.
    Argument:
        df: dataframe con informacion de los objetos cargados en el mapa.
        cluster: el cluster target.
    """
    if cluster not in df['nombre']:
        raise ValueError(f'Objeto {cluster} not in list')
    cl_info = df.select(['nombre', 'vecinos']).filter(pl.col('nombre') == cluster).row(0, named=True)
    vecinos = cl_info['vecinos']
    results = []
    for vecino in vecinos:
        if 'cluster' not in vecino and 'bodega' not in vecino:
            if iter < 2:
                segundos = get_vecinos(df, vecino, iter + 1)
                results.extend([v for v in segundos if 'cluster' in v])
        else:
            results.append(vecino)
    return set([v for v in results if v != cluster])


results = []
for objeto in objetos.iter_rows(named=True):
    tipo = objeto['tipo']
    if 'CLUSTER' in tipo:
        nombre = CLUSTER2MAPA[objeto['nombre'].upper()]
    elif 'BODEGA' in tipo:
        nombre = 'bodega_00'
    else:
        continue
    codigo = objeto['nombre']
    pozos = [k for k, v in POZO2CLUSTER.items() if v == nombre]
    vecinos = [CLUSTER2MAPA[vecino.upper()] if vecino.startswith('cluster') else CLUSTER2MAPA[vecino]
               for vecino in get_vecinos(objetos, codigo)]
    coords = obj_coords.filter(pl.col('nombre') == nombre).select(['lat', 'lon'])[0].to_dict()
    row = dict(
        nombre=nombre,
        codigo=codigo,
        tipo=tipo,
        vecinos=vecinos,
        pozos=pozos,
        coords=(coords['lat'][0], coords['lon'][0]),
    )
    results.append(row)

results = pl.DataFrame(results)

final = []
pbar = tqdm(total=len(results), desc='Adquiriendo aristas')
for row in results.iter_rows(named=True):
    new_vecinos = []
    for vecino in row['vecinos']:
        vecino_coords = results.filter(pl.col('nombre') == vecino).row(0, named=True)['coords']
        request = gmaps.distance_matrix(
            tuple(row['coords']),
            tuple(vecino_coords),
            mode='driving',
            units='metric'
        )
        if request['rows'][0]['elements'][0]['distance']['value'] == 0:
            print((row['nombre'], row['coords']), (vecino, vecino_coords), request)
        vecino_row = dict(
            nombre=vecino,
            dist=request['rows'][0]['elements'][0]['distance']['value'],
            tiempo=request['rows'][0]['elements'][0]['duration']['value'],
        )
        new_vecinos.append(vecino_row)
    row['vecinos'] = new_vecinos
    final.append(row)
    pbar.update(1)

final = pl.DataFrame(final)
final.write_ndjson('data/objetos_mapa/objetos_api.ndjson')
print(final)
