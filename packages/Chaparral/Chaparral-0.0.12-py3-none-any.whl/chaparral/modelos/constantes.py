'''
© Copyright ArdillaByte Inc. 2023

-----------------------------------------------
Define las constantes de información particular
de los clusters para usan en las varias clases.
-----------------------------------------------
'''

# Define el ruido a incluir en el tensor de estado
# para facilitar el aprendizaje de la red neuronal
RUIDO = 0
# Define qué tanto se multiplica el excedente en días
# de cada químico en cada pozo al finalizar el episodio
FACTOR_RECOMPENSA = 1e-3

# Define la recompensa por movimiento no permitido
RECOMPENSA_MOVIMIENTO_NO_PERMITIDO = -100

# Define el número de turnos para regresar a la bodega
HORAS_HABILES = 10
PENALIZACION_PASADAS_HORAS_HABILES = -100

# Define la capacidad del camion
NUM_BULKDRUMS = 8
NIVEL_MAXIMO_BULKDRUM = 250

# Define qué cantidad de días en excedente debe haber
# de cada químico en cada pozo para evitar penalización
VALOR_CRITICO_CARGA = 8 # usado para el cálculo de cuanto cargar en pozo
VALOR_CRITICO_TOLERANCIA = 0.75 * VALOR_CRITICO_CARGA # usado para el cálculo de la recompensa

# Define el tiempo de preparación para cargar un químico en un pozo
TIEMPO_DESCARGA = 1 / 60 * 25

# Define el escalamiento de la velocidad de consumo de un químico
# para pasar de la info suministrada (Gl/día) a la usada en el
# entorno (Gl/h)
ESCALA_VELOCIDAD_CONSUMO = 1 / 24

# Define el escalamiento de la velocidad del camión para pasar
# de la info suministrada (????/milisegundos) a la usada en el
# entorno (kh/h)
ESCALA_VELOCIDAD_CAMION = 1

# Define el escalamiento del tiempo de ruta
ESCALA_TIEMPO_RUTA = 1 / (60 * 60)

# Define el escalamiento para el render
FACTOR_RENDER_X = 2
FACTOR_RENDER_Y = 15
MEDIA_X = 3.9313048491215072
DESVEST_X = 0.019056068943662685
MEDIA_Y = -73.69699527751696
DESVEST_Y = 0.026686490709401194