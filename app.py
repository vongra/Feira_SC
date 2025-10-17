# ==============================================================================
# PARTE 1: PROCESSAMENTO DE DADOS (VERSÃO COMPLETA E FINAL)
# ==============================================================================
import pandas as pd
from PIL import Image
import re

# --- 1. CONFIGURAÇÕES E CARREGAMENTO DOS DADOS ---
ARQUIVO_01 = "Formulário de Participação em Grupos de Trabalho (GTs) – Reforma da Feira de São Cristóvão (respostas).xlsx"
ARQUIVO_02 = "FORMS FEIRA GTS FÍSICOS (Q1).xlsx"
MAPAS_DISPONIVEIS = {
    "Quadrante 01": "Q_01.jpeg",
    "Quadrante 02": "Q_02.jpeg"
}

try:
    primeiro_mapa = list(MAPAS_DISPONIVEIS.values())[0]
    img_test = Image.open(primeiro_mapa)
    print(f"Imagem '{primeiro_mapa}' carregada com sucesso para teste. Dimensões: {img_test.size}")
except FileNotFoundError:
    print(f"ERRO: Imagem '{primeiro_mapa}' NÃO ENCONTRADA! Verifique o nome e o local do arquivo.")
    exit()

COLUNA_NOME_BARRACA_01 = "Nome da barraca/box"
COLUNA_NOME_BARRACA_02 = "Barraca/Box"
COLUNA_SEGMENTO = "Segmento"
COLUNA_RESPONSAVEL = "Nome do feirante"

try:
    planilha_01 = pd.read_excel(ARQUIVO_01)
    planilha_02 = pd.read_excel(ARQUIVO_02)
    print("Arquivos de dados carregados com sucesso.")
except FileNotFoundError as e:
    print(f"Erro: Arquivo de dados não encontrado. Detalhe: {e}")
    exit()

# --- 2. PRÉ-PROCESSAMENTO DA PLANILHA 01 ---
if "Carimbo de data/hora" in planilha_01.columns:
    planilha_01 = planilha_01.drop(columns=["Carimbo de data/hora"])

# --- 3. PRÉ-PROCESSAMENTO DA PLANILHA 02 ---
posicao = planilha_02.columns.get_loc('N° de boxes')
nova_coluna_valores = planilha_02['N° de boxes'].astype(str) + '/' + planilha_02['Tamanho'].astype(str)
planilha_02 = planilha_02.drop(columns=['N° de boxes', 'Tamanho'])
planilha_02.insert(loc=posicao, column='N° de boxes/Tamanho', value=nova_coluna_valores)

# --- 4. REMOÇÃO DE DUPLICATAS ---
valores_planilha01 = set(planilha_01[COLUNA_NOME_BARRACA_01].dropna())
elementos_repetidos = valores_planilha01.intersection(set(planilha_02[COLUNA_NOME_BARRACA_02].dropna()))
if elementos_repetidos:
    linhas_antes = len(planilha_02)
    planilha_02 = planilha_02[~planilha_02[COLUNA_NOME_BARRACA_02].isin(elementos_repetidos)]
    linhas_removidas = linhas_antes - len(planilha_02)
    print(f"{linhas_removidas} linha(s) duplicadas foram removidas.")
else:
    print("Não foram encontradas duplicatas.")

# --- 5. UNIFICAÇÃO DAS PLANILHAS ---
colunas_planilha02 = planilha_02.columns
colunas_correspondentes_planilha01 = planilha_01.columns[:len(colunas_planilha02)]
mapa_de_nomes = dict(zip(colunas_planilha02, colunas_correspondentes_planilha01))
planilha_02_renomeada = planilha_02.rename(columns=mapa_de_nomes)
planilha_final = pd.concat([planilha_01, planilha_02_renomeada], ignore_index=True)

