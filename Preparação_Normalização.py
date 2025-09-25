print("Iniciando o Script 2: Preparação Final dos Dados.")

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from time import time
from imblearn.over_sampling import SMOTE

start_script_time = time()

print("\nCarregando o arquivo 'CICIDS'")
try:
    df_limpo = pd.read_csv('CICIDS.csv')
    print("Arquivo limpo carregado com sucesso.")
    print(f"Dimensões: {df_limpo.shape}")
except FileNotFoundError:
    print("ERRO: 'CICIDS.csv' não encontrado. Execute o Script de Limpeza corretamente")
    exit()
except Exception as e:
    print(f"Ocorreu um erro ao ler o arquivo: {e}")
    exit()

print("\nSeparando e codificando as variáveis")

# X contém todas as colunas de características
X = df_limpo.drop(columns=['Label'])
y_texto = df_limpo['Label']

# Substituição de One-Hot Encoding por Label Encoding
# No método anterior, eu usava: y = pd.get_dummies(df_limpo['Label'])
# Agora, implementei a codificação por rótulos numéricos (0 a 14), (que é mais eficiente em termos de memória)

# Cria, treina e aplica o LabelEncoder para converter texto em números
le = LabelEncoder()
y_encoded = le.fit_transform(y_texto)

# Converte o resultado de volta para um DataFrame para manter a consistência.
y = pd.DataFrame(y_encoded, columns=['Label'])

# Salva o "dicionário" de classes para uso no Script 3!
np.save('classes.npy', le.classes_)

print("Mapeamento de classes (dicionário) salvo em 'classes.npy'.")

print("\nDividindo em conjuntos de treinamento e teste")

# Divide os dados em 70% para treino e 30% para teste.
# 'stratify=y' garante que a proporção das classes seja a mesma em ambos os conjuntos
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
print(f"Tamanho do treino: {X_train.shape[0]} amostras | Tamanho do teste: {X_test.shape[0]} amostras.")

print("\nDistribuição de Classes antes do SMOTE ")

# Calcula a contagem original no treino
unique_original, counts_original = np.unique(y_train, return_counts=True)
contagem_treino_original = dict(zip(le.inverse_transform(unique_original), counts_original))

# Converte os valores numpy.int64 para int padrão para uma impressão limpa
contagem_treino_limpa = {classe: int(contagem) for classe, contagem in contagem_treino_original.items()}


print("Contagem no Conjunto de Treino:", contagem_treino_limpa)

print("\nAplicando o Rebalanceamento (Oversampling)")

# 1° Estratégia (SMOTE)

""" Manter a contagem original da classe BENIGN.

Manter a contagem original de qualquer classe de ataque que já tenha mais de 20.000 amostras.

Elevar a contagem para 20.000 para qualquer classe de ataque que tenha menos de 20.000 amostras. 

"""

"""
print("\nDefinindo a estratégia de rebalanceamento manualmente")

sampling_strategy = {

    # Regra 1: Manter a classe majoritária
    0:  1788058,  # BENIGN 

    # Regra 2: Manter as classes minoritárias que já são grandes 
    2:  68634,   # DDoS 
    4:  43074,   # DoS Hulk 
    10: 159152,  # PortScan 

    # Regra 3: Elevar todas as outras classes minoritárias "raras" para 20.000
    1:  20000,    # Bot 
    3:  20000,    # DoS GoldenEye 
    5:  20000,    # DoS Slowhttptest 
    6:  20000,    # DoS slowloris 
    7:  20000,    # FTP-Patator 
    8:  20000,    # Heartbleed 
    9:  20000,    # Infiltration 
    11: 20000,    # SSH-Patator
    12: 20000,    # Web Attack - Brute Force 
    13: 20000,    # Web Attack - Sql Injection 
    14: 20000,    # Web Attack - XSS 
}

# O restante do código do SMOTE usa este dicionário manual

print("Rebalanceando as classes com SMOTE e estratégia manualmente")

smote = SMOTE(sampling_strategy=sampling_strategy, k_neighbors=1, random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)

print("Rebalanceamento concluído.")

print(f"Tamanho do treino APÓS o SMOTE: {X_train_resampled.shape[0]} amostras")
unique, counts = np.unique(y_train_resampled, return_counts=True)

print("Nova distribuição de classes no treino:", dict(zip(le.inverse_transform(unique), counts)))

"""

# 2° Estratégia (SMOTE)

print("\nDefinindo a estratégia de rebalanceamento com base nos números fornecidos")

sampling_strategy = {

    
    0: 1836922,  # BENIGN
    1: 2201,     # Bot
    2: 92282,    # DDoS
    3: 9027,     # DoS GoldenEye
    4: 156340,   # DoS Hulk
    5: 6008,     # DoS Slowhttptest
    6: 8793,     # DoS slowloris
    7: 3973,     # FTP-Patator
    8: 300,      # Heartbleed
    9: 300,      # Infiltration
    10: 159421,  # PortScan
    11: 2980,    # SSH-Patator
    12: 1365,    # Web Attack - Brute Force
    13: 300,     # Web Attack - Sql Injection
    14: 679,     # Web Attack - XSS

}

print("Estratégia manual definida. Rebalanceando as classes com SMOTE")

