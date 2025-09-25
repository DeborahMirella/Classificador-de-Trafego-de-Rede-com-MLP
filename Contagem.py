import pandas as pd
from sklearn.preprocessing import LabelEncoder

NOME_ARQUIVO_LIMPO = 'CICIDS.csv' 

print(f"Carregando o arquivo '{NOME_ARQUIVO_LIMPO}' para verificar as classes...")

try:
    df = pd.read_csv(NOME_ARQUIVO_LIMPO)
    
  
    le = LabelEncoder()
    
    le.fit(df['Label'])
    
    print("\nDicionário Oficial de Classes")

    for indice, nome_da_classe in enumerate(le.classes_):
        print(f"Classe {indice} -> {nome_da_classe}")

    print("\nVerificação concluída com sucesso.")

except FileNotFoundError:
    print(f"\nERRO: O arquivo '{NOME_ARQUIVO_LIMPO}' não foi encontrado.")
except Exception as e:
    print(f"\nOcorreu um erro: {e}")