# --- 6. ATUALIZAÇÕES MANUAIS E LIMPEZA ---
planilha_final.loc[0, 'Número de funcionários'] = 2
planilha_final.loc[63, 'Número de funcionários'] = "nan"
planilha_final.loc[68, 'Número de funcionários'] = 3
planilha_final.loc[71, 'Número de funcionários'] = 15
planilha_final.loc[72, 'Número de funcionários'] = 5
planilha_final.loc[73, 'Número de funcionários'] = 15
planilha_final.loc[74, 'Número de funcionários'] = 10
planilha_final.loc[90, 'Número de funcionários'] = "nan"
planilha_final.loc[116, 'Número de funcionários'] = "nan"
planilha_final.loc[1, 'Numeração do Box'] = "B-7"
planilha_final.loc[2, 'Numeração do Box'] = "E-19"
planilha_final.loc[5, 'Numeração do Box'] = "E-52 / E-53"
planilha_final.loc[59, 'Numeração do Box'] = "B-8 / B-5 / B-6"
planilha_final.loc[85, 'Numeração do Box'] = "B-11"
planilha_final.loc[86, 'Numeração do Box'] = "E-57"
planilha_final.loc[88, 'Numeração do Box'] = "E-67"
planilha_final.loc[89, 'Numeração do Box'] = "C-2"
planilha_final.loc[90, 'Numeração do Box'] = "F-116/F117"
planilha_final.loc[91, 'Numeração do Box'] = "D-5"
planilha_final.loc[92, 'Numeração do Box'] = "D-32"
planilha_final.loc[93, 'Numeração do Box'] = "B-2 / B-3"
planilha_final.loc[95, 'Numeração do Box'] = "E-28"
planilha_final.loc[96, 'Numeração do Box'] = "D-3"
planilha_final.loc[98, 'Numeração do Box'] = "F-164"
planilha_final.loc[100, 'Numeração do Box'] = "E-42 / E-43"
planilha_final.loc[101, 'Numeração do Box'] = "D-30"
planilha_final.loc[102, 'Numeração do Box'] = "E-49 / E-50 / E-51"
planilha_final.loc[103, 'Numeração do Box'] = "D-1 / D-2 / D-14 / D-15"
planilha_final.loc[104, 'Numeração do Box'] = "E-7 / E-8 /E-9"
planilha_final.loc[105, 'Numeração do Box'] = "A-2 / A-3 / A-4 / A-9 / A-10 / A-11"
planilha_final.loc[106, 'Numeração do Box'] = "D-21 / D-22 / D-23 / D-24"
planilha_final.loc[107, 'Numeração do Box'] = "E-6 / E-10 / E-11 / E-12"
planilha_final.loc[108, 'Numeração do Box'] = "E-37"
planilha_final.loc[109, 'Numeração do Box'] = "E-26"
planilha_final.loc[111, 'Numeração do Box'] = "E-23"
planilha_final.loc[112, 'Numeração do Box'] = "A-14 / A-15 / A-8 / A-6 / E-54 / E-55"
planilha_final.loc[113, 'Numeração do Box'] = "E-45 / E-46 / E-47"
planilha_final.loc[114, 'Numeração do Box'] = "D-7"
planilha_final.loc[115, 'Numeração do Box'] = "E-19"
planilha_final.loc[116, 'Numeração do Box'] = "E-38"
planilha_final.loc[118, 'Numeração do Box'] = "D-10"
planilha_final.loc[119, 'Numeração do Box'] = "D-33 / D-34 / D-35 / D-36 / D-37"
planilha_final.loc[120, 'Numeração do Box'] = "E-59"
planilha_final.loc[121, 'Numeração do Box'] = "B-08"
planilha_final.loc[122, 'Numeração do Box'] = "D-12"
planilha_final.loc[123, 'Numeração do Box'] = "F-1 / F-13 / F-14"
planilha_final.loc[116, 'Segmento'] = "CULINÁRIA/BAR"
planilha_final.loc[62, 'Segmento'] = "ARTESANATO"
planilha_final = planilha_final.drop([3,4,53,87,94,124])

# --- 7. PADRONIZAÇÃO DA COLUNA 'SEGMENTO' ---
print("Iniciando a padronização da coluna 'Segmento'...")
planilha_final['Segmento'] = planilha_final['Segmento'].astype(str).str.lower().str.strip()
planilha_final['Segmento'] = planilha_final['Segmento'].replace(['artesanato', 'artesanato.', 'artesanatos', 'artesanatos.'], 'ARTESANATO')
planilha_final['Segmento'] = planilha_final['Segmento'].replace(['culinária/bar', 'culinaria/bar', 'BAR', 'balas', 'boxes, culinária/bar', 'cachaçaria e presentes','culinária/bar, comidas, bebidas e música', 'sorveteria' ], 'CULINÁRIA/BAR')
planilha_final['Segmento'] = planilha_final['Segmento'].replace(['restaurante', 'restaurantes', 'restaurante e bar'], 'RESTAURANTE')
planilha_final['Segmento'] = planilha_final['Segmento'].replace(['ambulantes'], 'AMBULANTES')
planilha_final['Segmento'] = planilha_final['Segmento'].replace(['karaoke', 'karaoke, culinária/bar', 'karaokê'], 'KARAOKÊ')
planilha_final['Segmento'] = planilha_final['Segmento'].replace(['roupas típicas e contemporâneas', 'roupas turísticas e souvenir', 'calçados'], 'ROUPAS TÍPICAS E CONTEMPORÂNEAS')
planilha_final['Segmento'] = planilha_final['Segmento'].replace(['bazar','outros (bazar)'], 'BAZAR')
planilha_final['Segmento'] = planilha_final['Segmento'].replace(['cultura', 'produção e curadoria', 'boxes, venda de cd e bebidas'], 'CULTURA')
planilha_final['Segmento'] = planilha_final['Segmento'].replace(['mercearia'], 'MERCEARIA')
planilha_final['Segmento'] = planilha_final['Segmento'].replace(['música', 'funk'], 'MUSICA')
planilha_final['Segmento'] = planilha_final['Segmento'].replace(['depósito'], 'DEPÓSITO')
planilha_final['Segmento'] = planilha_final['Segmento'].replace(['estúdio fotográfico', 'fotografia'], 'FOTOGRAFIA')
planilha_final['Segmento'] = planilha_final['Segmento'].replace(['outros'], 'OUTROS')
print("Padronização da coluna 'Segmento' concluída.")

