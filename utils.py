import re

def extrair_numeros(numero_processo):
    return re.sub(r'\D', '', numero_processo)