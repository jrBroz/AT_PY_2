from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import requests
import pandas as pd


def limpar_dados(df_perfeito:pd.DataFrame):
    
    df_perfeito.dropna(inplace=True)  # Remover linhas com valor ausente
    df_perfeito.dropna(axis=1, inplace=True)  # Remover colunas com valor ausente
    df_perfeito.fillna(value=0, inplace=True)  # Preencher valores ausentes com 0
    df_perfeito.drop_duplicates(keep=False, inplace=True)  # Remover duplicatas
    

    
    return df_perfeito


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
                Titulo = colunas[0].text.strip()        
                desenvolvedor = colunas[1].text.strip()
                publicador = colunas[2].text.strip()
                exclusivo = colunas[3].text.strip()
                europa = colunas[4].text.strip()
                Japao = colunas[5].text.strip()
                America_do_norte = colunas[6].text.strip()
                Brasil = colunas[7].text.strip()
                Referencia = colunas[8].text.strip()

                df = df._append({"Titulo": Titulo , "Desenvolvedor": desenvolvedor, "Publicador": publicador, "Exclusivo":exclusivo, "Europa": europa, "Japão": Japao, "América do Norte": America_do_norte, "Brasil": Brasil, "Referências": Referencia}, ignore_index=True)

    
                df_limpo = limpar_dados(df)
                    
                # df_sem_duplicatas = df.drop_duplicates(keep=False)
                # df_sem_linha_ausente = df_sem_duplicatas.dropna()
                # # #df = df.dropna() # Remover linhas com valor ausente
                # # df_sem_coluna_ausente = df_sem_linha_ausente.dropna()
                # # df = df.dropna(axis=1) # remove coluna com valor ausente
                # # df = df.fillna(0) #  preenche valor ausente com 0
                # # df = df.drop_duplicates() # Remover duplicatas 


                

        df_limpo.to_csv('Dados_PS4_WIKIPEDIA.csv',sep=',',encoding='utf-8') #gerar dados pra csv
        df_limpo.to_json('Dados_PS4_WIKIPEDIA.json') #gerar dados pra json
        df_limpo.to_excel('Dados_PS4_WIKIPEDIA.xlsx') #gerar dados pra excel

    except (RequestException, requests.ReadTimeout, requests.ConnectionError, requests.ConnectTimeout):
        
        print("ocorreu um erro no processo de requisição")
        
        
    

receber_e_guardar_dados()