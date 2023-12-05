import tabula
import pandas as pd
import os
import re

caminhos_arquivos_pdf = [
    "C:/Users/vanfe/OneDrive/Área de Trabalho/TCC2 Dados/chamadas regular e final pdf/sisu-2016-notas-de-corte.pdf",
    "C:/Users/vanfe/OneDrive/Área de Trabalho/TCC2 Dados/chamadas regular e final pdf/sisu-2017-notas-de-corte.pdf",
    "C:/Users/vanfe/OneDrive/Área de Trabalho/TCC2 Dados/chamadas regular e final pdf/sisu-2018-notas-de-corte.pdf",
    "C:/Users/vanfe/OneDrive/Área de Trabalho/TCC2 Dados/chamadas regular e final pdf/sisu-2019-notas-de-corte.pdf",
    "C:/Users/vanfe/OneDrive/Área de Trabalho/TCC2 Dados/chamadas regular e final pdf/sisu-2020-notas-de-corte.pdf",
    "C:/Users/vanfe/OneDrive/Área de Trabalho/TCC2 Dados/chamadas regular e final pdf/sisu-2021-notas-de-corte.pdf",
    "C:/Users/vanfe/OneDrive/Área de Trabalho/TCC2 Dados/chamadas regular e final pdf/sisu-2022-notas-de-corte.pdf"
]  

valor_filtro1 = 'Russas'
valor_filtro2 = 'RUSSAS'

# Pasta onde os arquivos CSV serão salvos
pasta_resultados = "resultados ch regular e final"
if not os.path.exists(pasta_resultados):
    os.makedirs(pasta_resultados)

nomes_colunas_desejados = ['COD. CURSO', 'CAMPUS', 'CURSO', 'FORMAÇÃO', 'TURNO', 'COTA', 'CORTE CH. REGULAR', 'CORTE FINAL']


# Loop através de cada arquivo PDF
for caminho_arquivo_pdf in caminhos_arquivos_pdf:
    dfs_todas_paginas = tabula.read_pdf(caminho_arquivo_pdf, pages='all', pandas_options={"header": None}, multiple_tables=False)

    # Obter o ano a partir do nome do arquivo
    ano = re.search(r'\d{4}', os.path.basename(caminho_arquivo_pdf)).group()

    # Lista para armazenar os DataFrames filtrados dos arquivos
    dfs_filtrados = []

    # Percorrer cada DataFrame da lista
    for df in dfs_todas_paginas:
        # Verificar se o DataFrame tem o número esperado de colunas
        if df.shape[1] > len(nomes_colunas_desejados):
            df = df.iloc[:, :-1]

        if df.shape[1] == len(nomes_colunas_desejados):
            df.columns = nomes_colunas_desejados

            # Adicionar a coluna "DATA" com o valor no formato "ano-mês-dia"
            df['DATA'] = f"{ano}-12-01"

            aux = nomes_colunas_desejados[1]
            print(aux)

            if aux == 'Campus':
                df_filtrado = df[df['Campus'].str.contains(valor_filtro1, case=False, na=False)]
            if aux == 'CAMPUS':
                df_filtrado = df[df['CAMPUS'].str.contains(valor_filtro2, case=False, na=False)]

            if not df_filtrado.empty:
                for coluna in df_filtrado.columns:
                    if df_filtrado[coluna].dtype == 'object':
                        df_filtrado[coluna] = df_filtrado[coluna].str.replace(',', '.', regex=True)

                # mostrar as linhas filtradas da tabela
                dfs_filtrados.append(df_filtrado)

    if dfs_filtrados:
        df_final = pd.concat(dfs_filtrados, ignore_index=True)

        nome_arquivo_csv = os.path.join(pasta_resultados, f"resultado_cham_reg_e_final_{ano}.csv")
        df_final.to_csv(nome_arquivo_csv, index=False, sep=',', header=True, date_format="%Y-%m-%d")  # Definir o separador como vírgula, incluir cabeçalho e definir o formato de data

        print(f"Arquivo CSV 'resultados_{ano}.csv' salvo com exito!")
    else:
        print(f"Nenhum valor encontrado no PDF de {ano}.")
