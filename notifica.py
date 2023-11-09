import streamlit as st
import pandas as pd

def importar_dados():
    xls = pd.ExcelFile('VagasEtecs.xlsx')
    df1 = pd.read_excel(xls, 'Vagas')
    df = pd.read_excel('VagasEtecs.xlsx', usecols=["CIDADE", "UNIDADE", "COMPONENTE CURRICULAR", "MATERIA"])
    return df, df1

def contar_cidades_disciplinas(df):
    contagem_cidades = df['CIDADE'].value_counts().reset_index()
    contagem_cidades.columns = ['CIDADE', 'Contagem']
    return contagem_cidades

def contar_disciplinas(df):
    contagem_componente_curricular = df['COMPONENTE CURRICULAR'].value_counts().reset_index()
    contagem_componente_curricular.columns = ['COMPONENTE CURRICULAR', 'Contador']
    return contagem_componente_curricular.sort_values(by='Contador', ascending=False).head(15)

def criar_graficos(df1, cidades_com_mais_materias):
    media_vagas = df1['CIDADE'].value_counts().mean()
    
    col1, col2, col3 = st.columns(3)
    
    col1.subheader("Distribuição de disciplinas - processo simplificado")
    city_counts = df1['CIDADE'].value_counts().head(15)
    st.bar_chart(city_counts)
    st.line_chart(media_vagas, use_container_width=True)

    col2.subheader("Top 15 Disciplinas Mais Ofertadas")
    subject_counts = dados_agrupados.sum(axis=1).head(15)
    st.bar_chart(subject_counts)

    col3.subheader("15 + cidades com editais abertos")
    st.bar_chart(cidades_com_mais_materias)

df, df1 = importar_dados()
contagem_cidades = contar_cidades_disciplinas(df)
contagem_componente_curricular = contar_disciplinas(df)
dados_agrupados = df.groupby(['CIDADE', 'MATERIA']).size().unstack().fillna(0)
dados_agrupados['Total'] = dados_agrupados.sum(axis=1)
cidades_mais_materias = dados_agrupados.sort_values(by='Total', ascending=False)
cidades_com_mais_materias = cidades_mais_materias.head(15)

st.set_page_config(page_title="Dashboard", layout="wide", initial_sidebar_state="expanded")
st.title("Dashboard de Análise de Dados")
st.info('Total Cidades', icon="📌")
st.metric("TOTAL DE VAGAS: QUANTIDADE DE EDITAIS PUBLICADOS", df1["CIDADE"].count())

with st.expander("⏰ Lista das Vagas Excel"):
    showData = st.multiselect('Filter: ', df1.columns, default=["UNIDADE", "CIDADE", "COMPONENTE CURRICULAR"])
    st.dataframe(df[showData], use_container_width=True)

st.subheader("Observações e Resultados")
st.write("""
Essas análises fornecem insights valiosos para a gestão e tomada de decisões da instituição de ensino técnico. Com base nos resultados apresentados, a instituição pode considerar estratégias para distribuir vagas de forma mais equitativa entre as cidades ou investigar a demanda por disciplinas menos ofertadas. Além disso, o conhecimento do prazo médio de inscrição pode ajudar na otimização dos recursos e no planejamento de cursos.
Esses insights são essenciais para garantir que a instituição atenda eficazmente às necessidades dos alunos e que a oferta de cursos seja alinhada com a demanda, contribuindo para uma experiência educacional mais eficiente e satisfatória.
""")
