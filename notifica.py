import streamlit as st
import pandas as pd
import folium
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import matplotlib.pyplot as plt

# Configuração da página
st.set_page_config(page_title="Dashboard", layout="wide", initial_sidebar_state="expanded")

# Carregando o arquivo Excel
xls = pd.ExcelFile('VagasEtecs.xlsx')

# Lendo cada aba (sheet) em um DataFrame
df1 = pd.read_excel(xls, 'Vagas')
# Carregando os dados desejados do arquivo Excel
df = pd.read_excel('VagasEtecs.xlsx', usecols=["CIDADE", "UNIDADE", "COMPONENTE CURRICULAR", "MATERIA"])
#df2 = pd.read_excel(xls, 'Cidades')
# Agrupe os dados por cidade e disciplina e conte o número de disciplinas em cada cidade
dados_agrupados = df.groupby(['CIDADE', 'MATERIA']).size().unstack().fillna(0)

# Exibição de KPIs
st.info('Total Cidades', icon="📌")
st.metric("TOTAL DE VAGAS: QUANTIDADE DE EDITAIS PUBLICADOS", df1["CIDADE"].count())

# Lista dos Aprovados Excel
with st.expander("⏰ Lista das Vagas Excel"):
    showData = st.multiselect('Filter: ', df1.columns, default=["UNIDADE", "CIDADE", "COMPONENTE CURRICULAR"])
    st.dataframe(df[showData], use_container_width=True)


# Use o método 'value_counts' para contar a frequência de cada cidade
contagem_cidades = df1['CIDADE'].value_counts()

# 'contagem_cidades' agora é uma série que contém a contagem de registros para cada cidade

# Se você quiser converter isso de volta para um DataFrame, pode fazer o seguinte:
df_contagem_cidades = contagem_cidades.reset_index()
df_contagem_cidades.columns = ['CIDADE', 'Contagem']
df2 = df_contagem_cidades
# Calcula a média das vagas
media_vagas = df2['Contagem'].mean()
# Agora 'df_contagem_cidades' contém as cidades e a contagem de registros para cada cidade
contagem_componente_curricular = df1['COMPONENTE CURRICULAR'].value_counts()

# 'contagem_cidades' agora é uma série que contém a contagem de registros para cada cidade

# Se você quiser converter isso de volta para um DataFrame, pode fazer o seguinte:
df_componente_curricular = contagem_componente_curricular.reset_index()
df_componente_curricular.columns = ['COMPONENTE CURRICULAR', 'Contador']
df_componente_curricular = df_componente_curricular.sort_values(by='Contador', ascending=False)
df_componente_curricular =df_componente_curricular.head(15)

# Crie duas colunas, uma para cada gráfico
col1, col2 = st.columns(2)

# Título do Dashboard
st.title("Dashboard de Análise de Dados")

# Gráfico de Barras das Cidades
col1.subheader("Distribuição de disciplinas - processo simplificado")
fig_cidades = plt.figure()
plt.bar(df2.head(15)['CIDADE'], df2.head(15)['Contagem'])
plt.axhline(y=media_vagas, color='r', linestyle='--', label=f'Média ({media_vagas:.2f})')
plt.xlabel('Cidade')
plt.ylabel('Vagas Oferecidas')
plt.title('disciplinas ofertadas e Linha Média')
plt.xticks(rotation=90)  # Rotaciona os rótulos do eixo x para melhor legibilidade
col1.pyplot(fig_cidades)

# Gráfico de Barras das Disciplinas
col2.subheader("Top 15 Disciplinas Mais Ofertadas")
fig_disciplinas = plt.figure()
plt.scatter(df_componente_curricular['COMPONENTE CURRICULAR'], df_componente_curricular['Contador'])
plt.xlabel('COMPONENTE CURRICULAR')
plt.ylabel('Número de Vagas')
plt.title('Distribuição de Vagas por Componente Curricular')
plt.xticks(rotation=90)  # Rotaciona os rótulos do eixo x para melhor legibilidade
col2.pyplot(fig_disciplinas)

    
# Carregue suas imagens
imagem1 = 'grafico.png'
imagem2 = 'mapa.png'

# Crie duas colunas para as imagens
col1, col2 = st.columns(2)

# Adicione as imagens às colunas
col1.image(imagem1, caption='gráfico: as 15 + por ofertas de vagas', use_column_width=True)
col2.image(imagem2, caption='Mapa: cidades com mais editais abertos', use_column_width=True)

# Observações e Resultados
st.subheader("Observações e Resultados")
st.write("""
Essas análises fornecem insights valiosos para a gestão e tomada de decisões da instituição de ensino técnico. Com base nos resultados apresentados, a instituição pode considerar estratégias para distribuir vagas de forma mais equitativa entre as cidades ou investigar a demanda por disciplinas menos ofertadas. Além disso, o conhecimento do prazo médio de inscrição pode ajudar na otimização dos recursos e no planejamento de cursos.
Esses insights são essenciais para garantir que a instituição atenda eficazmente às necessidades dos alunos e que a oferta de cursos seja alinhada com a demanda, contribuindo para uma experiência educacional mais eficiente e satisfatória.
""")


