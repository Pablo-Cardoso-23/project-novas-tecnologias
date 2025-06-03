import pandas as pd
from sklearn.cluster import KMeans
import os

# Função para limpar e converter valores de coordenadas
def limpar_valor(val):
    if pd.isna(val):
        return None
    # Converte para string, remove espaços e substitui vírgula por ponto
    s = str(val).strip().replace(',', '.')
    try:
        return float(s)
    except ValueError:
        # LOG: Imprimir valores que falham na conversão
        # print(f"CONTROLADORES (limpar_valor): Erro ao converter '{s}' (original: '{val}') para float.")
        return None

def gerar_pontos_criticos(caminho_csv, k=10): # Definindo um valor padrão para k
    try:
        # print(f"CONTROLADORES: Lendo CSV de: {caminho_csv}")
        if not os.path.exists(caminho_csv):
            print(f"CONTROLADORES: ERRO - Arquivo CSV não encontrado em: {caminho_csv}")
            return []

        df = pd.read_csv(caminho_csv, sep=';')
        # print(f"CONTROLADORES: CSV lido. Colunas: {df.columns.tolist()}")

        if 'latitude' not in df.columns or 'longitude' not in df.columns:
            print("CONTROLADORES: ERRO - Colunas 'latitude' ou 'longitude' não encontradas no CSV.")
            return []

        # Aplicar a limpeza
        df['latitude_limpa'] = df['latitude'].apply(limpar_valor)
        df['longitude_limpa'] = df['longitude'].apply(limpar_valor)

        # LOG: Verificar NaNs após a limpeza inicial
        # print(f"CONTROLADORES: NaNs em 'latitude_limpa' APÓS limpar_valor: {df['latitude_limpa'].isna().sum()}")
        # print(f"CONTROLADORES: NaNs em 'longitude_limpa' APÓS limpar_valor: {df['longitude_limpa'].isna().sum()}")

        # Criar dataframe de coordenadas e remover quaisquer linhas com NaNs resultantes da limpeza
        coordenadas = df[['latitude_limpa', 'longitude_limpa']].copy()
        coordenadas.rename(columns={'latitude_limpa': 'latitude', 'longitude_limpa': 'longitude'}, inplace=True) # Renomear para consistência
        coordenadas.dropna(inplace=True)

        # print(f"CONTROLADORES: Número de registros válidos para KMeans APÓS dropna: {len(coordenadas)}")
        if coordenadas.empty:
            print("CONTROLADORES: ALERTA - Nenhuma coordenada válida após limpeza e dropna. Não é possível aplicar KMeans.")
            return []

        # LOG: Descrever os dados que vão para o KMeans
        # print("CONTROLADORES: Estatísticas das coordenadas ANTES do KMeans (após limpeza e dropna):")
        # print(coordenadas.describe())
        
        # Garantir que k não é maior que o número de amostras disponíveis
        if len(coordenadas) < k:
            print(f"CONTROLADORES: ALERTA - Número de amostras válidas ({len(coordenadas)}) é menor que k ({k}). Ajustando k para {len(coordenadas)}.")
            k = len(coordenadas)
        
        if k == 0: # Se não houver coordenadas válidas, não podemos rodar o KMeans
             print("CONTROLADORES: ALERTA - k é 0, não há dados para KMeans.")
             return []

        # print(f"CONTROLADORES: Aplicando KMeans com k={k}")
        # Adicionado n_init='auto' para compatibilidade e para suprimir warnings de versões futuras.
        modelo = KMeans(n_clusters=k, random_state=42, n_init='auto') 
        modelo.fit(coordenadas)
        centros = modelo.cluster_centers_

        pontos_criticos = []
        for i, centro in enumerate(centros):
            # LOG: Imprimir cada centróide gerado
            # print(f"CONTROLADORES: Centróide {i}: lat={float(centro[0])}, lng={float(centro[1])}")
            pontos_criticos.append({'lat': float(centro[0]), 'lng': float(centro[1])})
        
        return pontos_criticos

    except Exception as e:
        print(f"CONTROLADORES: ERRO GERAL em gerar_pontos_criticos: {e}")
        import traceback
        traceback.print_exc()
        return []