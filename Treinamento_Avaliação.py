print("Iniciando o Script: Treinamento e Avaliação do MLP.")

import pandas as pd
import numpy as np 
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import seaborn as sns
import matplotlib.pyplot as plt
from time import time
import warnings

# Ignora avisos
warnings.filterwarnings('ignore', category=UserWarning, module='sklearn')


def plot_loss(model):
    """Plota a curva de minimização de perda do modelo."""
    plt.figure() 
    plt.plot(model.loss_curve_)
    plt.title('Minimização da Perda (Erro) do Gradiente')
    plt.xlabel('Épocas de Treinamento')
    plt.ylabel('Valor da Perda (Loss)')
    
def nn_diagram(X, y, model, show_weights=False): 
    """Desenha um diagrama da arquitetura da rede neural."""
    try:
        import VisualizeNN as VisNN
        # Cria uma estrutura de rede a partir das formas dos dados e camadas ocultas
        nn_struct = np.hstack(([X.shape[1]], np.asarray(model.hidden_layer_sizes), [y.shape[1]]))

        # Somente plota pesos se especificado.
        if show_weights:
            network = VisNN.DrawNN(nn_struct, model.coefs_)
        else:
            network = VisNN.DrawNN(nn_struct)
            
        network.draw()
        plt.title('Diagrama da Arquitetura do MLP')
    except ImportError:
        print("\nAVISO: Módulo 'VisualizeNN' não encontrado. Pulando o diagrama da arquitetura.")
    except Exception as e:
        print(f"\nOcorreu um erro ao gerar o diagrama da rede: {e}")

# Carregar os dados preparados 
print("\nCarregando os dados de treinamento e teste.")
try:
    X_train = pd.read_csv('X_train_scaled.csv')
    X_test = pd.read_csv('X_test_scaled.csv')
    y_train = pd.read_csv('y_train.csv')
    y_test = pd.read_csv('y_test.csv')
    class_names = np.load('classes.npy', allow_pickle=True)
    print("Dados e mapeamento de classes carregados com sucesso.")
except FileNotFoundError:
    print("ERRO: Arquivos de dados preparados não encontrados. Execute o Script 2 primeiro.")
    exit()

# Definir e treinar o modelo MLP
print("\nDefinindo a arquitetura do MLP.")
mlp = MLPClassifier(hidden_layer_sizes=(64, 32),
                    activation='relu',
                    solver='adam',
                    max_iter=500,
                    random_state=42,
                    verbose=True)

print("\nIniciando o treinamento do modelo...")
start_time = time()
mlp.fit(X_train, y_train.values.ravel())
end_time = time()
print(f"Treinamento concluído em {end_time - start_time:.2f} segundos.")

# Avaliar o desempenho do modelo 
print("\nRealizando predições no conjunto de teste.")
y_pred = mlp.predict(X_test)


# y_test e y_pred já estão no formato de lista simples (1D), então a conversão com .argmax() não é mais necessária.
# Uso .ravel() para garantir que y_test seja um vetor 1D.

y_test_labels = y_test.values.ravel()
y_pred_labels = y_pred # y_pred já está no formato correto.


# Calculo explícito da acurácia
accuracy = accuracy_score(y_test_labels, y_pred_labels)
print("\n\n ACURÁCIA GERAL")
print(f"A Acurácia Geral do modelo é: {accuracy:.4f} (ou {accuracy:.2%})")

print("\n\n RELATÓRIO DE AVALIAÇÃO DO MODELO")
report = classification_report(y_test_labels, y_pred_labels, labels=range(len(class_names)), target_names=class_names, zero_division=0, digits=4)
print(report)

# MATRIZ DE CONFUSÃO
print("\nMATRIZ DE CONFUSÃO")
try:
    cm = confusion_matrix(y_test_labels, y_pred_labels)
    plt.figure(figsize=(14, 11))
    sns.heatmap(cm, annot=True, fmt='d', xticklabels=class_names, yticklabels=class_names, cmap='Blues')
    plt.title('Matriz de Confusão', fontsize=16)
    plt.ylabel('Classe Verdadeira', fontsize=12)
    plt.xlabel('Classe Predita', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig('matriz_confusao.png', dpi=300)
    print("\nGráfico da Matriz de Confusão salvo como 'matriz_confusao.png'")
except Exception as e:
    print(f"\n>>> OCORREU UM ERRO INESPERADO ao criar ou salvar o gráfico: {e}")

print("\nScript 3 Concluído.")