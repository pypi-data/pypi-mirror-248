import json
import os

import googlemaps

from chaparral.mapa.convenciones import CLUSTER2MAPA

API_KEY = os.environ['GOOGLE_API_KEY']
gmaps = googlemaps.Client(key=API_KEY)

# Geocoding an address
ADDRESS = 'Cluster {cluster} Estación Chichimene, Acacías, Meta, Colombia'

geolocalizaciones = {}
for pozo in CLUSTER2MAPA.values():
    cluster = ADDRESS.format(cluster=pozo)
    geocode_result = gmaps.geocode(cluster)
    coords = geocode_result[0]['geometry']['location']
    geolocalizaciones[pozo] = coords

output_file_path = 'data/objetos_mapa/manual_geolocalizaciones.json'
json.dump(geolocalizaciones, open(output_file_path, 'w'), indent=4)

if __name__ == '__main__':
    pass