# O SMOTE agora usa este dicionário manual diretamente
# Mantemos k_neighbors=1 por segurança, para lidar com as classes ultra-raras
smote = SMOTE(sampling_strategy=sampling_strategy, k_neighbors=1, random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)

print("\nRebalanceamento concluído.")

print(f"Tamanho do treino APÓS o SMOTE: {X_train_resampled.shape[0]} amostras")

unique, counts = np.unique(y_train_resampled, return_counts=True)

# Cria o dicionário original, que ainda contém os tipos de dados do NumPy
contagem_original_apos_smote = dict(zip(le.inverse_transform(unique), counts))
contagem_limpa_apos_smote = {classe: int(contagem) for classe, contagem in contagem_original_apos_smote.items()}
print("Nova distribuição de classes no treino:", dict(zip(le.inverse_transform(unique), counts)))


# Normalizar as Características
print("\nNormalizando as características")

# Cria a ferramenta de normalização Z-score.
scaler = StandardScaler()

# Aprende a média e o desvio padrão apenas com os dados de treino.
scaler.fit(X_train_resampled)

# Aplica a normalização aprendida em ambos os conjuntos.
X_train_scaled = scaler.transform(X_train_resampled)
X_test_scaled = scaler.transform(X_test)

# Converte os arrays resultantes de volta para DataFrames.
X_train_scaled = pd.DataFrame(X_train_scaled, columns=X.columns)
X_test_scaled = pd.DataFrame(X_test_scaled, columns=X.columns)
print("Normalização concluída.")

# Salvar os conjuntos de dados preparados
print("\nSalvando os 4 arquivos finais...")
X_train_scaled.to_csv('X_train_scaled.csv', index=False)
X_test_scaled.to_csv('X_test_scaled.csv', index=False)

# Antigo
# y_train.to_csv('y_train.csv', index=False)
# y_test.to_csv('y_test.csv', index=False)

pd.DataFrame(y_train_resampled).to_csv('y_train.csv', index=False, header=['Label'])
pd.DataFrame(y_test).to_csv('y_test.csv', index=False, header=['Label'])

print("Arquivos salvos: X_train_scaled.csv, X_test_scaled.csv, y_train.csv, y_test.csv")

end_script_time = time()
print(f"\nTempo total de execução do Script: {end_script_time - start_script_time:.2f} segundos.")
print("\n Script 2 (Preparação Final) Concluído")

"""
Por que eu optei pela padronização z-score?

A Normalização Min-Max, que reescala os dados para um intervalo fixo [0,1], é extremamente sensível a outliers. 
Em um conjunto de dados de tráfego de rede, onde ataques podem gerar valores anômalos de magnitude muito superior à do tráfego normal, 
a presença de um único outlier poderia comprimir a maioria dos dados em um intervalo muito pequeno, resultando na perda de informação variacional.
A Padronização (Z-score), que reescala as características para que tenham uma média de 0 e um desvio padrão de 1, é mais robusta a outliers. 
Ela trata os valores extremos como pontos distantes da média, preservando a estrutura e a distribuição da maioria dos dados. Dado que os dados de deteção de intrusão 
são caracterizados pela presença de picos e valores extremos, a escolha do StandardScaler foi uma decisão metodológica deliberada para garantir que a escala das características 
não fosse distorcida por esses eventos, proporcionando um aprendizado mais estável e fidedigno para o modelo. 

O Que São Cada Um Desses Quatro Arquivos?

Estes quatro arquivos representam a divisão de todos os dados em dois pares. 

O Par de Treinamento 

Este é o conjunto de dados maior (70% do total) que usei para ensinar o modelo.

    X_train_scaled.csv: Dados de treino normalizados

    y_train.csv: Os rótulos de treinamento. Durante o treinamento, o modelo olha para X_train_scaled, faz uma previsão e a compara com y_train para aprender com seus erros.

O Par de Teste 

Este é o conjunto de dados menor (30% do total) que não foi usado durante todo o treinamento e é usado para uma avaliação final e imparcial.

    X_test_scaled.csv: Dados sem os rótulos 

    y_test.csv: Os rótulos.

Por Que optei por Separar Assim?

A decisão de separar os dados desta forma é um pilar que garante a integridade e a honestidade de todo o meu projeto. Existem três razões principais para isso:

    Para uma Avaliação Honesta e Evitar o "Overfitting":
    A razão mais importante. Se avaliássemos o modelo com os mesmos dados que ele usou para treinar, o modelo estaria viciado pois já sabria todas as respostas.

    Para Prevenir o Vazamento de Dados:
    Como estudei, a régua de normalização (fit) é usada apenas os dados de treino. Se não tivéssemos separado os dados antes, eu podería acidentalmente usar informações do conjunto de teste para calibrar essa régua, o que "contaminaria" o treinamento e redultaria em uma falsa sensação de sucesso.

    Para Eficiência no Desenvolvimento:
    A preparação dos dados (Scripts 1 e 2) é um processo pesado e demorado. O treinamento (Script 3) é onde eu quero os resultados. Ao salvar estes quatro arquivos, posso fazer o trabalho pesado apenas uma vez. Depois, posso rodar o Script 3 várias vezes, testando diferentes modelos e arquiteturas (se necessário)

"""