# --- 7.5: ADIÇÃO DA COLUNA DE URL DA FACHADA ---
planilha_final['URL_Fachada'] = None
print("Coluna 'URL_Fachada' adicionada.")
# Adicionando URLs de exemplo para alguns estabelecimentos para demonstração
planilha_final.loc[1, 'URL_Fachada'] = 'https://i.pinimg.com/736x/f5/a4/51/f5a4513689d93d8bf0a0c62f8319f6d7.jpg'
planilha_final.loc[2, 'URL_Fachada'] = 'https://lh3.googleusercontent.com/gps-cs-s/AC9h4np78wdM9uwzH_H_l4sDhBjcBq98Oo2KczTgEM2kGCI9bCr6Ey7M-MOA1hHWeQmnmMtEB8DPR-GmYvsYbDrxXAIHvCA0WZKtaTqOAGFD_S2WBNgQeMoefty26mtJUfM7hQ--VOqVwRUASigX=s1360-w1360-h1020-rw'
planilha_final.loc[92, 'URL_Fachada'] = 'https://lh3.googleusercontent.com/proxy/pBIhNzt3Qs6PXBcNpOPbjvyfVvB-qr7Kt8__vnYJkDDT4kgEua0K0ATIo7efm3ZeVNqNU4BLgf4dRlQ0sSk1_0bmgTih_fh1VnhjkMbNArle05rzuLP_N8fE1pdxh3BUwveSb5I999i9nXg44-lTsKJBEPdEcqvscTdLSg=s1360-w1360-h1020-rw'
print("URLs de fachada de exemplo adicionadas.")

