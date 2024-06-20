import pandas as pd


class falha_concatenacao(Exception):
    """Erro ao concatenar DataFrames"""

class exportar_DataFrame_para_excel(Exception):
    """Erro ao tentar converter um dataframe para formato excel"""

#======================= 

def limpar_dados(df_perfeito: pd.DataFrame) -> pd.DataFrame:
    """Funcao que faz uma limpeza de dados do dataframe passado como parâmetro."""
    df_perfeito = df_perfeito.dropna(subset=['nome_completo'])
    df_perfeito = df_perfeito.drop_duplicates(subset=['nome_completo'])  # Remover duplicatas
    df_perfeito = df_perfeito.dropna()  # Remover linhas com valores ausentes
    return df_perfeito



def ler_transformar_csv() -> pd.DataFrame:
    """Funcao que le e limpa os arquivos presentes no arquivo csv e cria um DataFrame com os arquivos"""
    try:
        with open("Mini_Projeto_2/dadosAT.csv", mode='r') as file:
            ler_csv = pd.read_csv(file)
            pd_csv = pd.DataFrame(ler_csv)
        
        # Limpar os dados
        pd_csv_limpo = limpar_dados(pd_csv)
        
        # Modifica o valor de 'nome_completo' pra alterar o luiz.pereira sem @gmail.com, realizando tratamento de dados
        pd_csv_limpo.loc[pd_csv_limpo['email'].str.contains('luiz.pereira', case=False), 'email'] = "luiz.pereira@example.com"
        
        return pd_csv_limpo

    except (IsADirectoryError, PermissionError, FileNotFoundError):
        print("Ocorreu um erro ao ler os arquivos...")


    
def ler_transformar_excel() -> pd.DataFrame:
    """Funcao que le e limpa os arquivos presentes no arquivo excel"""
    try:
        ler_excel = pd.read_excel("Mini_Projeto_2/dadosATNovo.xlsx")
        pd_excel = pd.DataFrame(ler_excel)
        pd_xlsx_limpo = limpar_dados(pd_excel)
        
        return pd_xlsx_limpo

    except (IsADirectoryError, PermissionError, FileNotFoundError):
        print("Ocorreu um erro ao ler os arquivos...")    

def ler_transformar_json() -> pd.DataFrame:
    """Funcao que le e limpa os arquivos presentes no arquivo json"""
    try:
        with open("Mini_Projeto_2/dadosATNovo.json", mode='r') as file:
            ler_json = pd.read_json(file)
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
            df.to_excel(writer, index=False)       
    except exportar_DataFrame_para_excel:
        print("Erro ao tentar converter um dataframe para formato excel")



def manipulacao_dados() -> None:
    """Funcao que recebe dados advindos das outras funções e concatena tudo em apenas 1 dataframe"""
    try:
        pd_csv = ler_transformar_csv()    
        pd_excel = ler_transformar_excel()
        pd_json = ler_transformar_json()
        
        # Identificar e atribuir novos IDs para registros com IDs iguais e nomes diferentes
        ids_contagem = {}
        for df in [pd_csv, pd_excel, pd_json]:
            ids_duplicados = df[df.duplicated(subset=['id'], keep=False)]  # Aqui ele pega os ids duplicados
            for idx, row in ids_duplicados.iterrows(): # Itera sobre as linhas com id duplicado
                id_original = row['id'] # aqui ele pega o id original
                nome = row['nome_completo'] # pega nome completo
                if (id_original, nome) not in ids_contagem: # Checa se o nome e ID nao ta no dicionario
                    ids_contagem[(id_original, nome)] = len(ids_contagem) + 1 # se n tiver ele adiciona o novo ID no dict
                novo_id = ids_contagem[(id_original, nome)] # o novo_id é resultado da combinação gerada acima.
                df.loc[idx, 'id'] = f'{id_original}_{novo_id}'  # Atualiza o ID no DataFrame original
        
        # Concatenar DataFrames
        pd_junto = pd.concat([pd_csv, pd_json, pd_excel], ignore_index=True)
        
        # Limpar dados do DataFrame resultante
        pd_junto = limpar_dados(pd_junto)
        
        # Exportar para Excel
        exportar_para_excel(pd_junto)
        
    except falha_concatenacao:
        print("Erro ao concatenar DataFrames")
    except exportar_DataFrame_para_excel:
        print("Erro ao tentar converter um dataframe para formato excel")

# Executar a função de manipulação de dados
manipulacao_dados()
