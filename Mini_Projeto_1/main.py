from io import StringIO
import re
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import requests
import pandas as pd

class FalhaAoEncontrarWikitableSortable(Exception):
    """A classe wikitable sortable não foi encontrada"""



def limpar_dados(df_perfeito: pd.DataFrame) -> pd.DataFrame:
    """Funcao que faz uma limpeza de dados do dataframe passado como parâmetro."""
    df_perfeito = df_perfeito.drop_duplicates()  # Remover duplicatas
    df_perfeito = df_perfeito.dropna()  # Remover linhas com valores ausentes
    df_perfeito = df_perfeito.replace("", "Vazio")
    return df_perfeito

def aplicar_regex(texto: str) -> str:
    """Função para aplicar expressões regulares no texto"""
    texto = re.sub(r'\s+', ' ', texto)  # Substituir múltiplos espaços por um único espaço
    texto = re.sub(r'\[.*?\]', '', texto)  # Remover referências em colchetes
    texto = texto.strip()  # Remover espaços em branco no início e no final
    return texto

def receber_e_guardar_dados_ps4():
    """Funcao que realiza uma requisicao a api e retorna os valores em uma tabela xlsx"""
    url = "https://pt.wikipedia.org/wiki/Lista_de_jogos_para_PlayStation_4"

    try:
        requisicao = requests.get(url).text
        soup = BeautifulSoup(requisicao, 'html.parser')

        tabela = soup.find('table', class_='wikitable sortable')
        if not tabela:
            raise FalhaAoEncontrarWikitableSortable()

        df = pd.DataFrame(columns=['Titulo', 'Desenvolvedor', 'Publicador', 'Exclusivo', 'Europa', 'Japão', 'América do Norte', 'Brasil', 'Referências'])

        for row in tabela.tbody.find_all('tr'):
            colunas = row.find_all('td')
            
            # Pegar os dados das colunas do site da wikipedia
            if colunas:
                Titulo = aplicar_regex(colunas[0].text)
                desenvolvedor = aplicar_regex(colunas[1].text)
                publicador = aplicar_regex(colunas[2].text)
                exclusivo = aplicar_regex(colunas[3].text)
                europa = aplicar_regex(colunas[4].text)
                Japao = aplicar_regex(colunas[5].text)
                America_do_norte = aplicar_regex(colunas[6].text)
                Brasil = aplicar_regex(colunas[7].text)
                Referencia = aplicar_regex(colunas[8].text)

                df = df._append({"Titulo": Titulo, "Desenvolvedor": desenvolvedor, "Publicador": publicador, "Exclusivo": exclusivo, "Europa": europa, "Japão": Japao, "América do Norte": America_do_norte, "Brasil": Brasil, "Referências": Referencia}, ignore_index=True)

        df_limpo = limpar_dados(df)

        df_limpo.to_excel('Dados_PS4_WIKIPEDIA.xlsx')  # gerar dados pra excel

    except (RequestException, requests.ReadTimeout, requests.ConnectionError, requests.ConnectTimeout, FalhaAoEncontrarWikitableSortable) as e:
        if isinstance(e, FalhaAoEncontrarWikitableSortable):
            print("A tabela 'wikitable sortable' não foi encontrada.")
        else:
            print("Ocorreu um erro no processo de requisição:")

receber_e_guardar_dados_ps4()