# --- 8. CRIAÇÃO E PREENCHIMENTO DAS COORDENADAS ---
planilha_final['Coordenada X'] = None
planilha_final['Coordenada Y'] = None
planilha_final.loc[1, ['Coordenada X', 'Coordenada Y']] = [1221, 1354]
planilha_final.loc[2, ['Coordenada X', 'Coordenada Y']] = [2428, 1529]
planilha_final.at[5, 'Coordenada X'] = [2608, 2608]
planilha_final.at[5, 'Coordenada Y'] = [2069, 2132]
planilha_final.loc[51, ['Coordenada X', 'Coordenada Y']] = [2718, 2522]
planilha_final.at[59, 'Coordenada X'] = [1423, 883, 1066]
planilha_final.at[59, 'Coordenada Y'] = [1254, 1557, 1447]
planilha_final.loc[84, ['Coordenada X', 'Coordenada Y']] = [2716, 1544]
planilha_final.loc[85, ['Coordenada X', 'Coordenada Y']] = [1388, 1499]
planilha_final.loc[86, ['Coordenada X', 'Coordenada Y']] = [2613, 2439]
planilha_final.loc[88, ['Coordenada X', 'Coordenada Y']] = [2716, 2597]
planilha_final.loc[89, ['Coordenada X', 'Coordenada Y']] = [2923, 2449]
planilha_final.at[90, 'Coordenada X'] = [1883, 1931]
planilha_final.at[90, 'Coordenada Y'] = [1074, 1059]
planilha_final.loc[91, ['Coordenada X', 'Coordenada Y']] = [2176, 1199]
planilha_final.loc[92, ['Coordenada X', 'Coordenada Y']] = [3076, 1747]
planilha_final.at[93, 'Coordenada X'] = [318, 403]
planilha_final.at[93, 'Coordenada Y'] = [2129, 2022]
planilha_final.loc[95, ['Coordenada X', 'Coordenada Y']] = [2593, 1772]
planilha_final.loc[96, ['Coordenada X', 'Coordenada Y']] = [1981, 1262]
planilha_final.loc[97, ['Coordenada X', 'Coordenada Y']] = [1978, 1044]
planilha_final.loc[100, ['Coordenada X', 'Coordenada Y']] = [3106, 1067]
planilha_final.loc[101, ['Coordenada X', 'Coordenada Y']] = [3076, 1639]
planilha_final.at[102, 'Coordenada X'] = [2963, 3031, 3106]
planilha_final.at[102, 'Coordenada Y'] = [2059, 2059, 2059]
planilha_final.at[103, 'Coordenada X'] = [1791, 1879, 1843, 1936]
planilha_final.at[103, 'Coordenada Y'] = [1331, 1302, 1479, 1447]
planilha_final.at[104, 'Coordenada X'] = [2029, 2029, 2029]
planilha_final.at[104, 'Coordenada Y'] = [1702, 1779, 1858]
planilha_final.at[105, 'Coordenada X'] = [1006, 1218, 1427, 1006, 1222, 1431]
planilha_final.at[105, 'Coordenada Y'] = [2188, 2192, 2192, 2454, 2454, 2454]
planilha_final.at[106, 'Coordenada X'] = [2516, 2603, 2703, 2803]
planilha_final.at[106, 'Coordenada Y'] = [1292, 1274, 1252, 1242]
planilha_final.at[107, 'Coordenada X'] = [2031, 2141, 2141, 2141]
planilha_final.at[107, 'Coordenada Y'] = [1644, 1644, 1707, 1779]
planilha_final.loc[108, ['Coordenada X', 'Coordenada Y']] = [2931, 1457]
planilha_final.loc[109, ['Coordenada X', 'Coordenada Y']] = [2608, 1627]
planilha_final.loc[111, ['Coordenada X', 'Coordenada Y']] = [2426, 1857]
planilha_final.at[112, 'Coordenada X'] = [2163, 2373, 2373, 1956, 2608, 2608]
planilha_final.at[112, 'Coordenada Y'] = [2454, 2454, 2184, 2184, 2202, 2282]
planilha_final.at[113, 'Coordenada X'] = [2956, 3026, 3103]
planilha_final.at[113, 'Coordenada Y'] = [1847, 1847, 1847]
planilha_final.loc[114, ['Coordenada X', 'Coordenada Y']] = [2383, 1162]
planilha_final.loc[115, ['Coordenada X', 'Coordenada Y']] = [2428, 1542]
planilha_final.loc[116, ['Coordenada X', 'Coordenada Y']] = [3091, 1447]
planilha_final.loc[118, ['Coordenada X', 'Coordenada Y']] = [2681, 1102]
planilha_final.loc[120, ['Coordenada X', 'Coordenada Y']] = [2613, 2596]
planilha_final.loc[122, ['Coordenada X', 'Coordenada Y']] = [2886, 1079]
planilha_final.at[123, 'Coordenada X'] = [1708, 1736, 1788]
planilha_final.at[123, 'Coordenada Y'] = [1054, 1126, 1109]
planilha_final.loc[6, ['Coordenada X', 'Coordenada Y']] = [3337, 723]
planilha_final.loc[7, ['Coordenada X', 'Coordenada Y']] = [3016, 696]
planilha_final.loc[9, ['Coordenada X', 'Coordenada Y']] = [1594, 1069]
planilha_final.loc[11, ['Coordenada X', 'Coordenada Y']] = [2243, 1504]
planilha_final.loc[12, ['Coordenada X', 'Coordenada Y']] = [1932, 1783]
planilha_final.at[13, 'Coordenada X'] = [2124, 2175, 2224]
planilha_final.at[13, 'Coordenada Y'] = [2121, 2139, 2158]
planilha_final.at[14, 'Coordenada X'] = [2383, 2483]
planilha_final.at[14, 'Coordenada Y'] = [1969, 1999]
planilha_final.loc[15, ['Coordenada X', 'Coordenada Y']] = [2683, 2053]
planilha_final.loc[16, ['Coordenada X', 'Coordenada Y']] = [2683, 2293]
planilha_final.loc[17, ['Coordenada X', 'Coordenada Y']] = [3123, 1523]
planilha_final.at[18, 'Coordenada X'] = [2838, 2838]
planilha_final.at[18, 'Coordenada Y'] = [1688, 1606]
planilha_final.loc[19, ['Coordenada X', 'Coordenada Y']] = [3381, 1161]
planilha_final.loc[20, ['Coordenada X', 'Coordenada Y']] = [2133, 1433]
planilha_final.at[21, 'Coordenada X'] = [3121, 3121]
planilha_final.at[21, 'Coordenada Y'] = [700, 615]
planilha_final.loc[23, ['Coordenada X', 'Coordenada Y']] = [3018, 615]
planilha_final.loc[24, ['Coordenada X', 'Coordenada Y']] = [2136, 1358]
planilha_final.loc[25, ['Coordenada X', 'Coordenada Y']] = [3343, 953]
planilha_final.loc[26, ['Coordenada X', 'Coordenada Y']] = [3301, 1160]
planilha_final.loc[27, ['Coordenada X', 'Coordenada Y']] = [1613, 1933]
planilha_final.loc[28, ['Coordenada X', 'Coordenada Y']] = [2433, 1583]

