# Classificador de Tráfego de Rede com Perceptron de Múltiplas Camadas (MLP)

Um projeto acadêmico de Machine Learning para a detecção de intrusão em redes de computadores, utilizando um modelo de Deep Learning para classificar tráfego benigno e malicioso. Esta obra foi desenvolvida como um exercício de ponta a ponta, abrangendo desde a limpeza de dados brutos até a avaliação rigorosa do modelo.

## 📋 Tabela de Conteúdos
1.  [Visão Geral do Projeto](#-visão-geral-do-projeto)
2.  [Dataset Utilizado](#-dataset-utilizado)
3.  [Metodologia e Fluxo de Trabalho](#-metodologia-e-fluxo-de-trabalho)
4.  [🚀 Instalação e Configuração](#-instalação-e-configuração)
5.  [🏃‍♂️ Como Executar](#️-como-executar)
6.  [📈 Resultados](#-resultados)
7.  [💡 Trabalhos Futuros](#-trabalhos-futuros)
8.  [Autora](#-autora)
9.  [Licença](#-licença)

## 📖 Visão Geral do Projeto

Este projeto implementa um classificador baseado em um Perceptron de Múltiplas Camadas (MLP) para identificar diferentes tipos de ataques cibernéticos a partir de dados de fluxo de rede. O objetivo é criar um pipeline de Machine Learning robusto, que seja capaz de processar um grande volume de dados, treinar um modelo de classificação multiclasse e avaliar sua performance de forma crítica e detalhada.

## 📊 Dataset Utilizado

O modelo foi treinado e avaliado utilizando o dataset **WTMC2021**, que contém uma vasta coleção de tráfego de rede capturado, incluindo tanto atividades benignas quanto uma diversidade de ataques modernos. As características (features) são baseadas em estatísticas de fluxo de rede, como duração, contagem de pacotes, tamanho dos pacotes, entre outras.

## 🏗️ Metodologia e Fluxo de Trabalho

O projeto foi estruturado de forma modular em um pipeline de três scripts principais para garantir a organização, eficiência e reprodutibilidade do processo:

1.  **`1_Carga_e_Limpeza.py`**: Responsável por carregar os múltiplos arquivos CSV brutos, unificá-los, e realizar uma limpeza fundamental, removendo dados corrompidos e colunas sem variância.
2.  **`2_Preparacao_Final.py`**: Pega o dataset limpo e o prepara para o modelo. Realiza a codificação dos rótulos (`LabelEncoder`), a divisão estratificada dos dados em conjuntos de treino e teste, e a normalização das características (`StandardScaler`).
3.  **`3_Treinamento_e_Avaliacao_MLP.py`**: Utiliza os dados preparados para definir, treinar e avaliar o modelo MLP. Ao final, gera um relatório de performance detalhado e visualizações como a Matriz de Confusão e a Curva de Perda.

## 🚀 Instalação e Configuração

Para executar este projeto em sua máquina local, siga os passos abaixo.

### Pré-requisitos
- Anaconda ou Miniconda instalado.

### Passos

1.  **Clone este repositório:**
    ```bash
    git clone [URL_DO_SEU_REPOSITORIO_GIT]
    cd [NOME_DA_PASTA_DO_PROJETO]
    ```

2.  **Crie o ambiente Conda:**
    É altamente recomendado criar um ambiente virtual para isolar as dependências do projeto. Execute o comando abaixo para criar o ambiente a partir do arquivo `environment.yml` (se fornecido).
    ```bash
    conda env create -f environment.yml
    ```
    *(**Nota:** Para criar o arquivo `environment.yml` a partir do seu ambiente já configurado, execute `conda env export > environment.yml`)*

3.  **Ative o ambiente:**
    ```bash
    conda activate MLP_cic_ids
    ```

## 🏃‍♂️ Como Executar

Com o ambiente configurado e ativo, execute os scripts na ordem correta:

1.  **Coloque os arquivos do dataset** na pasta `/data` (ou atualize o caminho no `Script 1`).

2.  **Execute o script de limpeza e unificação:**
    ```bash
    python 1_Carga_e_Limpeza.py
    ```
    *Isso irá gerar o arquivo `WTMC2021_limpo_unificado.csv`.*

3.  **Execute o script de preparação final:**
    ```bash
    python 2_Preparacao_Final.py
    ```
    *Isso irá gerar os quatro arquivos: `X_train_scaled.csv`, `X_test_scaled.csv`, `y_train.csv` e `y_test.csv`.*

4.  **Execute o script de treinamento e avaliação:**
    ```bash
    python 3_Treinamento_e_Avaliacao_MLP.py
    ```
    *Isso irá treinar o modelo, imprimir os resultados no terminal e salvar os gráficos de avaliação.*

## 📈 Resultados

O modelo final alcançou uma acurácia geral de **[insira sua acurácia, ex: 99.88%]**. A análise detalhada da performance, incluindo a Matriz de Confusão, revela um alto desempenho na detecção de classes volumétricas, mas aponta desafios na identificação de ataques com poucas amostras no dataset.

*(Aqui, a irmã pode inserir a imagem da sua Matriz de Confusão e outros gráficos)*

**Matriz de Confusão:**
![Matriz de Confusão](matriz_confusao.png)

## 💡 Trabalhos Futuros

Como aprimoramento desta obra, os seguintes caminhos podem ser explorados:
-   **Tratamento de Desbalanceamento:** Aplicação de técnicas de reamostragem, como o **SMOTE**, para melhorar o desempenho nas classes minoritárias.
-   **Otimização de Hiperparâmetros:** Utilização de ferramentas como **`GridSearchCV`** para encontrar a arquitetura de rede e os parâmetros de treinamento ideais.
-   **Modelos Alternativos:** Comparação do desempenho do MLP com outros algoritmos, como Random Forest e XGBoost.

## ✍️ Autora

* **Deborah Mirella**

## 📜 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
