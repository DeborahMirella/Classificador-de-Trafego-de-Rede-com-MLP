print("Iniciando o Script 1: Carregamento e Limpeza")

import pandas as pd
import numpy as np
import os
from time import time
from sklearn.feature_selection import VarianceThreshold
import warnings

warnings.filterwarnings('ignore', category=pd.errors.DtypeWarning)
warnings.filterwarnings('ignore', category=FutureWarning)

DATA_PATH = "/home/deborahmirella/Área de trabalho/IC2025/WTMC2021-Code/LabelledDataset/"
filenames = [
   "Friday-WorkingHours.pcap_REVI.csv", 
   "Monday-WorkingHours.pcap_REVI.csv",
   "Thursday-WorkingHours.pcap_REVI.csv", 
   "Tuesday-WorkingHours.pcap_REVI.csv",
   "Wednesday-WorkingHours.pcap_REVI.csv"
]

print("Iniciando Etapa 1: Carregamento e Unificação")
start_time = time()

list_of_dfs = []
for file in filenames:
    file_path = os.path.join(DATA_PATH, file)
    try:
        print(f"Carregando: {file}")
        df_temp = pd.read_csv(file_path, low_memory=False)
        df_temp.columns = df_temp.columns.str.strip()
        list_of_dfs.append(df_temp)
    except FileNotFoundError:
        print(f"O arquivo '{file}' não foi encontrado. Pulando.")
    except Exception as e:
        print(f"Erro ao carregar '{file}': {e}. Pulando.")

if not list_of_dfs:
    print("\nNenhum dado foi carregado.")
    exit()

print("\nConcatenando os DataFrames")
df = pd.concat(list_of_dfs, ignore_index=True)
print(f"Unificação concluída. Dimensão atual: {df.shape}")

print("\nIniciando Etapa 2: Limpeza e Tratamento")

# 1. Tratamento da Integridade das Amostras (Linhas)

# Trata valores nulos e infinitos
print("Tratando valores nulos e infinitos")

# Esta linha executa uma padronização de valores inválidos. Durante a extração de características de rede, operações como divisão por zero podem gerar valores de infinito (np.inf) e infinito negativo (-np.inf). 
# Este comando substitui todas as ocorrências desses valores pelo marcador padrão de dados ausentes do Pandas, np.nan (Not a Number), unificando todos os dados problemáticos sob uma única representação
df.replace([np.inf, -np.inf], np.nan, inplace=True)

# Guarda o número de linhas ANTES da remoção
# Para fins de documentação e transparência, esta linha registra o número total de amostras (linhas) presentes no DataFrame antes da etapa de remoção. 
# O atributo .shape retorna as dimensões (linhas, colunas), e o índice [0] seleciona especificamente a contagem de linhas.
linhas_antes = df.shape[0]

# Remove as linhas com dados nulos
# Este comando itera sobre cada linha do DataFrame e remove, de forma definitiva (inplace=True), qualquer linha que contenha ao menos um valor np.nan. 
# Esta operação é crucial, pois os algoritmos de redes neurais não podem processar dados ausentes, e garante que apenas amostras completas e íntegras prossigam para o treinamento.
df.dropna(inplace=True)

# Calcula e informa quantas linhas foram removidas
linhas_removidas = linhas_antes - df.shape[0]
print(f"Verificação de integridade concluída. Removidas {linhas_removidas} linhas com dados nulos/infinitos.")

# 2. Tratamento da Relevância das Características (Colunas)

# Remoção de Colunas de Baixa Variância
print("Procurando por colunas com variância zero (constantes)")

# Essa parte eu não entendi muito bem 

if 'Label' in df.columns: # Inicia-se uma verificação de segurança para garantir a presença da variável alvo
    X_numeric = df.drop(columns=['Label']).select_dtypes(include=np.number) # Esta linha isola as características preditoras que serão analisadas. Primeiramente, a coluna alvo (Label) é temporariamente removida (.drop()). Em seguida, o método .select_dtypes(include=np.number) filtra o resultado, criando um novo DataFrame X_numeric que contém exclusivamente as colunas de tipo numérico.
    y_labels = df['Label'] #  A variável alvo é armazenada de forma segura para ser reincorporada ao DataFrame após a limpeza das características
else:
    X_numeric = df.select_dtypes(include=np.number)
    y_labels = None

selector = VarianceThreshold() # Uma instância da classe VarianceThreshold do Scikit-learn é criada. Este algoritmo de seleção de características é projetado para remover todas as features cuja variância não atinge um certo limiar. Por padrão, o limiar é zero
selector.fit(X_numeric) # Esta é a fase de análise. O objeto selector calcula a variância para cada uma das colunas no DataFrame X_numeric e internamente identifica quais delas possuem variância zero.
cols_to_keep_auto = X_numeric.columns[selector.get_support()] # O método .get_support() retorna uma máscara booleana (um vetor de True/False), onde True corresponde às colunas com variância superior ao limiar. Ao aplicar esta máscara aos nomes das colunas de X_numeric, geramos uma lista final (cols_to_keep_auto) contendo apenas os nomes das características informativas que devem ser mantidas
colunas_removidas_auto = sorted(list(set(X_numeric.columns) - set(cols_to_keep_auto)))

if colunas_removidas_auto:
    print(f"\nRemoção automática ({len(colunas_removidas_auto)} colunas):")
    print(f"Motivo: Variância zero (colunas constantes, sem informação).")
    print(f"Colunas Removidas: {colunas_removidas_auto}")
else:
    print("\nRemoção automática: Nenhuma coluna com variância zero foi encontrada.")

# Reconstrói o DataFrame com as colunas relevantes
df = df[list(cols_to_keep_auto)]
if y_labels is not None:
    df['Label'] = y_labels

# Remoção manual das colunas solicitadas
cols_to_remove_manually = ['src_port', 'dst_port', 'protocol']
# Verifica quais dessas colunas realmente existem no DataFrame para evitar erros
existing_cols_to_remove = [col for col in cols_to_remove_manually if col in df.columns]

if existing_cols_to_remove:
    print(f"\nRemoção Manual ({len(existing_cols_to_remove)} colunas):")
    print(f"Motivo: Solicitado por mim.")
    print(f"Colunas Removidas: {existing_cols_to_remove}")
    df.drop(columns=existing_cols_to_remove, inplace=True)
else:
    print("\nRemoção ManualL: Nenhuma das colunas solicitadas foi encontrada para remoção.")

    
print(f"\nLimpeza concluída. Dimensão final: {df.shape}")

output_filename = 'CICIDS.csv'
print(f"\nIniciando Etapa 3: Salvamento")
print(f"Salvando o DataFrame limpo e unificado em '{output_filename}'.")
df.to_csv(output_filename, index=False)
end_time = time()
print(f"Arquivo salvo com sucesso! Processo total levou {end_time - start_time:.2f} segundos.")
print("\nScript Concluído")


