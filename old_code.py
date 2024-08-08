# # Configuração da página
# st.set_page_config(layout="wide")

# # Função para converter datas no formato ISO 8601 para o formato brasileiro
# def formatar_data(data_iso):
#     try:
#         data_obj = datetime.fromisoformat(data_iso.replace("Z", "+00:00"))
#         return data_obj.strftime("%d/%m/%Y %H:%M:%S")
#     except ValueError:
#         return data_iso

# # Função para ler e processar tabelas de um arquivo HTML
# @st.cache_data
# def read_html_manual(file_content: bytes):
#     arquivo_html = pd.read_html(file_content, header=0, skiprows=2)
#     tabela = arquivo_html[0]
#     return tabela

# # Função para salvar o arquivo no banco (placeholder)
# def save_arquivo_banco(file: bytes):
#     arquivo = file

# # URL da API e cabeçalho de autorização
# api_url = "https://api-publica.datajud.cnj.jus.br/api_publica_trf1/_search"
# headers = {
#     "Authorization": "APIKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw==",
#     "Content-Type": "application/json"
# }

# # MENU SIDEBAR
# # with st.sidebar:
# #     st.subheader('Menu')
# #     info_processuais = st.button("Informações processuais", use_container_width=True)
# #     info_lotes = st.button("Consultas em lote", use_container_width=True)
# #     info_cadastrais = st.button("Informações cadastrais", use_container_width=True)

# # CONTAINER PRINCIPAL
# with st.container():
#     st.header('Dashboard')

#     # Upload e exibição de arquivo HTML
#     uploaded_file = st.file_uploader(label="Subir arquivo", type=["htm", "html", "pdf"])
    
#     if uploaded_file is not None:
#         bytes_data = uploaded_file.read()
        
#         if 'tables' not in st.session_state:
#             st.session_state.tables = read_html_manual(bytes_data)
        
#         tables = st.session_state.tables

#         options_filter = st.selectbox(
#             "Selecione um filtro de preferência",
#             ["TODOS", "IDOSO", "NÃO", "PESSOA COM DEFICIÊNCIA", "IDOSO, PESSOA COM DEFICIÊNCIA", "DOENÇA GRAVE"]
#         )
        
#         if options_filter != "TODOS":
#             filtered_table = tables[tables['PREFERÊNCIA*'] == options_filter]
#         else:
#             filtered_table = tables
        
#         limited_table = filtered_table.head(200)
        
#         st.dataframe(limited_table, width=1000, height=600)
        