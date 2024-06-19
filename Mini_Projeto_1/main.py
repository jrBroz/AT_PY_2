import re
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import requests
import pandas as pd

class falha_ao_encontrar_wikitable_sortable(Exception):
    
    "a classe wikitable sortable não foi encontrada"

def limpar_dados(df_perfeito:pd.DataFrame) -> pd.DataFrame:
    """Funcao que faz uma limpeza de dados do dataframe passado como parâmetro."""
    
    df_perfeito = df_perfeito.drop_duplicates()  # Remover duplicatas
    df_perfeito = df_perfeito.dropna()  # Remover linhas com valores ausentes
    df_perfeito = df_perfeito.replace("", "Ausente")
    return df_perfeito


def colocar_regex(texto:str) -> str:
    """Função para aplicar expressões regulares no texto"""
    
    texto = re.sub(r'\s+', ' ', texto)  # Substituir múltiplos espaços por um único espaço
    texto = re.sub(r'\[.*?\]', '', texto)  # Remover referências em colchetes
    texto = texto.strip()  # Remover espaços em branco 
    return texto


def receber_e_guardar_dados():
    url = "https://pt.wikipedia.org/wiki/Lista_de_jogos_para_PlayStation_4"

    try:
        
        requisicao = requests.get(url).text
        soup = BeautifulSoup(requisicao, 'html.parser')

        tabela = soup.find('table', class_='wikitable sortable')

        df = pd.DataFrame(columns=['Titulo', 'Desenvolvedor', 'Publicador', 'Exclusivo', 'Europa', 'Japão', 'América do Norte', 'Brasil', 'Referências'])

        for row in tabela.tbody.find_all('tr'):
            
            colunas = row.find_all('td')
            
            # Pegar os dados das colunas do site da wikipedia
            if colunas != []: 
                Titulo = colocar_regex(colunas[0].text)
                desenvolvedor = colocar_regex(colunas[1].text)
                publicador = colocar_regex(colunas[2].text)
                exclusivo = colocar_regex(colunas[3].text)
                europa = colocar_regex(colunas[4].text)
                Japao = colocar_regex(colunas[5].text)
                America_do_norte = colocar_regex(colunas[6].text)
                Brasil = colocar_regex(colunas[7].text)
                Referencia = colocar_regex(colunas[8].text)

                df = df._append({"Titulo": Titulo , "Desenvolvedor": desenvolvedor, "Publicador": publicador, "Exclusivo":exclusivo, "Europa": europa, "Japão": Japao, "América do Norte": America_do_norte, "Brasil": Brasil, "Referências": Referencia}, ignore_index=True)

    
                df_limpo = limpar_dados(df)
                                
        df_limpo.to_csv('Dados_PS4_WIKIPEDIA.csv',sep=',',encoding='utf-8') #gerar dados pra csv
        df_limpo.to_json('Dados_PS4_WIKIPEDIA.json') #gerar dados pra json
        df_limpo.to_excel('Dados_PS4_WIKIPEDIA.xlsx') #gerar dados pra excel

        
    except (RequestException, requests.ReadTimeout, requests.ConnectionError, requests.ConnectTimeout,falha_ao_encontrar_wikitable_sortable) as e:
        
        if e == falha_ao_encontrar_wikitable_sortable:
            pass
  
        else:
            print("ocorreu um erro no processo de requisição")
        
        
    

receber_e_guardar_dados()