print("Processamento de dados da PARTE 1 concluído.")

# ==============================================================================
# PARTE 1.5: PREPARAÇÃO DOS DADOS PARA O GRÁFICO DE SEGMENTOS
# ==============================================================================
df_grafico_segmento = planilha_final.copy()
if 'Quadrante' in df_grafico_segmento.columns:
    df_grafico_segmento.dropna(subset=['Quadrante', COLUNA_SEGMENTO], inplace=True)
    df_grafico_segmento['Quadrante'] = df_grafico_segmento['Quadrante'].astype(str).str.strip().str.upper()
    tabela_contagem = pd.crosstab(df_grafico_segmento['Quadrante'], df_grafico_segmento[COLUNA_SEGMENTO])
    print("Dados para o gráfico de distribuição de segmentos gerados com sucesso.")
else:
    print("AVISO: Coluna 'Quadrante' não encontrada. O gráfico de barras de segmentos não será gerado.")
    tabela_contagem = pd.DataFrame()

# ==============================================================================
# PARTE 1.6: PREPARAÇÃO DOS DADOS PARA O GRÁFICO DE FUNCIONÁRIOS
# ==============================================================================
funcionarios_numeric = pd.to_numeric(planilha_final['Número de funcionários'], errors='coerce')
funcionarios_validos = funcionarios_numeric.dropna()
contagem_funcionarios = funcionarios_validos.value_counts().sort_index()
print("Dados para o gráfico de distribuição de funcionários gerados com sucesso.")


# ==============================================================================
# PARTE 2: CONSTRUÇÃO DA APLICAÇÃO DASH
# ==============================================================================
import dash
from dash import dcc, html, Input, Output, State, no_update
import plotly.graph_objects as go
import plotly.colors as pcolors
import dash_bootstrap_components as dbc

# --- PREPARAÇÃO DOS DADOS PARA PLOTAGEM DO MAPA ---
if 'Quadrante' not in planilha_final.columns:
    planilha_final['Quadrante'] = None 

pontos_no_mapa_inicial = planilha_final.dropna(subset=['Coordenada X', 'Coordenada Y', 'Quadrante']).copy()
linhas_expandidas = []
for index, row in pontos_no_mapa_inicial.iterrows():
    coord_x = row['Coordenada X']
    coord_y = row['Coordenada Y']
    if isinstance(coord_x, list) and isinstance(coord_y, list):
        for i in range(len(coord_x)):
            nova_linha = row.to_dict()
            nova_linha['Coordenada X'] = coord_x[i]
            nova_linha['Coordenada Y'] = coord_y[i]
            nova_linha['original_index'] = index
            linhas_expandidas.append(nova_linha)
    else:
        nova_linha = row.to_dict()
        nova_linha['original_index'] = index
        linhas_expandidas.append(nova_linha)
pontos_no_mapa = pd.DataFrame(linhas_expandidas)
print(f"Dados do mapa expandidos para {len(pontos_no_mapa)} pontos.")
pontos_no_mapa['Quadrante'] = pontos_no_mapa['Quadrante'].astype(float).astype(int).astype(str)
pontos_no_mapa['hover_text'] = pontos_no_mapa.apply(
    lambda row: (
        f"<span style='display: none;'>id:{row['original_index']}</span>"
        f"<b>{row.get(COLUNA_NOME_BARRACA_01, 'N/A')}</b><br><br>"
        f"Segmento: {row.get(COLUNA_SEGMENTO, 'N/A')}<br>"
        f"Responsável: {row.get(COLUNA_RESPONSAVEL, 'N/A')}"
    ),
    axis=1
)

