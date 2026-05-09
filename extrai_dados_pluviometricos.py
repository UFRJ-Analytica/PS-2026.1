import pandas as pd
import glob
import os
import traceback

# Define as pastas de entrada e saída
pasta_entrada = 'dados_pluviometricos'
pasta_saida = 'dados_pluviometricos_extraidos'

# Cria a pasta de saída automaticamente caso ela ainda não exista
os.makedirs(pasta_saida, exist_ok=True)

# Busca todos os arquivos .txt na pasta de entrada
arquivos_txt = glob.glob(os.path.join(pasta_entrada, '*.txt'))

if not arquivos_txt:
    print(f"Nenhum arquivo .txt encontrado na pasta '{pasta_entrada}'.")

# 1. Cria uma lista vazia para armazenar todos os dataframes extraídos
lista_dfs = []

for arquivo in arquivos_txt:
    try:
        # Extrair o nome do bairro do nome do arquivo (Ex: "campo_grande_202412_Plv.txt" -> "Campo Grande")
        nome_arquivo = os.path.basename(arquivo)
        nome_base = os.path.splitext(nome_arquivo)[0]
        partes_nome = nome_base.split('_')
        bairro_extraido = " ".join(partes_nome[:-2]).title()

        # Leitura cega do txt
        df_bruto = pd.read_csv(
            arquivo,
            skiprows=5, 
            sep=r'\s+', 
            header=None,
            na_values=['ND'] 
        )

        num_colunas = len(df_bruto.columns)

        # Trata as colunas dependendo do formato da estação e cria colunas vazias
        if num_colunas == 7:
            df_bruto.columns = ["Dia", "Hora", "15 min", "01 h", "04 h", "24 h", "96 h"]
            # Insere as colunas de 5 e 10 min vazias nas posições 2 e 3
            df_bruto.insert(2, "05 min", None)
            df_bruto.insert(3, "10 min", None)
            df_final = df_bruto
            
        elif num_colunas >= 9:
            df_final = pd.DataFrame()
            df_final['Dia'] = df_bruto.iloc[:, 0]
            df_final['Hora'] = df_bruto.iloc[:, 1]
            df_final['24 h'] = df_bruto.iloc[:, -2] # A penúltima coluna é sempre a de 24h
        else:
            print(f"Alerta: Arquivo {arquivo} tem um número desconhecido de colunas ({num_colunas}). Ignorado.")
            continue

        # Cria a nova coluna Bairro
        df_final['Bairro'] = bairro_extraido

        # Filtra apenas as colunas desejadas para o CSV unificado
        df_reduzido = df_final[['Dia', 'Hora', '24 h', 'Bairro']].copy()

        # Limpeza convertendo o texto para datas e removendo o "lixo"
        df_reduzido['Dia'] = pd.to_datetime(df_reduzido['Dia'], format='%d/%m/%Y', errors='coerce')
        df_reduzido = df_reduzido.dropna(subset=['Dia'])

        # =========================================================
        # NOVO: Filtro para pegar apenas do Mês 1 ao Mês 8
        # =========================================================
        df_reduzido = df_reduzido[df_reduzido['Dia'].dt.month <= 8].copy()

        # Transforma os tipos de dados
        df_reduzido['Dia'] = df_reduzido['Dia'].astype('datetime64[us]')
        df_reduzido['Hora'] = df_reduzido['Hora'].astype('string')
        df_reduzido['24 h'] = df_reduzido['24 h'].astype(float)
        df_reduzido['Bairro'] = df_reduzido['Bairro'].astype('string')

        # Adiciona a tabela desta estação na nossa lista geral
        lista_dfs.append(df_reduzido)
        print(f"Lido com sucesso: {nome_arquivo} -> Extraído de Janeiro a Agosto")

    except Exception as e:
        print(f"\n[!] Erro ao processar o arquivo {arquivo}:")
        print(traceback.format_exc())
        print("-" * 50)

# FASE FINAL: Consolidação
if lista_dfs:
    # O pd.concat empilha todos os dataframes um embaixo do outro
    df_total = pd.concat(lista_dfs, ignore_index=True)
    
    # Define o nome do super arquivo final
    caminho_csv_final = os.path.join(pasta_saida, 'dados_pluviometricos_consolidados.csv')
    
    # Exporta para CSV
    df_total.to_csv(caminho_csv_final, index=False)
    
    print(f"\n{'='*50}")
    print(f"SUCESSO! Todos os arquivos foram unificados.")
    print(f"Total de linhas (Meses 1 a 8): {len(df_total)}")
    print(f"Arquivo salvo em: {caminho_csv_final}")
    print(f"{'='*50}")
else:
    print("Nenhum dado válido pôde ser extraído dos arquivos.")