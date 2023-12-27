import re
import jsonlines

import polars as pl

from chaparral.mapa.convenciones import CLUSTER2MAPA


POZOS = []
for pozo in CLUSTER2MAPA.values():
    POZOS.extend(pozo.split('/'))


def estandarizar_nombre(nombre):
    nombre = nombre.\
        replace('CHICHIMENE', 'CH').\
        replace(':1', '').\
        replace('CLUSTER', 'CL')
    cluster = re.search(r'\w+-\d+(\w+)', nombre)
    if cluster:
        return cluster.group().strip()


def load_inventario(data: pl.DataFrame) -> pl.DataFrame:
    puntos = []
    for row in data.iter_rows(named=True):
        pozo = estandarizar_nombre(row['Punto'])
        if pozo:
            quimicos = row['Producto'].split()
            for quimico in quimicos:
                puntos.append({
                    'punto': pozo,
                    'quimico': quimico,
                    'nivel_actual': row['Saldo Gln'],
                    'velocidad_consumo': row['Gln/día'],
                    'dias_con_stock': row['Stock en días'],
                })
        else:
            print(f'no se halla punto {pozo}')
    return pl.DataFrame(puntos)


if __name__ == "__main__":
    file_path = '../../data/Inventario_Pozos.csv'
    status_pozos_path = '../../data/status_pozos.csv'
    out_path = '../../data/objetos_mapa/inventario.ndjson'
    df = pl.read_csv(file_path)
    status_pozos = pl.read_csv(status_pozos_path, infer_schema_length=10000)
    status_pozos = status_pozos.with_columns(pl.col('POZO').map_elements(lambda x: estandarizar_nombre(x)))
    inventario = load_inventario(df)
    print(inventario.shape)
    inventario = inventario.join(status_pozos, left_on='punto', right_on='POZO', how='outer').\
        filter(pl.col('Estado') == 'ON').drop(['CL', 'Estado'])
    print(inventario.shape)
    inventario.write_ndjson(out_path)

