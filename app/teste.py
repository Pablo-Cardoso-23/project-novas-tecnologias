import pandas as pd
import os

caminho_csv = os.path.join(os.path.dirname(__file__), 'data', 'ocorrenciasdf.csv')
print(caminho_csv)
df = pd.read_csv(caminho_csv)
print(df.columns)