# --- CRIAÇÃO DE MAPA DE CORES E ÍCONES PARA OS SEGMENTOS ---
segmentos_unicos = sorted(planilha_final[COLUNA_SEGMENTO].dropna().unique())
cores_disponiveis = pcolors.qualitative.Vivid
mapa_de_cores = {segmento: cores_disponiveis[i % len(cores_disponiveis)] for i, segmento in enumerate(segmentos_unicos)}
mapa_de_icones = {
    "ARTESANATO": "Artesanato_02.png",
    "CULINÁRIA/BAR": "Culinaria_02.png",
    "RESTAURANTE": "restaurante.png",
    "KARAOKÊ": "Karaoke_02.png",
    "AMBULANTES": "ambulante.png",
    "ROUPAS TÍPICAS E CONTEMPORÂNEAS": "Roupa.png",
    "DEPÓSITO": "Icone_Deposito.png",
    "CULTURA": "Icone_Cultura.png",
    "MERCEARIA": "Icone_Mercearia.png"
}

# --- CRIAÇÃO DAS FIGURAS DOS GRÁFICOS ---
fig_barras = go.Figure()
if not tabela_contagem.empty:
    for segmento in tabela_contagem.columns:
        fig_barras.add_trace(go.Bar(name=segmento, x=tabela_contagem.index, y=tabela_contagem[segmento], marker_color=mapa_de_cores.get(segmento)))
fig_barras.update_layout(title='Distribuição de Segmentos por Quadrante', xaxis_title='Quadrante', yaxis_title='Número de Estabelecimentos', barmode='group', template='plotly_dark', legend_title_text='Segmentos')
fig_funcionarios = go.Figure()
fig_funcionarios.add_trace(go.Bar(
    x=contagem_funcionarios.index, y=contagem_funcionarios.values,
    text=contagem_funcionarios.values, textposition='auto',
    marker_color='lightsalmon'
))
fig_funcionarios.update_layout(title='Distribuição do Número de Funcionários', xaxis_title='Nº de Funcionários por Estabelecimento', yaxis_title='Quantidade de Estabelecimentos', template='plotly_dark')

# --- INICIALIZAÇÃO DA APLICAÇÃO ---
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
app.title = "Dashboard Feira de São Cristóvão"
server = app.server # <-- ADIÇÃO IMPORTANTE PARA O DEPLOY

# --- LAYOUT DA APLICAÇÃO ---
app.layout = dbc.Container(fluid=True, children=[
    dbc.Row(dbc.Col(dbc.Card(dbc.CardBody(html.H1("Feira de São Cristóvão em Números", className="text-center", style={'font-family': 'Verdana, sans-serif'})), color="primary", inverse=True, className="my-3"))),
    dbc.Row(dbc.Col(dbc.Card(dbc.CardBody("Nesse dashboard visual você encontrará as informações mais importantes sobre os números da Feira de São Cristóvão."), className="mb-4 text-center"), width={"size": 8, "offset": 2})),
    dcc.Tabs(id="abas-principais", value='aba-mapa', children=[
        dcc.Tab(label='Mapa Interativo', value='aba-mapa', children=[
            dbc.Row([
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody([
                            html.H5("Selecione um Quadrante:", style={'color': 'black'}),
                            dcc.Dropdown(id='seletor-quadrante', options=[{'label': nome, 'value': nome} for nome in MAPAS_DISPONIVEIS.keys()], value='Quadrante 01', clearable=False),
                            html.Hr(),
                            html.H5("Filtre os Segmentos:", style={'color': 'black'}),
                            dbc.Checklist(
                                id='segmento-checklist',
                                options=[], value=[],
                                inputClassName="mx-2",
                            ),
                        ]),
                        style={'backgroundColor': '#f8f9fa', 'height': '100%'}
                    ),
                    width=3
                ),
                dbc.Col([
                    html.Div(children=[dcc.Graph(id='mapa-da-feira', style={'height': '100%', 'width': '100%'})],
                             style={'border': '1px solid #555', 'margin-top': '20px', 'overflow': 'auto'})
                ], width=9),
            ])
        ]),
        dcc.Tab(label='Gráficos e Estatísticas', value='aba-stats', children=[
            dbc.Row(dbc.Col(dcc.Graph(id='grafico-segmentos-quadrante', figure=fig_barras), width=12, className="mt-4")),
            dbc.Row(dbc.Col(dcc.Graph(id='grafico-distribuicao-funcionarios', figure=fig_funcionarios), width=12, className="mt-4")),
        ]),
    ]),
    dbc.Modal([dbc.ModalHeader(dbc.ModalTitle(id="modal-header")), dbc.ModalBody(id="modal-body")], id="info-modal", is_open=False, size="lg", centered=True),
])

