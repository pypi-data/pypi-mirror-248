import json
import os
from tqdm import tqdm

import polars as pl
import googlemaps

from chaparral.mapa.convenciones import CLUSTER2MAPA

API_KEY = os.environ['GOOGLE_API_KEY']
gmaps = googlemaps.Client(key=API_KEY)

geocodes_path = 'data/objetos_mapa/manual_geolocalizaciones.json'
geocodes = json.load(open(geocodes_path, 'r'))

vecinos_path = 'data/objetos_mapa/objetos.ndjson'
df = pl.read_ndjson(vecinos_path)


clusters = [objeto for objeto in df['nombre'].unique() if 'cluster' in objeto]
clusters.append('bodega_00')

aristas = []
for cluster in tqdm(clusters, desc='Processing vecinos'):
    cluster_nombre = CLUSTER2MAPA.get(cluster.upper(), None)
    vecinos = get_vecinos(cluster)
    if not cluster_nombre:
        print(f'No encuentro el nomber del cluster {cluster}')
        continue
    vecinos_nombres = [CLUSTER2MAPA.get(v.upper()) for v in vecinos]
    for vecino in vecinos_nombres:
        request = gmaps.distance_matrix(
            geocodes[cluster_nombre],
            geocodes[vecino],
            mode='driving',
            units='metric'
        )
        row = dict(
            src=cluster_nombre,
            trg=vecino,
            dist=request['rows'][0]['elements'][0]['distance']['value'],
            tiempo=request['rows'][0]['elements'][0]['duration']['value'],
        )
        aristas.append(row)

aristas = pl.DataFrame(aristas)
aristas.write_ndjson('data/objetos_mapa/aristas.ndjson')
print(aristas)
