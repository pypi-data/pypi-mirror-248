'''
© Copyright ArdillaByte Inc. 2023

-----------------------------------------------
Class to XXXX.
-----------------------------------------------
'''


NOMBRES_CLUSTERS = ['bodega_00', 'A', 'B', 'C']

DATOS_RUTAS = {
	'Bodega <-> A':{
        'longitud':2,
        'velocidad_promedio':2
    },
	'A <-> Bodega':{
        'longitud':2,
        'velocidad_promedio':2
    },
#
	'Bodega <-> C':{
        'longitud':4,
        'velocidad_promedio':1
    },
	'C <-> Bodega':{
        'longitud':4,
        'velocidad_promedio':1
    },
#
	'A <-> B':{
        'longitud':2,
        'velocidad_promedio':2
    },
	'B <-> A':{
        'longitud':2,
        'velocidad_promedio':2
    },
#
	'B <-> C':{
        'longitud':2,
        'velocidad_promedio':2
    },
	'C <-> B':{
        'longitud':2,
        'velocidad_promedio':2
    },
}

#C = Cluster(
#    nombre='C',
#    activo=False,
#    quimicos=[xyz],
#    niveles_actuales=[0],
#    velocidades_consumo=[0],
#    coordenadas=(-236.3568539525139, 115.90576491902122),
#    vecinos=['bodega_00', 'B'],
#)
