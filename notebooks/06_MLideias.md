# Machine Learning - PS26 Hackathon

UFRJ Analytica

> **Contexto pós-IVH:** este documento foi reformulado após a implementação do `04_indice_vulnerabilidade.ipynb`. O dataset final do IVH contém **37 bairros** (filtrados por chuva ≥5mm), com **335 eventos de alagamento** entre 2017 e 2024. A maioria dos bairros tem apenas 1-2 eventos no histórico, o que impôs ajustes na escolha e calibração dos modelos.

## 1. K-Means (não-supervisionado) — agrupar bairros por perfil

**O que é:** algoritmo que agrupa observações (no seu caso, bairros) em K grupos, onde cada bairro vai pro grupo cujo "centro" (centróide) está mais próximo dele no espaço de features.

**Por que faz sentido aqui:** queremos testar se existem perfis distintos de resposta à chuva. K-Means responde exatamente isso — descobre se os 37 bairros se agrupam naturalmente em perfis tipo "resiliente", "vulnerável crônico", "vulnerável apenas em eventos extremos", etc.

**Por que só K-Means (sem DBSCAN nem Hierárquico):** com 37 bairros, DBSCAN tende a rotular quase tudo como ruído e Hierárquico não agrega valor sobre K-Means com tão poucos pontos. Decisão pragmática: foca o esforço em fazer K-Means muito bem feito.

**O que implementar concretamente:**

Universo: os 37 bairros do `indice_vulnerabilidade_hidrica.parquet`.

Features (3, todas já prontas no dataset):

- `ivh_normalizado` — sensibilidade à chuva (0-100)
- `total_eventos` — volume absoluto de alagamentos
- `media_chuva_mm` — quanto chove em média nos dias de evento

Pipeline:

1. `StandardScaler` antes do K-Means (ele é sensível a escala)
2. Método do cotovelo (elbow method) + silhouette score pra escolher o K — provavelmente 2 ou 3, dado o tamanho do dataset; deixa o dado falar
3. `KMeans(n_clusters=K, random_state=42, n_init=10)`
4. Interpretar cada cluster olhando a média das features — esse é o trabalho de verdade, dar nome aos perfis

**Cuidado:** com 37 pontos, silhouette score fica ruidoso. Vale rodar várias seeds e olhar estabilidade dos clusters.

## 2. Poisson Regression (supervisionado) — quantificar sensibilidade dos bairros

**O que é:** modelo linear generalizado (GLM) onde o target é uma contagem — eventos discretos não-negativos como "número de chamados num bairro num dia". Em vez de assumir que o erro é normalmente distribuído (como na regressão linear comum), assume que o target segue uma distribuição de Poisson, que é a distribuição natural pra contagem de eventos raros num intervalo de tempo.

**Por que faz sentido aqui:** queremos quantificar estatisticamente o quanto cada bairro é sensível à chuva, controlando por precipitação. Poisson Regression é a escolha estatisticamente correta pra isso. Ela nunca prevê valores negativos (eventos = -3.7 não existe), respeita a natureza discreta da contagem, e os coeficientes têm interpretação direta e poderosa: "cada 10mm extra de chuva multiplica o número esperado de eventos por X".

**Foco interpretativo (não preditivo):** com apenas 335 eventos em 7 anos espalhados em 37 bairros, a Poisson não vai fazer previsões pontuais precisas — eventos de alagamento são raros e dependem de fatores não observados (entupimento de bueiro, maré, chuva localizada). O **produto principal** do modelo será:

- **Ranking de sensibilidade dos bairros** controlando por chuva (`exp(coef)` de cada bairro)
- **Efeito da chuva** no número esperado de eventos (`exp(coef)` de chuva_24h)
- **Sazonalidade mensal** (`exp(coef)` de cada mês)

Esse tipo de leitura é ouro pro relatório técnico e pro pitch — você consegue dizer coisas como "Guaratiba é 6x mais sensível à chuva que Copacabana, controlando pela quantidade de chuva" com fundamento estatístico (p-valor, intervalo de confiança).

**O que implementar:**

A unidade de observação é (bairro, dia), não mais (bairro). Cada linha é uma "oportunidade" de eventos acontecerem.

Estratégia do dataset (meio-termo): usar apenas dias em que choveu ≥5mm em alguma estação, expandindo para cada bairro associado àquela estação. Inclui dias com 0 eventos (target = 0) — fundamental pra Poisson calibrar corretamente. O dataset final terá milhares de linhas, maioria com target = 0.

Reconstrução do dataset (tarefa nova, não está pronta no IVH):

1. Pegar todos os dias com chuva ≥5mm em cada estação (2017-2024)
2. Expandir pra cada bairro associado àquela estação (mapeamento já feito na Célula 3 do notebook 04)
3. Cruzar com a tabela de eventos (Célula 5 do notebook 04) e contar quantos eventos ocorreram em cada (bairro, dia)
4. Salvar como `dataset_poisson.parquet`

Features (modelo enxuto):

- `chuva_24h` — chuva acumulada em 24h na estação associada ao bairro
- `bairro` (one-hot encoding) — captura o efeito específico de cada bairro
- `mes` — captura sazonalidade

Target: número de eventos de alagamento naquele (bairro, dia).

Pipeline:

1. Split temporal: treino 2017-2022, teste 2023-2024 — **nunca** split aleatório em série temporal
2. `statsmodels.GLM(family=Poisson())` é melhor que o `PoissonRegressor` do scikit-learn pro relatório, porque dá p-valores, intervalos de confiança e diagnósticos prontos
3. Avaliar com MAE e RMSE no conjunto de teste — comparar com baseline trivial (prever sempre a média ou sempre 0) pra honestidade metodológica
4. Interpretar os coeficientes via `exp(coef)` — esse é o "fator multiplicativo" mencionado acima

**Cuidados na implementação:**

- One-hot de bairro com 37 níveis cria 36 features. Com bairros que têm poucos eventos, considerar regularização L2 (`PoissonRegressor` do sklearn permite) ou agrupar bairros raros
- O dataset terá zero-inflation severa (maioria das linhas com target = 0). Reportar isso na discussão

**Discussão importante no relatório:**

Poisson assume que média = variância (equidispersion). Em dados reais de eventos raros, é quase certo que vocês vão ter overdispersion (variância >> média) — dias de chuva extrema explodem a contagem muito além do que a Poisson prevê. Verifiquem isso comparando média e variância do target, ou olhando o "deviance" do modelo. Se houver overdispersion, mencionem no relatório que **Negative Binomial Regression** seria ainda mais adequada (é uma generalização da Poisson que acomoda variância maior). Adicionalmente, dada a quantidade de zeros no dataset, **Zero-Inflated Poisson (ZIP)** ou modelos **Hurdle** seriam tecnicamente mais corretos. Reconhecer essas limitações ganha pontos no rigor mesmo sem implementar as alternativas.