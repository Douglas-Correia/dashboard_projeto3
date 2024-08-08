import streamlit as st
import pandas as pd
import requests
from datetime import datetime
from io import StringIO
from utils import extrair_numeros
from urls import justica_do_trabalho, justica_federal, tribunais_superiores, justica_eleitoral, justica_militar, justica_estadual

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
def read_html_manual(file_content: str):
    # Use StringIO para tratar a string como um arquivo
    arquivo_html = pd.read_html(StringIO(file_content), header=0, skiprows=2)
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

# CONTAINER PRINCIPAL
with st.container():
    st.header('Dashboard')

    # Nome do arquivo HTML a ser carregado
    file_path = "precatórios_federais_alimentares_orçamento_2025.htm"
    
    # Ler o arquivo HTML
    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()
    
    # Verificar se as tabelas já estão no estado da sessão
    if 'tables' not in st.session_state:
        st.session_state.tables = read_html_manual(file_content)
    
    tables = st.session_state.tables
    
    # Opções de filtro
    options_filter = st.selectbox(
        "Selecione um filtro de preferência",
        ["TODOS", "IDOSO", "NÃO", "PESSOA COM DEFICIÊNCIA", "IDOSO, PESSOA COM DEFICIÊNCIA", "DOENÇA GRAVE"]
    )
    
    # Filtrar a tabela com base na opção selecionada
    if options_filter != "TODOS":
        filtered_table = tables[tables['PREFERÊNCIA*'] == options_filter]
    else:
        filtered_table = tables
    
    # Limitar a tabela a 200 linhas
    limited_table = filtered_table.head(200)
    
    # Exibir a tabela no Streamlit
    st.dataframe(limited_table, width=1000, height=600)
        
    # Seletor de tipo de tribunal
    tipo_tribunal = st.selectbox(
        "Selecione o tipo de tribunal",
        ["Tribunais Superiores", "Justiça Federal", "Justiça Estadual", "Justiça do Trabalho", "Justiça Eleitoral", "Justiça Militar"]
    )

    # Seletor de tribunal específico com base no tipo escolhido
    if tipo_tribunal == "Tribunais Superiores":
        tribunal_escolhido = st.selectbox("Selecione o tribunal", list(tribunais_superiores.keys()))
        api_url = tribunais_superiores[tribunal_escolhido]
    elif tipo_tribunal == "Justiça Federal":
        tribunal_escolhido = st.selectbox("Selecione o tribunal", list(justica_federal.keys()))
        api_url = justica_federal[tribunal_escolhido]
    elif tipo_tribunal == "Justiça do Trabalho":
        tribunal_escolhido = st.selectbox("Selecione o tribunal", list(justica_do_trabalho.keys()))
        api_url = justica_do_trabalho[tribunal_escolhido]
    elif tipo_tribunal == "Justiça Estadual":
        tribunal_escolhido = st.selectbox("Selecione o tribunal", list(justica_estadual.keys()))
        api_url = justica_estadual[tribunal_escolhido]
    elif tipo_tribunal == "Justiça Eleitoral":
        tribunal_escolhido = st.selectbox("Selecione o tribunal", list(justica_eleitoral.keys()))
        api_url = justica_eleitoral[tribunal_escolhido]
    elif tipo_tribunal == "Justiça Militar":
        tribunal_escolhido = st.selectbox("Selecione o tribunal", list(justica_militar.keys()))
        api_url = justica_militar[tribunal_escolhido]
    else:
        tribunal_escolhido = st.selectbox("Selecione o tribunal", list(justica_estadual.keys()))
        api_url = justica_estadual[tribunal_escolhido]

    # Campo de busca para o número do processo
    numero_processo = st.text_input("Digite o número do processo")

    if st.button("Buscar processo"):
        # Verifica se o número do processo foi fornecido
        if numero_processo:
            numero_processo = extrair_numeros(numero_processo)
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