def receber_e_guardar_dados_xbox_360():
    """Funcao que realiza uma requisicao a api e retorna os valores em uma tabela xlsx"""
    url = "https://pt.wikipedia.org/wiki/Lista_de_jogos_para_Xbox_360"
    
    try:
        requisicao = requests.get(url).text
        soup = BeautifulSoup(requisicao, 'html.parser')

        tabela = soup.find('table', class_='wikitable sortable')
        if not tabela:
            raise FalhaAoEncontrarWikitableSortable()

        df = pd.DataFrame(columns=['Titulo', 'Genero', 'Desenvolvedora(s)', 'Publicadora(s)', 'NA', 'JP', 'AU', 'Addons', 'XBOX One', 'Ref'])

        for row in tabela.tbody.find_all('tr'):
            colunas = row.find_all('td')
            
            # Pegar os dados das colunas do site da wikipedia
            if colunas:
                Titulo = aplicar_regex(colunas[0].text)
                Genero = aplicar_regex(colunas[1].text)
                Desenvolvedora = aplicar_regex(colunas[2].text)
                Publicadora = aplicar_regex(colunas[3].text)
                NA = aplicar_regex(colunas[4].text)
                JP = aplicar_regex(colunas[5].text)
                AU = aplicar_regex(colunas[6].text)
                addons = aplicar_regex(colunas[7].text)
                XBOX_ONE = aplicar_regex(colunas[8].text)
                ref = aplicar_regex(colunas[9].text)
                df = df._append({"Titulo": Titulo, "Genero": Genero, "Desenvolvedora(s)": Desenvolvedora, "Publicadora(s)": Publicadora, "NA": NA, "JP": JP, "AU": AU, "Addons": addons, "XBOX One": XBOX_ONE, "Ref":ref}, ignore_index=True)

        df_limpo = limpar_dados(df) #Limpando dados

        df_limpo.to_excel('Dados_XBOX360_WIKIPEDIA.xlsx')  # gerar dados pra excel

    except (RequestException, requests.ReadTimeout, requests.ConnectionError, requests.ConnectTimeout, FalhaAoEncontrarWikitableSortable) as e:
        if isinstance(e, FalhaAoEncontrarWikitableSortable):
            print("A tabela 'wikitable sortable' não foi encontrada.")
        else:
            print("Ocorreu um erro no processo de requisição:", e)
            
            
receber_e_guardar_dados_xbox_360()


def receber_e_guardar_dados_xbox_series_x():
    """Funcao que realiza uma requisicao a api e retorna os valores em uma tabela xlsx"""
    url = "https://pt.wikipedia.org/wiki/Lista_de_jogos_para_Xbox_Series_X_e_Series_S"

    try:
        requisicao = requests.get(url).text
        soup = BeautifulSoup(requisicao, 'html.parser')

        tabela = soup.find('table', class_='wikitable sortable plainrowheaders')
        if not tabela:
            raise FalhaAoEncontrarWikitableSortable()

        df = pd.DataFrame(columns=['Titulo', 'Genero', 'Desenvolvedora(s)', 'Publicadora(s)', 'NA', 'JP', 'EU', 'Complementos', 'Ref'])

        for row in tabela.tbody.find_all('tr'):
            colunas = row.find_all('td')
            
            # Verificar se colunas contém dados suficientes
            if len(colunas) == 9:  # deve corresponder ao número de colunas esperado
                Titulo = aplicar_regex(colunas[0].text)
                Genero = aplicar_regex(colunas[1].text)
                Desenvolvedora = aplicar_regex(colunas[2].text)
                Publicadora = aplicar_regex(colunas[3].text)
                NA = aplicar_regex(colunas[4].text)
                JP = aplicar_regex(colunas[5].text)
                EU = aplicar_regex(colunas[6].text)
                Complementos = aplicar_regex(colunas[7].text)
                ref = aplicar_regex(colunas[8].text)
                

                df = df._append({"Titulo": Titulo, "Genero": Genero, "Desenvolvedora(s)": Desenvolvedora, 
                                "Publicadora(s)": Publicadora, "NA": NA, "JP": JP, "EU": EU, 
                                "Complementos": Complementos, "Ref": ref}, 
                                ignore_index=True)

        df_limpo = limpar_dados(df)

        df_limpo.to_excel('Dados_XBOX_series_x_WIKIPEDIA.xlsx', index=False)  # index=False para não salvar índices

    except (RequestException, requests.ReadTimeout, requests.ConnectionError, requests.ConnectTimeout, FalhaAoEncontrarWikitableSortable) as e:
        if isinstance(e, FalhaAoEncontrarWikitableSortable):
            print("A tabela 'wikitable sortable' não foi encontrada.")
        else:
            print("Ocorreu um erro no processo de requisição:", e)

receber_e_guardar_dados_xbox_series_x()





