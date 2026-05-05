# Definição do Projeto — PS26 Hackathon UFRJ Analytica

## Tema
Soluções com dados para problemas no Rio de Janeiro

## Pergunta de pesquisa
Quais bairros do Rio são cronicamente mais vulneráveis a chuva, 
controlando por quanto choveu de fato, e como essa vulnerabilidade 
evoluiu nos últimos 15 anos?

## Justificativa
O Rio de Janeiro sofre historicamente com alagamentos durante períodos 
de chuva. Mas nem todo bairro responde igual à mesma quantidade de 
chuva: alguns alagam com pouca precipitação, outros só em eventos 
extremos. Identificar esses padrões permite priorizar investimentos 
em drenagem e antecipar respostas da Defesa Civil.

## Conceito-chave: Índice de Vulnerabilidade Hídrica (IVH)
Em vez de simplesmente contar reclamações por bairro, calculamos a 
"sensibilidade à chuva" de cada bairro:

  IVH(bairro) = reclamações_de_drenagem_e_alagamento / mm_de_chuva

Isso normaliza pela quantidade de chuva que de fato caiu, revelando 
quais bairros são estruturalmente mais vulneráveis — não apenas os 
que recebem mais chuva.

## Fontes de dados
1. **Chamados 1746** (Data.Rio via BigQuery) 
   - 554.802 registros de drenagem/alagamento de 2010 a 2026
   - 166 bairros cobertos
   - Tipos: Drenagem, Saneamento, Alagamento, Bueiros, Enchentes
2. **Alerta Rio** (sistema-alerta-rio.com.br)
   - 33 estações pluviométricas
   - Granularidade de 15 minutos
   - Período sugerido: 2011-2025

## Hipóteses
- **H1:** A vulnerabilidade hídrica está correlacionada com perfil 
  socioeconômico do bairro (Zona Norte/Oeste mais vulneráveis que Zona Sul)
- **H2:** É possível agrupar os bairros em 3-5 perfis distintos de 
  resposta à chuva (clustering)
- **H3:** Alguns bairros melhoraram nos últimos 15 anos (após obras 
  de drenagem) enquanto outros pioraram
- **H4:** Bairros próximos geograficamente tendem a ter perfis 
  semelhantes de vulnerabilidade

## Metodologia (ciclo DMAIC adaptado)
1. **Define:** definir IVH e perfis de bairro
2. **Measure:** coletar 1746 (✅ feito) e Alerta Rio
3. **Analyze:** EDA descritiva + análise temporal
4. **Improve:** clustering não-supervisionado dos bairros
5. **Control:** dashboard interativo com mapa e simulador

## Thresholds de chuva (oficiais Alerta Rio)
- Fraca: 0–5 mm/h
- Moderada: 5–25 mm/h
- Forte: 25–50 mm/h
- Muito forte: >50 mm/h

## Modelos previstos
- **Não-supervisionado:** K-means e DBSCAN para clustering de bairros 
  por perfil de vulnerabilidade
- **Supervisionado (auxiliar):** Random Forest Regressor para prever 
  número de reclamações dado chuva e bairro
- **Análise temporal:** comparação de IVH por bairro entre janelas 
  de 5 anos (2010-2014, 2015-2019, 2020-2024)

## Entregáveis
- Notebooks de coleta, EDA e modelagem
- Dashboard Streamlit com:
  - Mapa interativo do Rio colorido por IVH
  - Ranking dos bairros cronicamente vulneráveis
  - Simulador: "se chover X mm, o que acontece em cada bairro?"
  - Análise temporal por bairro
- Relatório PDF (8-12 páginas)
- Apresentação (slides + pitch)

## Status atual
- [x] Setup do repositório e ambiente
- [x] Coleta dos chamados 1746 (554.802 registros tratados)
- [x] EDA inicial (top 20 bairros, sazonalidade, distribuição por hora)
- [ ] Coleta do Alerta Rio
- [ ] Cruzamento espacial estação ↔ bairro
- [ ] Cálculo do IVH
- [ ] Clustering de bairros
- [ ] Análise temporal
- [ ] Dashboard
- [ ] Relatório e apresentação

## Bairros já identificados como mais reclamados (1746)
Campo Grande, Santa Cruz, Bangu, Guaratiba, Realengo, Centro, Sepetiba, 
Paciência, Tijuca, Taquara, Barra da Tijuca, Jacarepaguá, Recreio, 
Botafogo, Copacabana, Madureira, Cosmos, Padre Miguel, Inhoaíba, Irajá

> Observação: alta concentração na Zona Oeste e Norte — primeira 
> evidência da hipótese H1.