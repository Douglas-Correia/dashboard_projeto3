import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# Configuração da página
st.set_page_config(layout="wide")

# Função para converter datas no formato ISO 8601 para o formato brasileiro
def formatar_data(data_iso):
    try:
        data_obj = datetime.fromisoformat(data_iso.replace("Z", "+00:00"))
        return data_obj.strftime("%d/%m/%Y %H:%M:%S")
    except ValueError:
        return data_iso

# Função para ler e processar tabelas de um arquivo HTML
@st.cache_data
def read_html_manual(file_content: bytes):
    arquivo_html = pd.read_html(file_content, header=0, skiprows=2)
    tabela = arquivo_html[0]
    return tabela

# Função para salvar o arquivo no banco (placeholder)
def save_arquivo_banco(file: bytes):
    arquivo = file

# URL da API e cabeçalho de autorização
api_url = "https://api-publica.datajud.cnj.jus.br/api_publica_trf1/_search"
headers = {
    "Authorization": "APIKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw==",
    "Content-Type": "application/json"
}

# MENU SIDEBAR
# with st.sidebar:
#     st.subheader('Menu')
#     info_processuais = st.button("Informações processuais", use_container_width=True)
#     info_lotes = st.button("Consultas em lote", use_container_width=True)
#     info_cadastrais = st.button("Informações cadastrais", use_container_width=True)

# CONTAINER PRINCIPAL
with st.container():
    st.header('Dashboard')

    # Upload e exibição de arquivo HTML
    uploaded_file = st.file_uploader(label="Subir arquivo", type=["htm", "html", "pdf"])
    
    if uploaded_file is not None:
        bytes_data = uploaded_file.read()
        
        if 'tables' not in st.session_state:
            st.session_state.tables = read_html_manual(bytes_data)
        
        tables = st.session_state.tables

        options_filter = st.selectbox(
            "Selecione um filtro de preferência",
            ["TODOS", "IDOSO", "NÃO", "PESSOA COM DEFICIÊNCIA", "IDOSO, PESSOA COM DEFICIÊNCIA", "DOENÇA GRAVE"]
        )
        
        if options_filter != "TODOS":
            filtered_table = tables[tables['PREFERÊNCIA*'] == options_filter]
        else:
            filtered_table = tables
        
        limited_table = filtered_table.head(200)
        
        st.dataframe(limited_table, width=1000, height=600)
        
    # Campo de busca para o número do processo
    numero_processo = st.text_input("Digite o número do processo")

    if st.button("Buscar processo"):
        # Verifica se o número do processo foi fornecido
        if numero_processo:
            # Corpo da solicitação para a API
            payload = {
                "query": {
                    "match": {
                        "numeroProcesso": numero_processo
                    }
                }
            }

            # Realiza a requisição POST para a API
            response = requests.post(api_url, headers=headers, json=payload)
            
            # Verifica se a requisição foi bem-sucedida
            if response.status_code == 200:
                data = response.json()
                hits = data.get("hits", {}).get("hits", [])
                
                if hits:
                    processo = hits[0]["_source"]
                    
                    st.subheader(f"Processo: {processo['numeroProcesso']}")
                    st.write(f"Classe: {processo['classe']['nome']}")
                    st.write(f"Sistema: {processo['sistema']['nome']}")
                    st.write(f"Formato: {processo['formato']['nome']}")
                    st.write(f"Tribunal: {processo['tribunal']}")
                    st.write(f"Data da última atualização: {formatar_data(processo['dataHoraUltimaAtualizacao'])}")
                    st.write(f"Grau: {processo['grau']}")
                    
                    st.subheader("Movimentos")
                    for movimento in processo.get("movimentos", []):
                        st.write(f"{formatar_data(movimento['dataHora'])}: {movimento['nome']}")
                else:
                    st.warning("Nenhum processo encontrado para o número fornecido.")
            else:
                st.error(f"Erro na requisição: {response.status_code}")
        else:
            st.warning("Por favor, insira um número de processo válido.")
