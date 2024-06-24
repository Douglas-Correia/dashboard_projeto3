import streamlit_javascript as st_js

def tamanho_tela():
    ui_width = st_js.st_javascript("window.innerWidth")
    return ui_width