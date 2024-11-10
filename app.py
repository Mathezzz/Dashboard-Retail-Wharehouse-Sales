# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 15:37:44 2024

@author: ander
"""

import streamlit as st
import pandas as pd
import plotly.express as px

# Configurações da página
st.set_page_config(layout='wide')

st.title('Vendas mensais paa análise')



# Importação dos dados em csv e limpeza
data = pd.read_csv('Retail and wherehouse Sale.csv')
data = data.dropna(how='all')
data = data.dropna(subset=['SUPPLIER', 'RETAIL SALES'])
data['RETAIL SALES'] = data['RETAIL SALES'].round(2)

# Visualizar dataframe para ajudar a construir os gráficos
# st.write(data)

# Filtros
# filtro_mes = st.sidebar.selectbox("Mês", options=data['MONTH'].unique())
# dados_filtrados = data[data['MONTH'] == filtro_mes]
## Tabelas --------------------------------------------------------------------
# Tabela 1
# Vendas totais mensal
df_vendas_mensais = data.groupby('MONTH')['RETAIL SALES'].sum().reset_index()


# Vendas mensais por distribuidor
df_vendas_por_distribuidor = data.groupby(['MONTH', 'SUPPLIER'])['RETAIL SALES'].sum().reset_index()

# Selecionar os N maiores fornecedores de cada mês
num=st.number_input(label="Quantidade de distribuidores", min_value=2, max_value=12, value=10) # Filtro não está na posição desejada, está em cima
top_fornecedores_por_mes = (df_vendas_por_distribuidor
                               .sort_values(['MONTH', 'RETAIL SALES'], ascending=[True, False])
                               .groupby('MONTH')
                               .head(num)
                               .reset_index(drop=True))


# Vendas totais por tipo de Item e mês
df_vendas_por_item = data.groupby(['MONTH', 'ITEM TYPE'])['RETAIL SALES'].sum().reset_index()

# Vendas por Item de cada distribuidor
df_item_por_distribuidor = data.groupby(['SUPPLIER', 'ITEM TYPE'])['RETAIL SALES'].sum().reset_index()




## Gráficos no Plotly ---------------------------------------------------------
# Gráfico de Vendas totais mensal
graf_vendas_mensais = px.line(df_vendas_mensais,
                              x='MONTH',
                              y='RETAIL SALES',
                              title='Vendas Mensais',
                              markers=True)

# Gráfico de vendas por distribuidor, de barras
graf_vendas_por_distribuidor = px.bar(top_fornecedores_por_mes,
                                      x='MONTH',
                                      y='RETAIL SALES',
                                      color='SUPPLIER',
                                      title=f'TOP {num} Vendas Mensais por Distribuidor')



# Gráficos para coluna 2:
# Gráfico de Vendas mensal por Tipo de Item
graf_vendas_por_item = px.line(df_vendas_por_item,
                                x='MONTH',
                                y='RETAIL SALES',
                                color='ITEM TYPE',
                                title='Vendas por Tipo de Bebida')


# Não ficou tão legal, remover depois:
filtro_fornecedor = st.multiselect(label='Fornecedor', options=df_item_por_distribuidor['SUPPLIER'].unique())
graf_item_por_distribuidor = px.bar(df_item_por_distribuidor[df_item_por_distribuidor['SUPPLIER'].isin(filtro_fornecedor)],
                                    x='RETAIL SALES',
                                    y='SUPPLIER',
                                    color='ITEM TYPE',
                                    title='Valor vendido de cada Item por Fornecedor',
                                    orientation='h')



## Visualizações no Streamlit -------------------------------------------------
# Divisão em colunas
# st.write(df_vendas_mensais)

coluna_1, coluna_2 = st.columns(2)
with coluna_1:
    st.plotly_chart(graf_vendas_mensais)
    st.plotly_chart(graf_vendas_por_distribuidor)
    st.table(pd.pivot_table(top_fornecedores_por_mes,
                            values='RETAIL SALES',
                            index='SUPPLIER',
                            columns='MONTH',
                            aggfunc='sum',
                            fill_value=0))
    
with coluna_2:
    # st.write(df_vendas_por_item)
    st.plotly_chart(graf_vendas_por_item)
    st.plotly_chart(graf_item_por_distribuidor)