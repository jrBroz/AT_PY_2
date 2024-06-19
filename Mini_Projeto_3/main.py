import pandas as pd
import sqlalchemy as db

def ler_excel():
    """Função que lê um arquivo Excel e retorna um dataframe"""
    try:
        ler_arquivo_xlsx = pd.read_excel("DADOS_AT_UNIFICADOS.xlsx")
        return ler_arquivo_xlsx
    
    except FileNotFoundError:
        return "O arquivo não existe."
    
    except PermissionError:
        return "Você não tem permissão para ler o arquivo."
    

def limpeza_dados(df: pd.DataFrame):
    """Funcao que faz a limpeza de dados."""
    df['jogos_preferidos'] = df['jogos_preferidos'].str.strip()
    return df


def analise_dados():
    """Função que realiza a análise dos dados utilizando sets"""

    arquivo_excel = ler_excel()

    if isinstance(arquivo_excel, str):
        print(arquivo_excel)
        return
    
    arquivo_excel = limpeza_dados(arquivo_excel)  # Limpa dados
    
    set_todos_jogos = set()
    set_jogos_relatados_apenas_um_usuario = set()
    aparicoes_de_jogos = {}

    if 'jogos_preferidos' not in arquivo_excel.columns:
        print("Não existe a coluna jogos_preferidos no arquivo.")
        return

    for jogos in arquivo_excel['jogos_preferidos']:
        if not isinstance(jogos, str):
            jogos = str(jogos)
        jogos_lista = jogos.split('|')
       
        for jogo in jogos_lista:
            jogo = jogo.strip()
            set_todos_jogos.add(jogo)
        
            if jogo in aparicoes_de_jogos:
                aparicoes_de_jogos[jogo] += 1
            else:
                aparicoes_de_jogos[jogo] = 1

    set_jogos_relatados_apenas_um_usuario = {jogo for jogo, count in aparicoes_de_jogos.items() if count == 1}

    max_aparicoes = max(aparicoes_de_jogos.values())
    jogos_com_maior_aparicao = [jogo for jogo, count in aparicoes_de_jogos.items() if count == max_aparicoes]

    # Criar DataFrame para os jogos com maior aparição
    df_jogo_com_maior_aparicao = pd.DataFrame(columns=['Jogo_Com_Maior_Aparicao', 'Numero_Aparicoes'])
    for jogo in jogos_com_maior_aparicao:
        df_jogo_com_maior_aparicao = df_jogo_com_maior_aparicao._append({'Jogo_Com_Maior_Aparicao': jogo, 'Numero_Aparicoes': max_aparicoes}, ignore_index=True)

    print("Todos os jogos:", set_todos_jogos)
    print("-" * 50)
    print("Jogos relatados por apenas um usuário:", set_jogos_relatados_apenas_um_usuario)
    print("-" * 50)
    print("Jogo com maior aparição:", df_jogo_com_maior_aparicao)
    
    return set_todos_jogos, set_jogos_relatados_apenas_um_usuario, df_jogo_com_maior_aparicao


def criar_inserir_BD():
    """Função que cria e se conecta com o banco de dados e insere os dados"""
    try:
        engine = db.create_engine('sqlite:///AT.db')
        conn = engine.connect()

        todos_jogos, jogos_relatados_apenas_um_usuario, df_jogo_com_maior_aparicao = analise_dados()
        
        # DataFrames para cada conjunto de dados     
        df_todos_jogos = pd.DataFrame({'Todos_Jogos': list(todos_jogos)})
        df_jogos_relatados_apenas_um_usuario = pd.DataFrame({'Jogos': list(jogos_relatados_apenas_um_usuario)})
        
        # Exportando para o banco de dados
        df_todos_jogos.to_sql('Todos_Jogos', engine, if_exists='replace', index=False)
        df_jogos_relatados_apenas_um_usuario.to_sql('Jogos_Relatados_Um_Usuario', engine, if_exists='replace', index=False, chunksize=100)


        dataframe_para_xlsx_jogos_relatados_apenas_um_usuario = pd.DataFrame({'Jogos_Relatados_por_apenas_um_usuario': list(jogos_relatados_apenas_um_usuario)})
        dataframe_para_xlsx_jogo_com_maior_aparicao = pd.DataFrame({'Jogos_com_maior_aparicao': list(df_jogo_com_maior_aparicao)})

        # Inserindo o DataFrame com os jogos com maior aparição em sql
        df_jogo_com_maior_aparicao.to_sql('Jogo_Maior_Aparicao', engine, if_exists='replace', index=False)
        
        conn.close()
        print("Dados foram inseridos no banco de dados.")

        #Exportar todos os dataframes juntos pra um arquivo xlsx só
        frames = [df_todos_jogos, df_jogo_com_maior_aparicao, df_jogos_relatados_apenas_um_usuario]
        totalidade = pd.concat([df_todos_jogos, dataframe_para_xlsx_jogos_relatados_apenas_um_usuario, dataframe_para_xlsx_jogo_com_maior_aparicao], axis=1)
        totalidade.to_excel("Dados_Unificados_Final.xlsx") 

    except db.exc.SQLAlchemyError:
        print("Houve um erro ao se comunicar com o BD")


criar_inserir_BD()
