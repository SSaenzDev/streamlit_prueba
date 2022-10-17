###Links
#https://coderzcolumn.com/tutorials/data-science/cufflinks-how-to-create-plotly-charts-from-pandas-dataframe-with-one-line-of-code#2
#https://coderzcolumn.com/tutorials/data-science/build-dashboard-using-streamlit-and-cufflinks
#https://coderzcolumn.com/tutorials/data-science/cufflinks-how-to-create-plotly-charts-from-pandas-dataframe-with-one-line-of-code#2

#Imports
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
import cufflinks as cf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
#Setttings


#Carga de datos
st.set_page_config(page_title='Reporte Diario ADIS',
                   layout='wide')
df = pd.read_excel(r'D:\Users\ssaenz\Mis documentos\Sofia\datasets\ADIS\Book1.xlsx')
df = df.replace(r"_x000D_\n", ' ', regex=True)


#Filtros
estado_ot = st.sidebar.multiselect(
    'Estado OT:',
    options= df['ESTADO_OT'].unique(),
    default= df['ESTADO_OT'].unique()
)
df_selection = df.query(
    'ESTADO_OT == @estado_ot'
    
)



#Datos
ACTIVOS = df[df['ACTIVO_ESTADO']==1]
TOTAL_OT = len(ACTIVOS)

OT_ESTADOS = ACTIVOS['ESTADO_OT']
SOLICITANTE = ACTIVOS['SIGLA_SOLICITANTE'] 


df_estados = pd.DataFrame(OT_ESTADOS.value_counts())
df_estados = df_estados.reset_index()

df_sigla = pd.DataFrame(SOLICITANTE.value_counts())
df_sigla = df_sigla.reset_index()

#Graficos
# plt.pie(OT_ESTADOS)
# my_circle=plt.Circle( (0,0), 0.7, color='white')
# p=plt.gcf()
# p.gca().add_artist(my_circle)

# This dataframe has 244 lines, but 4 distinct values for `day`



#Armado
st.title('Reporte Diario ADIS')
st.metric(label='TOTAL_OT', value= TOTAL_OT )
st.header('Tabla de OT')
st.dataframe(df_selection)


bar_fig = px.bar(
        df_sigla,
        x='index',
        y="SIGLA_SOLICITANTE",
        title="<b>OT por Sigla Solicitante</b>",
        color_discrete_sequence=["#0083B8"] * len(df_sigla),
        template="plotly_white"
)


pie_fig = df_estados.iplot(kind="pie", labels="index", values="ESTADO_OT",
                         title="<b>OT por Estados<b>",
                         asFigure=True,
                        hole=0.4)


col1, col2 = st.columns(2)
col1.plotly_chart(bar_fig, use_container_width=True)
col2.plotly_chart(pie_fig, use_container_width=True)