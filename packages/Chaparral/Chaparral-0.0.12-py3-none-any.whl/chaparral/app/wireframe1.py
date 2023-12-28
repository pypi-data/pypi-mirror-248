import os
import re

import streamlit as st
import polars as pl
import googlemaps

from chaparral.mapa.convenciones import POZO2CLUSTER, CLUSTER2MAPA


API_KEY = os.environ['GOOGLE_API_KEY']
OBJETOS_PATH = 'data/objetos_mapa/objetos_api.ndjson'

gmaps = googlemaps.Client(key=API_KEY)
objetos = pl.read_ndjson(OBJETOS_PATH)
bodega = objetos.filter(pl.col('codigo') == 'bodega_00')[0]


def clusters_por_quimico(quimico):
    dfi = inventario.filter(pl.col('quimico') == quimico)
    # return dfi
    puntos = []
    for row in dfi.iter_rows(named=True):
        cluster = None
        if row['punto'] in POZO2CLUSTER:
            # TODO: que hacer si el punto no esta en la lista?
            cluster = POZO2CLUSTER[row['punto']]
        elif row['punto'] in CLUSTER2MAPA.values():
            cluster = row['punto']
        else:
            st.write('missing cluster info for cluster:', row['punto'])
        if cluster:
            coords = objetos.filter(pl.col('nombre') == cluster)['coords'][0]
            puntos.append(dict(
                nombre=cluster,
                stock=row['stock'],
                lat=coords[0],
                lon=coords[1]
            ))
    return pl.DataFrame(puntos)


uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    raw_inventario = pl.read_csv(uploaded_file.read())
    inventario = load_inventario(raw_inventario)
else:
    st.stop()

quimicos = sorted(inventario.filter(pl.col('stock') > 0)['quimico'].unique())
quimico = st.selectbox('Seleccione Químico', quimicos)

data = clusters_por_quimico(quimico)
if data.is_empty():
    st.stop()

data = data.sort('stock', descending=False)
st.map(data.select(['lat', 'lon']))

for row in data.iter_rows(named=True):
    st.write('distancia to bodega')
    vecinos_bodega = bodega['vecinos'].to_list()[0]
    vecino = [v for v in vecinos_bodega if v['nombre'] == row['nombre']]
    if vecino:
        row['dst'] = vecino[0]['dist']
        row['tmp'] = vecino[0]['tiempo']
    st.write(row)

