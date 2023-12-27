import numpy as np
import streamlit as st
import polars as pl
import plotly.express as px

path = 'data/Inventario_Pozos.csv'
df = pl.read_csv(path)

estaciones = df['Cod.'].unique().to_list()
productos = df['Producto'].unique().to_list()

coords = df.select('Cod.').unique(). \
            with_columns([
                pl.lit(np.random.uniform(3.8925,  3.8955, len(estaciones))).alias('lat'),
                pl.lit(np.random.uniform(73.6645, 73.6675, len(estaciones))).alias('lon')
            ])

"""
⁦3°56'07"N⁩ ⁦73°40'33"W⁩
⁦3°56'04"N⁩ ⁦73°40'49"W⁩
⁦3°55'57"N⁩ ⁦73°41'14"W⁩
"""

stock_product = df. \
         select(['Producto', 'Stock en días']). \
         group_by('Producto'). \
         first(). \
         sort('Stock en días')

stock_pozos = df. \
         select(['Cod.', 'Stock en días']). \
         group_by('Cod.'). \
         first(). \
         sort('Stock en días').\
         with_columns(('Pozo_' + pl.col('Cod.').cast(str)).alias('Pozo'))

total_zero_products = stock_product.filter(pl.col('Stock en días') == 0).shape[0]
total_zero_pozos = stock_pozos.filter(pl.col('Stock en días') == 0).shape[0]

fig_low_product = px.bar(stock_product.head(10),
                         y='Producto',
                         x='Stock en días',
                         title='Productos Bajos en Stock'
                         )

fig_low_pozos = px.bar(stock_pozos.head(10),
                       y='Pozo',
                       x='Stock en días',
                       title='Pozos Bajos en Stock'
                       )

st.header('Proyecto Dist XYZ')
st.plotly_chart(fig_low_product)
st.plotly_chart(fig_low_pozos)

st.write(f'Total de productos con 0 stock: {total_zero_products}, Total de pozos con 0 stock: {total_zero_pozos}')

tab1, tab2 = st.tabs(['Todos', '0 Stock'])
with tab1:
    st.map(coords, size=1)
with tab2:
    st.map(coords.filter(stock_pozos['Stock en días'] == 0), size=1)

