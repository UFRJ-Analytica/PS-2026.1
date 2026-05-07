# Machine Learning - PS26 Hackathon

UFRJ Analytica

## 1. K-Means (não-supervisionado) — agrupar bairros por perfil

**O que é:** algoritmo que agrupa observações (no seu caso, bairros) em K grupos, onde cada bairro vai pro grupo cujo "centro" (centróide) está mais próximo dele no espaço de features.

**Por que faz sentido aqui:** queremos testar se existem 3-5 perfis distintos de resposta à chuva. K-Means responde exatamente isso — descobre se os 166 bairros se agrupam naturalmente em perfis tipo "resiliente", "vulnerável crônico", "vulnerável apenas em eventos extremos", etc.

**O que implementar concretamente:**

Cada bairro precisa virar uma linha numa matriz de features. Sugestões de features por bairro:

- IVH médio (chamados/mm)
- IVH em eventos de chuva fraca, moderada, forte e muito forte (4 features separadas — revela bairros que só alagam com chuva forte vs. os que alagam com qualquer coisa)
- Total de chamados absoluto
- Variância do IVH (bairros instáveis vs. previsíveis)
- Coordenada média (lat/lon) — opcional, mas ajuda no clustering espacial

Pipeline:

1. StandardScaler antes do K-Means (ele é sensível a escala)
2. Método do cotovelo (elbow method) + silhouette score pra escolher o K — chuto 3 a 5, mas deixa o dado falar
3. `KMeans(n_clusters=K, random_state=42, n_init=10)`
4. Interpretar cada cluster olhando a média das features — esse é o trabalho de verdade, dar nome aos perfis

## 2. DBSCAN (não-supervisionado) — identificar outliers

**O que é:** clustering baseado em densidade. Diferente do K-Means, ele não força todo mundo num grupo — pontos isolados viram "ruído" (outliers).

**Por que faz sentido aqui:** alguns bairros vão ser bizarramente vulneráveis ou bizarramente resilientes — casos extremos que não cabem em nenhum perfil. K-Means esconde esses caras porque força eles num cluster. DBSCAN expõe.

**O que implementar:**

- Mesma matriz de features do K-Means, mesmo StandardScaler
- Dois hiperparâmetros: `eps` (raio de vizinhança) e `min_samples`. Use o "k-distance plot" pra escolher eps
- `DBSCAN(eps=..., min_samples=...)`
- Pontos com label `-1` são os outliers — vão ser provavelmente os bairros mais interessantes pra discussão final

**Cuidado:** com só 166 bairros, DBSCAN pode rotular muita coisa como ruído. Não trate isso como bug.

## 3. Poisson Regression (supervisionado) — prever número de chamados

**O que é:** modelo linear generalizado (GLM) onde o target é uma contagem — eventos discretos não-negativos como "número de chamados num bairro num dia". Em vez de assumir que o erro é normalmente distribuído (como na regressão linear comum), assume que o target segue uma distribuição de Poisson, que é a distribuição natural pra contagem de eventos raros num intervalo de tempo.

**Por que faz sentido aqui:** queremos responder "se chover X mm no bairro Y, quantos chamados esperar?". Poisson Regression é a escolha estatisticamente correta pra isso. Ela nunca prevê valores negativos (chamados = -3.7 não existe), respeita a natureza discreta da contagem, e os coeficientes têm interpretação direta e poderosa: "cada 10mm extra de chuva multiplica o número esperado de chamados por X". Esse tipo de leitura é ouro pro relatório técnico e pro pitch — você consegue dizer coisas como "a sensibilidade de Campo Grande à chuva é 2.3x maior que a de Copacabana" com fundamento estatístico.

**O que implementar:**

A unidade de observação é (bairro, dia) ou (bairro, evento de chuva), não mais (bairro). Cada linha é uma "oportunidade" de chamados acontecerem.

Features sugeridas:

- mm de chuva acumulada em 1h, 4h, 24h, 96h
- Bairro (one-hot encoding)
- Mês ou estação do ano (sazonalidade)
- Lag features: chuva nos dias anteriores

Target: número de chamados naquele dia/evento naquele bairro.

Pipeline:

1. Split temporal (treino até 2022, teste 2023-2024) — nunca split aleatório em série temporal
2. `statsmodels.GLM(family=Poisson())` é melhor que o `PoissonRegressor` do scikit-learn pro relatório, porque dá p-valores, intervalos de confiança e diagnósticos prontos
3. Avaliar com MAE e RMSE no conjunto de teste
4. Interpretar os coeficientes via `exp(coef)` — esse é o "fator multiplicativo" que mencionei

**Discussão importante no relatório:** Poisson assume que média = variância (equidispersion). Em dados reais de chamados, é quase certo que vocês vão ter overdispersion (variância >> média) — dias de chuva extrema explodem a contagem muito além do que a Poisson prevê. Verifiquem isso comparando média e variância do target, ou olhando o "deviance" do modelo. Se houver overdispersion, mencionem no relatório que **Negative Binomial Regression** seria ainda mais adequada (é uma generalização da Poisson que acomoda variância maior). Reconhecer essa limitação ganha pontos no rigor mesmo sem implementar a alternativa.