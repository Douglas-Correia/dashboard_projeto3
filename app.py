import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

@st.cache_data
def read_html_manual(file_content: bytes):
    # Lê todas as tabelas do conteúdo HTML
    arquivo_html = pd.read_html(file_content, header=0, skiprows=2)
    
    # Seleciona a primeira tabela lida (posição 0)
    tabela = arquivo_html[0]
    return tabela

def save_arquivo_banco(file: bytes):
    arquivo = file

# MENU SIDEBAR
with st.sidebar:
    st.subheader('Menu')
    info_processuais = st.button("Informações processuais", use_container_width=True)
    info_lotes = st.button("Consultas em lote", use_container_width=True)
    info_cadastrais = st.button("Informações cadastrais", use_container_width=True)

with st.container():
    st.header('Dashboard')

    uploaded_file = st.file_uploader("Subir arquivo", type=["htm", "html"])
    
    if uploaded_file is not None:
        bytes_data = uploaded_file.read()
        # st.write("Arquivo: ", uploaded_file.name)
        
        # Armazenando a tabela lida em st.session_state para evitar recarregamento
        if 'tables' not in st.session_state:
            st.session_state.tables = read_html_manual(bytes_data)
        
        tables = st.session_state.tables

        button_save = st.button(label="Salvar arquivo", on_click=save_arquivo_banco)
        
        options_filter = st.selectbox(
            "Selecione um filtro de preferência",
            ["TODOS", "IDOSO", "NÃO", "PESSOA COM DEFICIÊNCIA", "IDOSO, PESSOA COM DEFICIÊNCIA", "DOENÇA GRAVE"]
        )
        
        if options_filter != "TODOS":
            # Filtra a tabela com base na preferência selecionada
            filtered_table = tables[tables['PREFERÊNCIA*'] == options_filter]
        else:
            filtered_table = tables
        
        # Limita a exibição a 200 linhas após o filtro
        limited_table = filtered_table.head(200)
        
        # Exibe a tabela limitada
        st.dataframe(limited_table, width=1450, height=600)