# --- CALLBACK PARA ATUALIZAR O CHECKLIST DINAMICAMENTE ---
@app.callback(
    Output('segmento-checklist', 'options'),
    Output('segmento-checklist', 'value'),
    Input('seletor-quadrante', 'value')
)
def update_checklist(quadrante_selecionado):
    mapeamento_quadrantes = {"Quadrante 01": ["1"], "Quadrante 02": ["2"]}
    valores_filtro_quadrante = mapeamento_quadrantes.get(quadrante_selecionado, [])
    pontos_do_quadrante = pontos_no_mapa[pontos_no_mapa['Quadrante'].isin(valores_filtro_quadrante)]
    segmentos_no_quadrante = sorted(pontos_do_quadrante[COLUNA_SEGMENTO].unique())
    novas_opcoes = []
    for s in segmentos_no_quadrante:
        nome_arquivo_icone = mapa_de_icones.get(s)
        label_content = []
        if nome_arquivo_icone:
            label_content.append(html.Img(src=app.get_asset_url(nome_arquivo_icone), style={'height': '20px', 'marginRight': '10px', 'verticalAlign': 'middle'}))
        label_content.append(html.Span(s, style={'verticalAlign': 'middle', 'color': 'black'}))
        novas_opcoes.append({'label': html.Div(label_content, className="d-flex align-items-center"), 'value': s})
    return novas_opcoes, segmentos_no_quadrante

# --- CALLBACK PARA ATUALIZAR O MAPA ---
@app.callback(
    Output('mapa-da-feira', 'figure'), 
    [Input('seletor-quadrante', 'value'),
     Input('segmento-checklist', 'value')]
)
def atualizar_mapa(quadrante_selecionado, segmentos_visiveis):
    if not quadrante_selecionado or not segmentos_visiveis:
        fig_vazia = go.Figure()
        arquivo_imagem = MAPAS_DISPONIVEIS.get(quadrante_selecionado, list(MAPAS_DISPONIVEIS.values())[0])
        try:
            img = Image.open(arquivo_imagem)
            img_width, img_height = img.size
            fig_vazia.add_layout_image(dict(source=img, xref="x", yref="y", x=0, y=0, sizex=img_width, sizey=img_height, sizing="stretch", layer="below"))
            fig_vazia.update_layout(
                xaxis=dict(showgrid=False, visible=False, range=[0, img_width]),
                yaxis=dict(showgrid=False, visible=False, range=[img_height, 0]),
                template="plotly_dark", margin=dict(l=0, r=0, t=40, b=0), height=900,
                title=f"Localização dos Estabelecimentos por Quadrante: {quadrante_selecionado}",
            )
        except FileNotFoundError:
            fig_vazia.update_layout(title=f"Erro: Imagem '{arquivo_imagem}' não encontrada!", template="plotly_dark")
        return fig_vazia

    mapeamento_quadrantes = {"Quadrante 01": ["1"], "Quadrante 02": ["2"]}
    valores_filtro_quadrante = mapeamento_quadrantes.get(quadrante_selecionado, [])
    arquivo_imagem = MAPAS_DISPONIVEIS[quadrante_selecionado]
    try:
        img = Image.open(arquivo_imagem)
        img_width, img_height = img.size
    except FileNotFoundError:
        fig_erro = go.Figure()
        fig_erro.update_layout(title=f"Erro: Imagem '{arquivo_imagem}' não encontrada!", template="plotly_dark")
        return fig_erro
    pontos_do_quadrante = pontos_no_mapa[pontos_no_mapa['Quadrante'].isin(valores_filtro_quadrante)]
    pontos_para_plotar = pontos_do_quadrante[pontos_do_quadrante[COLUNA_SEGMENTO].isin(segmentos_visiveis)]
    fig = go.Figure()
    TAMANHO_ICONE = 80
    for segmento in segmentos_visiveis:
        cor = mapa_de_cores.get(segmento)
        pontos_do_segmento = pontos_para_plotar[pontos_para_plotar[COLUNA_SEGMENTO] == segmento]
        if pontos_do_segmento.empty:
            continue
        fig.add_trace(go.Scatter(
            x=pontos_do_segmento['Coordenada X'], y=pontos_do_segmento['Coordenada Y'], name=segmento, mode='markers',
            marker=dict(symbol='square', color=cor, size=30, opacity=0),
            hovertext=pontos_do_segmento['hover_text'], hoverinfo='text',
        ))
    fig.add_layout_image(dict(source=img, xref="x", yref="y", x=0, y=0, sizex=img_width, sizey=img_height, sizing="stretch", layer="below"))
    for index, row in pontos_para_plotar.iterrows():
        segmento_ponto = row[COLUNA_SEGMENTO]
        nome_arquivo_icone = mapa_de_icones.get(segmento_ponto)
        if nome_arquivo_icone:
            try:
                caminho_completo = f"assets/{nome_arquivo_icone}"
                icone_img = Image.open(caminho_completo)
                fig.add_layout_image(
                    dict(
                        source=icone_img, xref="x", yref="y",
                        x=row['Coordenada X'], y=row['Coordenada Y'],
                        sizex=TAMANHO_ICONE, sizey=TAMANHO_ICONE,
                        xanchor="center", yanchor="middle", layer="above"
                    )
                )
            except FileNotFoundError:
                print(f"AVISO: Ícone não encontrado em '{caminho_completo}'.")
                fig.add_trace(go.Scatter(
                    x=[row['Coordenada X']], y=[row['Coordenada Y']], mode='markers',
                    marker=dict(color=mapa_de_cores.get(segmento_ponto), size=15, line=dict(width=2, color='DarkSlateGrey')),
                    hoverinfo='none', showlegend=False,
                ))
        else:
            fig.add_trace(go.Scatter(
                x=[row['Coordenada X']], y=[row['Coordenada Y']], mode='markers',
                marker=dict(color=mapa_de_cores.get(segmento_ponto, 'grey'), size=15, line=dict(width=2, color='DarkSlateGrey')),
                hoverinfo='none', showlegend=False,
            ))
    fig.update_layout(
        title=f"Localização dos Estabelecimentos por Quadrante: {quadrante_selecionado}",
        xaxis=dict(showgrid=False, visible=False, range=[0, img_width]),
        yaxis=dict(showgrid=False, visible=False, range=[img_height, 0]),
        template="plotly_dark",
        margin=dict(l=0, r=0, t=40, b=0),
        height=900,
        showlegend=False
    )
    return fig