def receber_e_guardar_dados_ps5():
    url = "https://pt.wikipedia.org/wiki/Lista_de_jogos_para_PlayStation_5"

    try:
        requisicao = requests.get(url).text
        soup = BeautifulSoup(requisicao, 'html.parser')

        tabela = soup.find('table', class_='wikitable sortable plainrowheaders')
        if not tabela:
            raise FalhaAoEncontrarWikitableSortable()

        colunas_esperadas = ['Titulo', 'Genero', 'Desenvolvedora(s)', 'Publicadora(s)', 'JP', 'AN', 'PAL', 'Addons', 'Ref']
        df = pd.DataFrame(columns=colunas_esperadas)

        for row in tabela.find_all('tr')[1:]:  # Ignorar a primeira linha de cabeçalho
            colunas = row.find_all(['th', 'td'])  # Buscar tanto th quanto td
            

            if len(colunas) >= 9:  # Verificar se a quantidade de colunas é igual as de colunas esperadas
                dados = [aplicar_regex(coluna.text) for coluna in colunas[:9]]
                
                # Debugando: 
                # print(dados)

                df = df._append(pd.Series(dados, index=colunas_esperadas), ignore_index=True)

        # Aplicar regex em todo o DataFrame 
        df = df.map(aplicar_regex) #O .applymap tá depredado
        
        # Limpar dados
        df_limpo = limpar_dados(df)

        df_limpo.to_excel('Dados_PS5_WIKIPEDIA.xlsx', index=False)  # index=False para não salvar índices

    except (RequestException, requests.ReadTimeout, requests.ConnectionError, requests.ConnectTimeout, FalhaAoEncontrarWikitableSortable) as e:
        if isinstance(e, FalhaAoEncontrarWikitableSortable):
            print("A tabela 'wikitable sortable' não foi encontrada.")
        else:
            print("Ocorreu um erro no processo de requisição:", e)
    except Exception as e:
        print(f"Ocorreu um erro inesperado ao processar a URL {url}: {e}")

receber_e_guardar_dados_ps5()



def receber_e_guardar_dados_switch():
    url = "https://pt.wikipedia.org/wiki/Lista_de_jogos_para_Nintendo_Switch"

    try:
        requisicao = requests.get(url).text
        soup = BeautifulSoup(requisicao, 'html.parser')

        tabelas = soup.find_all('table', class_='sortable')
        if not tabelas:
            raise FalhaAoEncontrarWikitableSortable()

        colunas_esperadas = ['Titulo', 'Desenvolvedor', 'Publicadora(s)', 'Lancamento', 'OBS', 'Ref']
        df_completo = pd.DataFrame(columns=colunas_esperadas)

        for tabela in tabelas:
            df = pd.DataFrame(columns=colunas_esperadas)

            for row in tabela.find_all('tr'):
                colunas = row.find_all('td')

                if len(colunas) >= 6:  # Deve corresponder ao número de colunas esperado
                    Titulo = aplicar_regex(colunas[0].text)
                    Desenvolvedor = aplicar_regex(colunas[1].text)
                    Publicadora = aplicar_regex(colunas[2].text)
                    Lancamento = aplicar_regex(colunas[3].text)
                    OBS = aplicar_regex(colunas[4].text)
                    ref = aplicar_regex(colunas[5].text)

                    df = df._append({"Titulo": Titulo, "Desenvolvedor": Desenvolvedor, 
                                     "Publicadora(s)": Publicadora, "Lancamento": Lancamento, "OBS": OBS, "Ref": ref}, 
                                    ignore_index=True)

            df_completo = pd.concat([df_completo, df], ignore_index=True)

        df_completo = df_completo.map(aplicar_regex)
        df_limpo = limpar_dados(df_completo)

        df_limpo.to_excel('Dados_switch_WIKIPEDIA.xlsx', index=False)  # index=False para não salvar índices

    except (requests.RequestException, requests.ReadTimeout, requests.ConnectionError, requests.ConnectTimeout, FalhaAoEncontrarWikitableSortable) as e:
        if isinstance(e, FalhaAoEncontrarWikitableSortable):
            print("A tabela 'wikitable sortable' não foi encontrada.")
        else:
            print("Ocorreu um erro no processo de requisição:", e)

    except Exception as e:
        print(f"Ocorreu um erro inesperado ao processar a URL {url}: {e}")

# Executar a função
receber_e_guardar_dados_switch()