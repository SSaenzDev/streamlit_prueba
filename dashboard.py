###Links
#https://shareplum.readthedocs.io/en/latest/
#https://shareplum.readthedocs.io/en/latest/files.html#id1
#https://coderzcolumn.com/tutorials/data-science/cufflinks-how-to-create-plotly-charts-from-pandas-dataframe-with-one-line-of-code#2
#https://coderzcolumn.com/tutorials/data-science/build-dashboard-using-streamlit-and-cufflinks
#https://coderzcolumn.com/tutorials/data-science/cufflinks-how-to-create-plotly-charts-from-pandas-dataframe-with-one-line-of-code#2

#Imports
import pandas as pd
import plotly.express as px
import streamlit as st
import cufflinks as cf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from io import StringIO
from shareplum import Site
from shareplum import Office365
from shareplum.site import Version


#Setttings API
authcookie = Office365('https://avicolasofia.sharepoint.com/', 
                       username='sebastian.saenz@mamayatech.com', password='Avicola2022').GetCookies()
site = Site('https://avicolasofia.sharepoint.com/sites/SOLUCIONESBIYANALITICA/',version=Version.v365, authcookie=authcookie)
folder = site.Folder('Documentos%20compartidos/ADIS')
df_raw = folder.get_file('TABLA_OTS_APP_streamlit.txt')


## Bytes to CSV
s=str(df_raw,'utf-8')
data = StringIO(s) 
df=pd.read_csv(data, sep=';', header=0)



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
df_estados = df_estados.rename(columns={'index':'ESTADOS'})


df_sigla = pd.DataFrame(SOLICITANTE.value_counts())
df_sigla = df_sigla.reset_index()
df_sigla = df_sigla.rename(columns={'index':'SIGLAS', 'SIGLA_SOLICITANTE':''})



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
        x='SIGLAS',
        y='',
        title="<b>OT por Sigla Solicitante</b>",
        color_discrete_sequence=["#0083B8"] * len(df_sigla),
        template="plotly_white"
)


pie_fig = df_estados.iplot(kind="pie", labels="ESTADOS", values="ESTADO_OT",
                         title="<b>OT por Estados<b>",
                         asFigure=True,
                        hole=0.4)


col1, col2 = st.columns(2)
col1.plotly_chart(bar_fig, use_container_width=True)
col2.plotly_chart(pie_fig, use_container_width=True)
