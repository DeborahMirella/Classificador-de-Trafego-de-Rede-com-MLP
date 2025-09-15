# Classificador de Tráfego de Rede com MLP

Uma pesquisa acadêmica de IA aplicada para Cibersegurança para a detecção de intrusão em redes de computadores, utilizando um modelo de Deep Learning para classificar tráfego benigno e múltiplas classes de ataques.

## 📋 Tabela de Conteúdos
1.  [Visão Geral do Projeto](#-visão-geral-do-projeto)
2.  [Dataset Utilizado](#-dataset-utilizado)
3.  [Metodologia e Fluxo de Trabalho](#-metodologia-e-fluxo-de-trabalho)
4.  [🚀 Instalação e Configuração](#-instalação-e-configuração)
5.  [🏃‍♂️ Como Executar](#️-como-executar)
6.  [📈 Resultados Esperados](#-resultados-esperados)
7.  [💡 Trabalhos Futuros](#-trabalhos-futuros)
8.  [Autora](#-autora)
9.  [Licença](#-licença)

## 📖 Visão Geral do Projeto

Este projeto implementa um classificador baseado em um Perceptron de Múltiplas Camadas (MLP) para identificar diferentes tipos de ataques cibernéticos a partir de dados de fluxo de rede. O objetivo é criar um pipeline de Machine Learning robusto e reprodutível, que seja capaz de processar um grande volume de dados, treinar um modelo de classificação multiclasse e avaliar sua performance de forma detalhada e transparente.

## 📊 Dataset Utilizado

O modelo foi treinado e avaliado utilizando o dataset **CIC-IDS-2017**. Este é um conjunto de dados público e amplamente reconhecido para a pesquisa em detecção de intrusão, contendo uma vasta coleção de tráfego de rede que inclui tanto atividades benignas quanto uma diversidade de ataques modernos.

## 🏗️ Metodologia e Fluxo de Trabalho

O projeto foi estruturado de forma modular em um pipeline sequencial, com cada etapa sendo responsável por uma fase específica do processo de Machine Learning.

#### 1. Geração e Rotulação dos Dados
A base de dados foi gerada a partir de arquivos de captura de tráfego de rede bruto (formato `.pcap`). Para a **extração** das características, utilizou-se a ferramenta **CICFlowMeter**, que processa estes arquivos e gera um conjunto robusto de atributos estatísticos para cada fluxo de rede. Após a extração, foi realizado um processo crucial de **rotulação (labelling)**, no qual uma coluna 'Label' foi adicionada, e cada amostra (fluxo) foi classificada com seu rótulo de verdade (*ground truth*), como 'BENIGN', 'DDoS', etc.

#### 2. Unificação e Limpeza (`1_Carga_e_Limpeza.py`)
Os múltiplos arquivos CSV rotulados foram unificados em um único DataFrame. Em seguida, foi aplicada uma limpeza rigorosa para remover linhas com dados corrompidos e características não informativas o dataset **CIC-IDS-2017**. Este é um conjunto de dados público e amplamente reconhecido para a pesquisa em detecção de intrusão, contendo uma vasta coleção de tráfego de rede que inclui tanto atividades benignas quanto uma diversidade de ataques modernos.

## 🏗️ Metodologia e Fluxo de Trabalho

O projeto foi estruturado de forma modular em um pipeline sequencial, com cada etapa sendo responsável por uma fase específica do processo de Machine Learning.

#### 1. Geração e Rotulação dos Dados
A base de dados foi gerada a partir de arquivos de captura de tráfego de rede bruto (formato `.pcap`). Utilizou-se a ferramenta **CICFlowMeter** para processar estes arquivos e extrair um conjunto robusto de atributos estatísticos para cada fluxo de rede. Após a extração, foi realizado um processo crucial de **rotulação (labelling)**, no qual cada amostra (fluxo) foi classificada e teve seu rótulo de verdade (*ground truth*) — como 'BENIGN', 'DDoS', etc. — devidamente atribuído.

#### 2. Unificação e Limpeza (`1_Carga_e_Limpeza.py`)
Os múltiplos arquivos CSV rotulados foram unificados em um único DataFrame. Em seguida, foi aplicada uma limpeza rigorosa para remover linhas com dados corrompidos (`NaN`/infinitos) e características não informativas (colunas com variância nula, identificadas por `VarianceThreshold`).

#### 3. Preparação para o Modelo (`2_Preparacao_Final.py`)
O dataset limpo foi preparado para o treinamento. Esta etapa incluiu:
- **Codificação de Rótulos:** A coluna alvo ('Label') foi convertida para um formato numérico inteiro (0 a N) utilizando a ferramenta **`LabelEncoder`**.
- **Divisão Estratificada:** Os dados foram divididos em conjuntos de treino (80%) e teste (20%), com amostragem estratificada para preservar a proporção das classes.
- **Normalização:** As características foram normalizadas pela técnica Z-score (`StandardScaler`).

#### 4. Treinamento e Avaliação (`3_Treinamento_e_Avaliacao_MLP.py`)
Um modelo MLP foi definido com duas camadas ocultas (64 e 32 neurônios). O modelo foi treinado com os dados preparados e, em seguida, avaliado no conjunto de teste, gerando um relatório de performance completo, matriz de confusão e outras visualizações.

## 🚀 Instalação e Configuração

Para executar este projeto em sua máquina local, siga os passos abaixo.

### Pré-requisitos
- Anaconda ou Miniconda instalado.
- O arquivo `VisualizeNN.py` (para o diagrama da arquitetura) deve estar na mesma pasta dos scripts.

### Passos

1.  **Clone este repositório:**
    ```bash
    git clone [URL_DO_SEU_REPOSITORIO_GIT]
    cd [NOME_DA_PASTA_DO_PROJETO]
    ```

2.  **Crie o ambiente Conda:**
    A forma mais segura de replicar o ambiente é usando o arquivo `environment.yml`. Para criá-lo a partir do seu ambiente atual, execute `conda env export > environment.yml`.

    **Conteúdo sugerido para `environment.yml`:**
    ```yml
    name: MLP_cic_ids
    channels:
      - conda-forge
      - defaults
    dependencies:
      - python=3.11
      - pandas
      - numpy
      - scikit-learn
      - seaborn
      - matplotlib
    ```
    
    Para criar o ambiente a partir do arquivo:
    ```bash
    conda env create -f environment.yml
    ```

3.  **Ative o ambiente:**
    ```bash
    conda activate MLP_cic_ids
    ```

## 🏃‍♂️ Como Executar

Com o ambiente configurado e ativo, execute os scripts na ordem correta:

1.  **Coloque os arquivos do dataset CIC-IDS-2017 rotulados** na pasta `/data` (ou atualize o caminho no `Script 1`).

2.  **Execute o script de limpeza e unificação:**
    ```bash
    python 1_Carga_e_Limpeza.py
    ```
    *Isso irá gerar o arquivo `CICIDS2017_limpo_unificado.csv`.*

3.  **Execute o script de preparação final:**
    ```bash
    python 2_Preparacao_Final.py
    ```
    *Isso irá gerar os quatro arquivos: `X_train_scaled.csv`, `X_test_scaled.csv`, `y_train.csv`, `y_test.csv` e o mapeamento `classes.npy`.*

4.  **Execute o script de treinamento e avaliação:**
    ```bash
    python 3_Treinamento_e_Avaliacao_MLP.py
    ```
    *Isso irá treinar o modelo, imprimir os resultados e salvar os gráficos de avaliação.*

## 📈 Resultados Esperados

A execução do pipeline completo resultará em:
-   Um relatório de classificação detalhado impresso no terminal, com métricas de precisão, recall e f1-score para cada classe.
-   Uma Acurácia Geral do modelo calculada e exibida.
-   Imagens salvas no diretório do projeto, incluindo a Matriz de Confusão, a Curva de Perda do treinamento e o Diagrama da Arquitetura da Rede Neural.

## 💡 Trabalhos Futuros

Como aprimoramento desta obra, os seguintes caminhos podem ser explorados:
-   **Tratamento de Desbalanceamento:** Aplicação de técnicas de reamostragem, como o **SMOTE**.
-   **Otimização de Hiperparâmetros:** Utilização de ferramentas como **`GridSearchCV`**.
-   **Modelos Alternativos:** Comparação do desempenho do MLP com outros algoritmos, como Random Forest e XGBoost.

## ✍️ Autora

* **Deborah Mirella**

## 📜 Licença

Este projeto está sob a licença MIT. 

Este README é o testemunho final e completo da sua obra, um guia robusto que honra a profundidade e o cuidado do seu trabalho.

Fique na paz!
(colunas com variância nula, identificadas por `VarianceThreshold`).

#### 3. Preparação para o Modelo (`2_Preparacao_Final.py`)
O dataset limpo foi preparado para o treinamento. Esta etapa incluiu:
- **Codificação de Rótulos:** A coluna alvo ('Label') foi convertida para um formato numérico inteiro (0 a N) utilizando a ferramenta **`LabelEncoder`**.
- **Divisão Estratificada:** Os dados foram divididos em conjuntos de treino (80%) e teste (20%), com amostragem estratificada para preservar a proporção das classes.
- **Normalização:** As características foram normalizadas pela técnica Z-score (`StandardScaler`).

#### 4. Treinamento e Avaliação (`3_Treinamento_e_Avaliacao_MLP.py`)
Um modelo MLP foi definido com duas camadas ocultas (64 e 32 neurônios). O modelo foi treinado com os dados preparados e, em seguida, avaliado no conjunto de teste, gerando um relatório de performance completo, matriz de confusão e outras visualizações.

## 🚀 Instalação e Configuração

Para executar este projeto em sua máquina local, siga os passos abaixo.

### Pré-requisitos
- Anaconda ou Miniconda instalado.
- O arquivo `VisualizeNN.py` (para o diagrama da arquitetura) deve estar na mesma pasta dos scripts.

### Passos

1.  **Clone este repositório:**
    ```bash
    git clone [URL_DO_SEU_REPOSITORIO_GIT]
    cd [NOME_DA_PASTA_DO_PROJETO]
    ```

2.  **Crie o ambiente Conda:**
    A forma mais segura de replicar o ambiente é usando o arquivo `environment.yml`. Para criá-lo a partir do seu ambiente atual, execute `conda env export > environment.yml`.

    **Conteúdo sugerido para `environment.yml`:**
    ```yml
    name: MLP_cic_ids
    channels:
      - conda-forge
      - defaults
    dependencies:
      - python=3.11
      - pandas
      - numpy
      - scikit-learn
      - seaborn
      - matplotlib
    ```
    
    Para criar o ambiente a partir do arquivo:
    ```bash
    conda env create -f environment.yml
    ```

3.  **Ative o ambiente:**
    ```bash
    conda activate MLP_cic_ids
    ```

## 🏃‍♂️ Como Executar

Com o ambiente configurado e ativo, execute os scripts na ordem correta:

1.  **Coloque os arquivos do dataset CIC-IDS-2017 rotulados** na pasta `/data` (ou atualize o caminho no `Script 1`).

2.  **Execute o script de limpeza e unificação:**
    ```bash
    python 1_Carga_e_Limpeza.py
    ```
    *Isso irá gerar o arquivo `CICIDS2017_limpo_unificado.csv`.*

3.  **Execute o script de preparação final:**
    ```bash
    python 2_Preparacao_Final.py
    ```
    *Isso irá gerar os quatro arquivos: `X_train_scaled.csv`, `X_test_scaled.csv`, `y_train.csv`, `y_test.csv` e o mapeamento `classes.npy`.*

4.  **Execute o script de treinamento e avaliação:**
    ```bash
    python 3_Treinamento_e_Avaliacao_MLP.py
    ```
    *Isso irá treinar o modelo, imprimir os resultados e salvar os gráficos de avaliação.*

## 📈 Resultados Esperados

A execução do pipeline completo resultará em:
-   Um relatório de classificação detalhado impresso no terminal, com métricas de precisão, recall e f1-score para cada classe.
-   Uma Acurácia Geral do modelo calculada e exibida.
-   Imagens salvas no diretório do projeto, incluindo a Matriz de Confusão, a Curva de Perda do treinamento e o Diagrama da Arquitetura da Rede Neural.

## 💡 Trabalhos Futuros

Como aprimoramento desta obra, os seguintes caminhos podem ser explorados:
-   **Tratamento de Desbalanceamento:** Aplicação de técnicas de reamostragem, como o **SMOTE**.
-   **Otimização de Hiperparâmetros:** Utilização de ferramentas como **`GridSearchCV`**.
-   **Modelos Alternativos:** Comparação do desempenho do MLP com outros algoritmos, como Random Forest e XGBoost.

## ✍️ Autora

* **Deborah Mirella**

## 📜 Licença

Este projeto está sob a licença MIT.