# --- CALLBACK PARA ABRIR/FECHAR E PREENCHER O MODAL ---
@app.callback(
    Output("info-modal", "is_open"),
    Output("modal-header", "children"),
    Output("modal-body", "children"),
    Input("mapa-da-feira", "clickData"),
    State("info-modal", "is_open"),
)
def toggle_modal(clickData, is_open):
    if not clickData:
        return False, no_update, no_update
    try:
        hover_text = clickData['points'][0]['hovertext']
        match = re.search(r"id:(\d+)", hover_text)
        if not match:
            return no_update, no_update, no_update
        
        ponto_clicado_index = int(match.group(1))
        info_completa = planilha_final.loc[ponto_clicado_index]
        
        header = f"{info_completa.get(COLUNA_NOME_BARRACA_01, 'Não informado')}"
        
        # --- INÍCIO DA MODIFICAÇÃO ---

        # 1. Preparar o conteúdo de texto
        info_textual = html.Div([
            html.P([html.Strong("Responsável: "), info_completa.get(COLUNA_RESPONSAVEL, 'Não informado')]),
            html.P([html.Strong("Segmento: "), info_completa.get(COLUNA_SEGMENTO, 'Não informado')]),
            html.P([html.Strong("Telefone: "), info_completa.get('Telefone', 'Não informado')]),
            html.P([html.Strong("Numeração do Box: "), info_completa.get('Numeração do Box', 'Não informado')]),
            html.P([html.Strong("Nº de Funcionários: "), f"{info_completa.get('Número de funcionários', 'Não informado')}"]),
        ])
        
        # 2. Preparar o conteúdo da imagem
        imagem_fachada = html.Div() # Começa vazio
        url_fachada = info_completa.get('URL_Fachada')
        if pd.notna(url_fachada) and url_fachada:
            imagem_fachada = html.Img(
                src=url_fachada, 
                style={
                    'width': '100%', 
                    'maxWidth': '350px', # Tamanho máximo para não ficar muito grande
                    'height': 'auto', 
                    'borderRadius': '5px',
                    'display': 'block',
                    'marginLeft': 'auto',
                    'marginRight': 'auto'
                }
            )

        # 3. Combinar texto e imagem em um layout de duas colunas
        body = dbc.Row([
            dbc.Col(info_textual, md=7), # Coluna da esquerda para o texto
            dbc.Col(imagem_fachada, md=5, className="d-flex align-items-center justify-content-center") # Coluna da direita para a imagem, centralizada
        ], align="center")

        # --- FIM DA MODIFICAÇÃO ---
        
        return not is_open, header, body
    except (KeyError, IndexError, ValueError) as e:
        print(f"Erro ao processar clickData para o modal: {e}")
        return False, no_update, no_update

# --- EXECUÇÃO DA APLICAÇÃO ---
# Bloco removido para deploy, pois o Render usará o Procfile e a variável 'server'
# if __name__ == '__main__':
#     app.run_server(debug=False)
