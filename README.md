# 🚍 Projeto — Sistema de Viabilidade de Serviços de Ônibus no Rio de Janeiro

## 📌 Sobre o Projeto

Este projeto tem como objetivo desenvolver um sistema capaz de prever a viabilidade econômica da criação de novos serviços de ônibus no município do Rio de Janeiro.

A proposta surgiu a partir da observação de problemas recorrentes no transporte público da cidade, como:
- superlotação;
- baixa quantidade de ônibus em circulação;
- ausência de linhas em determinadas regiões;
- dificuldades de planejamento operacional.

O sistema utiliza técnicas de Machine Learning para prever possíveis margens de lucro de novos serviços de ônibus com base em informações operacionais e ambientais.

---

# 🎯 Objetivos

## Objetivo Geral
Desenvolver um aplicativo capaz de calcular a viabilidade econômica da criação de um novo serviço de ônibus.

## Objetivos Específicos
- Criar modelos preditivos para estimar lucro operacional;
- Incentivar novos empreendimentos no transporte público;
- Melhorar o planejamento de linhas;
- Auxiliar empresas e gestores públicos;
- Melhorar a qualidade do transporte público no Rio de Janeiro.

---

# 📊 Fontes de Dados

Os dados utilizados no projeto foram obtidos através de bases públicas.

## 🚍 SMTR — Sistema Municipal de Transportes
Arquivos utilizados:
- `balanco_servico_dia.csv`
- `sumario_servico_dia_historico.csv`
- `ordem_servico_trajeto_alternativo_sentido.csv`
- `trajeto_alternativo_servico.csv`

## 🌧️ Sistema Alerta Rio
Dados pluviométricos utilizados para medir impacto da chuva no desempenho dos serviços.

---

# 🧹 Pré-processamento dos Dados

As etapas de pré-processamento incluíram:

- remoção de colunas irrelevantes;
- remoção de valores nulos;
- integração de múltiplos datasets;
- transformação de variáveis categóricas;
- normalização de variáveis numéricas;
- agrupamento de bairros por regiões;
- criação de features relacionadas à chuva;
- criação de feature de trajetos alternativos.

Também foi necessário converter dados climáticos de `.txt` para `.csv`.

---

# ⚙️ Pipeline do Projeto

## 1. Coleta de Dados
Coleta de informações públicas do SMTR e Alerta Rio.

## 2. Processamento
Limpeza, tratamento e integração dos dados.

## 3. Modelagem
Treinamento de modelos de regressão.

## 4. Avaliação
Comparação dos modelos utilizando métricas estatísticas.

---

# 🤖 Modelos Utilizados

## Dummy Regressor
Modelo baseline utilizado para comparação.

## Regressão Linear
Modelo simples e interpretável para análise de relações lineares.

## Ridge Regression
Modelo linear com regularização L2.

## XGBoost Regressor
Modelo baseado em Gradient Boosting utilizado para relações não lineares complexas.

---

# 📈 Resultados

## Resultados Sem Dados de Chuva

| Modelo | RMSE | R² |
|---|---|---|
| Dummy Regressor | 1.0140 | -0.0001 |
| Regressão Linear | 0.7400 | 0.4674 |
| Ridge | 0.7400 | 0.4673 |
| XGBoost | 0.2941 | 0.9137 |

---

## Resultados Com Dados de Chuva

| Modelo | RMSE | R² |
|---|---|---|
| Dummy Regressor | 0.9928 | 0.0000 |
| Regressão Linear | 0.2996 | 0.9147 |
| Ridge | 0.2980 | 0.9156 |
| XGBoost | 0.2670 | 0.9247 |

---

# 🔍 Principais Conclusões

- O XGBoost apresentou o melhor desempenho geral.
- Dados climáticos melhoraram significativamente os resultados.
- O modelo conseguiu aprender padrões relevantes relacionados à lucratividade.
- Variáveis externas possuem forte impacto operacional.

---

# 🛠️ Tecnologias Utilizadas

## Linguagem
- Python

## Bibliotecas
- pandas
- numpy
- scikit-learn
- xgboost
- matplotlib
- seaborn
- plotly

## Ambiente
- Jupyter Notebook

---

# 📂 Estrutura Esperada do Projeto

```bash
projeto/
│
│
├── dados_pluviometricos_extraidos
│   ├── Chuva_24h.csv
│   └── dados_pluviometricos_consolidados.csv
│
├── dataset_principal
│   ├── balanco_servico_dia.csv
│   ├── sumario_servico_dia_historico.csv
│   └── trajeto_alternativo_servico.csv
│
├── notebooks/
│   └── analise_faturamento_km.ipynb
│   └── km_apurada_x_trajeto_alternativo.ipynb
│   └── km_apurada_x_trajeto_alternativo.ipynb
│
├── extrai_dados_pluviometricos.py
│
└── README.md
```

---

# ▶️ Como Executar o Projeto

## 1. Clone o repositório

```bash
git clone <repositorio>
```

## 2. Crie um ambiente virtual

```bash
python -m venv venv
```

## 3. Ative o ambiente virtual

### Linux/macOS

```bash
source venv/bin/activate
```

### Windows

```bash
venv\\Scripts\\activate
```

## 4. Instale as dependências

```bash
pip install -r requirements.txt
```

## 5. Execute o notebook

```bash
jupyter notebook
```

---

# 📌 Trabalhos Futuros

- inclusão de mais dados climáticos;
- expansão para mais bairros;
- integração com APIs de trânsito;
- criação de dashboard web;
- deploy do modelo;
- utilização de séries temporais;
- previsão de demanda de passageiros.

---

# 👨‍💻 Aplicação Futura

O objetivo final do projeto é integrar o modelo a uma aplicação web onde o usuário poderá inserir:

- bairro de origem;
- bairro de destino;
- quantidade de viagens;
- quilometragem planejada;
- subsídio esperado;
- dia da semana.

E receber como saída:
- previsão de lucro;
- estimativa de viabilidade;
- análise operacional do serviço.

---

# 📄 Licença

Projeto desenvolvido para fins acadêmicos e de pesquisa