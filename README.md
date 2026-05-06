# RotaRio
Desenvolvido para o processo seletivo **Analytica UFRJ — PS 2026.1**.

--- 

### O que é?
O RotaRio é uma plataforma que tenta ajudar no problema de segurança pública na cidade do Rio de Janeiro, entregando ao usuário uma rota mais segura partindo de onde ele está até onde ele quer ir, evitando locais com ocorrências de violência.

**Público-alvo**: qualquer pessoa que queira se locomover no Rio com mais segurança, especialmente turistas e quem não conhece bem a cidade.

O que o usuário faz:
1. Informa origem e destino
2. Recebe a rota mais rápida e a rota com menor exposição a ocorrências registradas
3. Vê quantas ocorrências de violência cada rota atravessa nos últimos 6 meses
4. Decide a rota e o método de transporte

---

### Fontes de dados
- Fogo Cruzado: Tiroteios e disparos de arma de fogo no RJ [https://api.fogocruzado.org.br/search]
- Sistema Municipal de Transportes: GTFS do sistema de transporte do Rio [https://data.rio/]
- ISP-RJ: dados históricos de criminalidade por delegacia [http://www.ispdados.rj.gov.br/]

> **OBS:** o RJ deliberadamente não divulga coordenadas exatas de crimes patrimoniais (roubos, furtos). Diferente de São Paulo, o ISP-RJ fornece apenas granularidade de delegacia para esses crimes.

---

### Como funciona

```
Fogo Cruzado (crossfire)
        │
        ▼
   src/data.py         ← puxa ocorrências, carrega GTFS, limpa dados
        │
        ▼
  src/weights.py       ← calcula peso por ocorrência
        │
        ▼
  src/routing.py       ← monta Custom Model e faz requisição ao GraphHopper
        │
        ▼
     app.py            ← interface para o usuário final
```
O GraphHopper aplica esses pesos como penalidades nos segmentos de rua via Custom Model API, calculando a rota que minimiza a exposição acumulada.

--- 

## Estrutura do repositório

```
rotario/
│
├── data/
│   ├── raw/                        # dados brutos
│   │   ├── fogo_cruzado/
│   │   ├── gtfs/
│   │   └── isp_rj/
│   └── processed/                  # dados tratados, gerados por src/data.py
│
├── notebooks/
│   ├── 01_EDA_crossfire.ipynb    # EDA do Fogo Cruzado
│   ├── 02_EDA_ISP.ipynb.ipynb    # EDA do ISP-rj
│   └── 03_EDA_SMTR.ipynb         # EDA do SMTR          
│
├──Orientações_Analytica/      # material de referência
│
├── src/
│   └── __init__.py
│
├── .gitignore
├── app.py                          # onde mostrará ao usuário
├── requirements.txt
└── README.md
```

**Convenção:** nada em `data/raw/` é modificado manualmente. Todo tratamento passa pelo `src/data.py` e o resultado vai para `data/processed/`.

---