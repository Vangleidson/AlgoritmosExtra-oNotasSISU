import os
import re
import pandas as pd

arquivos_xlsx = [
    'C:/Users/vanfe/OneDrive/Área de Trabalho/TCC2 Dados/lista de espera xlsx/ListagemListaEspera_2017-1.xlsx',
    'C:/Users/vanfe/OneDrive/Área de Trabalho/TCC2 Dados/lista de espera xlsx/ListagemListaEspera_2018-1.xlsx',
    'C:/Users/vanfe/OneDrive/Área de Trabalho/TCC2 Dados/lista de espera xlsx/ListagemListaEspera_2019-1.xlsx',
    'C:/Users/vanfe/OneDrive/Área de Trabalho/TCC2 Dados/lista de espera xlsx/ListagemListaEspera_2020-1.xlsx',
    'C:/Users/vanfe/OneDrive/Área de Trabalho/TCC2 Dados/lista de espera xlsx/ListagemListaEspera_2021-1.xlsx',
    'C:/Users/vanfe/OneDrive/Área de Trabalho/TCC2 Dados/lista de espera xlsx/ListagemListaEspera_2022-1.xlsx'
     #'C:/Users/vanfe/OneDrive/Área de Trabalho/TCC2 Dados/lista de espera xlsx/teste2023.xlsx'

]

pasta_resultados = "resultados lista de espera"
if not os.path.exists(pasta_resultados):
    os.makedirs(pasta_resultados)

filtro_campus = 'MUNICIPIO_CAMPUS' 
filtro_matricula = 'ST_APROVADO'

valor_campus = 'Russas'
valor_matricula = 'S'

for arquivo_xlsx in arquivos_xlsx:
    df = pd.read_excel(arquivo_xlsx)
    df[filtro_campus] = df[filtro_campus].astype(str)
    df[filtro_matricula] = df[filtro_matricula].astype(str)
    df_filtrado = df[(df[filtro_campus] == valor_campus) & (df[filtro_matricula] == valor_matricula)]
    
    ano = re.search(r'\d{4}', os.path.basename(arquivo_xlsx)).group()

    saida = os.path.join(pasta_resultados, f"resultado_lista_espera_{ano}.xlsx")

    df_filtrado.to_excel(saida, index=False)

    print(f"Saída salva no arquivo: '{saida}'")