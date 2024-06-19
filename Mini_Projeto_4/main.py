from bs4 import BeautifulSoup
import requests
import pandas as pd
from sqlalchemy import create_engine, exc
import time


def ler_excel() -> pd.DataFrame:
    """Função que lê o arquivo Excel consolidado no mini projeto 3 e retorna um dataframe do mesmo."""
    try:
        ler_arquivo_xlsx = pd.read_excel("Dados_Unificados_Final.xlsx")
        return ler_arquivo_xlsx
    except (FileNotFoundError, PermissionError, Exception) as excecao: 

        if excecao == FileNotFoundError:

            print("O arquivo não existe.")
            return pd.DataFrame()  

        if excecao == PermissionError:

            print("Voce não tem permissao pra abrir")
            return pd.DataFrame()  
        else:
            print("Houve um eror ao ler o arquivo", excecao)
            return pd.DataFrame() 


def consulta_api(busca_usuario) -> list:
    """Função que consulta a API do Mercado Livre"""
    url = f"https://api.mercadolibre.com/sites/MLB/search?category=MLB186456&q={busca_usuario}"
    try:
        requisicao = requests.get(url)
        requisicao.raise_for_status()
        response = requisicao.json().get('results', [])
        
        listagem_guardar_sobre_jogos = []

        for resp in response:
            informacoes_necessarias = {
                'Nome': resp.get("title"),
                'Preco': resp.get("price"),
                'Permalink': resp.get("permalink")
            }
            listagem_guardar_sobre_jogos.append(informacoes_necessarias)
        
        
        
        return listagem_guardar_sobre_jogos

    except requests.RequestException as e:
        print(f"Erro na requisição: {e}")
        return []

def cria_BD():
    """Função que cria o banco de dados SQLite"""
    try:
        engine = create_engine('sqlite:///BancoMercado.db')
        return engine
 
    except  exc.SQLAlchemyError as erro_banco:  #Exception Base pro do sqlAlchemy
        print(f"Erro ao criar o banco de dados: {erro_banco}")
        return None

def gerar_dataframe_xlsx():
    """Função que gera o DataFrame e exporta para o banco de dados"""
    df_jogos = ler_excel()
    if df_jogos.empty:
        print("Erro ao ler o arquivo Excel ou o arquivo está vazio.")
        return

    engine = cria_BD()
    if engine is None:
        print("Erro ao criar o banco de dados.")
        return
    
    dados_finais = []
    for index, row in df_jogos.iterrows():
        info_jogo = consulta_api(row['Todos_Jogos']) # Aqui ele pega todas as linhas da coluna 'jogos_preferidos' e faz a consulta na api 
        dados_finais.extend(info_jogo)
        time.sleep(1) # respeita limite da api
            
    df_final = pd.DataFrame(dados_finais) # Aqui ele consolida todos os dados obtidos acima em um único DataFrame
    
    if not df_final.empty:
        try:
            df_final.to_sql('jogos_preferidos', con=engine, if_exists='replace', index=False) #Transforma os dados da coluna 'jogos_preferidos' em um banco de dados.
            print("Os dados foram transportados pro BD com sucesso.")
        except Exception as e:
            print(f"Erro ao exportar dados para o banco de dados: {e}")
    else:
        print("Nenhum dado foi retornado da API.")

if __name__ == "__main__":
    gerar_dataframe_xlsx()
