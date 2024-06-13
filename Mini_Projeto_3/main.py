import pandas as pd
import os
import sqlalchemy as db

    
def ler_excel():
    """Funcao que le um arquivo excel e retorna um dataframe"""    
    try:
    
        ler_arquivo_xlsx = pd.read_excel("DADOS_AT_UNIFICADOS.xlsx")

    
        return ler_arquivo_xlsx
    
    except(PermissionError, FileNotFoundError) as e:     
        
        if e == FileNotFoundError:
            return "O arquivo que voce procura nao existe que você procura não existe."
            
        if e == PermissionError:
            return "Voce nao tem permissao para ler o arquivo."
        
    
    
           
    #Falta terminar



def analise_dados():
    
    arquivo_Excel = ler_excel()
    set_todos_jogos = set
    set_para_jogos_relatados_apenas_um_usuario = set
    set_para_jogo_com_maior_aparicao = set    
    sets_por_coluna = {col: set(arquivo_Excel[col]) for col in arquivo_Excel.columns}
    
    sets_por_linha = [set(row) for row in arquivo_Excel.values]

    for col, s in sets_por_coluna.items():
        if arquivo_Excel[col] == 'jogos_preferidos':
            set_todos_jogos.add(arquivo_Excel[col])
            


    print(set_todos_jogos)
    # print("\nSets por linha:")
    # for i, s in enumerate(sets_por_linha):
    #     print(f"Linha {i}: {s}")




    


analise_dados()



def criar_inserir_BD():
    """Funcao que cria e se conecta com o banco de dados """

    try:
        engine = db.create_engine('sqlite:///AT.db')
        

        
        
        # df.to_sql('Tabela_Dados', engine, if_exists='replace', index=False, schema='')
        
        

        

    except (ConnectionError, IsADirectoryError, PermissionError, FileNotFoundError) as ex:
        
        if ex == ConnectionError: return 'Erro ao se conectar com banco de dados'
        
        else : return 'Houve um erro na leitura do arquivo.'