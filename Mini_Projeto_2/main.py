import pandas as pd

class falha_concatenacao(Exception):
    
    "Erro ao concatenar DataFrames"

class exportar_DataFrame_para_excel(Exception):
    
    "Erro ao tentar converter um dataframe para formato excel"
#======================= 



def limpar_dados(df_perfeito:pd.DataFrame):
    """Funcao que faz uma limpeza de dados do dataframe passado como parâmetro."""
    df_perfeito = df_perfeito.dropna() # Remover linhas com valor ausente
    df_perfeito = df_perfeito.dropna(axis=1) # remove coluna com valor ausente
    df_perfeito = df_perfeito.fillna(0) #  preenche valor ausente com 0
    df_perfeito = df_perfeito.drop_duplicates() # Remover duplicatas 

    
    return df_perfeito


def ler_transformar_csv():
    """Funcao que le e limpa os arquivos presentes no arquivo csv e cria um DataFrame com os arquivos"""
    try:
    
        ler_csv = pd.read_csv("Mini_Projeto_2/dadosAT.csv")
        pd_csv =  pd.DataFrame(ler_csv)
        
        pd_csv_limpo = limpar_dados(pd_csv)
        
        return pd_csv_limpo

    except (IsADirectoryError, PermissionError, FileNotFoundError):
        print("Ocorreu um erro ao ler os arquivos...")
    
    

def ler_transformar_excel():
    """Funcao que le e limpa os arquivos presentes no arquivo excel"""
    try:
    
        ler_excel =   pd.read_excel("Mini_Projeto_2/dadosAT.xlsx")
        pd_excel = pd.DataFrame(ler_excel)
     
        pd_xlsx_limpo = limpar_dados(pd_excel)
        
        return pd_xlsx_limpo
     
        
    except (IsADirectoryError, PermissionError, FileNotFoundError):
        print("Ocorreu um erro ao ler os arquivos...")    
    

def ler_transformar_json():
    """Funcao que le e limpa os arquivos presentes no arquivo json"""
    try:
    
        ler_json =  pd.read_json("Mini_Projeto_2/dadosAT.json")        
        pd_json = pd.DataFrame(ler_json)
        
        pd_json_limpo = limpar_dados(pd_json)
        
        return pd_json_limpo 

    except (IsADirectoryError, PermissionError, FileNotFoundError):
        print("Ocorreu um erro ao ler os arquivos...")
        
def exportar_para_excel(df_para_excel):
        """Funcao que exporta um DataFrame para o formato de excel e trata com excecao personalizada em caso de erro."""


        try:       
                df = pd.DataFrame(df_para_excel)

                with pd.ExcelWriter("DADOS_AT_UNIFICADOS.xlsx") as writer:
                    df.to_excel(writer)       
        
        except exportar_DataFrame_para_excel as e:
            print(e)

        
 
def manipulacao_dados():
    """Funcao que recebe dados advindos das outras funções e concatena tudo em apenas 1 dataframe"""
    
    try:
        pd_csv = ler_transformar_csv()    
        pd_excel = ler_transformar_excel()
        pd_json = ler_transformar_json()
        
        pd_junto = pd.concat([pd_csv, pd_json, pd_excel], axis=1, join='outer')
        pd_junto = limpar_dados(pd_junto) # Talvez tirar ja que teoricamente todos os arquivos estão 'limpos?'
        pd_total_convertido = exportar_para_excel(pd_junto)
        
        return pd_total_convertido
        
    except falha_concatenacao as e:
        print(e)
    

manipulacao_dados()    